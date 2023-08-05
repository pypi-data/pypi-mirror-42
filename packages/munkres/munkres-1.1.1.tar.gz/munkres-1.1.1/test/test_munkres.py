from munkres import Munkres, DISALLOWED, UnsolvableMatrix
import munkres
from nose.tools import assert_equals, raises

m = Munkres()

def _get_cost(matrix):
    indices = m.compute(matrix)
    return sum([matrix[row][column] for row, column in indices])

def test_documented_example():
    '''
    Test the matrix in the documented example.
    '''
    matrix = [[5, 9, 1],
              [10, 3, 2],
              [8, 7, 4]]
    cost = _get_cost(matrix)
    assert_equals(cost, 12)

def test_5_x_5():
    matrix = [[12, 9, 27, 10, 23],
              [7, 13, 13, 30, 19],
              [25, 18, 26, 11, 26],
              [9, 28, 26, 23, 13],
              [16, 16, 24, 6, 9]]
    cost = _get_cost(matrix)
    assert_equals(cost, 51)

def test_10_x_10():
    matrix = [[37, 34, 29, 26, 19, 8, 9, 23, 19, 29],
              [9, 28, 20, 8, 18, 20, 14, 33, 23, 14],
              [15, 26, 12, 28, 6, 17, 9, 13, 21, 7],
              [2, 8, 38, 36, 39, 5, 36, 2, 38, 27],
              [30, 3, 33, 16, 21, 39, 7, 23, 28, 36],
              [7, 5, 19, 22, 36, 36, 24, 19, 30, 2],
              [34, 20, 13, 36, 12, 33, 9, 10, 23, 5],
              [7, 37, 22, 39, 33, 39, 10, 3, 13, 26],
              [21, 25, 23, 39, 31, 37, 32, 33, 38, 1],
              [17, 34, 40, 10, 29, 37, 40, 3, 25, 3]]
    cost = _get_cost(matrix)
    assert_equals(cost, 66)

def test_20_x_20():
    matrix = [[5, 4, 3, 9, 8, 9, 3, 5, 6, 9, 4, 10, 3, 5, 6, 6, 1, 8, 10, 2],
              [10, 9, 9, 2, 8, 3, 9, 9, 10, 1, 7, 10, 8, 4, 2, 1, 4, 8, 4, 8],
              [10, 4, 4, 3, 1, 3, 5, 10, 6, 8, 6, 8, 4, 10, 7, 2, 4, 5, 1, 8],
              [2, 1, 4, 2, 3, 9, 3, 4, 7, 3, 4, 1, 3, 2, 9, 8, 6, 5, 7, 8],
              [3, 4, 4, 1, 4, 10, 1, 2, 6, 4, 5, 10, 2, 2, 3, 9, 10, 9, 9, 10],
              [1, 10, 1, 8, 1, 3, 1, 7, 1, 1, 2, 1, 2, 6, 3, 3, 4, 4, 8, 6],
              [1, 8, 7, 10, 10, 3, 4, 6, 1, 6, 6, 4, 9, 6, 9, 6, 4, 5, 4, 7],
              [8, 10, 3, 9, 4, 9, 3, 3, 4, 6, 4, 2, 6, 7, 7, 4, 4, 3, 4, 7],
              [1, 3, 8, 2, 6, 9, 2, 7, 4, 8, 10, 8, 10, 5, 1, 3, 10, 10, 2, 9],
              [2, 4, 1, 9, 2, 9, 7, 8, 2, 1, 4, 10, 5, 2, 7, 6, 5, 7, 2, 6],
              [4, 5, 1, 4, 2, 3, 3, 4, 1, 8, 8, 2, 6, 9, 5, 9, 6, 3, 9, 3],
              [3, 1, 1, 8, 6, 8, 8, 7, 9, 3, 2, 1, 8, 2, 4, 7, 3, 1, 2, 4],
              [5, 9, 8, 6, 10, 4, 10, 3, 4, 10, 10, 10, 1, 7, 8, 8, 7, 7, 8, 8],
              [1, 4, 6, 1, 6, 1, 2, 10, 5, 10, 2, 6, 2, 4, 5, 5, 3, 5, 1, 5],
              [5, 6, 9, 10, 6, 6, 10, 6, 4, 1, 5, 3, 9, 5, 2, 10, 9, 9, 5, 1],
              [10, 9, 4, 6, 9, 5, 3, 7, 10, 1, 6, 8, 1, 1, 10, 9, 5, 7, 7, 5],
              [2, 6, 6, 6, 6, 2, 9, 4, 7, 5, 3, 2, 10, 3, 4, 5, 10, 9, 1, 7],
              [5, 2, 4, 9, 8, 4, 8, 2, 4, 1, 3, 7, 6, 8, 1, 6, 8, 8, 10, 10],
              [9, 6, 3, 1, 8, 5, 7, 8, 7, 2, 1, 8, 2, 8, 3, 7, 4, 8, 7, 7],
              [8, 4, 4, 9, 7, 10, 6, 2, 1, 5, 8, 5, 1, 1, 1, 9, 1, 3, 5, 3]]
    cost = _get_cost(matrix)
    assert_equals(cost, 22)

def test_disallowed():
    matrix = [[5, 9, DISALLOWED],
              [10, DISALLOWED, 2],
              [8, DISALLOWED, 4]]
    cost = _get_cost(matrix)
    assert_equals(cost, 19)

def test_profit():
    profit_matrix = [[94, 66, 100, 18, 48],
                     [51, 63, 97, 79, 11],
                     [37, 53, 57, 78, 28],
                     [59, 43, 97, 88, 48],
                     [52, 19, 89, 60, 60]]
    import sys
    cost_matrix = munkres.make_cost_matrix(
        profit_matrix, lambda cost: sys.maxsize - cost
    )
    indices = m.compute(cost_matrix)
    profit = sum([profit_matrix[row][column] for row, column in indices])
    assert_equals(profit, 392)

def test_irregular():
    matrix = [[12, 26, 17],
              [49, 43, 36, 10, 5],
              [97, 9, 66, 34],
              [52, 42, 19, 36],
              [15, 93, 55, 80]]

    cost = _get_cost(matrix)
    assert_equals(cost, 43)

def test_rectangular():
    matrix = [[34, 26, 17, 12],
              [43, 43, 36, 10],
              [97, 47, 66, 34],
              [52, 42, 19, 36],
              [15, 93, 55, 80]]

    padded_matrix = m.pad_matrix(matrix, 0)
    padded_cost = _get_cost(padded_matrix)
    cost = _get_cost(matrix)
    assert_equals(padded_cost, cost)
    assert_equals(cost, 70)

@raises(UnsolvableMatrix)
def test_unsolvable():
    matrix = [[5, 9, DISALLOWED],
              [10, DISALLOWED, 2],
              [DISALLOWED, DISALLOWED, DISALLOWED]]
    m.compute(matrix)

