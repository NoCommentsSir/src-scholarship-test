from typing import List

import numpy as np


class Element:
    def __init__(self, index, value):
        self.index = index
        self.value = value


class SparseMatrix:
    def __init__(self, *, file=None, dense: np.array = None):
        self.data_: List[List[Element]] = []

        if file is not None:
            assert dense is None
            with open(file, 'r') as f:
                n = int(f.readline())
                for _ in range(n):
                    self.data_.append([])
                    line = f.readline().split()
                    for j in range(1, len(line), 2):
                        self.data_[-1].append(Element(index=int(line[j]),
                                                      value=float(line[j+1])))

        if dense is not None:
            assert file is None
            n = len(dense)
            for i in range(n):
                self.data_.append([])
                for j in range(n):
                    if dense[i, j] != 0:
                        self.data_[i].append(Element(j, dense[i, j]))

    def print(self):
        n = len(self.data_)
        print(f'{len(self.data_)} rows')
        for i in range(n):
            element_index = 0
            for j in range(n):
                if element_index < len(self.data_[i]):
                    if self.data_[i][element_index].index == j:
                        print(f'{self.data_[i][element_index].value:.2f} ', end='')
                    else:
                        print(f'{0:.2f} ', end='')
                else:
                    print(f'{0:.2f} ', end='')
            print()

    def to_dense(self):
        n = len(self.data_)
        A = np.zeros((n, n), dtype=float)
        for i in range(n):
            for element in self.data_[i]:
                A[i, element.index] = element.value
        return A

    def __matmul__(self, other):
        A1 = self.to_dense()
        A2 = other.to_dense()
        n_1 = len(A1[0])
        n_2 = len(A2[0])
        if n_1 != n_2:
            print("Error: matrix shape error")
            return
        arr = []
        for i in range(n_1):
            arr.append([0 for _ in range(n_1)])

        for i in range(n_1):
            for j in range(n_1):
                for k in range(n_1):
                    arr[i][j] += A1[i][k] * A2[k][j]
        arr = np.array(arr)
        result = SparseMatrix(dense=arr)
        return result

    def __pow__(self, power, modulo=None):

        # vvvvv your code here vvvvv
        A = self
        result = A
        for i in range(1, power):
            temp = result
            result = temp.__matmul__(A)
        # ^^^^^ your code here ^^^^^

        return result
