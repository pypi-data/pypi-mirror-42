# encoding: utf-8
'''
srfnef.templating
~~~~~~~~~~~~~~~~~

This module provides basic data and function types of the whole package,
including `dataclass` for data and `funcclass` for functions.

`DataClass`, as well as `FuncClass`, instances `io` to `.hdf5` files are implemented in `save`
and `load` natual modes.
'''

import json
import operator
import types
from abc import abstractmethod
from copy import copy

import attr
import deepdish as dd
import numpy as np

_tiny = 1e-8

_huge = 1e8

TYPE_BIND = {}


class DataClass:
    '''`DataClass` is suited for storing data objects. It is the most basic class type in
    `srfnef` package. All data and functions would be seriously considered to be defined as a
    Dataclass instance. More specific, only the field `.data` in a `DataClass` would be regarded
    as the only computable part with in an instance. Any other class that defined to contained
    data would a subclass of `DataClass`.
    '''

    def replace(self, **kwargs):
        '''Creates a new object of the same type of instance, replacing fields with values from
        changes.
        '''
        return attr.evolve(self, **kwargs)

    @classmethod
    def fields(cls):
        '''Returns a tuple of field names for this `DataClass` instance.
        '''
        return attr.fields_dict(cls)

    def to_dict(self, recurse = True):
        '''Return a dictionary of fields for this 'DataClass` instance.
        '''
        return attr.asdict(self, recurse)

    def to_tuple(self):
        '''Return a tuple of fields for this 'DataClass` instance.
        '''
        return attr.astuple(self)

    def to_json(self, file_path = ''):
        if not file_path == '' and '.hdf5' in file_path:
            x_saver(file_path, self)
        _dict = {'file_path': file_path, 'classname': self.__class__.__name__}
        _dict.update(self.to_dict(recurse = False))

        for key, val in _dict.items():
            if isinstance(val, np.int64):
                _dict[key] = int(val)
            if isinstance(val, np.ndarray) and not key == 'data':
                _dict[key] = val.tolist()
            if isinstance(val, np.ndarray) and key == 'data':
                _dict[key] = f'numpy.ndarray(shape = {val.shape}, dtype = {val.dtype})'
            if isinstance(val, DataClass):
                _dict[key] = json.loads(val.to_json(file_path + '/' + key))
        return json.dumps(_dict)

    @classmethod
    def from_json(cls, _json):
        _dict = json.loads(_json)
        if not _dict['file_path'] == '' and '.hdf5' in _dict['file_path']:
            return x_loader(_dict['file_path'])
        _class = TYPE_BIND[_dict['classname']]
        _dict.pop('file_path')
        _dict.pop('classname')
        for key, val in _dict.items():
            if isinstance(val, str) and len(val) > 13 and val[:13] == '{"file_path":':
                _dict[key] = DataClass.from_json(val)
        return _class(**_dict)

    def map(self, f):
        '''`Map` applis a function to the field `.data` of this DataClass instance, and return a
        new instance with the same type'''
        return self.replace(data = f(self.data))

    def _map_bin(self, f, other):
        '''`_map_bim` applis a binary function to this instance with another `DataClass`
        instance or np.ndarray or scale values. This function would apply on the field `.data`
        and return a new instance with same type'''

        if isinstance(other, (np.ndarray, list, tuple)) or np.isscalar(other):
            return self.replace(data = f(self.data, other))
        elif isinstance(other, DataClass):
            return self.replace(data = f(self.data, other.data))
        else:
            raise NotImplementedError('{} is not implemented yet.'.format(type(other)))

    @property
    def shape(self):
        ''' return the `shape` of `self.data`.'''
        assert 'data' in self.fields()
        return np.array(self.data.shape)

    def register(self, func):
        obj = self.replace()
        if isinstance(func, list):
            for f in func:
                obj = f(obj)
        elif callable(func):
            obj = func(obj)
        else:
            raise ValueError('func argument must be callable or a list of callables')
        return obj

    @classmethod
    def class_register(cls, func):
        _cls = cls
        if isinstance(func, list):
            for f in func:
                _cls = f(_cls)
        elif callable(func):
            _cls = func(_cls)
        else:
            raise ValueError('func argument must be callable or a list of callables')
        return _cls


def dataclass(cls):
    '''This function is a decorator that is used to add generated special methods to classes, as
    described below.

    The `dataclass()` decorator examines the class to find fields. A field is defined as class
    variable that has a type annotation. The order of the fields in all of the generated methods
    is the order in which they appear in the class definition.
    Be default the instance decorated by `dataclass` is attributed frozen, which means we prefer
    it to be immutable.

    Some basic arithmetic operators are mounted and would apply on `.data` field.
    '''
    base = attr.s(frozen = True, auto_attribs = True, slots = True)(cls)
    cls = types.new_class(base.__name__, (base, DataClass))
    return cls.class_register([unary_ops, binary_ops])


class FuncClass(DataClass):
    '''`FuncClass` is special subclass of `DataClass` which is callable. We prefer all functional
    class in this package would be defined as a subclass of `FuncClass`.

    Be default, the first input argument would be regarded as the key input.
    '''

    @abstractmethod
    def __call__(self, *args, **kwargs):
        '''`__call__` must be defined by any subclass of `FunClass`'''
        pass

    def currying(self, *args, **kwargs):
        ''' `currying` translate this `FuncClass` instance to a single-argument function and
        return it as a anonymous(namely `Curried) `FunClass`. Only the key argument would be the
        only argument in the new instance. The other arguments would be stored in the new `FuncClass`
        instance.
        '''
        return Curried(self, args, kwargs)

    @property
    def is_curried(self):
        '''check this `FuncClass` is `curried`, which means it only accepts one arguments.'''
        import inspect
        return 1 == len(inspect.signature(self.__call__).parameters)

    def __matmul__(self, func):
        ''' return a compostion of two `FuncClass` to a new anonymous(namely `Composited')
        instance. It only support two `is_curried` functions to composite.
        '''
        return Composited(self, func)

    def map(self, f):
        # TODO comments
        if isinstance(f, FuncClass):
            return f @ self
        elif callable(f):
            @funcclass
            class UnaryOp:
                def __call__(self, x):
                    return f(x)

            op = UnaryOp()
            return op @ self
        else:
            raise ValueError('f must be a FuncClass or callable')

    def _map_bin(self, f, other):
        # TODO
        if isinstance(f, FuncClass):
            return (f.currying(other)) @ self
        elif callable(f):
            @funcclass
            class BinaryOp:
                def __call__(self, x):
                    return f(x, other)

            op = BinaryOp()
            return op @ self


def funcclass(cls):
    '''This function is a decorator that is used to add generated special methods to classes, as
    described below.

    The `funcclass()` decorator are used to define function typed class in this package.
    '''
    base = attr.s(frozen = True, auto_attribs = True, slots = True)(cls)
    cls = types.new_class(base.__name__, (base, FuncClass))
    return cls


@funcclass
class Composited(FuncClass):
    f1: FuncClass
    f2: FuncClass

    def __call__(self, *args, **kwargs):
        if isinstance(self.f1, FuncClass):
            assert self.f1.is_curried

        return self.f1(self.f2(*args, **kwargs))


@funcclass
class Curried:
    f: FuncClass
    args: list
    kwargs: dict

    def __call__(self, x):
        return self.f(x, *self.args, **self.kwargs)


class UnaryOps:
    pass


class BinaryOps:
    @funcclass
    class Add:
        other: DataClass

        def __call__(self, obj):
            return obj + self.other

    @funcclass
    class Sub:
        other: DataClass

        def __call__(self, obj):
            return obj - self.other

    @funcclass
    class Mul:
        other: DataClass

        def __call__(self, obj):
            return obj * self.other

    @funcclass
    class Truediv:
        other: DataClass

        def __call__(self, obj):
            return obj / self.other


def unary_ops(obj):
    def abs(obj):
        return obj.map(operator.abs)

    def __neg__(obj):
        return obj.map(operator.neg)

    obj.abs = abs
    obj.__neg__ = __neg__
    return obj


def binary_ops(obj):
    def __eq__(obj: DataClass, other):
        return obj._map_bin(operator.eq, other)

    def __gt__(obj: DataClass, other):
        return obj._map_bin(operator.gt, other)

    def __ge__(obj: DataClass, other):
        return obj._map_bin(operator.ge, other)

    def __lt__(obj: DataClass, other):
        return obj._map_bin(operator.lt, other)

    def __le__(obj: DataClass, other):
        return obj._map_bin(operator.le, other)

    def __add__(obj: DataClass, other):
        return obj._map_bin(operator.add, other)

    def __sub__(obj: DataClass, other):
        return obj._map_bin(operator.sub, other)

    def __mul__(obj: DataClass, other):
        return obj._map_bin(operator.mul, other)

    def __truediv__(obj: DataClass, other):

        def remove_zeros(current, threshold = _tiny):
            if isinstance(current, np.ndarray) or np.isscalar(current):
                _data = copy(current)
            else:
                _data = copy(current.data)
            _data[_data < threshold] = _huge
            return current.replace(data = _data)

        if isinstance(other, DataClass):
            _other = remove_zeros(other)
        else:
            _other = other
        return obj._map_bin(operator.truediv, _other)

    def __floordiv__(obj: DataClass, other):
        return obj._map_bin(operator.floordiv, other)

    def __mod__(obj: DataClass, other):
        return obj._map_bin(operator.mod, other)

    def __pow__(obj: DataClass, other):
        return obj._map_bin(operator.pow, other)

    obj.__eq__ = __eq__
    obj.__gt__ = __gt__
    obj.__ge__ = __ge__
    obj.__lt__ = __lt__
    obj.__le__ = __le__
    obj.__add__ = __add__
    obj.__sub__ = __sub__
    obj.__mul__ = __mul__
    obj.__truediv__ = __truediv__
    obj.__floordiv__ = __floordiv__
    obj.__mod__ = __mod__
    obj.__pow__ = __pow__
    return obj


def _parse_dataclass_to_dict(instance: DataClass):
    dct = {'classname': type(instance).__name__}
    for key, value in instance.to_dict(recurse = False).items():
        if isinstance(value, DataClass):
            dct[key] = _parse_dataclass_to_dict(value)
        else:
            dct[key] = value
    return dct


def _parse_dict_to_dataclass(dct: dict):
    if dct['classname'] not in TYPE_BIND:
        raise NotImplementedError('{} not in TYPE_BIND: {}'.format(dct['classname'],
                                                                   TYPE_BIND.keys()))
    _cls = TYPE_BIND[dct['classname']]
    _dct = {}
    for key, value in dct.items():
        if isinstance(value, dict):
            _dct[key] = _parse_dict_to_dataclass(value)
        elif not key == 'classname' and not key.startswith('_'):
            _dct[key] = value
        else:
            pass
    return _cls(**_dct)


def x_saver(path, instance: DataClass, compression = None):
    """
    Save a DataClass object to an HDF5 file. for more details please visit
    'https://deepdish.readthedocs.io/en/latest/_modules/deepdish/io/hdf5io.html#save'

    This function requires the `deepdish`_ module to be installed.

    Parameters
    ----------
    path : string
        Filename to which the data is saved, must ends with '.hdf5
    data : DataClass or Funcclass
        Data to be saved. This can be any DataClass with fields a Numpy array, a string,
        another DataClass

    compression : string or tuple
        Set compression method, choosing from `blosc`, `zlib`, `lzo`, `bzip2`
        and more (see PyTables documentation). It can also be specified as a
        tuple (e.g. ``('blosc', 5)``), with the latter value specifying the
        level of compression, choosing from 0 (no compression) to 9 (maximum
        compression). The default is None

    See also
    --------
    load
    """
    if path.endswith('.hdf5'):
        dd.io.save(path, _parse_dataclass_to_dict(instance), compression = compression)


def x_loader(path, sel = None, unpack = False):
    """
    Loads an HDF5 saved with `save` and end with '.hdf5'. It will return a DataClass
    object which is well-formed.

    This function requires the `deepdish`_ module to be installed.

    Parameters
    ----------
    path : string
        Filename from which to load the data. must end with '.hdf5'
        path can be in form of path + x_path, for example
        'a.hdf5/b/c'
        it will load the '/b/c' group in a.hdf5
    sel : slice or tuple of slices
        If you specify `group` and the target is a numpy array, then you can
        use this to slice it. This is useful for opening subsets of large HDF5
        files. To compose the selection, you can use `deepdish.aslice`.
    unpack : bool
        If True, a single-entry dictionaries will be unpacked and the value
        will be returned directly. That is, if you save ``dict(a=100)``, only
        ``100`` will be loaded.

    Returns
    -------
    data : DataClass
        It will visit TYPE_BIND to find the bind bewteen a string and a specific
        DataClass class.

    See also
    --------
    save
    TYPE_BIND
    """
    if not '.hdf5' in path:
        return
    _path, x_path = path.split('.hdf5')
    _path += '.hdf5'
    if x_path == '':
        x_path = None

    return _parse_dict_to_dataclass(dd.io.load(_path, x_path, sel, unpack))


def save(*args, **kwargs):
    '''same as `x_loader`

    See also
    --------
    x_loader, load
    '''
    x_saver(*args, **kwargs)


def load(*args, **kwargs):
    '''same as `x_saver`

    See also
    --------
    x_saver, load
    '''
    return x_loader(*args, **kwargs)


@funcclass
class Saver:
    '''This type of `FuncClass` defined the saver during iteration.'''
    path: str
    interval: int

    def __call__(self, ind, x):
        if self.interval == 0:
            return
        if ind % self.interval == 0:
            x_saver(self.path.replace('?', str(ind)), x)


def saver(path, interval = 0):
    def wrapper(obj):
        _saver = Saver(path, interval)
        return obj.replace(saver = _saver)

    return wrapper


@funcclass
class Noop:
    '''Do nothing'''

    def __call__(self, *args, **kwargs):
        return


noop = Noop()


@funcclass
class Indentity:
    '''Indentity'''

    def __call__(self, *args, **kwargs):
        return args, kwargs


TYPE_BIND.update({'DataClass': DataClass, 'FuncClass': FuncClass, 'Saver': Saver, 'Noop': Noop})
TYPE_BIND.update({'Add': BinaryOps.Add, 'Sub': BinaryOps.Sub, 'Mul': BinaryOps.Mul, 'Truediv':
    BinaryOps.Truediv})

TYPE_BIND.update({'Composited': Composited, 'Curried': Curried})
