import numpy
import numpy.matlib

def test_matmult():
    mat_a = numpy.matlib.rand(10000,5000)
    mat_b = numpy.matlib.rand(5000,10000)

    result = numpy.dot(mat_a, mat_b)
    assert result.size == 100000000
