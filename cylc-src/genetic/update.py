import defopt
import sympy
import random
import numpy
import glob
import re
from matplotlib import pylab


#OBJFUN_EXPR = '1 + 2*(x-3)**4'
OBJFUN_EXPR = '1 + 0.1*(x-3)**2 - 0.2 * cos((x-3)*2*pi)'
FILE = 'data.npy'
X = sympy.Symbol('x')
#F = sympy.parsing.sympy_parser.parse_expr(OBJFUN_EXPR)


def init(*, a: float=0., b:float=1., nsample: int=100) -> None:
    """
    Random initialize
    :param a: min value of interval to search
    :param b: max value of interval to search
    :param nsample: number of samples 
    """

    xs = a + (b - a)*numpy.random.rand(nsample)
    print(f'param in the range {min(xs)} - {max(xs)}')

    # evaluate the cost function
    fs = sympy.utilities.lambdify(X, OBJFUN_EXPR, 'numpy')(xs)
    print(f'f in the range {min(fs)} - {max(fs)}')

    data = numpy.empty((2, nsample), numpy.float64)
    data[0, :] = xs
    data[1, :] = fs

    numpy.save(FILE, data)


def fitness(*, tol: float=1.e-4) -> None:
    """
    Evaluate fitness
    :param tol: cost function tolerance
    """
    data = numpy.load(FILE)
    fmin = min(data[1, :])
    print(f'min value: {fmin}')
    if fmin > tol:
        raise RuntimeError(f"\n\nNot yet achieved target fitness since min(f) = {fmin} > {tol}\n\n")



def select_breed(*, nselect: int=10):
    """
    Select candidates with highest score and breed them
    :param nselect: number of selected individuals  
    """
    data = numpy.load(FILE)
    print(f'data = {data}')
    nsample = data.shape[1]

    # indices with the smallest nselect objective function values
    inds = numpy.argpartition(data[1, :], nselect)[:nselect]
    print(f'{nselect} indices giving the smallest f values are: {inds}')

    # ransomly breed nsamples
    indsParentA = numpy.random.choice(inds, (nsample,), replace=True)
    indsParentB = numpy.random.choice(inds, (nsample,), replace=True)
    print(f'combining parents {[(indsParentA[i], indsParentB[i]) for i in range(len(indsParentA))]}')

    newData = 0.5*(data[:, indsParentA] + data[:, indsParentB])
    numpy.save(FILE, newData)



def plot() -> None:
    """
    Plot the last solution
    """
    data = numpy.load(FILE)
    pylab.plot(data[0, :], data[1, :], 'ko')
    i = numpy.argmin(data[1, :])
    xopt, fopt = data[0, i], data[1, :]
    pylab.plot([xopt], [fopt], 'r*')

    pylab.savefig('update.png')



if __name__ == '__main__':
    defopt.run([init, fitness, select_breed, plot])