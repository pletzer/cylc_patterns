import defopt
import sympy
import random
import numpy
import glob
import re
from matplotlib import pylab


#OBJFUN_EXPR = '1 + 2*(x-3)**4'
OBJFUN_EXPR = '1 + 0.1*(x-3)**2 - 0.2 * cos((x-3)*2*pi)'

def update(x0, objfun_expr) -> float:
    x = sympy.Symbol('x')
    f = sympy.parsing.sympy_parser.parse_expr(objfun_expr)
    deriv = sympy.diff(f, x)
    deriv2 = sympy.diff(deriv, x)
    fpp = deriv2.evalf(subs={x: x0})
    fp = deriv.evalf(subs={x: x0})
    xnew = x0 - fp/fpp
    print(f'old param: {x0} fp: {fp} fpp: {fpp} new param: {xnew}')
    return xnew


def init(*, a: float=0., b:float=1., outfile: str) -> None:
    """
    Random initialize and update
    :param a: min value of interval to search
    :param b: max value of interval to search
    :param outfile: output file storing the new param value 
    """
    x0 = a + (b - a)*random.random()
    xnew = update(x0, objfun_expr=OBJFUN_EXPR)
    numpy.save(outfile, xnew)


def merge(paramfilea: str, paramfileb: str, *, outfile: str) -> None:
    """
    Merge and update
    param: paramfilea: first parameter file
    param: paramfileb: second parameter file
    :param outfile: output file storing the new param value     
    """
    # numpy.load returns an array object
    xa = float(numpy.load(paramfilea, allow_pickle=True))
    xb = float(numpy.load(paramfileb, allow_pickle=True))
    x = sympy.Symbol('x')
    f = sympy.parsing.sympy_parser.parse_expr(OBJFUN_EXPR)
    fa = f.evalf(subs={x: xa})
    fb = f.evalf(subs={x: xb})
    # mix the two values, assumes fa & fb > 0
    x0 = (fb*xa + fa*xb)/(fa + fb)
    xnew = update(x0, objfun_expr=OBJFUN_EXPR)
    numpy.save(outfile, xnew)


def plot(*, directory: str='./', outfile: str='update.png') -> None:
    """
    Plot the search
    :param directory: directory where the params output files reside
    :param outfile: output png file
    """
    xvals = {}
    yvals = {}
    xmin = float('inf')
    xmax = - float('inf')

    x = sympy.Symbol('x')
    f = sympy.parsing.sympy_parser.parse_expr(OBJFUN_EXPR)

    for filename in glob.glob(directory + '/params*.npy'):
        # extract the level and instance
        m = re.search(r'params(\d+)\_(\d+)', filename)
        level, i = int(m.group(1)), int(m.group(2))
        # read the param 
        xi = float(numpy.load(filename, allow_pickle=True))
        fi = f.evalf(subs={x: xi})
        xvals[level] = xvals.get(level, []) + [xi]
        yvals[level] = yvals.get(level, []) + [fi]
        if xi < xmin:
            xmin = xi
        if xi > xmax:
            xmax = xi

    xvals2 = numpy.linspace(xmin, xmax, 100)
    fvals2 = sympy.utilities.lambdify(x, OBJFUN_EXPR, 'numpy')(xvals2)
    pylab.plot(xvals2, fvals2, 'b-')

    nlevels = max(xvals.keys()) + 1
    for level in range(nlevels):
        xnorm = level/float(nlevels)
        clr = (1 - xnorm, xnorm, 0.) #numpy.sin(xnorm*numpy.pi)**2)
        pylab.plot(xvals[level], yvals[level], color=clr, marker='+', linestyle='None')

    pylab.savefig(outfile)



if __name__ == '__main__':
    defopt.run([init, merge, plot])