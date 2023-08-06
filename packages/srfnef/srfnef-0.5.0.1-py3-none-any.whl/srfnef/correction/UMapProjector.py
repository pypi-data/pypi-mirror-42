# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: attenuation.py
@date: 2/25/2019
@desc:
'''
import numpy as np

from srfnef.data_types import Image
from srfnef.func_types import Projector
from srfnef.templating import funcclass

__all__ = ('UMapProjector',)


@funcclass
class UMapProjector:
    projector: Projector

    def __call__(self, u_map: Image, lors):
        u_map_proj = self.projector(u_map, lors)
        dx = u_map_proj.lors.data[:, 0] - u_map_proj.lors.data[:, 3]
        dy = u_map_proj.lors.data[:, 1] - u_map_proj.lors.data[:, 4]
        dz = u_map_proj.lors.data[:, 2] - u_map_proj.lors.data[:, 5]
        L = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
        u_map_proj = u_map_proj * L
        return u_map_proj.replace(data = np.exp(-u_map_proj.data))


from srfnef.templating import TYPE_BIND

TYPE_BIND.update({'UMapProjector': UMapProjector})
