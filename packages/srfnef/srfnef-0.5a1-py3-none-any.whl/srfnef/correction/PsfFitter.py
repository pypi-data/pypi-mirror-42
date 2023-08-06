# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: PsfFitter.py
@date: 2/15/2019
@desc:
'''

import numpy as np
import scipy.optimize as opt

import attr
from srfnef.templating import x_loader
from srfnef import _tqdm
from srfnef.templating import dataclass
from .PointImage import PointImage
__all__ = ('PsfFitter', 'FittedXY', 'FittedZ', 'Fitted')


@dataclass
class FittedXY:
    data: np.ndarray = attr.ib(converter = np.array)

    @property
    def axy(self):
        return self.data[:, 0]

    @property
    def sigx(self):
        return self.data[:, 1]

    @property
    def sigy(self):
        return self.data[:, 2]

    @property
    def ux(self):
        return self.data[:, 3]

    @property
    def uy(self):
        return self.data[:, 4]

    def __add__(self, other):
        new_data = np.vstack((self.data, other.data))
        return self.__class__(new_data)


@dataclass
class FittedZ:
    data: np.ndarray = attr.ib(converter = np.array)

    @property
    def az(self):
        return self.data[:, 0]

    @property
    def sigz(self):
        return self.data[:, 1]

    @property
    def uz(self):
        return self.data[:, 2]

    def __add__(self, other):
        new_data = np.vstack((self.data, other.data))
        return self.__class__(new_data)


@dataclass
class Fitted:
    fitted_xy: FittedXY
    fitted_z: FittedZ

    def __add__(self, other):
        new_fxy = self.fitted_xy + other.fitted_xy
        new_fz = self.fitted_z + other.fitted_z
        return self.__class__(new_fxy, new_fz)


@dataclass
class PsfFitter:
    half_slice_range: int
    half_patch_range: int
    mode: str
    out_path_xy: str
    out_path_z: str

    def __call__(self, pnt_img_path):
        data_xy = np.array([])
        data_z = np.array([])

        print('fitting psf kernel parameters')
        for _path in _tqdm(pnt_img_path):
            pnt_img = x_loader(_path)
            if pnt_img.type == 0:
                px, py, pz = pnt_img.point_ind
                nx, ny, nz = pnt_img.image.shape
                img_avg = np.average(pnt_img.image.data[
                                     px - self.half_patch_range:
                                     min(px + self.half_patch_range + 1, nx),
                                     py - self.half_patch_range:
                                     min(py + self.half_patch_range + 1, ny),
                                     pz - self.half_slice_range:
                                     min(pz + self.half_slice_range + 1, nz)],
                                     axis = 2)
                y, x = np.meshgrid(
                    np.arange(py - self.half_patch_range,
                              min(py + self.half_patch_range + 1, ny)),
                    np.arange(px - self.half_patch_range,
                              min(px + self.half_patch_range + 1, nx)))
                out_xy = _fit_gaussian(img_avg, (x, y), mode = self.mode, mu = [px, py])
                out_xy[1:3] = np.sqrt(out_xy[1:3])
                if data_xy.size == 0:
                    data_xy = out_xy
                else:
                    data_xy = np.vstack((data_xy, out_xy))

            else:
                px, py, pz = pnt_img.point_ind
                nx, ny, nz = pnt_img.image.shape

                img_avg = np.average(pnt_img.image.data[
                                     px - self.half_slice_range:
                                     min(px + self.half_slice_range + 1, nx),
                                     py - self.half_slice_range:
                                     min(py + self.half_slice_range + 1, ny),
                                     pz - self.half_patch_range:
                                     min(pz + self.half_patch_range + 1, nz)],
                                     axis = (0, 1))
                z = np.arange(pz - self.half_patch_range,
                              min(pz + self.half_patch_range + 1, nz))
                out_z = _fit_gaussian(img_avg, z, mode = 'fit_mu', mu = pz)
                out_z[1] = np.sqrt(out_z[1])
                if data_z.size == 0:
                    data_z = out_z
                else:
                    data_z = np.vstack((data_z, out_z))

        fxy = FittedXY(data_xy)
        fz = FittedZ(data_z)
        # return Fitted(fxy, fz)
        import h5py
        with h5py.File(self.out_path_xy, 'w') as fin:
            fin.create_dataset('axy', data = fxy.data[:, 0])
            fin.create_dataset('sigmax', data = fxy.data[:, 1])
            fin.create_dataset('sigmay', data = fxy.data[:, 2])
            fin.create_dataset('ux', data = fxy.data[:, 3])
            fin.create_dataset('uy', data = fxy.data[:, 4])

        with h5py.File(self.out_path_z, 'w') as fin:
            fin.create_dataset('az', data = fz.data[:, 0])
            fin.create_dataset('sigmaz', data = fz.data[:, 1])
            fin.create_dataset('uz', data = fz.data[:, 2])


from srfnef.templating import TYPE_BIND

TYPE_BIND.update(
    {'FittedXY': FittedXY, 'FittedZ': FittedZ, 'Fitted': Fitted, 'PsfFitter': PsfFitter})

_threshold = 1e-16


def _gaussian_1d(amp, sig2, mu):
    return lambda x: amp * np.exp(-(x - mu) ** 2 / 2 / sig2)


def _gaussian_2d(amp, sigx2, sigy2, mux, muy):
    return lambda x, y: amp * np.exp(-(x - mux) ** 2 / 2 / sigx2) * \
                        np.exp(-(y - muy) ** 2 / 2 / sigy2)


def _gaussian_3d(amp, sigx2, sigy2, sigz2, mux, muy, muz):
    return lambda x, y, z: amp * np.exp(-(x - mux) ** 2 / 2 / sigx2) * \
                           np.exp(-(y - muy) ** 2 / 2 / sigy2) * \
                           np.exp(-(z - muz) ** 2 / 2 / sigz2)


def _gaussian_1d_fix_mu(amp, sig2):
    return lambda x: amp * np.exp(-x ** 2 / 2 / sig2)


def _gaussian_2d_fix_mu(amp, sigx2, sigy2):
    return lambda x, y: amp * np.exp(-x ** 2 / 2 / sigx2) * \
                        np.exp(-y ** 2 / 2 / sigy2)


def _gaussian_3d_fix_mu(amp, sigx2, sigy2, sigz2):
    return lambda x, y, z: amp * np.exp(-x ** 2 / 2 / sigx2) * \
                           np.exp(-y ** 2 / 2 / sigy2) * \
                           np.exp(-z ** 2 / 2 / sigz2)


def _fit_gaussian(data, pos, mode = None, **kwargs):
    ndim = len(pos)
    if ndim > 3:
        ndim = 1
    if ndim == 1:
        if 'mu' in kwargs.keys():
            kmu = kwargs['mu']
            mu = kmu[0] if isinstance(kmu, tuple) else kmu
        else:
            mu = 0
        if isinstance(pos, tuple):
            pos = pos[0]

        x, data = pos.ravel(), data.ravel()
        x = x[data > _threshold]
        data = data[data > _threshold]
        if mode == 'fix_mu':
            def _error_function(p):
                return np.ravel(_gaussian_1d_fix_mu(*p)(x - mu) - data)

            if 'initial_guess' in kwargs.keys():
                init = kwargs['initial_guess']
            else:
                init = [np.max(data), 1]
            p = opt.leastsq(_error_function, init)
            return np.append(p[0], [mu])
        elif mode == 'fit_mu':
            def _error_function(p):
                return np.ravel(_gaussian_1d(*p)(x) - data)

            if 'initial_guess' in kwargs.keys():
                init = kwargs['initial_guess']
            else:
                init = [np.max(data), 1, mu]
            p = opt.leastsq(_error_function, init)
            return p[0]

        else:
            raise NotImplementedError
    elif ndim == 2:
        if 'mu' in kwargs.keys():
            kmu = kwargs['mu']
            mux, muy = kmu[0], kmu[1]
        else:
            mux = muy = 0

        x, y, data = pos[0].ravel(), pos[1].ravel(), data.ravel()
        maxv = np.max(data)
        x = x[data > _threshold * maxv]
        y = y[data > _threshold * maxv]
        data = data[data > _threshold * maxv]

        if mode == 'fix_mu':
            def _error_function(p):
                return np.ravel(_gaussian_2d_fix_mu(*p)(x - mux, y - muy) - data)

            if 'initial_guess' in kwargs.keys():
                init = kwargs['initial_guess']
            else:
                init = [np.max(data), 1, 1]
            p = opt.leastsq(_error_function, init)

            return np.append(p[0], [mux, muy])
        elif mode == 'fit_mu':
            def _error_function(p):
                return np.ravel(_gaussian_2d(*p)(x, y) - data)

            if 'initial_guess' in kwargs.keys():
                init = kwargs['initial_guess']
            else:
                init = [1e6, 1, 1, mux, muy]
            p = opt.leastsq(_error_function, init)
            return p[0]
        else:
            raise NotImplementedError
    elif ndim == 3:
        if 'mu' in kwargs.keys():
            kmu = kwargs['mu']
            mux, muy, muz = kmu[0], kmu[1], kmu[2]
        else:
            mux = muy = muz = 0

        x, y, z, data = pos[0].ravel(), pos[1].ravel(), pos[2].ravel(), data.ravel()
        maxv = np.max(data)
        x = x[data > _threshold * maxv]
        y = y[data > _threshold * maxv]
        z = z[data > _threshold * maxv]
        data = data[data > _threshold * maxv]
        if mode == 'fix_mu':
            def _error_function(p):
                return np.ravel(_gaussian_3d_fix_mu(*p)(x - mux, y - muy, z - muz) - data)

            if 'initial_guess' in kwargs.keys():
                init = kwargs['initial_guess']
            else:
                init = [np.max(data), 1, 1, 1]
            p = opt.leastsq(_error_function, init)
            return np.append(p[0], [mux, muy, muz])
        elif mode == 'fit_mu':
            def _error_function(p):
                return np.ravel(_gaussian_3d(*p)(x, y, z) - data)

            if 'initial_guess' in kwargs.keys():
                init = kwargs['initial_guess']
            else:
                init = [np.max(data), 1, 1, 1, mux, muy, muz]
            p = opt.leastsq(_error_function, init)
            return p[0]

        else:
            raise NotImplementedError
    else:
        raise NotImplementedError
