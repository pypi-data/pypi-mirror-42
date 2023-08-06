from abc import abstractmethod

import attr
import numpy as np
from numba import jit

from .data_types import Image, Listmode, Emap_MLEM
from .templating import funcclass, noop, FuncClass
from .utils import _tqdm

running_env = jit(nopython = True, parallel = True)


@funcclass
class Projector:
    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


def projector_picker(method: str = 'siddon'):
    from .model_impl import ProjectorDistanceDriven, ProjectorSiddon
    if method == 'siddon':
        return ProjectorSiddon
    elif method == 'distance-driven':
        return ProjectorDistanceDriven
    else:
        raise NotImplementedError


@funcclass
class BackProjector:
    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


def bprojector_picker(method: str = 'siddon'):
    from .model_impl import BackProjectorSiddon, BackProjectorDistanceDriven
    if method == 'siddon':
        return BackProjectorSiddon
    elif method == 'distance-driven':
        return BackProjectorDistanceDriven
    else:
        raise NotImplementedError


@funcclass
class MLEM:
    n_iter: int
    projector: Projector
    bprojector: BackProjector
    emap: Emap_MLEM
    saver: FuncClass = attr.ib(default = noop)

    def __call__(self, listmode: Listmode):
        x = Image(np.ones(self.emap.shape, dtype = np.float32), self.emap.center,
                  self.emap.size)
        for ind in _tqdm(range(self.n_iter)):
            proj = self.projector(x, listmode.lors)
            bp = self.bprojector(listmode / proj)
            x = x * bp / self.emap
            self.saver(ind + 1, x)
        return x


from srfnef.templating import TYPE_BIND

TYPE_BIND.update({'Projector': Projector, 'BackProjector': BackProjector, 'MLEM': MLEM})
