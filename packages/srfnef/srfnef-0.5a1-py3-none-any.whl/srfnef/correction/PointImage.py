# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: PointImage.py
@date: 2/14/2019
@desc:
'''

import numpy as np
import attr
from srfnef.data import Image
from srfnef.templating import dataclass

__all__ = ('PointImage',)


@dataclass
class PointImage:
    image: Image
    point_ind: np.ndarray = attr.ib(converter = np.array)
    type: int  # 0 for xy and 1 for z


from srfnef.templating import TYPE_BIND


TYPE_BIND.update({'PointImage': PointImage})
