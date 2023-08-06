# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: _proj_distance_driven.py
@date: 1/21/2019
@desc:
'''
import math

import numpy as np
from numba import jit, cuda, float32

from srfnef.data_types import Image, Listmode, LORs, PETCylindricalScanner
from srfnef.func_types import Projector
from srfnef.templating import funcclass
from srfnef.utils import _pi

running_env = jit(nopython = True, parallel = True)


@running_env
def position_to_block_angle(pos, nb_blocks):
    xc, yc, _ = pos
    angle_per_block = 2 * _pi / nb_blocks
    iangle = (angle_per_block / 2 + math.atan2(yc, xc)) / angle_per_block
    return iangle % nb_blocks


@running_env
def _kernel_proj_3d_distance_driven(i, image, fst, snd, blockdy2, blockdz2, unit_size, center,
                                    nb_blocks, vproj):
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
    ctheta1, stheta1 = math.cos(itheta1 * angle_per_block), math.sin(itheta1 * angle_per_block)
    ctheta2, stheta2 = math.cos(itheta2 * angle_per_block), math.sin(itheta2 * angle_per_block)
    x1t, x1b = x1 - stheta1 * blockdy2, x1 + stheta1 * blockdy2
    x2t, x2b = x2 + stheta2 * blockdy2, x2 - stheta2 * blockdy2
    y1t, y1b = y1 + ctheta1 * blockdy2, y1 - ctheta1 * blockdy2
    y2t, y2b = y2 - ctheta2 * blockdy2, y2 + ctheta2 * blockdy2

    z1t, z1b = z1 + blockdz2, z1 - blockdz2
    z2t, z2b = z2 + blockdz2, z2 - blockdz2
    L1 = 0.
    L2 = 0.
    if abs(xd) >= abs(yd):
        calpha = abs(xd) / (xd ** 2 + yd ** 2) ** 0.5
        cgamma = abs(xd) / (xd ** 2 + zd ** 2) ** 0.5
        yt = (x1 - x1t) * (y2t - y1t) / (x2t - x1t) + y1t + ny2
        yb = (x1 - x1b) * (y2b - y1b) / (x2b - x1b) + y1b + ny2
        L1 += abs(yt - yb)
        yt = (x2 - x1t) * (y2t - y1t) / (x2t - x1t) + y1t + ny2
        yb = (x2 - x1b) * (y2b - y1b) / (x2b - x1b) + y1b + ny2
        L1 += abs(yt - yb)
        L1 *= abs(x2 - x1) / 2
        zt = ((x1 - x1t) * (z2t - z1t) / (x2t - x1t) + z1t) / dz + nz2
        zb = ((x1 - x1b) * (z2b - z1b) / (x2b - x1b) + z1b) / dz + nz2
        L2 += abs(zt - zb)
        zt = ((x2 - x1t) * (z2t - z1t) / (x2t - x1t) + z1t) / dz + nz2
        zb = ((x2 - x1b) * (z2b - z1b) / (x2b - x1b) + z1b) / dz + nz2
        L2 += abs(zt - zb)
        L2 *= abs(x2 - x1) / 2
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
                for iz in range(max(0, int(zb)), min(nz, 1 + int(zt))):
                    wz = min(iz + 1, zt) - max(iz, zb)
                    vproj[i] += image[ix, iy, iz] * wy * wz
    else:
        calpha = abs(yd) / (yd ** 2 + xd ** 2) ** 0.5
        cgamma = abs(yd) / (yd ** 2 + zd ** 2) ** 0.5
        xt = (y1 - y1t) * (x2t - x1t) / (y2t - y1t) + x1t + nx2
        xb = (y1 - y1b) * (x2b - x1b) / (y2b - y1b) + x1b + nx2
        L1 += abs(xt - xb)
        xt = (y2 - y1t) * (x2t - x1t) / (y2t - y1t) + x1t + nx2
        xb = (y2 - y1b) * (x2b - x1b) / (y2b - y1b) + x1b + nx2
        L1 += abs(xt - xb)
        L1 *= abs(y2 - y1) / 2
        zt = ((y1 - y1t) * (z2t - z1t) / (y2t - y1t) + z1t) / dz + nz2
        zb = ((y1 - y1b) * (z2b - z1b) / (y2b - y1b) + z1b) / dz + nz2
        L2 += abs(zt - zb)
        zt = ((y2 - y1t) * (z2t - z1t) / (y2t - y1t) + z1t) / dz + nz2
        zb = ((y2 - y1b) * (z2b - z1b) / (y2b - y1b) + z1b) / dz + nz2
        L2 += abs(zt - zb)
        L2 *= abs(y2 - y1) / 2
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
                for iz in range(max(0, int(zb)), min(nz, 1 + int(zt))):
                    wz = min(iz + 1, zt) - max(iz, zb)
                    vproj[i] += image[ix, iy, iz] * wx * wz
    if L1 * L2 > 0:
        vproj[i] /= L1 * L2


@running_env
def proj_distance_driven(image, lors, blockdy2, blockdz2, unit_size, center, nb_blocks):
    vproj = np.zeros((lors.shape[0],), dtype = np.float32)
    for i in range(lors.shape[0]):
        _kernel_proj_3d_distance_driven(i, image, lors[i, :3], lors[i, 3:],
                                        blockdy2, blockdz2, unit_size, center, nb_blocks, vproj)
    return vproj


@cuda.jit(device = True)
def position_to_block_angle_cuda(pos, nb_blocks):
    xc, yc, _ = pos
    angle_per_block = 2 * _pi / nb_blocks
    #     angle = round(math.atan2(yc, xc) // angle_per_block) * angle_per_block
    iangle = (angle_per_block / 2 + math.atan2(yc, xc)) / angle_per_block
    #     iangle = math.floor(angle)
    return iangle % nb_blocks


@cuda.jit(device = True)
def _kernel_proj_3d_distance_driven_cuda(i, image, fst, snd, blockdy2, blockdz2, unit_size, center,
                                         nb_blocks, vproj):
    dx, dy, dz = unit_size
    dz /= dx
    x1, y1, z1 = (fst[0] - center[0]) / dx, (fst[1] - center[1]) / dx, \
                 (fst[2] - center[2]) / dx
    x2, y2, z2 = (snd[0] - center[0]) / dx, (snd[1] - center[1]) / dx, \
                 (snd[2] - center[2]) / dx
    xd, yd, zd = x2 - x1, y2 - y1, z2 - z1
    if xd ** 2 + yd ** 2 < 100:
        return
    nx, ny, nz = image.shape
    nx2, ny2, nz2 = nx / 2, ny / 2, nz / 2

    itheta1 = position_to_block_angle_cuda(fst, nb_blocks)
    itheta2 = position_to_block_angle_cuda(snd, nb_blocks)
    angle_per_block = 2 * _pi / nb_blocks

    ctheta1, stheta1 = math.cos(itheta1 * angle_per_block), math.sin(itheta1 * angle_per_block)
    ctheta2, stheta2 = math.cos(itheta2 * angle_per_block), math.sin(itheta2 * angle_per_block)
    x1t, x1b = x1 - stheta1 * blockdy2, x1 + stheta1 * blockdy2
    x2t, x2b = x2 + stheta2 * blockdy2, x2 - stheta2 * blockdy2
    y1t, y1b = y1 + ctheta1 * blockdy2, y1 - ctheta1 * blockdy2
    y2t, y2b = y2 - ctheta2 * blockdy2, y2 + ctheta2 * blockdy2

    z1t, z1b = z1 + blockdz2, z1 - blockdz2
    z2t, z2b = z2 + blockdz2, z2 - blockdz2
    L1 = 0.
    L2 = 0.
    if abs(xd) >= abs(yd):
        calpha = abs(xd) / (xd ** 2 + yd ** 2) ** 0.5
        cgamma = abs(xd) / (xd ** 2 + zd ** 2) ** 0.5
        yt = (x1 - x1t) * (y2t - y1t) / (x2t - x1t) + y1t + ny2
        yb = (x1 - x1b) * (y2b - y1b) / (x2b - x1b) + y1b + ny2
        L1 += abs(yt - yb)
        yt = (x2 - x1t) * (y2t - y1t) / (x2t - x1t) + y1t + ny2
        yb = (x2 - x1b) * (y2b - y1b) / (x2b - x1b) + y1b + ny2
        L1 += abs(yt - yb)
        L1 *= abs(x2 - x1) / 2
        zt = ((x1 - x1t) * (z2t - z1t) / (x2t - x1t) + z1t) / dz + nz2
        zb = ((x1 - x1b) * (z2b - z1b) / (x2b - x1b) + z1b) / dz + nz2
        L2 += abs(zt - zb)
        zt = ((x2 - x1t) * (z2t - z1t) / (x2t - x1t) + z1t) / dz + nz2
        zb = ((x2 - x1b) * (z2b - z1b) / (x2b - x1b) + z1b) / dz + nz2
        L2 += abs(zt - zb)
        L2 *= abs(x2 - x1) / 2

        for ix in range(nx):
            xc = ix - nx2 + 0.5
            yt = (xc - x1t) * (y2t - y1t) / (x2t - x1t) + y1t + ny2
            yb = (xc - x1b) * (y2b - y1b) / (x2b - x1b) + y1b + ny2
            if yb > yt:
                yt, yb = yb, yt
            if yb >= ny or yt < 0:
                continue
            zt = ((xc - x1t) * (z2t - z1t) / (x2t - x1t) + z1t) / dz + nz2
            zb = ((xc - x1b) * (z2b - z1b) / (x2b - x1b) + z1b) / dz + nz2
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
                    vproj[i] += image[ix, iy, iz] * wy * wz
    else:
        calpha = abs(yd) / (yd ** 2 + xd ** 2) ** 0.5
        cgamma = abs(yd) / (yd ** 2 + zd ** 2) ** 0.5
        xt = (y1 - y1t) * (x2t - x1t) / (y2t - y1t) + x1t + nx2
        xb = (y1 - y1b) * (x2b - x1b) / (y2b - y1b) + x1b + nx2
        L1 += abs(xt - xb)
        xt = (y2 - y1t) * (x2t - x1t) / (y2t - y1t) + x1t + nx2
        xb = (y2 - y1b) * (x2b - x1b) / (y2b - y1b) + x1b + nx2
        L1 += abs(xt - xb)
        L1 *= abs(y2 - y1) / 2
        zt = ((y1 - y1t) * (z2t - z1t) / (y2t - y1t) + z1t) / dz + nz2
        zb = ((y1 - y1b) * (z2b - z1b) / (y2b - y1b) + z1b) / dz + nz2
        L2 += abs(zt - zb)
        zt = ((y2 - y1t) * (z2t - z1t) / (y2t - y1t) + z1t) / dz + nz2
        zb = ((y2 - y1b) * (z2b - z1b) / (y2b - y1b) + z1b) / dz + nz2
        L2 += abs(zt - zb)
        L2 *= abs(y2 - y1) / 2

        for iy in range(ny):
            yc = iy - ny2 + 0.5
            xt = (yc - y1t) * (x2t - x1t) / (y2t - y1t) + x1t + nx2
            xb = (yc - y1b) * (x2b - x1b) / (y2b - y1b) + x1b + nx2
            if xb > xt:
                xt, xb = xb, xt
            if xb >= nx or xt < 0:
                continue
            zt = ((yc - y1t) * (z2t - z1t) / (y2t - y1t) + z1t) / dz + nz2
            zb = ((yc - y1b) * (z2b - z1b) / (y2b - y1b) + z1b) / dz + nz2
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
                    vproj[i] += image[ix, iy, iz] * wx * wz
                    # L += weight
    if L1 * L2 > 0:
        vproj[i] /= L1 * L2


@cuda.jit
def proj_distance_driven_cuda(image, lors, blockdy2, blockdz2, unit_size, center, nb_blocks, vproj):
    i = cuda.grid(1)
    if i >= lors.shape[0]:
        return
    _kernel_proj_3d_distance_driven_cuda(i, image, lors[i, :3], lors[i, 3:],
                                         blockdy2, blockdz2, unit_size, center, nb_blocks, vproj)


@funcclass
class ProjectorDistanceDriven(Projector):
    scanner: PETCylindricalScanner
    device: str = 'gpu'

    def __call__(self, image: Image, lors: LORs):
        nb_blocks = self.scanner.nb_blocks_per_ring
        blockdy2 = self.scanner.blocks.unit_size[1] / 2
        blockdz2 = self.scanner.blocks.unit_size[2] / 2

        if self.device == 'cpu':
            vproj = proj_distance_driven(image.data, lors.data, blockdy2, blockdz2,
                                         image.size / image.shape, image.center, nb_blocks)
        elif self.device == 'gpu':
            # print('projecting in gpu device...')
            blockdim = (256,)
            griddim = (1 + int(len(lors) / blockdim[0]),)
            vproj = np.zeros((len(lors),), dtype = np.float32)
            if not isinstance(image.data, np.ndarray):
                vproj = cuda.device_array((len(lors),), dtype = float32)
            proj_distance_driven_cuda[griddim, blockdim](image.data, lors.data, blockdy2,
                                                         blockdz2, image.size / image.shape,
                                                         image.center, nb_blocks, vproj)
        else:
            raise NotImplementedError
        return Listmode(vproj, lors)
