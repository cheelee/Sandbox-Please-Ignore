import numpy
import numpy.matlib

def test_matmult():
    mat_a = numpy.matlib.rand(2000,1000)
    mat_b = numpy.matlib.rand(1000,5000)

    result = numpy.dot(mat_a, mat_b)
    assert result.size == 10000000
