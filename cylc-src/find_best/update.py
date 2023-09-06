import defopt
import sympy
import random
import numpy


OBJFUN_EXPR = '1 + 2*(x-3)**4'


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
    xa = numpy.load(paramfilea, allow_pickle=True)
    xb = numpy.load(paramfileb, allow_pickle=True)
    # mix the two values
    x0 = 0.5*(xa + xb)
    xnew = update(x0, objfun_expr=OBJFUN_EXPR)
    numpy.save(outfile, xnew)



if __name__ == '__main__':
    defopt.run([init, merge])