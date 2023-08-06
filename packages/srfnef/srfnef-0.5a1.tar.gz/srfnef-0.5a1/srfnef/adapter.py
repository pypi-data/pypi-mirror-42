# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: adapter.py
@date: 2/26/2019
@desc:
'''
import json

import h5py
import numpy as np

from .data_types import Block, PETCylindricalScanner, Listmode, LORs


def _block_from_API(path):
    with open(path, 'r') as fin:
        dct = json.load(fin)
        _shape = dct['scanner']['petscanner']['block']['grid']
        _size = dct['scanner']['petscanner']['block']['size']
        _block = Block(_size, _shape)
        return _block


def _scanner_from_API(path):
    _block = _block_from_API(path)
    with open(path, 'r') as fin:
        dct = json.load(fin)
        _inner_radius = dct['scanner']['petscanner']['ring']['inner_radius']
        _outer_radius = dct['scanner']['petscanner']['ring']['outer_radius']
        _nb_rings = dct['scanner']['petscanner']['ring']['nb_rings']
        _nb_blocks_per_ring = dct['scanner']['petscanner']['ring']['nb_blocks_per_ring']
        _gap = dct['scanner']['petscanner']['ring']['gap']
        _scanner = PETCylindricalScanner(_inner_radius, _outer_radius, _nb_rings,
                                         _nb_blocks_per_ring, _gap, _block)
        return _scanner


PETCylindricalScanner.from_old_API = classmethod(lambda cls, path: _scanner_from_API(path))


def load_listmode_from_h5(path, scanner):
    with h5py.File(path, 'r') as fin:
        fst = np.array(fin['listmode_data']['fst'])
        snd = np.array(fin['listmode_data']['snd'])
    return Listmode.from_lors(LORs.from_fst_snd(fst, snd)).compress(scanner)
