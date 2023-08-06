from __future__ import print_function
#      ___          ___       ___          ___          ___          ___
#     /\  \        /\  \     /\  \        /\  \        /\  \        /\  \
#    /::\  \      /::\  \    \:\  \      /::\  \      /::\  \      /::\  \
#   /:/\:\  \    /:/\:\  \    \:\  \    /:/\:\  \    /:/\:\  \    /:/\:\  \
#  /:/  \:\  \  /:/  \:\  \   /::\  \  /::\~\:\  \  /::\~\:\  \  /::\~\:\  \
# /:/__/ \:\__\/:/__/ \:\__\ /:/\:\__\/:/\:\ \:\__\/:/\:\ \:\__\/:/\:\ \:\__\
# \:\  \ /:/  /\:\  \  \/__//:/  \/__/\/_|::\/:/  /\:\~\:\ \/__/\:\~\:\ \/__/
#  \:\  /:/  /  \:\  \     /:/  /        |:|::/  /  \:\ \:\__\   \:\ \:\__\
#   \:\/:/  /    \:\  \    \/__/         |:|\/__/    \:\ \/__/    \:\ \/__/
#    \::/  /      \:\__\                 |:|  |       \:\__\       \:\__\
#     \/__/        \/__/                  \|__|        \/__/        \/__/
#
#
#
#                      .----------------.----------------.
#                     /|               /|               /|
#                    / |              / |              / |
#                   /  |     011     /  |    111      /  |
#                  /   |            /   |            /   |
#                 .----------------.----+-----------.    |
#                /|    . ---------/|----.----------/|----.
#               / |   /|         / |   /|         / |   /|
#              /  |  / | 001    /  |  / |  101   /  |  / |
#             /   | /  |       /   | /  |       /   | /  |
#            . -------------- .----------------.    |/   |
#            |    . ---+------|----.----+------|----.    |
#            |   /|    .______|___/|____.______|___/|____.
#            |  / |   /   010 |  / |   /    110|  / |   /
#            | /  |  /        | /  |  /        | /  |  /
#            . ---+---------- . ---+---------- .    | /
#            |    |/          |    |/          |    |/             z
#            |    . ----------|----.-----------|----.              ^   y
#            |   /    000     |   /     100    |   /               |  /
#            |  /             |  /             |  /                | /
#            | /              | /              | /                 o----> x
#            . -------------- . -------------- .
#
#
# Face Refinement:
#
#      2_______________3                    _______________
#      |               |                   |       |       |
#   ^  |               |                   |(0, 1) |(1, 1) |
#   |  |               |                   |       |       |
#   |  |       x       |        --->       |-------+-------|
#   t1 |               |                   |       |       |
#      |               |                   |(0, 0) |(1, 0) |
#      |_______________|                   |_______|_______|
#      0      t0-->    1
#
#
# Face and Edge naming conventions:
#
#                      fZp
#                       |
#                 6 ------eX3------ 7
#                /|     |         / |
#               /eZ2    .        / eZ3
#             eY2 |        fYp eY3  |
#             /   |            / fXp|
#            4 ------eX2----- 5     |
#            |fXm 2 -----eX1--|---- 3          z
#           eZ0  /            |  eY1           ^   y
#            | eY0   .  fYm  eZ1 /             |  /
#            | /     |        | /              | /
#            0 ------eX0------1                o----> x
#                    |
#                   fZm
#
#
#            fX                                  fY
#      2___________3                       2___________3
#      |     e1    |                       |     e1    |
#      |           |                       |           |
#   e2 |     x     | e3      z          e2 |     x     | e3      z
#      |           |         ^             |           |         ^
#      |___________|         |___> y       |___________|         |___> x
#      0    e0     1                       0    e0     1
#           fZ
#      2___________3
#      |     e1    |
#      |           |
#   e2 |     x     | e3      y
#      |           |         ^
#      |___________|         |___> x
#      0    e0     1

import numpy as np
import scipy.sparse as sp
import properties

from discretize import utils
from . import TreeUtils

from .InnerProducts import InnerProducts
from .TensorMesh import TensorMesh, BaseTensorMesh
from .MeshIO import TreeMeshIO
import time
from six import integer_types

MAX_BITS = 20


class TreeMesh(BaseTensorMesh, InnerProducts, TreeMeshIO):

    _meshType = 'TREE'

    _levels = properties.Integer(
        "discretization level",
        min=0
    )

    _cells = properties.Set(
        "cells in the tree mesh",
        properties.Integer(
            "cell number",
            min=0
        ),
        default=set
    )

    def __init__(self, h, x0=None, **kwargs):
        assert type(h) is list, 'h must be a list'
        assert len(h) in [2, 3], "TreeMesh is only in 2D or 3D."

        if '_levels' in kwargs.keys():
            self._levels = kwargs.pop('_levels')

        BaseTensorMesh.__init__(self, h, x0, **kwargs)

        if self._levels is None:
            self._levels = int(np.log2(len(self.h[0])))

        # self._levels = levels
        self._levelBits = int(np.ceil(np.sqrt(self._levels)))+1

        self.__dirty__ = True  #: The numbering is dirty!

        if '_cells' in kwargs.keys():
            self._cells = kwargs.pop('_cells')
        else:
            self._cells.add(0)

    @properties.validator('_levels')
    def check_levels(self, change):
        assert np.all(
            len(_) == 2**change['value'] for _ in self.h
        ), "must make h and levels match"

    @property
    def __dirty__(self):
        return (
            self.__dirtyFaces__ or
            self.__dirtyEdges__ or
            self.__dirtyNodes__ or
            self.__dirtyCells__ or
            self.__dirtyHanging__ or
            self.__dirtySets__
        )

    @__dirty__.setter
    def __dirty__(self, val):
        assert val is True
        self.__dirtyFaces__ = True
        self.__dirtyEdges__ = True
        self.__dirtyNodes__ = True
        self.__dirtyCells__ = True
        self.__dirtyHanging__ = True
        self.__dirtySets__ = True

        deleteThese = [
            '__sortedCells',
            '_gridCC', '_gridN',
            '_gridFx', '_gridFy', '_gridFz',
            '_gridEx', '_gridEy', '_gridEz',
            '_area', '_edge', '_vol',
            '_faceDiv', '_edgeCurl', '_nodalGrad',
            '_aveFx2CC', '_aveFy2CC', '_aveFz2CC', '_aveF2CC', '_aveF2CCV',
            '_aveEx2CC', '_aveEy2CC', '_aveEz2CC', '_aveE2CC', '_aveE2CCV',
            '_aveN2CC', '_h_gridded'

        ]

        for p in deleteThese:
            if hasattr(self, p):
                delattr(self, p)

    @property
    def fill(self):
        """
        How filled is the mesh compared to a TensorMesh?
        As a fraction: [0, 1].
        """
        return float(self.nC)/((2**self.maxLevel)**self.dim)

    @property
    def maxLevel(self):
        """
        The maximum level used, which may be
        less than `levels`.
        """
        level = 0
        for cell in self._cells:
            p = self._pointer(cell)
            level = max(level, p[-1])
        return level

    def __str__(self):
        outStr = '  ---- {0!s}TreeMesh ----  '.format(
            ('Oc' if self.dim == 3 else 'Quad')
        )

        def printH(hx, outStr=''):
            i = -1
            while True:
                i = i + 1
                if i > hx.size:
                    break
                elif i == hx.size:
                    break
                h = hx[i]
                n = 1
                for j in range(i+1, hx.size):
                    if hx[j] == h:
                        n = n + 1
                        i = i + 1
                    else:
                        break
                if n == 1:
                    outStr += ' {0:.2f}, '.format(h)
                else:
                    outStr += ' {0:d}*{1:.2f}, '.format(n, h)
            return outStr[:-1]

        if self.dim == 2:
            outStr += '\n   x0: {0:.2f}'.format(self.x0[0])
            outStr += '\n   y0: {0:.2f}'.format(self.x0[1])
            outStr += printH(self.hx, outStr='\n   hx:')
            outStr += printH(self.hy, outStr='\n   hy:')
        elif self.dim == 3:
            outStr += '\n   x0: {0:.2f}'.format(self.x0[0])
            outStr += '\n   y0: {0:.2f}'.format(self.x0[1])
            outStr += '\n   z0: {0:.2f}'.format(self.x0[2])
            outStr += printH(self.hx, outStr='\n   hx:')
            outStr += printH(self.hy, outStr='\n   hy:')
            outStr += printH(self.hz, outStr='\n   hz:')
        outStr += '\n  nC: {0:d}'.format(self.nC)
        outStr += '\n  Fill: {0:2.2f}%'.format((self.fill*100))
        return outStr

    @property
    def nC(self):
        return len(self._cells)

    @property
    def nN(self):
        self.number()
        return len(self._nodes) - len(self._hangingN)

    @property
    def nF(self):
        return self.nFx + self.nFy + (0 if self.dim == 2 else self.nFz)

    @property
    def nFx(self):
        self.number()
        return len(self._facesX) - len(self._hangingFx)

    @property
    def nFy(self):
        self.number()
        return len(self._facesY) - len(self._hangingFy)

    @property
    def nFz(self):
        if self.dim == 2:
            return None
        self.number()
        return len(self._facesZ) - len(self._hangingFz)

    @property
    def nE(self):
        return self.nEx + self.nEy + (0 if self.dim == 2 else self.nEz)

    @property
    def nEx(self):
        if self.dim == 2:
            return self.nFy
        self.number()
        return len(self._edgesX) - len(self._hangingEx)

    @property
    def nEy(self):
        if self.dim == 2:
            return self.nFx
        self.number()
        return len(self._edgesY) - len(self._hangingEy)

    @property
    def nEz(self):
        if self.dim == 2:
            return None
        self.number()
        return len(self._edgesZ) - len(self._hangingEz)

    @property
    def nhN(self):
        self.number()
        return len(self._hangingN)

    @property
    def nhF(self):
        return self.nhFx + self.nhFy + (0 if self.dim == 2 else self.nhFz)

    @property
    def nhFx(self):
        self.number()
        return len(self._hangingFx)

    @property
    def nhFy(self):
        self.number()
        return len(self._hangingFy)

    @property
    def nhFz(self):
        if self.dim == 2:
            return None
        self.number()
        return len(self._hangingFz)

    @property
    def nhE(self):
        return self.nhEx + self.nhEy + (0 if self.dim == 2 else self.nhEz)

    @property
    def nhEx(self):
        if self.dim == 2:
            return self.nhFy
        self.number()
        return len(self._hangingEx)

    @property
    def nhEy(self):
        if self.dim == 2:
            return self.nhFx
        self.number()
        return len(self._hangingEy)

    @property
    def nhEz(self):
        if self.dim == 2:
            return None
        self.number()
        return len(self._hangingEz)

    @property
    def ntN(self):
        self.number()
        return len(self._nodes)

    @property
    def ntF(self):
        return self.ntFx + self.ntFy + (0 if self.dim == 2 else self.ntFz)

    @property
    def vntF(self):
        return [self.ntFx, self.ntFy] + ([] if self.dim == 2 else [self.ntFz])

    @property
    def ntFx(self):
        self.number()
        return len(self._facesX)

    @property
    def ntFy(self):
        self.number()
        return len(self._facesY)

    @property
    def ntFz(self):
        if self.dim == 2:
            return None
        self.number()
        return len(self._facesZ)

    @property
    def ntE(self):
        return self.ntEx + self.ntEy + (0 if self.dim == 2 else self.ntEz)

    @property
    def vntE(self):
        return [self.ntEx, self.ntEy] + ([] if self.dim == 2 else [self.ntEz])

    @property
    def ntEx(self):
        if self.dim == 2:
            return self.ntFy
        self.number()
        return len(self._edgesX)

    @property
    def ntEy(self):
        if self.dim == 2:
            return self.ntFx
        self.number()
        return len(self._edgesY)

    @property
    def ntEz(self):
        if self.dim == 2:
            return None
        self.number()
        return len(self._edgesZ)

    @property
    def _sortedCells(self):
        if getattr(self, '__sortedCells', None) is None:
            self.__sortedCells = sorted(self._cells)
        return self.__sortedCells

    @property
    def permuteCC(self):
        # TODO: cache these?
        P = SortGrid(self.gridCC)
        return sp.identity(self.nC).tocsr()[P, :]

    @property
    def permuteF(self):
        # TODO: cache these?
        P = SortGrid(self.gridFx)
        P += SortGrid(self.gridFy, offset=self.nFx)
        if self.dim == 3:
            P += SortGrid(self.gridFz, offset=self.nFx+self.nFy)
        return sp.identity(self.nF).tocsr()[P, :]

    @property
    def permuteE(self):
        # TODO: cache these?
        if self.dim == 2:
            P = SortGrid(self.gridFy)
            P += SortGrid(self.gridFx, offset=self.nEx)
            return sp.identity(self.nE).tocsr()[P, :]
        if self.dim == 3:
            P = SortGrid(self.gridEx)
            P += SortGrid(self.gridEy, offset=self.nEx)
            P += SortGrid(self.gridEz, offset=self.nEx+self.nEy)
            return sp.identity(self.nE).tocsr()[P, :]

    def _index(self, pointer):
        assert len(pointer) is self.dim+1

        assert pointer[-1] <= self._levels
        return TreeUtils.index(
            self.dim, MAX_BITS, self._levelBits, pointer[:-1], pointer[-1]
        )

    def _pointer(self, index):
        assert type(index) in integer_types
        return TreeUtils.point(self.dim, MAX_BITS, self._levelBits, index)

    def __contains__(self, v):
        return self._asIndex(v) in self._cells

    def refine(self, function=None, recursive=True,
               cells=None, balance=True, verbose=False,
               _inRecursion=False):

        if type(function) in integer_types:
            level = function
            function = lambda cell: level

        if not _inRecursion:
            self.__dirty__ = True
            if verbose:
                print('Refining Mesh')

        cells = cells if cells is not None else sorted(self._cells)
        recurse = []
        tic = time.time()
        for cell in cells:
            p = self._pointer(cell)

            if p[-1] >= self._levels:
                continue

            result = function(Cell(self, cell, p))
            if type(result) is bool:
                do = result
            elif type(result) in integer_types:
                do = result > p[-1]
            else:

                raise Exception(
                    'You must tell the program what to refine.' +
                    ' Use BOOL or INT (level)'
                )

            if do:
                recurse += self._refineCell(cell, p)

        if verbose:
            print('   ', time.time() - tic)

        if recursive and len(recurse) > 0:

            recurse += self.refine(
                function=function, recursive=True, cells=recurse,
                balance=balance, verbose=verbose, _inRecursion=True
            )

        if balance and not _inRecursion:
            self.balance()
        return recurse

    def corsen(
        self, function=None, recursive=True, cells=None,
        balance=True, verbose=False, _inRecursion=False
    ):

        if type(function) in integer_types:
            level = function
            function = lambda cell: level

        if not _inRecursion:
            self.__dirty__ = True
            if verbose:
                print('Corsening Mesh')

        cells = cells if cells is not None else sorted(self._cells)
        recurse = []
        tic = time.time()
        for cell in cells:
            if cell not in self._cells:
                continue  # already removed
            p = self._pointer(cell)

            if p[-1] >= self._levels:
                continue

            result = function(Cell(self, cell, p))
            if type(result) is bool:
                do = result
            elif type(result) in integer_types:
                do = result < p[-1]
            else:

                raise Exception(
                    'You must tell the program what to corsen.' +
                    ' Use BOOL or INT (level)'
                )

            if do:
                recurse += self._corsenCell(cell, p)

        if verbose:
            print('   ', time.time() - tic)

        if recursive and len(recurse) > 0:
            recurse += self.corsen(
                function=function, recursive=True,
                cells=recurse, balance=balance,
                verbose=verbose, _inRecursion=True
            )

        if balance and not _inRecursion:
            self.balance()
        return recurse

    def _refineCell(self, ind, pointer=None):
        ind = self._asIndex(ind)
        pointer = self._asPointer(pointer if pointer is not None else ind)
        if ind not in self:
            raise IndexError(ind)
        children = self._childPointers(pointer, returnAll=True)
        for child in children:
            self._cells.add(self._asIndex(child))
        self._cells.remove(ind)
        return [self._asIndex(child) for child in children]

    def _corsenCell(self, ind, pointer=None):
        ind = self._asIndex(ind)
        pointer = self._asPointer(pointer if pointer is not None else ind)
        if ind not in self:
            raise IndexError(ind)
        parent = self._parentPointer(pointer)
        children = self._childPointers(parent, returnAll=True)
        for child in children:
            self._cells.remove(self._asIndex(child))
        parentInd = self._asIndex(parent)
        self._cells.add(parentInd)
        return [parentInd]

    def _asPointer(self, ind):
        if type(ind) in integer_types:
            return self._pointer(ind)
        if type(ind) is list:
            assert len(ind) == (self.dim + 1), (
                str(ind) + ' is not valid pointer'
            )
            assert ind[-1] <= self._levels, (
                str(ind) + ' is not valid pointer'
            )
            return ind
        if isinstance(ind, np.ndarray):
            return ind.tolist()
        raise Exception

    def _asIndex(self, pointer):
        if type(pointer) in integer_types:
            return pointer
        if type(pointer) is list:
            return self._index(pointer)
        raise Exception

    def _childPointers(
        self, pointer, direction=0, positive=True, returnAll=False
    ):
        l = self._levelWidth(pointer[-1] + 1)

        if self.dim == 2:

            children = [
                [pointer[0], pointer[1], pointer[-1] + 1],
                [pointer[0] + l, pointer[1], pointer[-1] + 1],
                [pointer[0], pointer[1] + l, pointer[-1] + 1],
                [pointer[0] + l, pointer[1] + l, pointer[-1] + 1]
            ]

        elif self.dim == 3:

            children = [
                [pointer[0], pointer[1], pointer[2], pointer[-1]+1],
                [pointer[0]+l, pointer[1], pointer[2], pointer[-1]+1],
                [pointer[0], pointer[1]+l, pointer[2], pointer[-1]+1],
                [pointer[0]+l, pointer[1]+l, pointer[2], pointer[-1]+1],
                [pointer[0], pointer[1], pointer[2]+l, pointer[-1]+1],
                [pointer[0]+l, pointer[1], pointer[2]+l, pointer[-1]+1],
                [pointer[0], pointer[1]+l, pointer[2]+l, pointer[-1]+1],
                [pointer[0]+l, pointer[1]+l, pointer[2]+l, pointer[-1]+1]
            ]
        if direction == 0:
            ind = [0, 2, 4, 6] if not positive else [1, 3, 5, 7]
        if direction == 1:
            ind = [0, 1, 4, 5] if not positive else [2, 3, 6, 7]
        if direction == 2:
            ind = [0, 1, 2, 3] if not positive else [4, 5, 6, 7]

        if returnAll:
            return children
        return [children[_] for _ in ind[:(self.dim-1)*2]]

    def _parentPointer(self, pointer):
        if pointer[-1] == 0:
            return None
        mod = self._levelWidth(pointer[-1] - 1)
        return [p - (p % mod) for p in pointer[:-1]] + [pointer[-1]-1]

    def _cellN(self, p):
        """Node location [x,y(,z)] of a single cell,
        closest to origin, given a pointer.
        """
        p = self._asPointer(p)
        return [hi[:p[ii]].sum() for ii, hi in enumerate(self.h)]

    def _cellH(self, p):
        """Widths of a single cell given a pointer."""
        p = self._asPointer(p)
        w = self._levelWidth(p[-1])
        return [hi[p[ii]:p[ii]+w].sum() for ii, hi in enumerate(self.h)]

    def _cellC(self, p):
        """
            Cell center of a single cell (without origin correction),
            given a pointer.
        """
        return (np.array(self._cellH(p))/2.0 + self._cellN(p)).tolist()

    def _levelWidth(self, level):
        return 2**(self._levels - level)

    def _isInsideMesh(self, pointer):
        inside = True
        for p in pointer[:-1]:
            inside = inside and p >= 0 and p < 2**self._levels
        return inside

    def _getNextCell(self, ind, direction=0, positive=True, _lookUp=True):
        """
            Returns a None, int, list, or nested list
            The int is the cell number.

        """
        if direction >= self.dim:
            return None
        pointer = self._asPointer(ind)
        if pointer[-1] > self._levels:
            return None

        step = (1 if positive else -1) * self._levelWidth(pointer[-1])
        nextCell = [
            p if ii is not direction else p + step for ii,
            p in enumerate(pointer)
        ]
        # raise Exception(pointer, nextCell)
        if not self._isInsideMesh(nextCell):
            return None

        # it might be the same size as me?
        if nextCell in self:
            return self._index(nextCell)

        if nextCell[-1] + 1 <= self._levels:  # if I am not the smallest.
            children = self._childPointers(
                pointer, direction=direction, positive=positive
            )
            nextCells = [
                self._getNextCell(
                    child, direction=direction, positive=positive,
                    _lookUp=False
                )
                for child in children
            ]

            if nextCells[0] is not None:
                return nextCells

        if not _lookUp:
            return None

        # it might be bigger than me?
        return self._getNextCell(
            self._parentPointer(pointer), direction=direction,
            positive=positive
        )

    def balance(
        self, recursive=True, cells=None, verbose=False, _inRecursion=False
    ):

        tic = time.time()
        if not _inRecursion:
            self.__dirty__ = True
            if verbose:
                print('Balancing Mesh:')

        cells = cells if cells is not None else sorted(self._cells)

        # calcDepth = lambda i: lambda A: i if type(A) is not list else max(map(calcDepth(i+1), A))
        # flatten   = lambda A: A if calcDepth(0)(A) == 1 else flatten([_ for __ in A for _ in (__ if type(__) is list else [__])])

        recurse = set()

        for cell in cells:
            p = self._asPointer(cell)

            if p[-1] == self._levels:
                continue

            cs = list(range(6))
            cs[0] = self._getNextCell(cell, direction=0, positive=False)
            cs[1] = self._getNextCell(cell, direction=0, positive=True)
            cs[2] = self._getNextCell(cell, direction=1, positive=False)
            cs[3] = self._getNextCell(cell, direction=1, positive=True)
            cs[4] = self._getNextCell(cell, direction=2, positive=False)  # this will be None if in 2D
            cs[5] = self._getNextCell(cell, direction=2, positive=True)  # this will be None if in 2D

            do = np.any([
                type(c) is list and np.any([type(_) is list for _ in c])
                for c in cs if c is not None
            ])
            # depth = calcDepth(0)(cs)
            # print(depth, depth > 2, do, [jj for jj in flatten(cs) if jj is not None])
            # recurse += [jj for jj in flatten(cs) if jj is not None]

            if do and cell in self:
                newCells = self._refineCell(cell)
                recurse.update([_ for _ in cs if type(_) in integer_types])  # only add the bigger ones!
                recurse.update(newCells)

        if verbose:
            print('   ', len(cells), time.time() - tic)
        if recursive and len(recurse) > 0:
            self.balance(cells=sorted(recurse), _inRecursion=True)

    @property
    def gridCC(self):
        """
        Returns an M by N numpy array with the center locations of all cells
        in order. M is the number of cells and N=1,2,3 is the dimension of the
        mesh.
        """

        if getattr(self, '_gridCC', None) is None:
            self._gridCC = np.zeros((len(self._cells), self.dim))
            for ii, ind in enumerate(self._sortedCells):
                p = self._asPointer(ind)
                self._gridCC[ii, :] = self._cellC(p) + self.x0
        return self._gridCC

    @property
    def gridN(self):
        """
        Returns an M by N numpy array with the widths of all cells in order.
        M is the number of nodes and N=1,2,3 is the dimension of the mesh.
        """

        self.number()
        R = self._deflationMatrix('N', withHanging=False)
        return R.T * self._gridN + np.repeat([self.x0], self.nN, axis=0)

    @property
    def h_gridded(self):
        """
        Returns an (nC, dim) numpy array with the widths of all cells in order
        """

        if getattr(self, '_h_gridded', None) is None:
            self._h_gridded = np.zeros((len(self._cells), self.dim))
            for ii, ind in enumerate(self._sortedCells):
                p = self._asPointer(ind)
                self._h_gridded[ii, :] = self._cellH(p)
        return self._h_gridded

    @property
    def gridFx(self):
        self.number()
        R = self._deflationMatrix('Fx', withHanging=False)
        return R.T * self._gridFx + np.repeat([self.x0], self.nFx, axis=0)

    @property
    def gridFy(self):
        self.number()
        R = self._deflationMatrix('Fy', withHanging=False)
        return R.T * self._gridFy + np.repeat([self.x0], self.nFy, axis=0)

    @property
    def gridFz(self):
        if self.dim < 3:
            return None
        self.number()
        R = self._deflationMatrix('Fz', withHanging=False)
        return R.T * self._gridFz + np.repeat([self.x0], self.nFz, axis=0)

    @property
    def gridEx(self):
        if self.dim == 2:
            return self.gridFy
        self.number()
        R = self._deflationMatrix('Ex', withHanging=False)
        return R.T * self._gridEx + np.repeat([self.x0], self.nEx, axis=0)

    @property
    def gridEy(self):
        if self.dim == 2:
            return self.gridFx
        self.number()
        R = self._deflationMatrix('Ey', withHanging=False)
        return R.T * self._gridEy + np.repeat([self.x0], self.nEy, axis=0)

    @property
    def gridEz(self):
        if self.dim < 3:
            return None
        self.number()
        R = self._deflationMatrix('Ez', withHanging=False)
        return R.T * self._gridEz + np.repeat([self.x0], self.nEz, axis=0)

    @property
    def vol(self):
        if getattr(self, '_vol', None) is None:
            self._vol = np.zeros(len(self._cells))
            for ii, ind in enumerate(self._sortedCells):
                p = self._asPointer(ind)
                self._vol[ii] = np.prod(self._cellH(p))
        return self._vol

    @property
    def area(self):
        self.number()
        if getattr(self, '_area', None) is None:
            Rf = self._deflationMatrix('F', withHanging=False)
            self._area = Rf.T * (
                np.r_[self._areaFxFull, self._areaFyFull] if self.dim == 2 else
                np.r_[self._areaFxFull, self._areaFyFull, self._areaFzFull]
            )
        return self._area

    @property
    def edge(self):
        self.number()
        if self.dim == 2:
            return np.r_[self.area[self.nFx:], self.area[:self.nFx]]
        if getattr(self, '_edge', None) is None:
            Re = self._deflationMatrix('E', withHanging=False)
            self._edge = (
                Re.T * np.r_[
                    self._edgeExFull, self._edgeEyFull, self._edgeEzFull
                ]
            )

        return self._edge

    def _createNumberingSets(self, force=False):
        if not self.__dirtySets__ and not force:
            return

        self._nodes = set()

        self._facesX = set()
        self._facesY = set()
        if self.dim == 3:
            self._facesZ = set()
            self._edgesX = set()
            self._edgesY = set()
            self._edgesZ = set()

        for ind in self._cells:
            p = self._asPointer(ind)
            w = self._levelWidth(p[-1])
            if self.dim == 2:
                i00 = ind
                iw0 = self._index([p[0] + w, p[1], p[2]])
                i0w = self._index([p[0], p[1] + w, p[2]])
                iww = self._index([p[0] + w, p[1] + w, p[2]])

                self._nodes.add(i00)
                self._nodes.add(iw0)
                self._nodes.add(i0w)
                self._nodes.add(iww)

                self._facesX.add(i00)
                self._facesX.add(iw0)

                self._facesY.add(i00)
                self._facesY.add(i0w)

            elif self.dim == 3:
                i000 = ind
                iw00 = self._index([p[0] + w, p[1], p[2], p[3]])
                i0w0 = self._index([p[0], p[1] + w, p[2], p[3]])
                i00w = self._index([p[0], p[1], p[2] + w, p[3]])
                iww0 = self._index([p[0] + w, p[1] + w, p[2], p[3]])
                iw0w = self._index([p[0] + w, p[1], p[2] + w, p[3]])
                i0ww = self._index([p[0], p[1] + w, p[2] + w, p[3]])
                iwww = self._index([p[0] + w, p[1] + w, p[2] + w, p[3]])

                self._nodes.add(i000)
                self._nodes.add(iw00)
                self._nodes.add(i0w0)
                self._nodes.add(iww0)
                self._nodes.add(i00w)
                self._nodes.add(iw0w)
                self._nodes.add(i0ww)
                self._nodes.add(iwww)

                self._facesX.add(i000)
                self._facesX.add(iw00)

                self._facesY.add(i000)
                self._facesY.add(i0w0)

                self._facesZ.add(i000)
                self._facesZ.add(i00w)

                self._edgesX.add(i000)
                self._edgesX.add(i0w0)
                self._edgesX.add(i00w)
                self._edgesX.add(i0ww)

                self._edgesY.add(i000)
                self._edgesY.add(iw00)
                self._edgesY.add(i00w)
                self._edgesY.add(iw0w)

                self._edgesZ.add(i000)
                self._edgesZ.add(iw00)
                self._edgesZ.add(i0w0)
                self._edgesZ.add(iww0)

        self.__dirtySets__ = False

    def _numberCells(self, force=False):
        if not self.__dirtyCells__ and not force:
            return
        self._cc2i = dict()
        self._i2cc = dict()
        for ii, c in enumerate(sorted(self._cells)):
            self._cc2i[c] = ii
            self._i2cc[ii] = c
        self.__dirtyCells__ = False

    def _numberNodes(self, force=False):
        if not self.__dirtyNodes__ and not force:
            return
        self._createNumberingSets(force=force)
        gridN = []
        self._n2i = dict()
        for ii, n in enumerate(sorted(self._nodes)):
            self._n2i[n] = ii
            gridN.append(self._cellN(self._pointer(n)))
        self._gridN = np.array(gridN)

        self.__dirtyNodes__ = False

    def _numberFaces(self, force=False):
        if not self.__dirtyFaces__ and not force:
            return
        self._createNumberingSets(force=force)

        for ind in self._cells:
            p = self._asPointer(ind)
            w = self._levelWidth(p[-1])

        gridFx = []
        areaFx = []
        self._fx2i = dict()
        for ii, fx in enumerate(sorted(self._facesX)):
            self._fx2i[fx] = ii
            p = self._pointer(fx)
            n, h = self._cellN(p), self._cellH(p)
            if self.dim == 2:
                gridFx.append([n[0], n[1] + h[1]/2.0])
                areaFx.append(h[1])
            elif self.dim == 3:
                gridFx.append([n[0], n[1] + h[1]/2.0, n[2] + h[2]/2.0])
                areaFx.append(h[1]*h[2])
        self._gridFx = np.array(gridFx)
        self._areaFxFull = np.array(areaFx)

        gridFy = []
        areaFy = []
        self._fy2i = dict()
        for ii, fy in enumerate(sorted(self._facesY)):
            self._fy2i[fy] = ii
            p = self._pointer(fy)
            n, h = self._cellN(p), self._cellH(p)
            if self.dim == 2:
                gridFy.append([n[0] + h[0]/2.0, n[1]])
                areaFy.append(h[0])
            elif self.dim == 3:
                gridFy.append([n[0] + h[0]/2.0, n[1], n[2] + h[2]/2.0])
                areaFy.append(h[0]*h[2])
        self._gridFy = np.array(gridFy)
        self._areaFyFull = np.array(areaFy)

        if self.dim == 2:
            self.__dirtyFaces__ = False
            return

        gridFz = []
        areaFz = []
        self._fz2i = dict()
        for ii, fz in enumerate(sorted(self._facesZ)):
            self._fz2i[fz] = ii
            p = self._pointer(fz)
            n, h = self._cellN(p), self._cellH(p)
            gridFz.append([n[0] + h[0]/2.0, n[1] + h[1]/2.0, n[2]])
            areaFz.append(h[0]*h[1])
        self._gridFz = np.array(gridFz)
        self._areaFzFull = np.array(areaFz)

        self.__dirtyFaces__ = False

    def _numberEdges(self, force=False):
        if self.dim == 2:
            self.__dirtyEdges__ = False
            return
        if not self.__dirtyEdges__ and not force:
            return
        self._createNumberingSets(force=force)

        gridEx = []
        edgeEx = []
        self._ex2i = dict()
        for ii, ex in enumerate(sorted(self._edgesX)):
            self._ex2i[ex] = ii
            p = self._pointer(ex)
            n, h = self._cellN(p), self._cellH(p)
            gridEx.append([n[0] + h[0]/2.0, n[1], n[2]])
            edgeEx.append(h[0])
        self._gridEx = np.array(gridEx)
        self._edgeExFull = np.array(edgeEx)

        gridEy = []
        edgeEy = []
        self._ey2i = dict()
        for ii, ey in enumerate(sorted(self._edgesY)):
            self._ey2i[ey] = ii
            p = self._pointer(ey)
            n, h = self._cellN(p), self._cellH(p)
            gridEy.append([n[0], n[1] + h[1]/2.0, n[2]])
            edgeEy.append(h[1])
        self._gridEy = np.array(gridEy)
        self._edgeEyFull = np.array(edgeEy)

        gridEz = []
        edgeEz = []
        self._ez2i = dict()
        for ii, ez in enumerate(sorted(self._edgesZ)):
            self._ez2i[ez] = ii
            p = self._pointer(ez)
            n, h = self._cellN(p), self._cellH(p)
            gridEz.append([n[0], n[1], n[2] + h[2]/2.0])
            edgeEz.append(h[2])
        self._gridEz = np.array(gridEz)
        self._edgeEzFull = np.array(edgeEz)

        self.__dirtyEdges__ = False

    def _hanging(self, force=False):
        if not self.__dirtyHanging__ and not force:
            return

        self._numberCells(force=force)
        self._numberNodes(force=force)
        self._numberFaces(force=force)
        self._numberEdges(force=force)

        self._hangingN = dict()
        self._hangingFx = dict()
        self._hangingFy = dict()
        if self.dim == 3:
            self._hangingFz = dict()
            self._hangingEx = dict()
            self._hangingEy = dict()
            self._hangingEz = dict()

        # Compute from x faces
        for fx in self._facesX:
            p = self._pointer(fx)

            if p[-1] + 1 > self._levels:
                continue
            sl = p[-1] + 1  #: small level

            test = self._index(p[:-1] + [sl])
            if test not in self._facesX:
                # Return early without checking the other faces
                continue
            w = self._levelWidth(sl)

            if self.dim == 2:
                chy0 = self._cellH([p[0], p[1], sl])[1]
                chy1 = self._cellH([p[0], p[1] + w, sl])[1]
                A = (chy0 + chy1)

                self._hangingFx[self._fx2i[test]] = (
                    [self._fx2i[fx], chy0 / A],
                )
                self._hangingFx[
                    self._fx2i[self._index([p[0], p[1] + w, sl])]
                ] = (
                    [self._fx2i[fx], chy1 / A],
                )

                n0, n1 = fx, self._index([p[0], p[1] + 2*w, p[-1]])
                self._hangingN[self._n2i[test]] = ([self._n2i[n0], 1.0], )
                self._hangingN[
                    self._n2i[self._index([p[0], p[1] + w, sl])]
                ] = (
                    [self._n2i[n0], 1.0 - chy0 / A],
                    [self._n2i[n1], 1.0 - chy1 / A]
                )
                self._hangingN[
                    self._n2i[self._index([p[0], p[1] + 2*w, sl])]
                ] = ([self._n2i[n1], 1.0], )

            elif self.dim == 3:

                chy0 = self._cellH([p[0], p[1], p[2], sl])[1]
                chy1 = self._cellH([p[0], p[1] + w, p[2], sl])[1]
                chz0 = self._cellH([p[0], p[1], p[2], sl])[2]
                chz1 = self._cellH([p[0], p[1], p[2] + w, sl])[2]
                lenY = chy0 + chy1
                lenZ = chz0 + chz1
                A = lenY * lenZ

                ey0 = fx
                ey1 = self._index([p[0], p[1], p[2] + 2*w, p[-1]])
                ez0 = fx
                ez1 = self._index([p[0], p[1] + 2*w, p[2], p[-1]])

                n0 = fx
                n1 = self._index([p[0], p[1] + 2*w, p[2], p[-1]])
                n2 = self._index([p[0], p[1], p[2] + 2*w, p[-1]])
                n3 = self._index([p[0], p[1] + 2*w, p[2] + 2*w, p[-1]])

                i000 = test
                i010 = self._index([p[0], p[1] + w, p[2], sl])
                i001 = self._index([p[0], p[1], p[2] + w, sl])
                i011 = self._index([p[0], p[1] + w, p[2] + w, sl])
                i020 = self._index([p[0], p[1] + 2*w, p[2], sl])
                i021 = self._index([p[0], p[1] + 2*w, p[2] + w, sl])
                i002 = self._index([p[0], p[1], p[2] + 2*w, sl])
                i012 = self._index([p[0], p[1] + w, p[2] + 2*w, sl])
                i022 = self._index([p[0], p[1] + 2*w, p[2] + 2*w, sl])

                self._hangingFx[self._fx2i[i000]] = (
                    [self._fx2i[fx], chy0*chz0 / A],
                )
                self._hangingFx[self._fx2i[i010]] = (
                    [self._fx2i[fx], chy1*chz0 / A],
                )
                self._hangingFx[self._fx2i[i001]] = (
                    [self._fx2i[fx], chy0*chz1 / A],
                )
                self._hangingFx[self._fx2i[i011]] = (
                    [self._fx2i[fx], chy1*chz1 / A],
                )

                self._hangingEy[self._ey2i[i000]] = ([self._ey2i[ey0], 1.0], )
                self._hangingEy[self._ey2i[i010]] = ([self._ey2i[ey0], 1.0], )
                self._hangingEy[self._ey2i[i001]] = (
                    [self._ey2i[ey0], 0.5], [self._ey2i[ey1], 0.5]
                )
                self._hangingEy[self._ey2i[i011]] = (
                    [self._ey2i[ey0], 0.5], [self._ey2i[ey1], 0.5]
                )
                self._hangingEy[self._ey2i[i002]] = ([self._ey2i[ey1], 1.0], )
                self._hangingEy[self._ey2i[i012]] = ([self._ey2i[ey1], 1.0], )

                self._hangingEz[self._ez2i[i000]] = ([self._ez2i[ez0], 1.0], )
                self._hangingEz[self._ez2i[i001]] = ([self._ez2i[ez0], 1.0], )
                self._hangingEz[self._ez2i[i010]] = (
                    [self._ez2i[ez0], 0.5], [self._ez2i[ez1], 0.5]
                )
                self._hangingEz[self._ez2i[i011]] = (
                    [self._ez2i[ez0], 0.5], [self._ez2i[ez1], 0.5]
                )
                self._hangingEz[self._ez2i[i020]] = ([self._ez2i[ez1], 1.0], )
                self._hangingEz[self._ez2i[i021]] = ([self._ez2i[ez1], 1.0], )

                self._hangingN[self._n2i[i000]] = ([self._n2i[n0],   1.0], )
                self._hangingN[self._n2i[i010]] = (
                    [self._n2i[n0],   0.5], [self._n2i[n1], 0.5]
                )
                self._hangingN[self._n2i[i020]] = ([self._n2i[n1],   1.0], )
                self._hangingN[self._n2i[i001]] = (
                    [self._n2i[n0],   0.5], [self._n2i[n2], 0.5]
                )
                self._hangingN[self._n2i[i011]] = (
                    [self._n2i[n0],   0.25], [self._n2i[n1], 0.25],
                    [self._n2i[n2], 0.25], [self._n2i[n3], 0.25]
                )
                self._hangingN[self._n2i[i021]] = (
                    [self._n2i[n1],   0.5], [self._n2i[n3], 0.5]
                )
                self._hangingN[self._n2i[i002]] = ([self._n2i[n2],   1.0], )
                self._hangingN[self._n2i[i012]] = (
                    [self._n2i[n2],   0.5], [self._n2i[n3], 0.5]
                )
                self._hangingN[self._n2i[i022]] = ([self._n2i[n3],   1.0], )

        # Compute from y faces
        for fy in self._facesY:
            p = self._pointer(fy)

            if p[-1] + 1 > self._levels:
                continue
            sl = p[-1] + 1  #: small level

            test = self._index(p[:-1] + [sl])
            if test not in self._facesY:
                # Return early without checking the other faces
                continue
            w = self._levelWidth(sl)

            if self.dim == 2:
                chx0 = self._cellH([p[0], p[1], sl])[0]
                chx1 = self._cellH([p[0] + w, p[1], sl])[0]

                self._hangingFy[self._fy2i[test]] = (
                    [self._fy2i[fy], chx0 / (chx0 + chx1)],
                )
                self._hangingFy[self._fy2i[self._index([p[0] + w, p[1], sl])]] = ([self._fy2i[fy], chx1 / (chx0 + chx1)], )

                n0, n1 = fy, self._index([p[0] + 2*w, p[1], p[-1]])
                self._hangingN[self._n2i[test]] = ([self._n2i[n0], 1.0], )
                self._hangingN[self._n2i[self._index([p[0] + w, p[1], sl])]] = ([self._n2i[n0], 0.5], [self._n2i[n1], 0.5])
                self._hangingN[self._n2i[self._index([p[0] + 2*w, p[1], sl])]] = ([self._n2i[n1], 1.0], )

            elif self.dim == 3:

                chx0 = self._cellH([p[0], p[1], p[2], sl])[0]
                chx1 = self._cellH([p[0] + w, p[1], p[2], sl])[0]
                chz0 = self._cellH([p[0], p[1], p[2], sl])[2]
                chz1 = self._cellH([p[0], p[1], p[2] + w, sl])[2]
                lenX = chx0 + chx1
                lenZ = chz0 + chz1
                A = lenX * lenZ

                ex0 = fy
                ex1 = self._index([p[0], p[1], p[2] + 2*w, p[-1]])
                ez0 = fy
                ez1 = self._index([p[0] + 2*w, p[1], p[2], p[-1]])

                n0 = fy
                n1 = self._index([p[0] + 2*w, p[1], p[2], p[-1]])
                n2 = self._index([p[0], p[1], p[2] + 2*w, p[-1]])
                n3 = self._index([p[0] + 2*w, p[1], p[2] + 2*w, p[-1]])

                i000 = test
                i100 = self._index([p[0] + w, p[1], p[2], sl])
                i001 = self._index([p[0], p[1], p[2] + w, sl])
                i101 = self._index([p[0] + w, p[1], p[2] + w, sl])
                i200 = self._index([p[0] + 2*w, p[1], p[2], sl])
                i201 = self._index([p[0] + 2*w, p[1], p[2] + w, sl])
                i002 = self._index([p[0], p[1], p[2] + 2*w, sl])
                i102 = self._index([p[0] + w, p[1], p[2] + 2*w, sl])
                i202 = self._index([p[0] + 2*w, p[1], p[2] + 2*w, sl])

                self._hangingFy[self._fy2i[i000]] = (
                    [self._fy2i[fy], chx0*chz0 / A],
                )
                self._hangingFy[self._fy2i[i100]] = (
                    [self._fy2i[fy], chx1*chz0 / A],
                )
                self._hangingFy[self._fy2i[i001]] = (
                    [self._fy2i[fy], chx0*chz1 / A],
                )
                self._hangingFy[self._fy2i[i101]] = (
                    [self._fy2i[fy], chx1*chz1 / A],
                )

                self._hangingEx[self._ex2i[i000]] = ([self._ex2i[ex0], 1.0], )
                self._hangingEx[self._ex2i[i100]] = ([self._ex2i[ex0], 1.0], )
                self._hangingEx[self._ex2i[i001]] = (
                    [self._ex2i[ex0], 0.5], [self._ex2i[ex1], 0.5]
                )
                self._hangingEx[self._ex2i[i101]] = (
                    [self._ex2i[ex0], 0.5], [self._ex2i[ex1], 0.5]
                )
                self._hangingEx[self._ex2i[i002]] = ([self._ex2i[ex1], 1.0], )
                self._hangingEx[self._ex2i[i102]] = ([self._ex2i[ex1], 1.0], )

                self._hangingEz[self._ez2i[i000]] = ([self._ez2i[ez0], 1.0], )
                self._hangingEz[self._ez2i[i001]] = ([self._ez2i[ez0], 1.0], )
                self._hangingEz[self._ez2i[i100]] = (
                    [self._ez2i[ez0], 0.5], [self._ez2i[ez1], 0.5]
                )
                self._hangingEz[self._ez2i[i101]] = (
                    [self._ez2i[ez0], 0.5], [self._ez2i[ez1], 0.5]
                )
                self._hangingEz[self._ez2i[i200]] = ([self._ez2i[ez1], 1.0], )
                self._hangingEz[self._ez2i[i201]] = ([self._ez2i[ez1], 1.0], )

                self._hangingN[self._n2i[i000]] = ([self._n2i[n0],   1.0], )
                self._hangingN[self._n2i[i100]] = (
                    [self._n2i[n0],   0.5], [self._n2i[n1], 0.5]
                )
                self._hangingN[self._n2i[i200]] = ([self._n2i[n1],   1.0], )
                self._hangingN[self._n2i[i001]] = (
                    [self._n2i[n0],   0.5], [self._n2i[n2], 0.5]
                )
                self._hangingN[self._n2i[i101]] = (
                    [self._n2i[n0],   0.25], [self._n2i[n1], 0.25],
                    [self._n2i[n2], 0.25], [self._n2i[n3], 0.25]
                )
                self._hangingN[self._n2i[i201]] = (
                    [self._n2i[n1],   0.5], [self._n2i[n3], 0.5]
                )
                self._hangingN[self._n2i[i002]] = ([self._n2i[n2],   1.0], )
                self._hangingN[self._n2i[i102]] = (
                    [self._n2i[n2],   0.5], [self._n2i[n3], 0.5]
                )
                self._hangingN[self._n2i[i202]] = ([self._n2i[n3],   1.0], )

        if self.dim == 2:
            self.__dirtyHanging__ = False
            return

        # Compute from z faces
        for fz in self._facesZ:
            p = self._pointer(fz)

            if p[-1] + 1 > self._levels:
                continue
            sl = p[-1] + 1  #: small level

            test = self._index(p[:-1] + [sl])
            if test not in self._facesZ:
                # Return early without checking the other faces
                continue
            w = self._levelWidth(sl)

            chx0 = self._cellH([p[0], p[1], p[2], sl])[0]
            chx1 = self._cellH([p[0] + w, p[1], p[2], sl])[0]
            chy0 = self._cellH([p[0], p[1], p[2], sl])[1]
            chy1 = self._cellH([p[0], p[1] + w, p[2], sl])[1]
            lenX = chx0 + chx1
            lenY = chy0 + chy1
            A = lenX * lenY

            ex0 = fz
            ex1 = self._index([p[0], p[1] + 2*w, p[2], p[-1]])
            ey0 = fz
            ey1 = self._index([p[0] + 2*w, p[1], p[2], p[-1]])

            n0 = fz
            n1 = self._index([p[0] + 2*w, p[1], p[2], p[-1]])
            n2 = self._index([p[0], p[1] + 2*w, p[2], p[-1]])
            n3 = self._index([p[0] + 2*w, p[1] + 2*w, p[2], p[-1]])

            i000 = test
            i100 = self._index([p[0] + w, p[1], p[2], sl])
            i010 = self._index([p[0], p[1] + w, p[2], sl])
            i110 = self._index([p[0] + w, p[1] + w, p[2], sl])
            i200 = self._index([p[0] + 2*w, p[1], p[2], sl])
            i210 = self._index([p[0] + 2*w, p[1] + w, p[2], sl])
            i020 = self._index([p[0], p[1] + 2*w, p[2], sl])
            i120 = self._index([p[0] + w, p[1] + 2*w, p[2], sl])
            i220 = self._index([p[0] + 2*w, p[1] + 2*w, p[2], sl])

            self._hangingFz[self._fz2i[i000]] = (
                [self._fz2i[fz], chx0*chy0 / A],
            )
            self._hangingFz[self._fz2i[i100]] = (
                [self._fz2i[fz], chx1*chy0 / A],
            )
            self._hangingFz[self._fz2i[i010]] = (
                [self._fz2i[fz], chx0*chy1 / A],
            )
            self._hangingFz[self._fz2i[i110]] = (
                [self._fz2i[fz], chx1*chy1 / A],
            )

            self._hangingEx[self._ex2i[i000]] = ([self._ex2i[ex0], 1.0], )
            self._hangingEx[self._ex2i[i100]] = ([self._ex2i[ex0], 1.0], )
            self._hangingEx[self._ex2i[i010]] = (
                [self._ex2i[ex0], 0.5], [self._ex2i[ex1], 0.5]
            )
            self._hangingEx[self._ex2i[i110]] = (
                [self._ex2i[ex0], 0.5], [self._ex2i[ex1], 0.5]
            )
            self._hangingEx[self._ex2i[i020]] = ([self._ex2i[ex1], 1.0], )
            self._hangingEx[self._ex2i[i120]] = ([self._ex2i[ex1], 1.0], )

            self._hangingEy[self._ey2i[i000]] = ([self._ey2i[ey0], 1.0], )
            self._hangingEy[self._ey2i[i010]] = ([self._ey2i[ey0], 1.0], )
            self._hangingEy[self._ey2i[i100]] = (
                [self._ey2i[ey0], 0.5], [self._ey2i[ey1], 0.5]
            )
            self._hangingEy[self._ey2i[i110]] = (
                [self._ey2i[ey0], 0.5], [self._ey2i[ey1], 0.5]
            )
            self._hangingEy[self._ey2i[i200]] = ([self._ey2i[ey1], 1.0], )
            self._hangingEy[self._ey2i[i210]] = ([self._ey2i[ey1], 1.0], )

            self._hangingN[self._n2i[i000]] = ([self._n2i[n0], 1.0], )
            self._hangingN[self._n2i[i100]] = (
                [self._n2i[n0], 0.5], [self._n2i[n1], 0.5]
            )
            self._hangingN[self._n2i[i200]] = ([self._n2i[n1], 1.0], )
            self._hangingN[self._n2i[i010]] = (
                [self._n2i[n0], 0.5], [self._n2i[n2], 0.5]
            )
            self._hangingN[self._n2i[i110]] = (
                [self._n2i[n0], 0.25], [self._n2i[n1], 0.25],
                [self._n2i[n2], 0.25], [self._n2i[n3], 0.25]
            )
            self._hangingN[self._n2i[i210]] = (
                [self._n2i[n1], 0.5], [self._n2i[n3], 0.5]
            )
            self._hangingN[self._n2i[i020]] = ([self._n2i[n2], 1.0], )
            self._hangingN[self._n2i[i120]] = (
                [self._n2i[n2], 0.5], [self._n2i[n3], 0.5]
            )
            self._hangingN[self._n2i[i220]] = ([self._n2i[n3], 1.0], )

        self.__dirtyHanging__ = False

    def number(self, balance=True, force=False):
        if not self.__dirty__ and not force:
            return
        if balance:
            self.balance()
        self._hanging(force=force)

    def _deflationMatrix(self, location, withHanging=True, asOnes=False):
        assert location in [
            'N', 'F', 'Fx', 'Fy', 'E', 'Ex', 'Ey'
        ] + (['Fz', 'Ez'] if self.dim == 3 else [])

        args = dict()
        args['N'] = (self._nodes,  self._hangingN,  self._n2i)
        args['Fx'] = (self._facesX, self._hangingFx, self._fx2i)
        args['Fy'] = (self._facesY, self._hangingFy, self._fy2i)
        if self.dim == 3:
            args['Fz'] = (self._facesZ, self._hangingFz, self._fz2i)
            args['Ex'] = (self._edgesX, self._hangingEx, self._ex2i)
            args['Ey'] = (self._edgesY, self._hangingEy, self._ey2i)
            args['Ez'] = (self._edgesZ, self._hangingEz, self._ez2i)
        elif self.dim == 2:
            args['Ex'] = (self._facesY, self._hangingFy, self._fy2i)
            args['Ey'] = (self._facesX, self._hangingFx, self._fx2i)
        if location in ['F', 'E']:
            Rlist = [
                self._deflationMatrix(
                    location + subLoc, withHanging=withHanging, asOnes=asOnes
                ) for subLoc in ['x', 'y', 'z'][:self.dim]]
            return sp.block_diag(Rlist)

        return self.__deflationMatrix(
            *args[location], withHanging=withHanging, asOnes=asOnes
        )

    def __deflationMatrix(self, theSet, theHang, theIndex,
                          withHanging=True, asOnes=False):
        reducedInd = dict()  # final reduced index
        ii = 0
        row, col, val = [], [], []
        for fx in sorted(theSet):
            if theIndex[fx] not in theHang:
                reducedInd[theIndex[fx]] = ii
                row += [theIndex[fx]]
                col += [ii]
                val += [1.0]
                ii += 1
        if withHanging:
            for hfkey in theHang.keys():
                hf = theHang[hfkey]
                row += [hfkey]*len(hf)
                col += [reducedInd[_[0]] for _ in hf]
                if asOnes:
                    val += [1.0]*len(hf)
                else:
                    val += [_[1] for _ in hf]

        return sp.csr_matrix((val, (row, col)), shape=(len(theSet), len(reducedInd)))

    @property
    def faceDiv(self):
        if getattr(self, '_faceDiv', None) is None:
            self.number()

            # TODO: Preallocate!
            row, col, val = [], [], []
            PM = [-1, 1]*self.dim  # plus / minus

            # TODO total number of faces?
            offset = [0]*2 + [self.ntFx]*2 + [self.ntFx+self.ntFy]*2

            for ii, ind in enumerate(self._sortedCells):

                p = self._pointer(ind)
                w = self._levelWidth(p[-1])

                if self.dim == 2:
                    facesX = [
                        self._fx2i[self._index([p[0], p[1], p[2]])],
                        self._fx2i[self._index([p[0] + w, p[1], p[2]])]
                    ]
                    facesY = [
                        self._fy2i[self._index([p[0], p[1], p[2]])],
                        self._fy2i[self._index([p[0], p[1] + w, p[2]])]
                    ]

                    faces = facesX + facesY

                elif self.dim == 3:
                    facesX = [
                        self._fx2i[self._index([p[0], p[1], p[2], p[3]])],
                        self._fx2i[self._index([p[0] + w, p[1], p[2], p[3]])]
                    ]

                    facesY = [
                        self._fy2i[self._index([p[0], p[1], p[2], p[3]])],
                        self._fy2i[self._index([p[0], p[1] + w, p[2], p[3]])]
                    ]

                    facesZ = [
                        self._fz2i[self._index([p[0], p[1], p[2], p[3]])],
                        self._fz2i[self._index([p[0], p[1], p[2] + w, p[3]])]
                    ]

                    faces = facesX + facesY + facesZ

                for off, pm, face in zip(offset, PM, faces):
                    row += [ii]
                    col += [face + off]
                    val += [pm]

            D = sp.csr_matrix((val, (row, col)), shape=(self.nC, self.ntF))
            R = self._deflationMatrix('F', asOnes=True)
            VOL = self.vol

            if self.dim == 2:
                S = np.r_[self._areaFxFull, self._areaFyFull]

            elif self.dim == 3:
                S = np.r_[self._areaFxFull, self._areaFyFull, self._areaFzFull]

            self._faceDiv = utils.sdiag(1.0/VOL)*D*utils.sdiag(S)*R

        return self._faceDiv

    @property
    def faceDivx(self):
        if getattr(self, '_faceDivx', None) is None:
            self.number()

            # TODO: Preallocate!
            row, col, val = [], [], []
            PM = [-1, 1]*self.dim  # plus / minus

            for ii, ind in enumerate(self._sortedCells):

                p = self._pointer(ind)
                w = self._levelWidth(p[-1])

                if self.dim == 2:
                    facesX = [
                        self._fx2i[self._index([p[0], p[1], p[2]])],
                        self._fx2i[self._index([p[0] + w, p[1], p[2]])]
                    ]

                elif self.dim == 3:
                    facesX = [
                        self._fx2i[self._index([p[0], p[1], p[2], p[3]])],
                        self._fx2i[self._index([p[0] + w, p[1], p[2], p[3]])]
                    ]

                for pm, faceX in zip(PM, facesX):
                    row += [ii]
                    col += [faceX]
                    val += [pm]

            Dx = sp.csr_matrix((val, (row, col)), shape=(self.nC, self.ntFx))
            Rx = self._deflationMatrix('Fx', asOnes=True)
            VOL = self.vol

            self._faceDivx = (
                utils.sdiag(1.0/VOL)*Dx*utils.sdiag(self._areaFxFull)*Rx
            )

        return self._faceDivx

    @property
    def faceDivy(self):
        if getattr(self, '_faceDivy', None) is None:
            self.number()

            # TODO: Preallocate!
            row, col, val = [], [], []
            PM = [-1, 1]*self.dim  # plus / minus

            for ii, ind in enumerate(self._sortedCells):

                p = self._pointer(ind)
                w = self._levelWidth(p[-1])

                if self.dim == 2:
                    facesY = [
                        self._fy2i[self._index([p[0], p[1], p[2]])],
                        self._fy2i[self._index([p[0], p[1] + w, p[2]])]
                    ]

                elif self.dim == 3:
                    facesY = [
                        self._fy2i[self._index([p[0], p[1], p[2], p[3]])],
                        self._fy2i[self._index([p[0], p[1] + w, p[2], p[3]])]
                    ]

                for pm, faceY in zip(PM, facesY):
                    row += [ii]
                    col += [faceY]
                    val += [pm]

            Dy = sp.csr_matrix((val, (row, col)), shape=(self.nC, self.ntFy))
            Ry = self._deflationMatrix('Fy', asOnes=True)
            VOL = self.vol

            self._faceDivy = (
                utils.sdiag(1.0/VOL)*Dy*utils.sdiag(self._areaFyFull)*Ry
            )

        return self._faceDivy

    @property
    def faceDivz(self):
        if getattr(self, '_faceDivz', None) is None:
            self.number()

            # TODO: Preallocate!
            row, col, val = [], [], []
            PM = [-1, 1]*self.dim  # plus / minus

            for ii, ind in enumerate(self._sortedCells):

                p = self._pointer(ind)
                w = self._levelWidth(p[-1])

                facesZ = [
                    self._fz2i[self._index([p[0], p[1], p[2], p[3]])],
                    self._fz2i[self._index([p[0], p[1], p[2] + w, p[3]])]
                ]

                for pm, faceZ in zip(PM, facesZ):
                    row += [ii]
                    col += [faceZ]
                    val += [pm]

            Dz = sp.csr_matrix((val, (row, col)), shape=(self.nC, self.ntFz))
            Rz = self._deflationMatrix('Fz', asOnes=True)
            VOL = self.vol

            self._faceDivz = (
                utils.sdiag(1.0/VOL)*Dz*utils.sdiag(self._areaFzFull)*Rz
            )

        return self._faceDivz

    @property
    def cellGradStencil(self):
        if getattr(self, '_cellGradStencil', None) is None:

            self._cellGradStencil = sp.vstack([
                self._cellGradxStencil, self._cellGradyStencil
            ])
            if self.dim == 3:
                self._cellGradStencil = sp.vstack([
                    self._cellGradStencil, self._cellGradzStencil
                ])

        return self._cellGradStencil

    @property
    def _cellGradxStencil(self):
        self.number()

        faceParent = dict()
        theHang = self._hangingFx
        for key in theHang.keys():
            if not theHang[key][0][0] in faceParent.keys():
                faceParent[theHang[key][0][0]] = [key]
            else:
                faceParent[theHang[key][0][0]] += [key]

        row, col, val = [], [], []
        PM = [-1, 1]  # *mesh.dim  # plus / minus

        for ii, ind in enumerate(self._sortedCells):

            p = self._pointer(ind)

            if self.dim == 2:
                cells = self._getNextCell(
                    self._index([p[0], p[1], p[2]]), direction=0
                )
            elif self.dim == 3:
                cells = self._getNextCell(
                    self._index([p[0], p[1], p[2], p[3]]), direction=0
                )

            if cells:
                if isinstance(cells, int):
                    cells = [cells]

                for cell in cells:

                    pN = self._pointer(cell)

                    # Check if neighbour has lower tree level
                    if pN[-1] < p[-1]:
                        if self.dim == 2:
                            hangs = faceParent[
                                self._fx2i[self._index([pN[0], pN[1], pN[2]])]
                            ]
                            count = int(np.abs((p[1] - pN[1]) % 2))

                        elif self.dim == 3:
                            hangs = faceParent[
                                self._fx2i[
                                    self._index([pN[0], pN[1], pN[2], pN[3]])
                                ]]
                            count = int(np.abs((p[1] - pN[1]) % 2))
                            count += int(2*np.abs((p[2] - pN[2]) % 2))
                        face = hangs[count]
                    else:
                        if self.dim == 2:
                            face = self._fx2i[
                                self._index([pN[0], pN[1], pN[2]])
                            ]
                        elif self.dim == 3:
                            face = self._fx2i[
                                self._index([pN[0], pN[1], pN[2], pN[3]])
                            ]

                    row += [face]*2
                    col += [self._cc2i[ind], self._cc2i[cell]]
                    val += PM

        Gx = sp.csr_matrix((val, (row, col)), shape=(self.ntFx, self.nC))

        return Gx

    @property
    def _cellGradyStencil(self):
        self.number()

        faceParent = dict()
        theHang = self._hangingFy
        for key in theHang.keys():
            if not theHang[key][0][0] in faceParent.keys():
                faceParent[theHang[key][0][0]] = [key]
            else:
                faceParent[theHang[key][0][0]] += [key]

        row, col, val = [], [], []
        PM = [-1, 1]   # plus / minus

        for ii, ind in enumerate(self._sortedCells):

            p = self._pointer(ind)

            if self.dim == 2:
                cells = self._getNextCell(
                    self._index([p[0], p[1], p[2]]), direction=1
                )
            elif self.dim == 3:
                cells = self._getNextCell(
                    self._index([p[0], p[1], p[2], p[3]]), direction=1
                )

            if cells:
                if isinstance(cells, int):
                    cells = [cells]

                for cell in cells:

                    pN = self._pointer(cell)

                    # Check if neighbour has lower tree level
                    if pN[-1] < p[-1]:
                        if self.dim == 2:
                            hangs = faceParent[
                                self._fy2i[self._index([pN[0], pN[1], pN[2]])]
                            ]
                            count = int(np.abs((p[0] - pN[0]) % 2))

                        elif self.dim == 3:
                            hangs = faceParent[
                                self._fy2i[
                                    self._index([pN[0], pN[1], pN[2], pN[3]])
                                ]
                            ]
                            count = int(np.abs((p[0] - pN[0]) % 2))
                            count += int(2*np.abs((p[2] - pN[2]) % 2))
                        face = hangs[count]
                    else:
                        if self.dim == 2:
                            face = self._fy2i[
                                self._index([pN[0], pN[1], pN[2]])
                            ]
                        elif self.dim == 3:
                            face = self._fy2i[
                                self._index([pN[0], pN[1], pN[2], pN[3]])
                            ]

                    row += [face]*2
                    col += [self._cc2i[ind], self._cc2i[cell]]
                    val += PM

        Gy = sp.csr_matrix((val, (row, col)), shape=(self.ntFy, self.nC))

        return Gy

    @property
    def _cellGradzStencil(self):
        self.number()
        assert self.dim == 3, 'cellGradzStencil only possible for TreeMesh 3D'

        faceParent = dict()
        theHang = self._hangingFz
        for key in theHang.keys():
            if not theHang[key][0][0] in faceParent.keys():
                faceParent[theHang[key][0][0]] = [key]
            else:
                faceParent[theHang[key][0][0]] += [key]

        row, col, val = [], [], []
        PM = [-1, 1]  # *mesh.dim  # plus / minus

        for ii, ind in enumerate(self._sortedCells):

            p = self._pointer(ind)

            cells = self._getNextCell(
                self._index([p[0], p[1], p[2], p[3]]), direction=2
            )

            if cells:
                if isinstance(cells, int):
                    cells = [cells]

                for cell in cells:

                    pN = self._pointer(cell)

                    # Check if neighbour has lower tree level
                    if pN[-1] < p[-1]:
                        hangs = faceParent[
                            self._fz2i[
                                self._index([pN[0], pN[1], pN[2], pN[3]])
                            ]
                        ]
                        count = int(np.abs((p[0] - pN[0]) % 2))
                        count += int(2*np.abs((p[1] - pN[1]) % 2))
                        face = hangs[count]
                    else:
                        face = self._fz2i[
                            self._index([pN[0], pN[1], pN[2], pN[3]])
                        ]

                    row += [face]*2
                    col += [self._cc2i[ind], self._cc2i[cell]]
                    val += PM

        Gz = sp.csr_matrix((val, (row, col)), shape=(self.ntFz, self.nC))

        return Gz

    @property
    def cellGrad(self):
        """
        Cell centered Gradient operator built off of the faceDiv operator.
        Grad =  - (Mf)^{-1} * Div * diag (volume)
        """
        if getattr(self, '_cellGrad', None) is None:

            indBoundary = np.ones(self.nC, dtype=float)

            indBoundary_Fx = (self.aveFx2CC.T * indBoundary) >= 1
            ix = np.zeros(self.nFx)
            ix[indBoundary_Fx] = 1.
            Pafx = utils.sdiag(ix)

            indBoundary_Fy = (self.aveFy2CC.T * indBoundary) >= 1
            iy = np.zeros(self.nFy)
            iy[indBoundary_Fy] = 1.
            Pafy = utils.sdiag(iy)

            MfI = self.getFaceInnerProduct(invMat=True)

            if self.dim == 2:
                Pi = sp.block_diag([Pafx, Pafy])

            elif self.dim == 3:
                indBoundary_Fz = (self.aveFz2CC.T * indBoundary) >= 1
                iz = np.zeros(self.nFz)
                iz[indBoundary_Fz] = 1.
                Pafz = utils.sdiag(iz)
                Pi = sp.block_diag([Pafx, Pafy, Pafz])

            self._cellGrad = -Pi * MfI * self.faceDiv.T * utils.sdiag(self.vol)

        return self._cellGrad

    @property
    def cellGradx(self):
        """
        Cell centered Gradient operator in x-direction (Gradx)
        Grad = sp.vstack((Gradx, Grady, Gradz))
        """
        if getattr(self, '_cellGradx', None) is None:

            nFx = self.nFx
            indBoundary = np.ones(self.nC, dtype=float)

            indBoundary_Fx = (self.aveFx2CC.T * indBoundary) >= 1
            ix = np.zeros(self.nFx)
            ix[indBoundary_Fx] = 1.
            Pafx = utils.sdiag(ix)

            MfI = self.getFaceInnerProduct(invMat=True)
            MfIx = utils.sdiag(MfI.diagonal()[:nFx])

            self._cellGradx = (
                -Pafx * MfIx * self.faceDivx.T * utils.sdiag(self.vol)
            )

        return self._cellGradx

    @property
    def cellGrady(self):
        """
        Cell centered Gradient operator in y-direction (Gradx)
        Grad = sp.vstack((Gradx, Grady, Gradz))
        """
        if getattr(self, '_cellGrady', None) is None:

            nFx = self.nFx
            nFy = self.nFy
            indBoundary = np.ones(self.nC, dtype=float)

            indBoundary_Fy = (self.aveFy2CC.T * indBoundary) >= 1
            iy = np.zeros(self.nFy)
            iy[indBoundary_Fy] = 1.
            Pafy = utils.sdiag(iy)

            MfI = self.getFaceInnerProduct(invMat=True)
            MfIy = utils.sdiag(MfI.diagonal()[nFx:nFx+nFy])

            self._cellGrady = (
                -Pafy * MfIy * self.faceDivy.T * utils.sdiag(self.vol)
            )

        return self._cellGrady

    @property
    def cellGradz(self):
        """
        Cell centered Gradient operator in y-direction (Gradz)
        Grad = sp.vstack((Gradx, Grady, Gradz))
        """
        if getattr(self, '_cellGradz', None) is None:

            nFx = self.nFx
            nFy = self.nFy
            indBoundary = np.ones(self.nC, dtype=float)

            indBoundary_Fz = (self.aveFz2CC.T * indBoundary) >= 1
            iz = np.zeros(self.nFz)
            iz[indBoundary_Fz] = 1.
            Pafz = utils.sdiag(iz)

            MfI = self.getFaceInnerProduct(invMat=True)
            MfIz = utils.sdiag(MfI.diagonal()[nFx+nFy:])

            self._cellGradz = (
                -Pafz * MfIz * self.faceDivz.T * utils.sdiag(self.vol)
            )

        return self._cellGradz

    @property
    def edgeCurl(self):
        """Construct the 3D curl operator."""
        assert self.dim > 2, "Edge Curl only programed for 3D."

        if getattr(self, '_edgeCurl', None) is None:
            self.number()
            # TODO: Preallocate!
            row, col, val = [], [], []
            faceOffset = 0
            offset = [self.ntEx]*2 + [self.ntEx+self.ntEy]*2
            PM = [1, -1, -1, 1]
            for ii, fx in enumerate(sorted(self._facesX)):

                p = self._pointer(fx)
                w = self._levelWidth(p[-1])

                edges = [
                    self._ey2i[self._index([p[0], p[1], p[2], p[3]])],
                    self._ey2i[self._index([p[0], p[1], p[2] + w, p[3]])],
                    self._ez2i[self._index([p[0], p[1], p[2], p[3]])],
                    self._ez2i[self._index([p[0], p[1] + w, p[2], p[3]])],
                ]

                for off, pm, edge in zip(offset, PM, edges):
                    row += [ii + faceOffset]
                    col += [edge + off]
                    val += [pm]

            faceOffset = self.ntFx
            offset = [0]*2 + [self.ntEx+self.ntEy]*2
            PM = [-1, 1, 1, -1]
            for ii, fy in enumerate(sorted(self._facesY)):

                p = self._pointer(fy)
                w = self._levelWidth(p[-1])

                edges = [
                    self._ex2i[self._index([p[0], p[1], p[2], p[3]])],
                    self._ex2i[self._index([p[0], p[1], p[2] + w, p[3]])],
                    self._ez2i[self._index([p[0], p[1], p[2], p[3]])],
                    self._ez2i[self._index([p[0] + w, p[1], p[2], p[3]])],
                ]

                for off, pm, edge in zip(offset, PM, edges):
                    row += [ii + faceOffset]
                    col += [edge + off]
                    val += [pm]

            faceOffset = self.ntFx + self.ntFy
            offset = [0]*2 + [self.ntEx]*2
            PM = [1, -1, -1, 1]
            for ii, fz in enumerate(sorted(self._facesZ)):

                p = self._pointer(fz)
                w = self._levelWidth(p[-1])

                edges = [
                    self._ex2i[self._index([p[0], p[1], p[2], p[3]])],
                    self._ex2i[self._index([p[0], p[1] + w, p[2], p[3]])],
                    self._ey2i[self._index([p[0], p[1], p[2], p[3]])],
                    self._ey2i[self._index([p[0] + w, p[1], p[2], p[3]])],
                ]

                for off, pm, edge in zip(offset, PM, edges):
                    row += [ii + faceOffset]
                    col += [edge + off]
                    val += [pm]

            Rf = self._deflationMatrix('F', withHanging=True, asOnes=False)
            Re = self._deflationMatrix('E')

            Rf_ave = utils.sdiag(1./Rf.sum(axis=0)) * Rf.T

            C = sp.csr_matrix((val, (row, col)), shape=(self.ntF, self.ntE))
            S = np.r_[self._areaFxFull, self._areaFyFull, self._areaFzFull]
            L = np.r_[self._edgeExFull, self._edgeEyFull, self._edgeEzFull]
            self._edgeCurl = Rf_ave*utils.sdiag(1.0/S)*C*utils.sdiag(L)*Re
        return self._edgeCurl

    @property
    def nodalGrad(self):
        if getattr(self, '_nodalGrad', None) is None:
            self.number()
            # TODO: Preallocate!
            row, col, val = [], [], []
            # kinda a hack for the 2D gradient
            # because edges are not stored
            edgesX = self._facesY if self.dim == 2 else self._edgesX
            offset = 0
            for ex in edgesX:
                p = self._pointer(ex)
                w = self._levelWidth(p[-1])
                if self.dim == 2:
                    row += [self._fy2i[ex] + offset]*2
                    nodePlus = self._index([p[0] + w, p[1], p[2]])
                elif self.dim == 3:
                    row += [self._ex2i[ex] + offset]*2
                    nodePlus = self._index([p[0] + w, p[1], p[2], p[3]])
                col += [self._n2i[ex], self._n2i[nodePlus]]
                val += [-1, 1]

            edgesY = self._facesX if self.dim == 2 else self._edgesY
            offset = self.ntFy if self.dim == 2 else self.ntEx
            for ey in edgesY:
                p = self._pointer(ey)
                w = self._levelWidth(p[-1])
                if self.dim == 2:
                    row += [self._fx2i[ey] + offset]*2
                    nodePlus = self._index([p[0], p[1] + w, p[2]])
                elif self.dim == 3:
                    row += [self._ey2i[ey] + offset]*2
                    nodePlus = self._index([p[0], p[1] + w, p[2], p[3]])
                col += [self._n2i[ey], self._n2i[nodePlus]]
                val += [-1, 1]
            if self.dim == 3:

                edgesZ = self._edgesZ
                offset = self.ntEx + self.ntEy
                for ez in edgesZ:
                    p = self._pointer(ez)
                    w = self._levelWidth(p[-1])
                    row += [self._ez2i[ez] + offset]*2
                    nodePlus = self._index([p[0], p[1], p[2] + w, p[3]])
                    col += [self._n2i[ez], self._n2i[nodePlus]]
                    val += [-1, 1]

            G = sp.csr_matrix((val, (row, col)), shape=(self.ntE, self.ntN))
            if self.dim == 2:
                L = np.r_[self._areaFyFull, self._areaFxFull]
            elif self.dim == 3:
                L = np.r_[self._edgeExFull, self._edgeEyFull, self._edgeEzFull]

            Rn = self._deflationMatrix('N')
            Re = self._deflationMatrix('E', withHanging=True, asOnes=False)

            Re_ave = utils.sdiag(1./Re.sum(axis=0)) * Re.T

            self._nodalGrad = Re_ave*utils.sdiag(1/L)*G*Rn
        return self._nodalGrad

    @property
    def aveEx2CC(self):
        if getattr(self, '_aveEx2CC', None) is None:
            row, col, val = [], [], []

            if self.dim == 2:
                raise Exception('aveEx2CC not implemented in 2D')

            if self.dim == 3:
                PM = [1./4.]*4

                for ii, ind in enumerate(self._sortedCells):
                    p = self._pointer(ind)
                    w = self._levelWidth(p[-1])

                    edgesx = [
                        self._ex2i[self._index([p[0], p[1], p[2], p[3]])],
                        self._ex2i[self._index([p[0], p[1]+w, p[2], p[3]])],
                        self._ex2i[self._index([p[0], p[1], p[2]+w, p[3]])],
                        self._ex2i[self._index([p[0], p[1]+w, p[2]+w, p[3]])],
                    ]

                    for pm, edge in zip(PM, edgesx):
                        row += [ii]
                        col += [edge]
                        val += [pm]

            Av = sp.csr_matrix((val, (row, col)), shape=(self.nC, self.ntEx))
            Re = self._deflationMatrix('Ex', asOnes=False, withHanging=True)

            self._aveEx2CC = Av*Re
        return self._aveEx2CC

    @property
    def aveEy2CC(self):
        "Construct the averaging operator on cell edges to cell centers."
        if getattr(self, '_aveEy2CC', None) is None:
            row, col, val = [], [], []

            if self.dim == 2:
                raise NotImplementedError('aveEy2CC not implemented in 2D')

            if self.dim == 3:
                PM = [1./4.]*4  # plus / plus

                for ii, ind in enumerate(self._sortedCells):
                    p = self._pointer(ind)
                    w = self._levelWidth(p[-1])

                    edgesy = [
                        self._ey2i[self._index([p[0], p[1], p[2], p[3]])],
                        self._ey2i[self._index([p[0]+w, p[1], p[2], p[3]])],
                        self._ey2i[self._index([p[0], p[1], p[2]+w, p[3]])],
                        self._ey2i[self._index([p[0]+w, p[1], p[2]+w, p[3]])],
                    ]

                    for pm, edge in zip(PM, edgesy):
                        row += [ii]
                        col += [edge]
                        val += [pm]

            Av = sp.csr_matrix((val, (row, col)), shape=(self.nC, self.ntEy))
            Re = self._deflationMatrix('Ey', asOnes=False, withHanging=True)

            self._aveEy2CC = Av*Re
        return self._aveEy2CC

    @property
    def aveEz2CC(self):
        "Construct the averaging operator on cell edges to cell centers."
        # raise Exception('Not yet implemented!')
        if getattr(self, '_aveEz2CC', None) is None:
            row, col, val = [], [], []

            if self.dim == 2:
                raise Exception('There are no z edges in 2D')

            if self.dim == 3:
                PM = [1./4.]*4  # plus / plus

                for ii, ind in enumerate(self._sortedCells):
                    p = self._pointer(ind)
                    w = self._levelWidth(p[-1])

                    edgesz = [
                        self._ez2i[self._index([p[0], p[1], p[2], p[3]])],
                        self._ez2i[self._index([p[0]+w, p[1], p[2], p[3]])],
                        self._ez2i[self._index([p[0], p[1]+w, p[2], p[3]])],
                        self._ez2i[self._index([p[0]+w, p[1]+w, p[2], p[3]])],
                    ]

                    for pm, edge in zip(PM, edgesz):
                        row += [ii]
                        col += [edge]
                        val += [pm]

            Av = sp.csr_matrix((val, (row, col)), shape=(self.nC, self.ntEz))
            Re = self._deflationMatrix('Ez', asOnes=False, withHanging=True)

            self._aveEz2CC = Av*Re

        return self._aveEz2CC

    @property
    def aveE2CC(self):
        "Construct the averaging operator on cell edges to cell centers."
        if getattr(self, '_aveE2CC', None) is None:
            if self.dim == 2:
                raise Exception('aveE2CC not implemented in 2D')
            elif self.dim == 3:
                self._aveE2CC = 1./self.dim*sp.hstack([
                    self.aveEx2CC, self.aveEy2CC, self.aveEz2CC
                ])
        return self._aveE2CC

    @property
    def aveE2CCV(self):
        "Construct the averaging operator on cell edges to cell centers."
        # raise Exception('Not yet implemented!')
        if getattr(self, '_aveE2CCV', None) is None:
            if self.dim == 2:
                raise Exception('aveE2CC not implemented in 2D')
            elif self.dim == 3:
                self._aveE2CCV = sp.block_diag([
                    self.aveEx2CC, self.aveEy2CC, self.aveEz2CC
                ])
        return self._aveE2CCV

    @property
    def aveFx2CC(self):
        if getattr(self, '_aveFx2CC', None) is None:

            self.number()

            row, col, val = [], [], []
            PM = [1./2.]*2  # 0.5, 0.5

            for ii, ind in enumerate(self._sortedCells):
                p = self._pointer(ind)
                w = self._levelWidth(p[-1])

                if self.dim == 2:
                    facesx = [
                        self._fx2i[self._index([p[0], p[1], p[2]])],
                        self._fx2i[self._index([p[0] + w, p[1], p[2]])],
                    ]

                elif self.dim == 3:
                    facesx = [
                        self._fx2i[self._index([p[0], p[1], p[2], p[3]])],
                        self._fx2i[self._index([p[0] + w, p[1], p[2], p[3]])],
                    ]

                for pm, face in zip(PM, facesx):
                    row += [ii]
                    col += [face]
                    val += [pm]

            Av = sp.csr_matrix((val, (row, col)), shape=(self.nC, self.ntFx))
            Rf = self._deflationMatrix('Fx', asOnes=True, withHanging=True)

            self._aveFx2CC = Av*Rf
        return self._aveFx2CC

    @property
    def aveFy2CC(self):
        if getattr(self, '_aveFy2CC', None) is None:

            self.number()

            row, col, val = [], [], []
            PM = [1./2.]*2  # 0.5, 0.5

            for ii, ind in enumerate(self._sortedCells):
                p = self._pointer(ind)
                w = self._levelWidth(p[-1])

                if self.dim == 2:
                    facesy = [
                        self._fy2i[self._index([p[0], p[1], p[2]])],
                        self._fy2i[self._index([p[0], p[1] + w, p[2]])],
                    ]
                elif self.dim == 3:
                    facesy = [
                        self._fy2i[self._index([p[0], p[1], p[2], p[3]])],
                        self._fy2i[self._index([p[0], p[1] + w, p[2], p[3]])],
                    ]

                for pm, face in zip(PM, facesy):
                    row += [ii]
                    col += [face]
                    val += [pm]

            Av = sp.csr_matrix((val, (row, col)), shape=(self.nC, self.ntFy))
            Rf = self._deflationMatrix('Fy', asOnes=True, withHanging=True)

            self._aveFy2CC = Av*Rf
        return self._aveFy2CC

    @property
    def aveFz2CC(self):
        if getattr(self, '_aveFz2CC', None) is None:

            self.number()

            row, col, val = [], [], []
            PM = [1./2.]*2  # 0.5, 0.5

            for ii, ind in enumerate(self._sortedCells):
                p = self._pointer(ind)
                w = self._levelWidth(p[-1])

                if self.dim == 2:
                    raise Exception('There are no z-faces in 2D')
                elif self.dim == 3:
                    facesz = [
                        self._fz2i[self._index([p[0], p[1], p[2], p[3]])],
                        self._fz2i[self._index([p[0], p[1], p[2] + w, p[3]])],
                    ]

                for pm, face in zip(PM, facesz):
                    row += [ii]
                    col += [face]
                    val += [pm]

            Av = sp.csr_matrix((val, (row, col)), shape=(self.nC, self.ntFz))
            Rf = self._deflationMatrix('Fz', asOnes=True, withHanging=True)
            self._aveFz2CC = Av*Rf
        return self._aveFz2CC

    @property
    def aveF2CC(self):
        "Construct the averaging operator on cell faces to cell centers."
        if getattr(self, '_aveF2CC', None) is None:
            if self.dim == 2:
                self._aveF2CC = 1./self.dim*sp.hstack([
                    self.aveFx2CC, self.aveFy2CC
                ]).tocsr()
            elif self.dim == 3:
                self._aveF2CC = 1./self.dim*sp.hstack([
                    self.aveFx2CC, self.aveFy2CC, self.aveFz2CC
                ]).tocsr()
        return self._aveF2CC

    @property
    def aveF2CCV(self):
        "Construct the averaging operator on cell faces to cell centers."
        if getattr(self, '_aveF2CCV', None) is None:
            if self.dim == 2:
                self._aveF2CCV = sp.block_diag([
                    self.aveFx2CC, self.aveFy2CC
                ]).tocsr()
            elif self.dim == 3:
                self._aveF2CCV = sp.block_diag([
                    self.aveFx2CC, self.aveFy2CC, self.aveFz2CC
                ]).tocsr()
        return self._aveF2CCV

    @property
    def aveN2CC(self):
        if getattr(self, '_aveN2CC', None) is None:
            row, col, val = [], [], []
            PM = [1./2.**self.dim] * 2**self.dim

            for ii, ind in enumerate(self._sortedCells):
                p = self._pointer(ind)
                w = self._levelWidth(p[-1])

                if self.dim == 2:
                    nodes = [
                        self._n2i[self._index([p[0], p[1], p[2]])],
                        self._n2i[self._index([p[0]+w, p[1], p[2]])],
                        self._n2i[self._index([p[0], p[1]+w, p[2]])],
                        self._n2i[self._index([p[0]+w, p[1]+w, p[2]])],
                    ]

                if self.dim == 3:
                    nodes = [
                        self._n2i[self._index([p[0], p[1], p[2], p[3]])],
                        self._n2i[self._index([p[0]+w, p[1], p[2], p[3]])],
                        self._n2i[self._index([p[0], p[1]+w, p[2], p[3]])],
                        self._n2i[self._index([p[0]+w, p[1]+w, p[2], p[3]])],
                        self._n2i[self._index([p[0], p[1],  p[2]+w, p[3]])],
                        self._n2i[self._index([p[0]+w, p[1], p[2]+w, p[3]])],
                        self._n2i[self._index([p[0], p[1]+w, p[2]+w, p[3]])],
                        self._n2i[self._index([p[0]+w, p[1]+w, p[2]+w, p[3]])],
                    ]

                for pm, node in zip(PM, nodes):
                    row += [ii]
                    col += [node]
                    val += [pm]

            Av = sp.csr_matrix((val, (row, col)), shape=(self.nC, self.ntN))
            Re = self._deflationMatrix('N', asOnes=False, withHanging=True)

            self._aveN2CC = Av*Re
        return self._aveN2CC

    def aveCC2Fx(self):
        if getattr(self, '_aveCC2Fx', None) is None:
            self.number()

            faceParent = dict()
            theHang = self._hangingFx
            for key in theHang.keys():
                if not theHang[key][0][0] in faceParent.keys():
                    faceParent[theHang[key][0][0]] = [key]
                else:
                    faceParent[theHang[key][0][0]] += [key]

            row, col, val = [], [], []
            PM = [0.5, 0.5]  # *mesh.dim  # plus / minus

            for ii, ind in enumerate(self._sortedCells):

                p = self._pointer(ind)
            #     w = self._levelWidth(p[-1])

                if self.dim == 2:
                    cells = self._getNextCell(
                        self._index([p[0], p[1], p[2]]), direction=0
                    )
                elif self.dim == 3:
                    cells = self._getNextCell(
                        self._index([p[0], p[1], p[2], p[3]]), direction=0
                    )

                if cells:
                    if isinstance(cells, int):
                        cells = [cells]

                    for cell in cells:

                        pN = self._pointer(cell)

                        if pN[-1] < p[-1]:
                            if self.dim == 2:
                                hangs = faceParent[
                                    self._fx2i[
                                        self._index([pN[0], pN[1], pN[2]])
                                    ]
                                ]
                                count = int(np.abs((p[1] - pN[1]) % 2))

                            elif self.dim == 3:
                                hangs = faceParent[
                                    self._fx2i[
                                        self._index(
                                            [pN[0], pN[1], pN[2], pN[3]]
                                        )
                                    ]
                                ]
                                count = int(np.abs((p[1] - pN[1]) % 2))
                                count += int(2*np.abs((p[2] - pN[2]) % 2))
                            face = hangs[count]
                        else:
                            if self.dim == 2:
                                face = self._fx2i[
                                    self._index([pN[0], pN[1], pN[2]])
                                ]
                            elif self.dim == 3:
                                face = self._fx2i[
                                    self._index([pN[0], pN[1], pN[2], pN[3]])
                                ]

                        row += [face]*2
                        col += [self._cc2i[ind], self._cc2i[cell]]
                        val += PM

            self._aveCC2Fx = sp.csr_matrix(
                (val, (row, col)), shape=(self.ntFx, self.nC)
            )
        # self._aveCC2Fx = aveCC2Fx * utils.sdiag(1./aveCC2Fx.sum(0))

        return self._aveCC2Fx

    def aveCC2Fy(self):
        if getattr(self, '_aveCC2Fy', None) is None:
            self.number()

            faceParent = dict()
            theHang = self._hangingFy
            for key in theHang.keys():
                if not theHang[key][0][0] in faceParent.keys():
                    faceParent[theHang[key][0][0]] = [key]
                else:
                    faceParent[theHang[key][0][0]] += [key]
            row, col, val = [], [], []
            PM = [0.5, 0.5]  # *mesh.dim  # plus / minus

            for ii, ind in enumerate(self._sortedCells):

                p = self._pointer(ind)
            #     w = self._levelWidth(p[-1])

                if self.dim == 2:
                    cells = self._getNextCell(
                        self._index([p[0], p[1], p[2]]), direction=1
                    )
                elif self.dim == 3:
                    cells = self._getNextCell(
                        self._index([p[0], p[1], p[2], p[3]]), direction=1
                    )

                if cells:
                    if isinstance(cells, int):
                        cells = [cells]

                    for cell in cells:

                        pN = self._pointer(cell)

                        if pN[-1] < p[-1]:
                            if self.dim == 2:
                                hangs = faceParent[
                                    self._fy2i[
                                        self._index([pN[0], pN[1], pN[2]])
                                    ]
                                ]
                                count = int(np.abs((p[0] - pN[0]) % 2))

                            elif self.dim == 3:
                                hangs = faceParent[
                                    self._fy2i[
                                        self._index(
                                            [pN[0], pN[1], pN[2], pN[3]]
                                        )
                                    ]
                                ]
                                count = int(np.abs((p[0] - pN[0]) % 2))
                                count += int(2*np.abs((p[3] - pN[3]) % 2))
                            face = hangs[count]
                        else:
                            if self.dim == 2:
                                face = self._fy2i[
                                    self._index([pN[0], pN[1], pN[2]])
                                ]
                            elif self.dim == 3:
                                face = self._fy2i[
                                    self._index([pN[0], pN[1], pN[2], pN[3]])
                                ]

                        row += [face]*2
                        col += [self._cc2i[ind], self._cc2i[cell]]
                        val += PM

            self._aveCC2Fy = sp.csr_matrix(
                (val, (row, col)), shape=(self.ntFy, self.nC)
            )
        # self._aveCC2Fy = aveCC2Fy * utils.sdiag(1./aveCC2Fy.sum(0))

        return self._aveCC2Fy

    def aveCC2Fz(self):
        if getattr(self, '_aveCC2Fz', None) is None:
            faceParent = dict()
            theHang = self._hangingFz
            for key in theHang.keys():
                if not theHang[key][0][0] in faceParent.keys():
                    faceParent[theHang[key][0][0]] = [key]
                else:
                    faceParent[theHang[key][0][0]] += [key]

            row, col, val = [], [], []
            PM = [0.5, 0.5]  # *mesh.dim  # plus / minus

            for ii, ind in enumerate(self._sortedCells):

                p = self._pointer(ind)
            #     w = self._levelWidth(p[-1])

                cells = self._getNextCell(
                    self._index([p[0], p[1], p[2], p[3]]), direction=2
                )

                if cells:
                    if isinstance(cells, int):
                        cells = [cells]

                    for cell in cells:

                        pN = self._pointer(cell)

                        if pN[-1] < p[-1]:
                            hangs = faceParent[
                                self._fz2i[
                                    self._index([pN[0], pN[1], pN[2], pN[3]])
                                ]
                            ]
                            count = int(np.abs((p[0] - pN[0]) % 2))
                            count += int(2*np.abs((p[1] - pN[1]) % 2))
                            face = hangs[count]
                        else:
                            face = self._fz2i[
                                self._index([pN[0], pN[1], pN[2], pN[3]])
                            ]

                        row += [face]*2
                        col += [self._cc2i[ind], self._cc2i[cell]]
                        val += PM

            self._aveCC2Fz = sp.csr_matrix(
                (val, (row, col)), shape=(self.ntFz, self.nC)
            )
        # self._aveCC2Fz = aveCC2Fz * utils.sdiag(1./aveCC2Fz.sum(0))

        return self._aveCC2Fz

    def _getFaceP(self, xFace, yFace, zFace):
        ind1, ind2, ind3 = [], [], []
        for ind in self._sortedCells:
            p = self._pointer(ind)
            w = self._levelWidth(p[-1])

            posX = 0 if xFace == 'fXm' else w
            posY = 0 if yFace == 'fYm' else w
            if self.dim == 3:
                posZ = 0 if zFace == 'fZm' else w

            ind1.append(self._fx2i[self._index([p[0] + posX, p[1]] + p[2:])])
            ind2.append(self._fy2i[self._index([p[0], p[1] + posY] + p[2:])] +
                        self.ntFx)
            if self.dim == 3:
                ind3.append(
                    self._fz2i[self._index([p[0], p[1], p[2] + posZ, p[3]])] +
                    self.ntFx + self.ntFy
                )

        if self.dim == 2:
            IND = np.r_[ind1, ind2]
        if self.dim == 3:
            IND = np.r_[ind1, ind2, ind3]

        PXXX = sp.coo_matrix(
            (np.ones(self.dim*self.nC), (range(self.dim*self.nC), IND)),
            shape=(self.dim*self.nC, self.ntF)
        ).tocsr()

        Rf = self._deflationMatrix('F', withHanging=True, asOnes=True)

        return PXXX * Rf

    def _getFacePxx(self):
        self.number()

        def Pxx(xFace, yFace):
            return self._getFaceP(xFace, yFace, None)
        return Pxx

    def _getFacePxxx(self):
        self.number()

        def Pxxx(xFace, yFace, zFace):
            return self._getFaceP(xFace, yFace, zFace)
        return Pxxx

    def _getEdgeP(self, xEdge, yEdge, zEdge):
        if self.dim == 2:
            # this should be a reordering of the face inner product?
            raise Exception('Not implemented')

        ind1, ind2, ind3 = [], [], []
        for ind in self._sortedCells:
            p = self._pointer(ind)
            w = self._levelWidth(p[-1])

            posX = (
                [0, 0] if xEdge == 'eX0' else [w, 0] if xEdge == 'eX1'
                else [0, w] if xEdge == 'eX2' else [w, w]
            )
            posY = (
                [0, 0] if yEdge == 'eY0' else [w, 0] if yEdge == 'eY1'
                else [0, w] if yEdge == 'eY2' else [w, w]
            )
            posZ = (
                [0, 0] if zEdge == 'eZ0' else [w, 0] if zEdge == 'eZ1'
                else [0, w] if zEdge == 'eZ2' else [w, w]
            )

            ind1.append(
                self._ex2i[
                    self._index([p[0], p[1] + posX[0], p[2] + posX[1], p[3]])
                ]
            )
            ind2.append(
                self._ey2i[
                    self._index([p[0] + posY[0], p[1], p[2] + posY[1], p[3]])
                ] + self.ntEx
            )
            ind3.append(
                self._ez2i[
                    self._index([p[0] + posZ[0], p[1] + posZ[1], p[2], p[3]])
                ] + self.ntEx + self.ntEy
            )

        IND = np.r_[ind1, ind2, ind3]

        PXXX = sp.coo_matrix(
            (np.ones(self.dim*self.nC), (range(self.dim*self.nC), IND)),
            shape=(self.dim*self.nC, self.ntE)
        ).tocsr()

        Re = self._deflationMatrix('E')

        return PXXX * Re

    def _getEdgePxx(self):
        raise Exception('Not implemented') # this should be a reordering of the face inner product?

    def _getEdgePxxx(self):
        self.number()
        def Pxxx(xEdge, yEdge, zEdge):
            return self._getEdgeP(xEdge, yEdge, zEdge)
        return Pxxx

    def point2index(self, locs):
        locs = utils.asArray_N_x_Dim(locs, self.dim)

        TOL = 1e-10

        Nx = self.vectorNx
        Ny = self.vectorNy
        Nz = self.vectorNz

        pointers = list(range(self.dim))
        Nx = np.r_[Nx[0] - TOL, Nx[1:-1], Nx[-1] + TOL]
        pointers[0] = np.searchsorted(Nx, locs[:, 0])
        Ny = np.r_[Ny[0] - TOL, Ny[1:-1], Ny[-1] + TOL]
        pointers[1] = np.searchsorted(Ny, locs[:, 1])
        if self.dim == 3:
            Nz = np.r_[Nz[0] - TOL, Nz[1:-1], Nz[-1] + TOL]
            pointers[2] = np.searchsorted(Nz, locs[:, 2])

        if np.any([np.any(P == len(N)) or np.any(P == 0) for P, N in zip(pointers, [Nx, Ny, Nz])]):
            raise Exception('There are points outside of the mesh.')

        out = []
        for pointer in zip(*pointers):
            for level in range(self._levels+1):
                width = self._levelWidth(level)
                testPointer = [((p-1)//width)*width for p in pointer] + [level]
                test = self._index(testPointer)
                if test in self:
                    out += [test]
                    break
        return out

    def getInterpolationMat(self, locs, locType, zerosOutside=False):
        """ Produces interpolation matrix

        :param numpy.ndarray locs: Location of points to interpolate to
        :param str locType: What to interpolate (see below)
        :rtype: scipy.sparse.csr_matrix
        :return: M, the interpolation matrix

        locType can be::

            'Ex'    -> x-component of field defined on edges
            'Ey'    -> y-component of field defined on edges
            'Ez'    -> z-component of field defined on edges
            'Fx'    -> x-component of field defined on faces
            'Fy'    -> y-component of field defined on faces
            'Fz'    -> z-component of field defined on faces
            'N'     -> scalar field defined on nodes
            'CC'    -> scalar field defined on cell centers
        """
        if 'E' in locType and self.dim == 2:
            raise Exception('Interpolation for edges is not supported in 2D.')
        locs = utils.asArray_N_x_Dim(locs, self.dim)

        TOL = 1e-10
        self.number()

        cells = self.point2index(locs)
        row, col, val = [], [], []
        numberer = getattr(self, '_'+locType.lower()+'2i')

        if zerosOutside is False:
            assert np.all(self.isInside(locs)), "Points outside of mesh"
        else:
            indZeros = np.logical_not(self.isInside(locs))
            locs[indZeros, :] = np.array([v.mean() for v in self.getTensor('CC')])

        if locType in ['Fx', 'Fy', 'Fz', 'Ex', 'Ey', 'Ez']:
            ind = {'x': 0, 'y': 1, 'z': 2}[locType[1]]
            assert self.dim >= ind, 'mesh is not high enough dimension.'
            antiInd = {
                'x': [1, 2], 'y': [0, 2], 'z': [0, 1]
            }[locType[1]][:self.dim-1]
            nF_nE = self.vntF if 'F' in locType else self.vntE
            components = [utils.spzeros(locs.shape[0], n) for n in nF_nE]

            for ii, cell in enumerate(cells):
                loc = locs[ii, :]
                p = self._asPointer(cell)
                h, n = self._cellH(p), self._cellN(p)
                w = self._levelWidth(p[-1])
                if 'E' in locType:
                    iLocs, weights = utils.interputils._interpmat2D(
                        np.array([(loc-n-self.x0)[antiInd]]),
                        np.r_[0., h[antiInd[0]]+TOL],
                        np.r_[0., h[antiInd[1]]+TOL]
                    )
                    newcol = [
                        numberer[
                            self._index([
                                __+w*iLocs[IND][0] if _ == antiInd[0]
                                else __+w*iLocs[IND][1] if _ == antiInd[1]
                                else __ for _, __ in enumerate(p[:-1])
                            ] + [p[-1]])
                        ] for IND in range(4)
                    ]  # sorry
                elif 'F' in locType:
                    _, weights = utils.interputils._interpmat1D(
                        np.r_[(loc-n-self.x0)[ind]], np.r_[0., h[ind]+TOL]
                    )
                    plusFace = self._index(
                        [
                            __+w if _ == ind else __
                            for _, __ in enumerate(p[:-1])
                        ] +
                        [p[-1]]
                    )
                    newcol = [numberer[cell], numberer[plusFace]]
                row += [ii]*len(newcol)
                col += newcol
                val += [weights]

            val = np.hstack(val)
            components[ind] = sp.csr_matrix(
                (val, (row, col)), shape=(locs.shape[0], nF_nE[ind])
            )
            # remove any zero blocks (hstack complains)
            components = [comp for comp in components if comp.shape[1] > 0]
            Q = sp.hstack(components).tocsr()
            if 'E' in locType:
                R = self._deflationMatrix(
                    locType[0], asOnes=False, withHanging=True
                )
            else: # faces
                R = self._deflationMatrix(
                    locType[0], asOnes=True, withHanging=True
                )
        elif locType == 'N':
            for ii, cell in enumerate(cells):
                loc = locs[ii, :]
                p = self._asPointer(cell)
                h, n = self._cellH(p), self._cellN(p)
                w = self._levelWidth(p[-1])

                iLocs, weights = utils.interputils._interpmat3D(
                    np.array([(loc-n-self.x0)]),
                    *[np.r_[0., h[_]+TOL] for _ in range(3)]
                )
                newcol = [
                    numberer[
                        self._index(
                            [__+w*iLocs[IND][_] for _, __ in enumerate(p[:-1])] +
                            [p[-1]])
                    ] for IND in range(8)
                ]  # sorry

                row += [ii]*len(newcol)
                col += newcol
                val += [weights]

            val = np.hstack(val)
            Q = sp.csr_matrix((val, (row, col)), shape=(locs.shape[0], self.ntN))
            R = self._deflationMatrix('N', withHanging=True)
        elif locType == 'CC':
            for ii, cell in enumerate(cells):
                row += [ii]
                col += [numberer[cell]]
                val += [1.0]

            val = np.hstack(val)
            Q = sp.csr_matrix((val, (row, col)), shape=(locs.shape[0], self.nC))
            R = utils.Identity()
        else:
            raise NotImplementedError(
                'getInterpolationMat: locType==' + locType +
                ' and mesh.dim=='+str(self.dim)
            )

        if zerosOutside:
            Q[indZeros, :] = 0

        return Q * R

    def plotGrid(
        self, ax=None, showIt=False,
        grid=True,
        cells=False, cellLine=False,
        nodes=False,
        facesX=False, facesY=False, facesZ=False,
        edgesX=False, edgesY=False, edgesZ=False
    ):

        import matplotlib.pyplot as plt
        import matplotlib
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.colors as colors
        import matplotlib.cm as cmx

        # self.number()
        axOpts = {'projection': '3d'} if self.dim == 3 else {}
        if ax is None:
            ax = plt.subplot(111, **axOpts)
        else:
            assert isinstance(ax, matplotlib.axes.Axes), "ax must be an Axes!"
            fig = ax.figure

        if grid:
            X, Y, Z = [], [], []
            for ind in self._sortedCells:
                p = self._asPointer(ind)
                n = self._cellN(p)
                h = self._cellH(p)
                if self.dim == 2:
                    X += [n[0], n[0] + h[0], n[0] + h[0], n[0], n[0], np.nan]
                    Y += [n[1], n[1], n[1] + h[1], n[1] + h[1], n[1], np.nan]
                elif self.dim == 3:
                    X += [n[0], n[0] + h[0], n[0] + h[0], n[0], n[0], np.nan]*2
                    Y += [n[1], n[1], n[1] + h[1], n[1] + h[1], n[1], np.nan]*2
                    Z += [n[2]]*5+[np.nan]
                    Z += [n[2] + h[2], n[2] + h[2], n[2] + h[2],
                          n[2] + h[2], n[2] + h[2], np.nan]
                    sides = [0, 0], [h[0], 0], [0, h[1]], [h[0], h[1]]
                    for s in sides:
                        X += [n[0] + s[0], n[0] + s[0]]
                        Y += [n[1] + s[1], n[1] + s[1]]
                        Z += [n[2], n[2] + h[2]]

            X += self.x0[0]
            Y += self.x0[1]
            if self.dim == 2:
                ax.plot(X, Y, 'b-')
            elif self.dim == 3:
                Z += self.x0[2]
                ax.plot(X, Y, 'b-', zs=Z)

        if self.dim == 2:
            if cells:
                ax.plot(self.gridCC[:, 0], self.gridCC[:, 1], 'r.')
            if cellLine:
                ax.plot(self.gridCC[:, 0], self.gridCC[:, 1], 'r:')
                ax.plot(self.gridCC[[0, -1], 0], self.gridCC[[0, -1], 1], 'ro')
            if nodes:
                ax.plot(self._gridN[:, 0], self._gridN[:, 1], 'ms')
                ax.plot(
                    self._gridN[list(self._hangingN.keys()), 0],
                    self._gridN[list(self._hangingN.keys()), 1], 'ms',
                    ms=10, mfc='none', mec='m'
                )
            if facesX:
                ax.plot(self._gridFx[:, 0], self._gridFx[:, 1], 'g>')
                ax.plot(
                    self._gridFx[list(self._hangingFx.keys()), 0],
                    self._gridFx[list(self._hangingFx.keys()), 1], 'gs',
                    ms=10, mfc='none', mec='g'
                )
            if facesY:
                ax.plot(self._gridFy[:, 0], self._gridFy[:, 1], 'g^')
                ax.plot(
                    self._gridFy[list(self._hangingFy.keys()), 0],
                    self._gridFy[list(self._hangingFy.keys()), 1], 'gs',
                    ms=10, mfc='none', mec='g'
                )
            ax.set_xlabel('x1')
            ax.set_ylabel('x2')
        elif self.dim == 3:
            if cells:
                ax.plot(
                    self.gridCC[:, 0], self.gridCC[:, 1], 'r.',
                    zs=self.gridCC[:, 2]
                )
            if cellLine:
                ax.plot(
                    self.gridCC[:, 0], self.gridCC[:, 1], 'r:',
                    zs=self.gridCC[:, 2]
                )
                ax.plot(
                    self.gridCC[[0, -1], 0], self.gridCC[[0, -1], 1], 'ro',
                    zs=self.gridCC[[0, -1], 2]
                )

            if nodes:
                ax.plot(
                    self._gridN[:, 0], self._gridN[:, 1], 'ms',
                    zs=self._gridN[:, 2]
                )
                ax.plot(
                    self._gridN[list(self._hangingN.keys()), 0],
                    self._gridN[list(self._hangingN.keys()), 1],
                    'ms', ms=10, mfc='none', mec='m',
                    zs=self._gridN[list(self._hangingN.keys()), 2]
                )
                for key in self._hangingN.keys():
                    for hf in self._hangingN[key]:
                        ind = [key, hf[0]]
                        ax.plot(
                            self._gridN[ind, 0], self._gridN[ind, 1], 'm:',
                            zs=self._gridN[ind, 2]
                        )

            if facesX:
                ax.plot(
                    self._gridFx[:, 0], self._gridFx[:, 1], 'g>',
                    zs=self._gridFx[:, 2]
                )
                ax.plot(
                    self._gridFx[list(self._hangingFx.keys()), 0],
                    self._gridFx[list(self._hangingFx.keys()), 1],
                    'gs', ms=10, mfc='none', mec='g',
                    zs=self._gridFx[list(self._hangingFx.keys()), 2]
                )
                for key in self._hangingFx.keys():
                    for hf in self._hangingFx[key]:
                        ind = [key, hf[0]]
                        ax.plot(
                            self._gridFx[ind, 0], self._gridFx[ind, 1],
                            'g:', zs=self._gridFx[ind, 2]
                        )

            if facesY:
                ax.plot(
                    self._gridFy[:, 0], self._gridFy[:, 1], 'g^',
                    zs=self._gridFy[:, 2]
                )
                ax.plot(
                    self._gridFy[list(self._hangingFy.keys()), 0],
                    self._gridFy[list(self._hangingFy.keys()), 1],
                    'gs', ms=10, mfc='none', mec='g',
                    zs=self._gridFy[list(self._hangingFy.keys()), 2]
                )
                for key in self._hangingFy.keys():
                    for hf in self._hangingFy[key]:
                        ind = [key, hf[0]]
                        ax.plot(
                            self._gridFy[ind, 0], self._gridFy[ind, 1],
                            'g:', zs=self._gridFy[ind, 2]
                        )

            if facesZ:
                ax.plot(
                    self._gridFz[:, 0], self._gridFz[:, 1], 'g^',
                    zs=self._gridFz[:, 2]
                )
                ax.plot(
                    self._gridFz[list(self._hangingFz.keys()), 0],
                    self._gridFz[list(self._hangingFz.keys()), 1],
                    'gs', ms=10, mfc='none', mec='g',
                    zs=self._gridFz[list(self._hangingFz.keys()), 2]
                )
                for key in self._hangingFz.keys():
                    for hf in self._hangingFz[key]:
                        ind = [key, hf[0]]
                        ax.plot(
                            self._gridFz[ind, 0], self._gridFz[ind, 1],
                            'g:', zs=self._gridFz[ind, 2]
                        )

            if edgesX:
                ax.plot(
                    self._gridEx[:, 0], self._gridEx[:, 1], 'k>',
                    zs=self._gridEx[:, 2]
                )
                ax.plot(
                    self._gridEx[list(self._hangingEx.keys()), 0],
                    self._gridEx[list(self._hangingEx.keys()), 1],
                    'ks', ms=10, mfc='none', mec='k',
                    zs=self._gridEx[list(self._hangingEx.keys()), 2]
                )
                for key in self._hangingEx.keys():
                    for hf in self._hangingEx[key]:
                        ind = [key, hf[0]]
                        ax.plot(
                            self._gridEx[ind, 0], self._gridEx[ind, 1],
                            'k:', zs=self._gridEx[ind, 2]
                        )

            if edgesY:
                ax.plot(
                    self._gridEy[:, 0], self._gridEy[:, 1], 'k<',
                    zs=self._gridEy[:, 2]
                )
                ax.plot(
                    self._gridEy[list(self._hangingEy.keys()), 0],
                    self._gridEy[list(self._hangingEy.keys()), 1],
                    'ks', ms=10, mfc='none', mec='k',
                    zs=self._gridEy[list(self._hangingEy.keys()), 2]
                )
                for key in self._hangingEy.keys():
                    for hf in self._hangingEy[key]:
                        ind = [key, hf[0]]
                        ax.plot(
                            self._gridEy[ind, 0], self._gridEy[ind, 1],
                            'k:', zs=self._gridEy[ind, 2]
                        )

            if edgesZ:
                ax.plot(
                    self._gridEz[:, 0], self._gridEz[:, 1], 'k^',
                    zs=self._gridEz[:, 2]
                )
                ax.plot(
                    self._gridEz[list(self._hangingEz.keys()), 0],
                    self._gridEz[list(self._hangingEz.keys()), 1],
                    'ks', ms=10, mfc='none', mec='k',
                    zs=self._gridEz[list(self._hangingEz.keys()), 2]
                )
                for key in self._hangingEz.keys():
                    for hf in self._hangingEz[key]:
                        ind = [key, hf[0]]
                        ax.plot(
                            self._gridEz[ind, 0], self._gridEz[ind, 1],
                            'k:', zs=self._gridEz[ind, 2]
                        )
            ax.set_xlabel('x1')
            ax.set_ylabel('x2')
            ax.set_zlabel('x3')
        ax.grid(True)

        if showIt:
            plt.show()

    def plotImage(self, I, ax=None, showIt=False, grid=False, clim=None):
        if self.dim == 3:
            raise Exception('Use plot slice?')

        import matplotlib.pyplot as plt
        import matplotlib
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.colors as colors
        import matplotlib.cm as cmx

        if ax is None:
            ax = plt.subplot(111)
        jet = cm = plt.get_cmap('jet')
        cNorm = colors.Normalize(
            vmin=I.min() if clim is None else clim[0],
            vmax=I.max() if clim is None else clim[1])

        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
        ax.set_xlim((self.x0[0], self.h[0].sum()))
        ax.set_ylim((self.x0[1], self.h[1].sum()))
        for ii, node in enumerate(self._sortedCells):
            x0, sz = self._cellN(node), self._cellH(node)
            ax.add_patch(
                plt.Rectangle((x0[0], x0[1]), sz[0], sz[1],
                facecolor=scalarMap.to_rgba(I[ii]),
                edgecolor='k' if grid else 'none')
            )
            # if text: ax.text(self.center[0], self.center[1], self.num)
        # http://stackoverflow.com/questions/8342549/matplotlib-add-colorbar-to-a-sequence-of-line-plots
        scalarMap._A = []
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        if showIt:
            plt.show()
        return [scalarMap]

    def plotSlice(
        self, v, vType='CC',
        normal='Z', ind=None, grid=True, view='real',
        ax=None, clim=None, showIt=False,
        pcolorOpts=None, streamOpts=None, gridOpts=None
    ):

        if pcolorOpts is None:
            pcolorOpts = {}
        if streamOpts is None:
            streamOpts = {'color': 'k'}
        if gridOpts is None:
            gridOpts = {'color': 'k', 'alpha': 0.5}
        assert vType in ['CC', 'F', 'E']
        assert self.dim == 3

        import matplotlib.pyplot as plt
        import matplotlib
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.colors as colors
        import matplotlib.cm as cmx

        #: Size of the sliced dimension
        szSliceDim = len(getattr(self, 'h'+normal.lower()))
        if ind is None:
            ind = int(szSliceDim//2)
        assert type(ind) in integer_types, 'ind must be an integer'
        indLoc = getattr(self, 'vectorCC'+normal.lower())[ind]
        normalInd = {'X': 0, 'Y': 1, 'Z': 2}[normal]
        antiNormalInd = {'X': [1, 2], 'Y': [0, 2], 'Z': [0, 1]}[normal]
        h2d = []
        x2d = []
        if 'X' not in normal:
            h2d.append(self.hx)
            x2d.append(self.x0[0])
        if 'Y' not in normal:
            h2d.append(self.hy)
            x2d.append(self.x0[1])
        if 'Z' not in normal:
            h2d.append(self.hz)
            x2d.append(self.x0[2])
        tM = TensorMesh(h2d, x2d)  #: Temp Mesh

        def getLocs(*args):
            if len(args) == 1:
                grids = (args[0], args[0], args[0])
            else:
                assert len(args) == 3
                grids = args
            one = np.ones((grids[0].shape[0], 1))*indLoc
            if normal == 'X':
                return np.hstack((one, grids[0][:, [0]], grids[1][:, [1]]))
            if normal == 'Y':
                return np.hstack((grids[0][:, [0]], one, grids[1][:, [1]]))
            if normal == 'Z':
                return np.hstack((grids[0][:, [0]], grids[1][:, [1]], one))

        def doSlice(v):
            if vType == 'CC':
                P = self.getInterpolationMat(getLocs(tM.gridCC), 'CC')
            elif vType in ['F', 'E']:
                Ps = []
                gridX = getLocs(getattr(tM, 'grid' + vType + 'x'))
                gridY = getLocs(getattr(tM, 'grid' + vType + 'y'))
                Ps += [self.getInterpolationMat(
                    gridX, vType + ('y' if normal == 'X' else 'x')
                )]
                Ps += [self.getInterpolationMat(
                    gridY, vType + ('y' if normal == 'Z' else 'z')
                )]
                P = sp.vstack(Ps)
            return P*v

        v2d = doSlice(v)

        if ax is None:
            fig = plt.figure()
            ax = plt.subplot(111)
        else:
            assert isinstance(ax, matplotlib.axes.Axes), "ax must be an matplotlib.axes.Axes"
            fig = ax.figure

        out = tM._plotImage2D(
            v2d, vType=vType, view=view, ax=ax, clim=clim,
            pcolorOpts=pcolorOpts, streamOpts=streamOpts
        )

        ax.set_xlabel('y' if normal == 'X' else 'x')
        ax.set_ylabel('y' if normal == 'Z' else 'z')
        ax.set_title(
            'Slice {0:d}, {1!s} = {2:4.2f}'.format(ind, normal, indLoc)
        )

        if grid:
            _ = antiNormalInd
            X = []
            Y = []
            for cell in self._cells:
                p = self._pointer(cell)
                n, h = self._cellN(p), self._cellH(p)
                if n[normalInd] < indLoc and n[normalInd]+h[normalInd] > indLoc:
                    X += [
                        n[_[0]], n[_[0]] + h[_[0]], n[_[0]] + h[_[0]],
                        n[_[0]], n[_[0]], np.nan
                    ]
                    Y += [
                        n[_[1]], n[_[1]], n[_[1]] + h[_[1]], n[_[1]] + h[_[1]],
                        n[_[1]], np.nan
                    ]
            out = list(out)
            out += ax.plot(X, Y, **gridOpts)
            if len(out) > 2:  # this is not robust, searching for the streamlines would be better
                out[1].lines.set_zorder(200)
                out[1].arrows.set_zorder(201)
        if showIt:
            plt.show()
        return tuple(out)

    def __len__(self):
        return self.nC

    def __getitem__(self, key):
        if isinstance(key, slice):
            # Get the start, stop, and step from the slice
            return [self[ii] for ii in xrange(*key.indices(len(self)))]
        elif isinstance(key, int):
            if key < 0:  # Handle negative indices
                key += len(self)
            if key >= len(self):
                raise IndexError(
                    "The index ({0:d}) is out of range.".format(key)
                )

            self._numberCells()  # no-op if numbered
            index = self._i2cc[key]
            pointer = self._asPointer(index)
            return Cell(self, index, pointer)
        else:
            raise TypeError("Invalid argument type.")


class Cell(object):
    def __init__(self, mesh, index, pointer):
        self.mesh = mesh
        self._index = index
        self._pointer = pointer

    @property
    def nodes(self):
        """The node index in _gridN (this may include hanging nodes)."""
        M = self.mesh
        M._numberNodes()
        p = self._pointer
        i = self._index
        w = M._levelWidth(p[-1])

        if M.dim == 2:
            n = [
                i,
                M._index([p[0] + w, p[1], p[2]]),
                M._index([p[0], p[1] + w, p[2]]),
                M._index([p[0] + w, p[1] + w, p[2]]),
            ]
        elif self.dim == 3:
            n = [
                i,
                M._index([p[0] + w, p[1], p[2], p[3]]),
                M._index([p[0], p[1] + w, p[2], p[3]]),
                M._index([p[0] + w, p[1] + w, p[2], p[3]]),
                M._index([p[0], p[1], p[2] + w, p[3]]),
                M._index([p[0] + w, p[1], p[2] + w, p[3]]),
                M._index([p[0], p[1] + w, p[2] + w, p[3]]),
                M._index([p[0] + w, p[1] + w, p[2] + w, p[3]]),
            ]
        return [M._n2i[_] for _ in n]

    @property
    def center(self):
        if getattr(self, '_center', None) is None:
            self._center = np.array(self.mesh._cellC(self._pointer))
        return self._center

    @property
    def h(self):
        return self.mesh._cellH(self._pointer)

    @property
    def x0(self):
        return self.mesh._cellN(self._pointer)

    @property
    def dim(self):
        return self.mesh.dim


def SortGrid(grid, offset=0):
    """Sorts a grid by the x0 location."""

    eps = 1e-7

    def mycmp(c1, c2):
        c1 = grid[c1-offset]
        c2 = grid[c2-offset]
        if c1.size == 2:
            if np.abs(c1[1] - c2[1]) < eps:
                return c1[0] - c2[0]
            return c1[1] - c2[1]
        elif c1.size == 3:
            if np.abs(c1[2] - c2[2]) < eps:
                if np.abs(c1[1] - c2[1]) < eps:
                    return c1[0] - c2[0]
                return c1[1] - c2[1]
            return c1[2] - c2[2]

    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0

    return sorted(list(range(offset, grid.shape[0]+offset)), key=K)
