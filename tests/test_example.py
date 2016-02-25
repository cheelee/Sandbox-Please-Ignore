import numpy

def test_numpy():
    a = numpy.arange(15).reshape(3, 5)
    assert a.size == 15
