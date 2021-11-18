# -*- coding: utf-8 -*-
"""
Created on Wed May 15 13:15:49 2019

@author: URJC
"""
import numpy as np
import numpy.linalg as la
from scipy import ndimage as scpimg


# from GMRVUtils.generic import ObjPool


def labeledImgAStar(labeledImg,
                    spacing=None,
                    hFunc='ecuclidian',  # hFuncAppend = False, !Todo
                    distanceField=None,  # s
                    costFunc=None,
                    costFuncAppend=True,
                    retDebugInfo=False):
    if spacing is None:
        spacing = np.ones([len(labeledImg.shape)])

    _startIdxs = zip(*np.nonzero(labeledImg == 1))  # ojo no es un array es un iterador

    def _endFuc(node):
        return labeledImg[node.idx] == 2

    _blockedIdxs = []  # podia utilizar zip(*np.nonzero(labeledImg == 3))
    # mejor meterlo en closedset directamente

    closedSet = (labeledImg == 3)

    def _add2ClosedSetFunc(node):
        closedSet[node.idx] = True

    def _isInClosedSetFunc(node):
        return closedSet[node.idx]

    if callable(hFunc):
        def _hFunc(node):
            return hFunc(node.idx)

    elif hFunc == 'distanceField':
        if distanceField is None:
            distanceField = \
                scpimg.distance_transform_edt(labeledImg != 2, sampling=spacing)

        def _hFunc(node):
            return distanceField[node.idx]

        # funciona bien si hay pocos goals
    elif hFunc == 'ecuclidian':
        endSet = np.array([x for x in zip(*np.nonzero(labeledImg == 2))])

        def _hFunc(node):
            return np.min([la.norm((node.npidx - end) * spacing)
                           for end in endSet])

    else:
        raise ValueError("Invalid hFunc")

    if costFunc is None:
        def _costFunc(n1, n2):
            return n2.g
    #            #esto es debería se lo correcto, pero se rellena al crear el nodo
    #            v = (n1.npidx-n2.npidx)*spacing
    #            v *= v
    #            return np.sqrt(v.sum()) + costFunc(n1.idx,n2.idx)

    elif costFuncAppend == True and costFunc is not None:
        def _costFunc(n1, n2):
            return n2.g + costFunc(n1.idx, n2.idx)

    else:
        def _costFunc(n1, n2):
            return costFunc(n1.idx, n2.idx)

    # solo se usan para calcular el siguiente elemento
    sl = len(labeledImg.shape)
    ones = np.ones(sl, dtype=np.int)
    bottom = -ones
    index = ones * 3
    center = tuple(ones)

    inc = np.array(
        [np.array(i) + bottom for i in np.ndindex(*index) if center != i])

    inc = np.roll(inc, -(3 ** (sl - 1)), axis=0)
    s2 = spacing * spacing
    dist = np.array([np.sqrt(np.sum(np.abs(i) * s2)) for i in inc])

    shape = np.array(labeledImg.shape, dtype=np.int)
    zero = np.zeros(3, dtype=np.int)

    def _neighbourFunc(node):
        for i, d in zip(inc, dist):
            cp = node.npidx + i

            # Se comprueba si esta dentro de la imagen
            if np.any(np.less(cp, zero)) or \
                    np.any(np.greater_equal(cp, shape)):
                continue

            newNode = AStarNode(tuple(cp))
            newNode.g = d + node.g
            yield newNode

    if retDebugInfo:
        p, osIdx = _genericAStar(_startIdxs, _blockedIdxs, _endFuc,
                                 _add2ClosedSetFunc, _isInClosedSetFunc,
                                 _hFunc, _costFunc,
                                 _neighbourFunc, retOpenSet=True)
        openSet = np.full(labeledImg.shape, False)

        idx = [n.idx for _, n in osIdx.items()]
        idx = [i for i in zip(*idx)]
        openSet[tuple(idx)] = True

        return p, openSet, closedSet

    return _genericAStar(_startIdxs, _blockedIdxs, _endFuc,
                         _add2ClosedSetFunc, _isInClosedSetFunc,
                         _hFunc, _costFunc,
                         _neighbourFunc)


class AStarNode():
    '''
        A* Algorithm Node:

        idx must be hashable
        __eq__ check npidx
        __lt__, __le__, __gt__, and __ge__, check f
    '''

    def __init__(self, idx):
        self.parent = None
        self.idx = idx
        self.npidx = np.array(idx)
        self.g = 0  # distancia recorrida
        self.h = 0  # euristica (la sacas del campo de distancia)
        self.f = 0  # g+h

    def __eq__(self, other): return self.npidx == other.npidx

    def __hash__(self): return hash(self.idx)

    def __lt__(self, other): return self.f < other.f

    def __le__(self, other): return self.f <= other.f

    def __gt__(self, other): return self.f > other.f

    def __ge__(self, other): return self.f >= other.f


# Algoritmo generico
def _genericAStar(startIdxs, blockedIdxs, endFuc,
                  add2ClosedSetFunc, isInClosedSetFunc,
                  hFunc, costFunc,
                  neighbourFunc,
                  retOpenSet=False):
    openSet = dict([[idx, AStarNode(idx)] for idx in startIdxs])

    for _, node in openSet.items():
        node.h = hFunc(node)
        node.g = costFunc(node, node)
        node.f = node.h + node.g

    # Nodos que no pueden visitarse
    # blockedSet = set ([AStarNode(idx) for idx in blockedIdxs])
    for idx in blockedIdxs:
        add2ClosedSetFunc(node)

    while openSet:  # itera mientra haya elementos
        # Se calcula el nodo cuya estimación a destino es menor
        _, currentNode = min(openSet.items(), key=lambda x: x[1])

        # todo: Se puede usar el del tambien
        openSet.pop(currentNode.idx)
        add2ClosedSetFunc(currentNode)

        # condición de parada
        if endFuc(currentNode):
            path = []
            while currentNode is not None:
                path.append(currentNode.idx)
                currentNode = currentNode.parent
            if retOpenSet:
                return path, openSet
            return path

        for node in neighbourFunc(currentNode):
            # Se comprueba si es un obstaculo o si ha sido visitado
            if isInClosedSetFunc(node):
                continue

            inOpenSet = node.idx in openSet
            #            print(inOpenSet)
            node.parent = currentNode
            node.h = openSet[node.idx].h if inOpenSet else hFunc(node)
            node.g = costFunc(currentNode, node)
            node.f = node.h + node.g
            #            if node.h < 0:
            #                print("Caos!")
            #            if node.g < 0:
            #                print("Caos!")

            #            print(node.parent.idx, node.f, node.h, node.g)
            #            if inOpenSet:
            #               if openSet[node.idx].parent is not None:
            #                   print(  openSet[node.idx].parent.idx, openSet[node.idx].f, openSet[node.idx].h, openSet[node.idx].g)
            #               else:
            #                   print(None, openSet[node.idx].f, openSet[node.idx].h, openSet[node.idx].g)

            #            if inOpenSet:
            #                if openSet[node.idx].f > node.f:
            #                    print("sorter ", openSet[node.idx].f, node.f)
            #                elif openSet[node.idx].f == node.f:
            #                    print ('equal', openSet[node.idx].f, node.f)
            #                else:
            #                    print("longer", openSet[node.idx].f, node.f)

            if not inOpenSet or \
                    openSet[node.idx].f > node.f:
                openSet[node.idx] = node

    #                   if openSet[node.idx].parent is not None:
    #                       print(openSet[node.idx].parent.idx, openSet[node.idx].f, openSet[node.idx].h, openSet[node.idx].g)
    #                   else:
    #                       print(None, openSet[node.idx].f, openSet[node.idx].h, openSet[node.idx].g)

    return None


# Multiple Starts and Multiple target
def AStarMSMT(labeledImg):
    # Pep8 recomienda no usar funciones lambda y asignarlas a una variable

    distanceField = \
        scpimg.distance_transform_edt(labeledImg != 2)

    def _hfunc(idx):
        return distanceField[idx]

    hFunc = _hfunc

    # quitar de un set es rápido es una tabla hash
    # se podría probar con listas tambien
    #    https://www.ics.uci.edu/~pattis/ICS-33/lectures/complexitypython.txt
    #   todo: https://sourcemaking.com/design_patterns/object_pool/python/1
    openSet = dict([[idx, AStarNode(idx)]
                    for idx in zip(*np.nonzero(labeledImg == 1))])

    for _, node in openSet.items():
        node.h = hFunc(node.idx)
        node.g = 0  # Todo + cost
        node.f = node.h + node.g

    #    targetSet = dict()
    # los obstaculos se guardan como visitados así no se reccoren
    closedSet = (labeledImg == 3)

    # Constantes
    #    sl = len(labeledImg.shape)
    #    ones = np.ones(sl,dtype=np.int)
    #    bottom = -ones
    #    index = ones*3
    #    center = tuple(ones)
    #
    #    inc = np.array(
    #            [np.array(i) + bottom for i in np.ndindex(*index) if center != i],
    #            dtype=np.int)
    #
    #    s2= np.array([1,1,1])
    #    dist = np.array([np.sqrt(np.sum(np.abs(i)*s2)) for i in inc])
    #
    #    shape = np.array(labeledImg.shape,dtype = np.int)
    #    zero = np.zeros(3, dtype = np.int)

    inc = np.array([(-1, 1, 0), (0, 1, 0), (1, 1, 0),
                    (-1, 0, 0), (1, 0, 0),
                    (-1, -1, 0), (0, -1, 0), (1, -1, 0),
                    (-1, 1, 1), (0, 1, 1), (1, 1, 1),
                    (-1, 0, 1), (0, 0, 1), (1, 0, 1),
                    (-1, -1, 1), (0, -1, 1), (1, -1, 1),
                    (-1, 1, -1), (0, 1, -1), (1, 1, -1),
                    (-1, 0, -1), (0, 0, -1), (1, 0, -1),
                    (-1, -1, -1), (0, -1, -1), (1, -1, -1)
                    ], dtype=np.int)

    s2 = np.array([1, 1, 1])
    dist = np.array([np.sqrt(np.sum(np.abs(i) * s2)) for i in inc])

    shape = np.array(labeledImg.shape, dtype=np.int)
    zero = np.zeros(3, dtype=np.int)

    while openSet:  # itera mientra haya elementos
        # Se calcula el nodo cuya estimación a destino es menor
        currentF = np.inf
        currentNode = None
        for _, node in openSet.items():
            if node.f < currentF:
                currentNode = node
                currentF = node.f

        # todo: Se puede usar el del tambien
        openSet.pop(currentNode.idx)
        closedSet[currentNode.idx] = True

        # condición de parada
        if labeledImg[currentNode.idx] == 2:
            path = []
            while currentNode is not None:
                path.append(currentNode.idx)
                currentNode = currentNode.parent
            return path

        for i, d in zip(inc, dist):
            cp = currentNode.npidx + i

            # Se comprueba si esta dentro de la imagen
            if np.any(np.less(cp, zero)) or \
                    np.any(np.greater_equal(cp, shape)):
                continue

            newNode = AStarNode(tuple(cp))

            # Se comprueba si es un obstaculo o si ha sido visitado
            if closedSet[newNode.idx]:  # Todo: cambiar
                continue

            inOpenSet = newNode.idx in openSet

            newNode.parent = currentNode
            newNode.h = openSet[newNode.idx].h if inOpenSet else hFunc(newNode.idx)
            newNode.g = d + currentNode.g  # Todo + cost
            newNode.f = newNode.h + newNode.g

            if not inOpenSet or \
                    openSet[newNode.idx].f > newNode.f:
                openSet[newNode.idx] = newNode

    return None
