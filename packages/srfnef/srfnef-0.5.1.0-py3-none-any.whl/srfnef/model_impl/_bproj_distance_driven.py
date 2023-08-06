# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: _bproj_distance_driven.py
@date: 1/21/2019
@desc:
'''

import math

import attr
import numpy as np
from numba import jit, cuda, float32

from srfnef.data_types import Image, Listmode, PETCylindricalScanner
from srfnef.func_types import BackProjector
from srfnef.templating import funcclass
from srfnef.utils import _pi

running_env = jit(nopython = True, parallel = True)


@jit
def position_to_block_angle(pos, nb_blocks):
    xc, yc, _ = pos
    angle_per_block = 2 * _pi / nb_blocks
    iangle = (angle_per_block / 2 + math.atan2(yc, xc)) // angle_per_block
    return iangle


@jit
def _kernel_bproj_3d_distance_driven(vproj, fst, snd, blockdy2, blockdz2, nb_blocks,
                                     center, unit_size, image):
    dx, dy, dz = unit_size
    cx, cy, cz = center
    x1, y1, z1 = fst
    x2, y2, z2 = snd
    xd, yd, zd = x2 - x1, y2 - y1, z2 - z1
    if xd ** 2 + yd ** 2 < 100:
        return
    nx, ny, nz = image.shape
    nx2, ny2, nz2 = nx / 2, ny / 2, nz / 2

    itheta1 = position_to_block_angle(fst, nb_blocks)
    itheta2 = position_to_block_angle(snd, nb_blocks)
    angle_per_block = 2 * _pi / nb_blocks
    # if abs(itheta1 % nb_blocks - itheta2 % nb_blocks) <= 1.:
    #     return
    ctheta1, stheta1 = math.cos(itheta1 * angle_per_block), math.sin(itheta1 * angle_per_block)
    ctheta2, stheta2 = math.cos(itheta2 * angle_per_block), math.sin(itheta2 * angle_per_block)
    x1t, x1b = x1 - stheta1 * blockdy2, x1 + stheta1 * blockdy2
    x2t, x2b = x2 + stheta2 * blockdy2, x2 - stheta2 * blockdy2
    y1t, y1b = y1 + ctheta1 * blockdy2, y1 - ctheta1 * blockdy2
    y2t, y2b = y2 - ctheta2 * blockdy2, y2 + ctheta2 * blockdy2

    z1t, z1b = z1 + blockdz2, z1 - blockdz2
    z2t, z2b = z2 + blockdz2, z2 - blockdz2
    if abs(xd) >= abs(yd):
        calpha = abs(xd) / (xd ** 2 + yd ** 2) ** 0.5
        cgamma = abs(xd) / (xd ** 2 + zd ** 2) ** 0.5
        for ix in range(nx):
            xc = (ix - nx2 + 0.5) * dx + cx
            yt = ((xc - x1t) * (y2t - y1t) / (x2t - x1t) + y1t - cy) / dy + ny2
            yb = ((xc - x1b) * (y2b - y1b) / (x2b - x1b) + y1b - cy) / dy + ny2
            if yb > yt:
                yt, yb = yb, yt
            if yb >= ny or yt < 0:
                continue
            zt = ((xc - x1t) * (z2t - z1t) / (x2t - x1t) + z1t - cz) / dz + nz2
            zb = ((xc - x1b) * (z2b - z1b) / (x2b - x1b) + z1b - cz) / dz + nz2
            if zb > zt:
                zt, zb = zb, zt
            if zb >= nz or zt < 0:
                continue
            for iy in range(max(0, int(yb)), min(ny, 1 + int(yt))):
                wy = min(iy + 1, yt) - max(iy, yb)
                # wy /= (yt - yb)
                for iz in range(max(0, int(zb)), min(nz, 1 + int(zt))):
                    wz = min(iz + 1, zt) - max(iz, zb)
                    # wz /= (zt - zb)
                    # vproj[i] += image[ix, iy, iz] * wy * wz / calpha / cgamma
                    # cuda.atomic.add(image, (ix, iy, iz), wy * wz / calpha / cgamma * vproj[i])
                    image[ix, iy, iz] += wy * wz * vproj
    else:
        calpha = abs(yd) / (yd ** 2 + xd ** 2) ** 0.5
        cgamma = abs(yd) / (yd ** 2 + zd ** 2) ** 0.5
        for iy in range(ny):
            yc = (iy - ny2 + 0.5) * dy + cy
            xt = ((yc - y1t) * (x2t - x1t) / (y2t - y1t) + x1t - cx) / dx + nx2
            xb = ((yc - y1b) * (x2b - x1b) / (y2b - y1b) + x1b - cx) / dx + nx2
            if xb > xt:
                xt, xb = xb, xt
            if xb >= nx or xt < 0:
                continue
            zt = ((yc - y1t) * (z2t - z1t) / (y2t - y1t) + z1t - cz) / dz + nz2
            zb = ((yc - y1b) * (z2b - z1b) / (y2b - y1b) + z1b - cz) / dz + nz2
            if zb > zt:
                zt, zb = zb, zt
            if zb >= nz or zt < 0:
                continue
            for ix in range(max(0, int(xb)), min(nx, 1 + int(xt))):
                wx = min(ix + 1, xt) - max(ix, xb)
                # wx /= (xt - xb)
                for iz in range(max(0, int(zb)), min(nz, 1 + int(zt))):
                    wz = min(iz + 1, zt) - max(iz, zb)
                    # wz /= (zt - zb)
                    # vproj[i] += image[ix, iy, iz] * wx * wz / calpha / cgamma
                    # cuda.atomic.add(image, (ix, iy, iz), wx * wz / calpha / cgamma * vproj[i])
                    image[ix, iy, iz] += wx * wz * vproj


# @jit
def bproj_distance_driven(vproj, lors, shape, blockdy2, blockdz2, nb_blocks, center, unit_size):
    image = np.zeros(shape, dtype = np.float32)
    for i in range(lors.shape[0]):
        _kernel_bproj_3d_distance_driven(vproj[i], lors[i, :3], lors[i, 3:],
                                         blockdy2, blockdz2, nb_blocks, center, unit_size, image)
    return image


@cuda.jit(device = True)
def position_to_block_angle_cuda(pos, nb_blocks):
    xc, yc, _ = pos
    angle_per_block = 2 * _pi / nb_blocks
    #     angle = round(math.atan2(yc, xc) // angle_per_block) * angle_per_block
    iangle = (angle_per_block / 2 + math.atan2(yc, xc)) // angle_per_block
    #     iangle = math.floor(angle)
    return iangle


@cuda.jit(device = True)
def _kernel_bproj_3d_distance_driven_cuda(i, vproj, fst, snd, blockdy2, blockdz2, nb_blocks,
                                          center, unit_size, image):
    dx, dy, dz = unit_size
    cx, cy, cz = center
    x1, y1, z1 = fst
    x2, y2, z2 = snd
    xd, yd, zd = x2 - x1, y2 - y1, z2 - z1
    if xd ** 2 + yd ** 2 < 100:
        return
    nx, ny, nz = image.shape
    nx2, ny2, nz2 = nx / 2, ny / 2, nz / 2

    itheta1 = position_to_block_angle_cuda(fst, nb_blocks)
    itheta2 = position_to_block_angle_cuda(snd, nb_blocks)
    angle_per_block = 2 * _pi / nb_blocks
    # if abs(itheta1 % nb_blocks - itheta2 % nb_blocks) <= 1.:
    #     return
    ctheta1, stheta1 = math.cos(itheta1 * angle_per_block), math.sin(itheta1 * angle_per_block)
    ctheta2, stheta2 = math.cos(itheta2 * angle_per_block), math.sin(itheta2 * angle_per_block)
    x1t, x1b = x1 - stheta1 * blockdy2, x1 + stheta1 * blockdy2
    x2t, x2b = x2 + stheta2 * blockdy2, x2 - stheta2 * blockdy2
    y1t, y1b = y1 + ctheta1 * blockdy2, y1 - ctheta1 * blockdy2
    y2t, y2b = y2 - ctheta2 * blockdy2, y2 + ctheta2 * blockdy2

    z1t, z1b = z1 + blockdz2, z1 - blockdz2
    z2t, z2b = z2 + blockdz2, z2 - blockdz2
    if abs(xd) >= abs(yd):
        calpha = abs(xd) / (xd ** 2 + yd ** 2) ** 0.5
        cgamma = abs(xd) / (xd ** 2 + zd ** 2) ** 0.5
        for ix in range(nx):
            xc = (ix - nx2 + 0.5) * dx + cx
            yt = ((xc - x1t) * (y2t - y1t) / (x2t - x1t) + y1t - cy) / dy + ny2
            yb = ((xc - x1b) * (y2b - y1b) / (x2b - x1b) + y1b - cy) / dy + ny2
            if yb > yt:
                yt, yb = yb, yt
            if yb >= ny or yt < 0:
                continue
            zt = ((xc - x1t) * (z2t - z1t) / (x2t - x1t) + z1t - cz) / dz + nz2
            zb = ((xc - x1b) * (z2b - z1b) / (x2b - x1b) + z1b - cz) / dz + nz2
            if zb > zt:
                zt, zb = zb, zt
            if zb >= nz or zt < 0:
                continue
            for iy in range(max(0, int(yb)), min(ny, 1 + int(yt))):
                wy = min(iy + 1, yt) - max(iy, yb)
                # wy /= (yt - yb)
                for iz in range(max(0, int(zb)), min(nz, 1 + int(zt))):
                    wz = min(iz + 1, zt) - max(iz, zb)
                    # wz /= (zt - zb)
                    # vproj[i] += image[ix, iy, iz] * wy * wz / calpha / cgamma
                    # cuda.atomic.add(image, (ix, iy, iz), wy * wz / calpha / cgamma * vproj[i])
                    cuda.atomic.add(image, (ix, iy, iz), wy * wz * vproj[i])
    else:
        calpha = abs(yd) / (yd ** 2 + xd ** 2) ** 0.5
        cgamma = abs(yd) / (yd ** 2 + zd ** 2) ** 0.5
        for iy in range(ny):
            yc = (iy - ny2 + 0.5) * dy + cy
            xt = ((yc - y1t) * (x2t - x1t) / (y2t - y1t) + x1t - cx) / dx + nx2
            xb = ((yc - y1b) * (x2b - x1b) / (y2b - y1b) + x1b - cx) / dx + nx2
            if xb > xt:
                xt, xb = xb, xt
            if xb >= nx or xt < 0:
                continue
            zt = ((yc - y1t) * (z2t - z1t) / (y2t - y1t) + z1t - cz) / dz + nz2
            zb = ((yc - y1b) * (z2b - z1b) / (y2b - y1b) + z1b - cz) / dz + nz2
            if zb > zt:
                zt, zb = zb, zt
            if zb >= nz or zt < 0:
                continue
            for ix in range(max(0, int(xb)), min(nx, 1 + int(xt))):
                wx = min(ix + 1, xt) - max(ix, xb)
                # wx /= (xt - xb)
                for iz in range(max(0, int(zb)), min(nz, 1 + int(zt))):
                    wz = min(iz + 1, zt) - max(iz, zb)
                    # wz /= (zt - zb)
                    # vproj[i] += image[ix, iy, iz] * wx * wz / calpha / cgamma
                    # cuda.atomic.add(image, (ix, iy, iz), wx * wz / calpha / cgamma * vproj[i])
                    cuda.atomic.add(image, (ix, iy, iz), wx * wz * vproj[i])


@cuda.jit
def bproj_distance_driven_cuda(vproj, lors, blockdy2, blockdz2, nb_blocks, center, unit_size,
                               image):
    i = cuda.grid(1)
    if i >= lors.shape[0]:
        return
    _kernel_bproj_3d_distance_driven_cuda(i, vproj, lors[i, :3], lors[i, 3:],
                                          blockdy2, blockdz2, nb_blocks, center, unit_size, image)


@funcclass
class BackProjectorDistanceDriven(BackProjector):
    shape: np.ndarray = attr.ib(converter = np.array)
    center: np.ndarray = attr.ib(converter = np.array)
    size: np.ndarray = attr.ib(converter = np.array)
    scanner: PETCylindricalScanner
    device: str = 'gpu'

    def __call__(self, listmode: Listmode):
        nb_blocks = int(self.scanner.nb_blocks_per_ring)
        blockdy2 = self.scanner.blocks.unit_size[1] / 2
        blockdz2 = self.scanner.blocks.unit_size[2] / 2
        _center = self.center
        _unit_size = self.size / self.shape

        if self.device == 'cpu':
            image_data = bproj_distance_driven(listmode.data, listmode.lors.data, self.shape,
                                               blockdy2, blockdz2, nb_blocks, _center, _unit_size)
        elif self.device == 'gpu':
            blockdim = (256,)
            griddim = (1 + int(len(listmode.lors) / blockdim[0]),)
            image_data = np.zeros(self.shape, dtype = np.float32)
            if not isinstance(listmode.data, np.ndarray):
                image_data = cuda.device_array(self.shape, dtype = float32)
            bproj_distance_driven_cuda[griddim, blockdim](listmode.data, listmode.lors.data,
                                                          blockdy2, blockdz2, nb_blocks, _center,
                                                          _unit_size, image_data)
        else:
            raise NotImplementedError
        return Image(image_data, self.center, self.size)

    @property
    def unit_size(self):
        return self.size / self.shape
