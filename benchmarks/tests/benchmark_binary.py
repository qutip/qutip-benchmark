"""This file contains the biary operations that will be benchmarked.
All the functions in this file should return the function that will
be tested. The tested funtion must have as inputs:

    A: input 2D array

    dtype: data type of A (np, qt.data.Dense ... )

    rep: number of times that the operations will be repeated.
The function does not need to return anything else. The getters
have as input parameters only dtype. If the getter returns a
 NotImplementedError it will be omitted in the benchmarks."""


def get_matmul():
    def matmul(A, B, rep):
        for _ in range(rep):
            x = A@B
        return x

    return matmul


def get_add():
    def add(A, B, rep):
        for _ in range(rep):
            x = A+B

        return x
    return add
