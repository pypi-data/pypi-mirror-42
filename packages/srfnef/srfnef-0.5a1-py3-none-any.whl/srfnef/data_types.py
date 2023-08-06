from copy import deepcopy

import attr
import numpy as np
import scipy.ndimage as nd
from numba import jit
from scipy import sparse

from .templating import dataclass, TYPE_BIND
from .utils import is_notebook, _tqdm


@dataclass
class Block:
    size: np.ndarray = attr.ib(converter = np.array)
    shape: np.ndarray = attr.ib(converter = np.array)

    @property
    def unit_size(self):
        return np.array([self.size[i] / self.shape[i] for i in range(len(self.size))])


@dataclass
class PETCylindricalScanner:
    inner_radius: float
    outer_radius: float
    nb_rings: int
    nb_blocks_per_ring: int
    gap: float
    blocks: Block

    @property
    def axial_length(self):
        return self.blocks.size[2] * self.nb_rings + self.gap * (self.nb_rings - 1)

    @property
    def central_bin_size(self):
        return 2 * np.pi * self.inner_radius / self.nb_detectors_per_ring / 2

    @property
    def nb_detectors_per_block(self):
        return np.prod(self.blocks.shape)

    @property
    def nb_detectors_per_ring(self):
        return self.nb_detectors_per_block * self.nb_blocks_per_ring

    @property
    def nb_detectors(self):
        return self.nb_detectors_per_ring * self.nb_rings

    @property
    def angle_per_block(self):
        return 2 * np.pi / self.nb_blocks_per_ring

    @property
    def nb_thin_rings(self):
        return self.nb_rings * self.blocks.shape[2]

    @property
    def nb_detectors_per_thin_ring(self):
        return self.blocks.shape[1] * self.nb_blocks_per_ring


@dataclass
class LORs:
    data: np.ndarray

    @property
    def fst(self):
        return self.data[:, :3]

    @property
    def snd(self):
        return self.data[:, 3:]

    @property
    def shape(self):
        return self.data.shape

    def __len__(self):
        return self.data.shape[0]

    def __bool__(self):
        return self.__len__() > 0

    @classmethod
    def from_scanner(cls, scanner):
        _lors = _mesh_detector(scanner)
        return cls(_lors)

    @classmethod
    def from_scanner_ring(cls, scanner, i, j):
        _lors = _mesh_detector_ring(scanner, i, j)
        return cls(_lors)

    @classmethod
    def from_scanner_thin_ring(cls, scanner, i, j):
        _lors = _mesh_detector_thin_ring(scanner, i, j)
        return cls(_lors)

    @classmethod
    def from_fst_snd(cls, fst, snd):
        return cls(np.hstack((fst, snd)))


def _mesh_detector(scanner):
    lors = np.zeros((scanner.nb_detectors * scanner.nb_detectors, 6), dtype = np.float32)

    R = (scanner.inner_radius + scanner.outer_radius) / 2
    theta = 2 * np.pi / scanner.nb_blocks_per_ring * np.arange(scanner.nb_blocks_per_ring)
    x = np.ones(scanner.blocks.shape[1], ) * R
    y = (np.arange(scanner.blocks.shape[1]) + 0.5) * scanner.blocks.unit_size[1] - \
        scanner.blocks.size[1] / 2
    z = (np.arange(scanner.blocks.shape[2]) + 0.5) * scanner.blocks.unit_size[2]
    xx = np.kron(x, [1] * scanner.nb_blocks_per_ring)
    yy = np.kron(y, [1] * scanner.nb_blocks_per_ring)
    theta1 = np.kron(theta, [[1]] * scanner.blocks.shape[1]).ravel()
    xx1 = xx * np.cos(theta1) - yy * np.sin(theta1)
    yy1 = xx * np.sin(theta1) + yy * np.cos(theta1)

    xx2 = np.kron(xx1, [[1]] * scanner.blocks.shape[2]).ravel()
    yy2 = np.kron(yy1, [[1]] * scanner.blocks.shape[2]).ravel()
    zz2 = np.kron(z, [1] * scanner.blocks.shape[1] * scanner.nb_blocks_per_ring).ravel()

    xd = np.kron(xx2, [[1]] * scanner.nb_rings).ravel()
    yd = np.kron(yy2, [[1]] * scanner.nb_rings).ravel()
    zd = np.kron(zz2, [[1]] * scanner.nb_rings).ravel()
    for i in range(scanner.nb_rings):
        zd[i * scanner.nb_detectors_per_ring + np.arange(scanner.nb_detectors_per_ring)] += \
            i * scanner.blocks.size[2] + i * scanner.gap - scanner.axial_length / 2

    lors[:, 0] = np.kron(xd, [1] * scanner.nb_detectors)
    lors[:, 1] = np.kron(yd, [1] * scanner.nb_detectors)
    lors[:, 2] = np.kron(zd, [1] * scanner.nb_detectors)
    lors[:, 3] = np.kron(xd, [[1]] * scanner.nb_detectors).ravel()
    lors[:, 4] = np.kron(yd, [[1]] * scanner.nb_detectors).ravel()
    lors[:, 5] = np.kron(zd, [[1]] * scanner.nb_detectors).ravel()

    return lors


def _mesh_detector_ring(scanner, i, j):
    lors = np.zeros((scanner.nb_detectors_per_ring * scanner.nb_detectors_per_ring, 6),
                    dtype = np.float32)

    R = (scanner.inner_radius + scanner.outer_radius) / 2
    theta = 2 * np.pi / scanner.nb_blocks_per_ring * np.arange(scanner.nb_blocks_per_ring)
    x = np.ones(scanner.blocks.shape[1], ) * R
    y = (np.arange(scanner.blocks.shape[1]) + 0.5) * scanner.blocks.unit_size[1] - \
        scanner.blocks.size[1] / 2
    z = (np.arange(scanner.blocks.shape[2]) + 0.5) * scanner.blocks.unit_size[2]
    xx = np.kron(x, [1] * scanner.nb_blocks_per_ring)
    yy = np.kron(y, [1] * scanner.nb_blocks_per_ring)
    theta1 = np.kron(theta, [[1]] * scanner.blocks.shape[1]).ravel()
    xx1 = xx * np.cos(theta1) - yy * np.sin(theta1)
    yy1 = xx * np.sin(theta1) + yy * np.cos(theta1)

    xx2 = np.kron(xx1, [[1]] * scanner.blocks.shape[2]).ravel()
    yy2 = np.kron(yy1, [[1]] * scanner.blocks.shape[2]).ravel()
    zz2 = np.kron(z, [1] * scanner.blocks.shape[1] * scanner.nb_blocks_per_ring).ravel()

    xd = xx2
    yd = yy2
    zd = zz2

    lors[:, 0] = np.kron(xd, [1] * scanner.nb_detectors_per_ring)
    lors[:, 1] = np.kron(yd, [1] * scanner.nb_detectors_per_ring)
    lors[:, 2] = np.kron(zd + i * scanner.blocks.size[2] + i * scanner.gap,
                         [1] * scanner.nb_detectors_per_ring)
    lors[:, 3] = np.kron(xd, [[1]] * scanner.nb_detectors_per_ring).ravel()
    lors[:, 4] = np.kron(yd, [[1]] * scanner.nb_detectors_per_ring).ravel()
    lors[:, 5] = np.kron(zd + j * scanner.blocks.size[2] + j * scanner.gap,
                         [[1]] * scanner.nb_detectors_per_ring).ravel()

    return lors


def _mesh_detector_thin_ring(scanner, i, j):
    lors = np.zeros((scanner.nb_detectors_per_thin_ring * scanner.nb_detectors_per_thin_ring, 6),
                    dtype = np.float32)

    R = (scanner.inner_radius + scanner.outer_radius) / 2
    theta = 2 * np.pi / scanner.nb_blocks_per_ring * np.arange(scanner.nb_blocks_per_ring)
    x = np.ones(scanner.blocks.shape[1], ) * R
    y = (np.arange(scanner.blocks.shape[1]) + 0.5) * scanner.blocks.unit_size[1] - \
        scanner.blocks.size[1] / 2
    z = 0.5 * scanner.blocks.unit_size[2]
    xx = np.kron(x, [1] * scanner.nb_blocks_per_ring)
    yy = np.kron(y, [1] * scanner.nb_blocks_per_ring)
    theta1 = np.kron(theta, [[1]] * scanner.blocks.shape[1]).ravel()
    xx1 = xx * np.cos(theta1) - yy * np.sin(theta1)
    yy1 = xx * np.sin(theta1) + yy * np.cos(theta1)

    xd = np.kron(xx1, [[1]] * 1).ravel()
    yd = np.kron(yy1, [[1]] * 1).ravel()
    zd = np.kron(z, [1] * scanner.blocks.shape[1] * scanner.nb_blocks_per_ring).ravel()

    lors[:, 0] = np.kron(xd, [1] * scanner.nb_detectors_per_thin_ring)
    lors[:, 1] = np.kron(yd, [1] * scanner.nb_detectors_per_thin_ring)
    lors[:, 2] = np.kron(zd + i * scanner.blocks.unit_size[2] + i * scanner.gap,
                         [1] * scanner.nb_detectors_per_thin_ring)
    lors[:, 3] = np.kron(xd, [[1]] * scanner.nb_detectors_per_thin_ring).ravel()
    lors[:, 4] = np.kron(yd, [[1]] * scanner.nb_detectors_per_thin_ring).ravel()
    lors[:, 5] = np.kron(zd + j * scanner.blocks.unit_size[2] + j * scanner.gap,
                         [[1]] * scanner.nb_detectors_per_thin_ring).ravel()

    return lors


@dataclass
class Sinogram:
    data: sparse.csr_matrix
    scanner: PETCylindricalScanner

    @property
    def shape(self):
        return self.data.shape

    @property
    def vproj(self):
        return self.data

    @classmethod
    def initializer(cls, scanner):
        D = np.ones((scanner.nb_detectors, scanner.nb_detectors), dtype = np.float32)
        return cls(sparse.csr_matrix(D), scanner)

    def to_listmode(self):
        return _sinogram_to_listmode(self)


def _sinogram_to_listmode(sino: Sinogram):
    scanner = sino.scanner
    csr = sino.data
    row, col = csr.nonzero()
    iy1 = row % scanner.blocks.shape[1]
    ib1 = (row // scanner.blocks.shape[1]) % scanner.nb_blocks_per_ring
    i_thin_ring1 = row // scanner.nb_detectors_per_thin_ring
    lors_data = np.zeros((csr.nnz, 6), dtype = np.float32)
    x0 = (scanner.inner_radius + scanner.outer_radius) / 2
    y0 = (iy1 + 0.5) * scanner.blocks.unit_size[1] - scanner.blocks.size[1] / 2
    theta = scanner.angle_per_block * ib1
    lors_data[:, 0] = x0 * np.cos(theta) - y0 * np.sin(theta)
    lors_data[:, 1] = x0 * np.sin(theta) + y0 * np.cos(theta)
    lors_data[:, 2] = (i_thin_ring1 + 0.5) * scanner.blocks.unit_size[2] - scanner.axial_length / 2

    iy2 = col % scanner.blocks.shape[1]
    ib2 = (col // scanner.blocks.shape[1]) % scanner.nb_blocks_per_ring
    i_thin_ring2 = col // scanner.nb_detectors_per_thin_ring
    #     print(iy1, iy2, ib1, ib2, i_thin_ring1, i_thin_ring2)
    x0 = (scanner.inner_radius + scanner.outer_radius) / 2
    y0 = (iy2 + 0.5) * scanner.blocks.unit_size[1] - scanner.blocks.size[1] / 2
    theta = scanner.angle_per_block * ib2
    lors_data[:, 3] = x0 * np.cos(theta) - y0 * np.sin(theta)
    lors_data[:, 4] = x0 * np.sin(theta) + y0 * np.cos(theta)
    lors_data[:, 5] = (i_thin_ring2 + 0.5) * scanner.blocks.unit_size[2] - scanner.axial_length / 2

    return Listmode(csr.data, LORs(lors_data))


@dataclass
class Image:
    """
    Image data with center and size info.
    """

    data: np.ndarray
    center: np.ndarray = attr.ib(converter = np.array)
    size: np.ndarray = attr.ib(converter = np.array)

    # quaternion: tuple

    @property
    def ndim(self):
        return len(self.data.shape)

    @property
    def unit_size(self):
        return np.array([self.size[i] / self.shape[i] for i in range(self.ndim)])

    def shift(self, dist):
        '''shift image in mm'''
        _dist = dist / self.unit_size
        return self.replace(data = nd.shift(self.data, _dist, order = 1))

    def rotate(self, angle):
        '''rotate x-y'''
        if angle == 0:
            return self
        return self.replace(data = nd.rotate(self.data, np.rad2deg(angle), order = 1,
                                             reshape = False))

    def zoom(self, scale):
        return self.replace(data = nd.zoom(self.data, scale, order = 1))

    def adder(self, o2, angle, dist):
        o2 = o2.rotate(angle)
        o2 = o2.shift(dist)
        return self.replace(data = self.data + o2.data)

    @property
    def central_slices(self):
        t0 = self.data[int(self.shape[0] / 2), :, :]
        t1 = self.data[:, int(self.shape[1] / 2), :]
        t2 = self.data[:, :, int(self.shape[2] / 2)]
        return t0, t1, t2

    @property
    def central_profiles(self):
        p0 = self.data[:, int(self.shape[1] / 2), int(self.shape[2] / 2)]
        p1 = self.data[int(self.shape[0] / 2), :, int(self.shape[2] / 2)]
        p2 = self.data[int(self.shape[0] / 2), int(self.shape[1] / 2), :]
        return p0, p1, p2

    def imshow(self, axis = 2):
        assert is_notebook()
        from matplotlib import pyplot as plt
        plt.imshow(self.central_slices[axis])


@dataclass
class Listmode:
    data: np.ndarray
    lors: LORs

    @property
    def vproj(self):
        return self.data

    @classmethod
    def from_scanner(cls, scanner):
        _lors = LORs.from_scanner(scanner)
        _data = np.ones((len(_lors),), dtype = np.float32)
        return cls(_data, _lors)

    def __len__(self):
        return len(self.lors)

    @classmethod
    def from_lors(cls, lors: LORs):
        return cls(np.ones((len(lors),), dtype = np.float32), lors)

    def to_sinogram(self, scanner: PETCylindricalScanner):
        iblock1 = _position_to_block_index(self.lors.data[:, :3], scanner)
        iblock2 = _position_to_block_index(self.lors.data[:, 3:], scanner)
        iring1 = _position_to_thin_ring_index(self.lors.data[:, :3], scanner)
        iring2 = _position_to_thin_ring_index(self.lors.data[:, 3:], scanner)
        _fst = _rotate_to_block0(self.lors.data[:, :3], scanner, iblock1)
        iy1 = _position_to_y_index_per_block(_fst, scanner)
        _snd = _rotate_to_block0(self.lors.data[:, 3:], scanner, iblock2)
        iy2 = _position_to_y_index_per_block(_snd, scanner)
        row = iy1 + scanner.blocks.shape[1] * iblock1 + scanner.nb_detectors_per_thin_ring * iring1
        col = iy2 + scanner.blocks.shape[1] * iblock2 + scanner.nb_detectors_per_thin_ring * iring2

        return Sinogram(sparse.csr_matrix((self.data, (row, col)), shape = (scanner.nb_detectors,
                                                                            scanner.nb_detectors
                                                                            )), scanner)

    def compress(self, scanner: PETCylindricalScanner):
        return self.to_sinogram(scanner).to_listmode()


def _position_to_block_index(pos, scanner: PETCylindricalScanner):
    xc, yc = pos[:, 0], pos[:, 1]
    return np.round(np.arctan2(yc, xc) / scanner.angle_per_block).astype(
        int) % scanner.nb_blocks_per_ring


def _position_to_thin_ring_index(pos, scanner: PETCylindricalScanner):
    zc = pos[:, 2]
    return np.floor((zc + scanner.axial_length / 2) / scanner.blocks.unit_size[2]).astype(int)


def _rotate_to_block0(pos, scanner: PETCylindricalScanner, iblock):
    angle = iblock * scanner.angle_per_block
    _pos = np.zeros(pos.shape)
    xc, yc = pos[:, 0], pos[:, 1]
    _pos[:, 0] = xc * np.cos(angle) + yc * np.sin(angle)
    _pos[:, 1] = -xc * np.sin(angle) + yc * np.cos(angle)
    _pos[:, 2] = pos[:, 2]
    return _pos


def _position_to_y_index_per_block(pos, scanner: PETCylindricalScanner):
    return np.round((pos[:, 1] + scanner.blocks.size[1] / 2) // scanner.blocks.unit_size[1]).astype(
        int)


@jit
def _mesh_detector(scanner):
    R = (scanner.inner_radius + scanner.outer_radius) / 2
    theta = 2 * np.pi / scanner.nb_blocks_per_ring * np.arange(scanner.nb_blocks_per_ring)

    x = np.ones(scanner.blocks.shape[1], ) * R
    y = (np.arange(scanner.blocks.shape[1]) - scanner.blocks.shape[1] / 2 + 0.5) * \
        scanner.blocks.unit_size[1]
    z = (np.arange(scanner.blocks.shape[2]) - scanner.blocks.shape[2] / 2 + 0.5) * \
        scanner.blocks.unit_size[2]
    xx = np.kron(x, [1] * scanner.nb_blocks_per_ring)
    yy = np.kron(y, [1] * scanner.nb_blocks_per_ring)
    theta1 = np.kron(theta, [[1]] * scanner.blocks.shape[1]).ravel()
    xx1 = xx * np.cos(theta1) - yy * np.sin(theta1)
    yy1 = xx * np.sin(theta1) + yy * np.cos(theta1)

    xd = np.kron(xx1, [[1]] * scanner.blocks.shape[2]).ravel()
    yd = np.kron(yy1, [[1]] * scanner.blocks.shape[2]).ravel()
    zd = np.kron(z, [1] * scanner.blocks.shape[1] * scanner.nb_blocks_per_ring).ravel()

    lors = np.zeros((scanner.nb_detectors * scanner.nb_detectors, 6), dtype = np.float32)
    for i in range(scanner.nb_detectors):
        for j in range(scanner.nb_detectors):
            j1 = j
            lors[i * scanner.nb_detectors + j, :] = [xd[i], yd[i], zd[i], xd[j1], yd[j1], zd[j1]]
    return lors


@dataclass
class UMap(Image):
    pass


@dataclass
class Emap_MLEM(Image):
    # TODO correct emap generations in ring mode.
    @classmethod
    def from_scanner(cls, scanner: PETCylindricalScanner, bprojector, mode = 'thin-ring'):
        emap = cls(np.zeros(bprojector.shape, np.float32), bprojector.center, bprojector.size)

        # if not np.abs(scanner.blocks.unit_size[2] - bprojector.unit_size[2]) < _tiny:
        if mode == 'full':
            _emap = bprojector(Listmode.from_lors(LORs.from_scanner(scanner)))
            return cls(_emap.data, _emap.center, _emap.size)
        elif mode == 'ring-full':
            _lors0 = LORs.from_scanner_ring(scanner, 0, 0)
            for i in _tqdm(np.arange(scanner.nb_rings)):
                for j in _tqdm(np.arange(scanner.nb_rings)):
                    if i > j:
                        continue
                    _lors = deepcopy(_lors0)
                    _lors.data[:, 2] += i * scanner.blocks.size[2] + i * scanner.gap - \
                                        scanner.axial_length / 2
                    _lors.data[:, 5] += j * scanner.blocks.size[2] + j * scanner.gap - \
                                        scanner.axial_length / 2
                    _emap = bprojector(Listmode.from_lors(_lors))
                    if i == j:
                        emap = emap + _emap
                    else:
                        emap = emap + _emap * 2
            return emap
        elif mode == 'ring':
            _lors0 = LORs.from_scanner_ring(scanner, 0, 0)
            for d in _tqdm(np.arange(0, scanner.nb_rings)):
                _lors = deepcopy(_lors0)
                _lors.data[:, 5] += d * scanner.blocks.size[2] + d * scanner.gap
                _emap = bprojector(Listmode.from_lors(_lors))
                for i in np.arange(scanner.nb_rings):
                    j = i + d
                    if not 0 <= j < scanner.nb_rings:
                        continue
                    if d == 0:
                        emap = emap + _emap.shift(
                            [0, 0, i * scanner.blocks.size[
                                2] + i * scanner.gap - scanner.axial_length / 2])
                    else:
                        emap = emap + _emap.shift(
                            [0, 0, i * scanner.blocks.size[
                                2] + i * scanner.gap - scanner.axial_length / 2]) * 2
            return emap
        elif mode == 'thin-ring-full':
            _lors0 = LORs.from_scanner_thin_ring(scanner, 0, 0)
            for i in _tqdm(np.arange(scanner.nb_thin_rings)):
                for j in np.arange(scanner.nb_thin_rings):
                    if i > j:
                        continue
                    _lors = deepcopy(_lors0)
                    _lors.data[:, 2] += i * scanner.blocks.unit_size[2] + i // \
                                        scanner.blocks.shape[
                                            2] * scanner.gap - scanner.axial_length / 2
                    _lors.data[:, 5] += j * scanner.blocks.unit_size[2] + j // \
                                        scanner.blocks.shape[
                                            2] * scanner.gap - scanner.axial_length / 2
                    _emap = bprojector(Listmode.from_lors(_lors))
                    if i == j:
                        emap = emap + _emap
                    else:
                        emap = emap + _emap * 2
            return emap
        elif mode == 'thin-ring':
            _lors0 = LORs.from_scanner_thin_ring(scanner, 0, 0)
            for d in _tqdm(np.arange(0, scanner.nb_thin_rings)):
                _lors = deepcopy(_lors0)
                _lors.data[:, 5] += d * scanner.blocks.unit_size[2]
                _emap = bprojector(Listmode.from_lors(_lors))
                for i in np.arange(scanner.nb_thin_rings):
                    j = i + d
                    if not 0 <= j < scanner.nb_thin_rings:
                        continue
                    if d == 0:
                        emap = emap + _emap.shift(
                            [0, 0, i * scanner.blocks.unit_size[2] - scanner.axial_length / 2])
                    else:
                        emap = emap + _emap.shift(
                            [0, 0, i * scanner.blocks.unit_size[2] - scanner.axial_length / 2]) * 2
            return emap
        else:
            raise NotImplementedError

    @classmethod
    def from_scanner_full(cls, scanner: PETCylindricalScanner, bprojector):
        _emap = bprojector(Listmode.from_lors(LORs.from_scanner(scanner)))
        return cls(_emap.data, _emap.center, _emap.size)


@dataclass
class Emap_SART(Image):
    pass

    # @classmethod
    # def from_scanner(cls, scanner: PETCylindricalScanner, bprojector: BackProjector):
    #     _size = copy(scanner.blocks.size)
    #     _shape = copy(scanner.blocks.shape)
    #     _size[2] /= _shape[2]
    #     _shape[2] = 1
    #     _blocks = scanner.blocks.replace(shape = _shape, size = _size)
    #     _scanner = scanner.replace(blocks = _blocks, nb_rings = 1)
    #     emap = cls(np.zeros(bprojector.shape, np.float32), bprojector.center, bprojector.size)
    #     for d in _tqdm(range(-scanner.nb_thin_rings + 1, scanner.nb_thin_rings)):
    #         _emap = cls.from_scanner_full(_scanner, bprojector)
    #         off0 = scanner.axial_length / 2
    #         for j in range(scanner.nb_thin_rings):
    #             if not (0 <= j + d < scanner.nb_thin_rings):
    #                 continue
    #             emap = emap.adder(_emap, 0,
    #                               np.array([0, 0, off0 - j * scanner.blocks.unit_size[2]]))
    #     return emap

    @classmethod
    def from_scanner_full(cls, scanner: PETCylindricalScanner, projector, bprojector):
        _lors = LORs.from_scanner(scanner)
        _img = Image(np.ones(bprojector.shape, np.float32), bprojector.center, bprojector.size)
        _proj = projector(scanner, _lors)
        return bprojector(_proj)


TYPE_BIND.update({'Block': Block, 'PETCylindricalScanner': PETCylindricalScanner,
                  'LORs': LORs, 'Sinogram': Sinogram, 'Image': Image, 'Listmode': Listmode,
                  'UMap': UMap, 'Emap_MLEM': Emap_MLEM, 'Emap_SART': Emap_SART})
