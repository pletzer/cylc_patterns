import defopt
import sympy
import numpy
import glob
import re
from matplotlib import pylab


#OBJFUN_EXPR = '1 + 2*(x-3)**4'
OBJFUN_EXPR = '1 + 0.1*(x-3)**2 - 0.2 * cos((x-3)*2*pi)'
FILE = 'data.npy'
X = sympy.Symbol('x')
#F = sympy.parsing.sympy_parser.parse_expr(OBJFUN_EXPR)


def init(*, xmin: float=0., xmax:float=1., nsample: int=100) -> None:
    """
    Random initialize
    :param xmin: min value of interval to search
    :param xmax: max value of interval to search
    :param nsample: number of samples 
    """

    xs = xmin + (xmax - xmin)*numpy.random.rand(nsample)
    print(f'param in the range {min(xs)} - {max(xs)}')

    # evaluate the cost function
    fs = sympy.utilities.lambdify(X, OBJFUN_EXPR, 'numpy')(xs)
    print(f'f in the range {min(fs)} - {max(fs)}')

    data = numpy.empty((2, nsample), numpy.float64)
    data[0, :] = xs
    data[1, :] = fs

    numpy.save(FILE, data)


def fitness(*, tol: float=1.e-2, it: int=0) -> None:
    """
    Evaluate fitness
    :param tol: cost function tolerance
    :param it: iteration number
    """
    data = numpy.load(FILE)
    numpy.save(f'data{it:04d}.npy', data)
    xs = data[0, :]
    std = xs.std()
    if std > tol:
        raise RuntimeError(f"\n\nSpread of parameter is too large: std={std} > {tol}\n\n")



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



def plot(*, xmin: float=0., xmax:float=1., ymin: float=0., ymax: float=1.) -> None:
    """
    Plot the last solution
    :param xmin: min x value for plotting
    :param xmax: max x value for plotting
    :param ymin: min y value for plotting
    :param ymax: max y value for plotting
    """
    for filename in glob.glob('data*.npy'):
        # extract the iteration number
        m = re.search(r'data(\d+).npy', filename)
        if m:
            it = int(m.group(1))
            print(f'loading file {filename}')
            data = numpy.load(filename)
            pylab.figure()
            pylab.plot(data[0, :], data[1, :], 'bo')
            pylab.xlim(xmin, xmax)
            pylab.ylim(ymin, ymax)
            pylab.title(f'iteration {it}')
            pylab.savefig(f'update{it:04d}.png')
    # final
    data = numpy.load(FILE)
    pylab.figure()
    pylab.plot(data[0, :], data[1, :], 'cx')
    i = numpy.argmin(data[1, :])
    xopt, fopt = data[0, i], data[1, i]
    print(f'best solution is {xopt}, giving f = {fopt}')
    pylab.plot([xopt], [fopt], 'r*')
    pylab.savefig('update.png')



if __name__ == '__main__':
    defopt.run([init, fitness, select_breed, plot])