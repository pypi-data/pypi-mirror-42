# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: __init__.py
@date: 2/26/2019
@desc:
'''
__all__ = (
    'ProjectorSiddon', 'ProjectorDistanceDriven', 'BackProjectorSiddon',
    'BackProjectorDistanceDriven')
from srfnef.templating import TYPE_BIND
from ._bproj_distance_driven import BackProjectorDistanceDriven
from ._bproj_siddon import BackProjectorSiddon
from ._proj_distance_driven import ProjectorDistanceDriven
from ._proj_siddon import ProjectorSiddon

TYPE_BIND.update({'BackProjectorDistanceDriven': BackProjectorDistanceDriven,
                  'BackProjectorSiddon': BackProjectorSiddon,
                  'ProjectorDistanceDriven': ProjectorDistanceDriven,
                  'ProjectorSiddon': ProjectorSiddon})
