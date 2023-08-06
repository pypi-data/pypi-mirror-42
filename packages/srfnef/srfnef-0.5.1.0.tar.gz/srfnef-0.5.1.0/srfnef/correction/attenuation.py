
import numpy as np

from srfnef.data_types import Image, Listmode
from srfnef.func_types import Projector
from srfnef.templating import funcclass, BinaryOps

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
        u_map_proj = u_map_proj * L * L
        return u_map_proj.replace(data = np.exp(-u_map_proj.data))


def corrector(u_map_proj: Listmode, mode = 'outer'):
    if mode == 'outer':
        # return lambda x: mlem(x / u_map_proj)
        return lambda obj: obj @ BinaryOps.Truediv(u_map_proj)
        # def wrapper(obj):
        #     projector2 = obj.projector @ BinaryOps.Truediv(u_map_proj)
        #     return obj.replace(projector = projector2)
        # return wra
    elif mode == 'proj':
        # projector2 = lambda x, lors: u_map_proj * mlem.projector(x, lors)
        def wrapper(obj):
            projector2 = BinaryOps.Mul(u_map_proj) @ obj.projector
            return obj.replace(projector = projector2)

        return wrapper
    elif mode == 'bproj':
        # bprojector2 = lambda listmode: mlem.bprojector(listmode / u_map_proj)
        def wrapper(obj):
            bprojector2 = obj.bprojector @ BinaryOps.Truediv(u_map_proj)
            return obj.replace(bprojector = bprojector2)

        return wrapper
    elif mode == 'proj_bproj':
        # projector2 = lambda x, lors: u_map_proj * mlem.projector(x, lors)
        # bprojector2 = lambda listmode: mlem.bprojector(listmode / u_map_proj)
        def wrapper(obj):
            projector2 = BinaryOps.Mul(u_map_proj) @ obj.projector
            bprojector2 = obj.bprojector @ BinaryOps.Truediv(u_map_proj)
            return obj.replace(projector = projector2, bprojector = bprojector2)

        return wrapper
    else:
        raise AttributeError('mode can only be \' outer\', \' proj\', \' bproj\' or \' '
                             'proj_bproj\'')


from srfnef.templating import TYPE_BIND

TYPE_BIND.update({'UMapProjector': UMapProjector})
