import defopt
import sympy
import numpy
import glob
import re
from matplotlib import pylab


#OBJFUN_EXPR = '1 + 2*(x-3)**4'
OBJFUN_EXPR = '1 + 0.1*(x-3)**2 - 0.2 * cos((x-3)*2*pi)'
X = sympy.Symbol('x')
#F = sympy.parsing.sympy_parser.parse_expr(OBJFUN_EXPR)


def init(*, xmin: float=0., xmax:float=1., nsample: int=100, id: int=0) -> None:
    """
    Random initialize
    :param xmin: min value of interval to search
    :param xmax: max value of interval to search
    :param nsample: number of samples
    :param id: ID of this instance
    """

    xs = xmin + (xmax - xmin)*numpy.random.rand(nsample)
    print(f'param in the range {min(xs)} - {max(xs)}')

    # evaluate the cost function
    fs = sympy.utilities.lambdify(X, OBJFUN_EXPR, 'numpy')(xs)
    print(f'f in the range {min(fs)} - {max(fs)}')

    data = numpy.empty((2, nsample), numpy.float64)
    data[0, :] = xs
    data[1, :] = fs

    datafile = f'data_id{id:03d}.npy'
    print(f'init: saving data in file {datafile}')
    numpy.save(datafile, data)


def fitness(*, tol: float=1.e-2, it: int=0, id: int=0) -> None:
    """
    Evaluate fitness
    :param tol: cost function tolerance
    :param it: iteration number
    :param id: ID of this instance
    """
    datafile = f'data_id{id:03d}.npy'
    data = numpy.load(datafile)
    datafile = f'data_id{id:03d}_it{it:04d}.npy'
    print(f'fitness: saving data in file {datafile}')
    numpy.save(datafile, data)
    xs = data[0, :]
    std = xs.std()
    if std > tol:
        raise RuntimeError(f"\n\nSpread of parameter is too large: std={std} > {tol}\n\n")


def select_breed(*, nselect: int=10, it: int=0, xmin: float=0., xmax:float=1., ymin: float=0., ymax: float=1.):
    """
    Select candidates with highest score and breed them
    :param nselect: number of selected individuals
    :param it: iteration number
    :param xmin: min x value for plotting
    :param xmax: max x value for plotting
    :param ymin: min y value for plotting
    :param ymax: max y value for plotting
    """
    data_all = []
    nsample_all = []
    id_all = []
    for filename in glob.glob(f'data_id*_it{it:04}.npy'):
        m = re.search(r'data_id(\d+)*_it\d+.npy', filename)
        id = int(m.group(1))
        data = numpy.load(filename)
        nsample_all.append(data.shape[1])
        data_all.append(data)
        id_all.append(id)

    print(f'select_breed: number of ids: {len(data_all)}')
    print(f'select_breed: shape of id 0: {data_all[0].shape}')
    data = numpy.concatenate(data_all, axis=1)
    print(f'select_breed: shape of concatenated array: {data.shape}')
    nsample = data.shape[1]

    # do some plotting
    pylab.plot(data[0,:], data[1,:], 'bx')
    pylab.xlim(xmin, xmax)
    pylab.ylim(ymin, ymax)
    pylab.title(f'it = {it}')
    figfile = f'plot_it{it:04d}.png'
    print(f'plot: saving plot in file {figfile}')
    pylab.savefig(figfile)


    # indices with the smallest nselect objective function values
    inds = numpy.argpartition(data[1, :], nselect)[:nselect]
    print(f'{nselect} indices giving the smallest f values are: {inds}')

    datafile = 'last_selected_data.npy'
    print(f'select_breed: writing file {datafile}')
    numpy.save(datafile, data[:, inds])

    # randomly breed nsample individuals and assign them to different IDs
    n = len(data_all)
    print(f'select_breed: n = {n}')
    for i in range(n):

        # allow for the same member to be chosen multiple times
        indsParentA = numpy.random.choice(inds, (nsample_all[i],), replace=True)
        indsParentB = numpy.random.choice(inds, (nsample_all[i],), replace=True)
    
        print(f'combining parents {[(indsParentA[i], indsParentB[i]) for i in range(len(indsParentA))]}')

        newData = 0.5*(data[:, indsParentA] + data[:, indsParentB])

        datafile = f'data_id{id_all[i]:03d}_it{it:04d}.npy'
        print(f'select_breed: saving data in file {datafile}')
        numpy.save(datafile, newData)

        ## this file will be read by fitness...
        datafile = f'data_id{id_all[i]:03d}.npy'
        print(f'select_breed: saving data in file {datafile}')
        numpy.save(datafile, newData)



def plot(*, xmin: float=0., xmax:float=1., ymin: float=0., ymax: float=1.) -> None:
    """
    Plot the last solution
    :param xmin: min x value for plotting
    :param xmax: max x value for plotting
    :param ymin: min y value for plotting
    :param ymax: max y value for plotting
    """

    # final
    data = numpy.load('last_selected_data.npy')

    pylab.figure()
    pylab.plot(data[0, :], data[1, :], 'cx')
    i = numpy.argmin(data[1, :])
    xopt, fopt = data[0, i], data[1, i]
    print(f'best solution is {xopt}, giving f = {fopt}')
    pylab.plot([xopt], [fopt], 'r*')
    pylab.savefig('update.png')



if __name__ == '__main__':
    defopt.run([init, fitness, select_breed, plot])