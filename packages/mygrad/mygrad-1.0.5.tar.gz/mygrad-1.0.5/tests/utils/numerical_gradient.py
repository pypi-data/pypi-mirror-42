from decimal import Decimal

import numpy as np
from typing import Tuple, List, Optional

from mygrad._utils import reduce_broadcast


def to_decimal_array(arr):
    """ Convert numpy ND-array to Decimal-type object array of the same shape.
        Used for facilitating high-precision arithmetic.

        Parameters
        ----------
        arr : Union[float, numpy.ndarray]

        Returns
        -------
        numpy.ndarray
            Decimal-type object array"""
    arr = np.asarray(arr)

    if arr.dtype.kind == "O":
        return arr
    return np.array(tuple(Decimal(float(i)) for i in arr.flat), dtype=Decimal).reshape(arr.shape)


def numerical_gradient(f, *args, back_grad, vary_ind=None,
                       h=Decimal(1)/Decimal(int(1e8)),
                       as_decimal=True, kwargs=None):
    """ Computes numerical partial derivatives of f(x0, x1, ...) in each
        of its variables, using the central difference method.
        This is a "fast" method - it varies entire arrays at once. Thus
        this is only appropriate for trivial vectorized functions that
        map accross entries of arrays (like add or multiply). E.g.
        matrix multiplication is *not* suited for this style of gradient.

        Parameters
        ----------
        f : Callable[[numpy.ndarray, ...], numpy.ndarray]
            f(x, ...) -> numpy.ndarray
        *args : Tuple[numpy.ndarray, ...]
            The input arguments to be fed to f.

        back_grad : numpy.ndarray
            The gradient being back-propagated to x and y, via f

        vary_ind : Optional[Tuple[int, ...]]
            If `None`, the partials of f with respect to all the inputs are.
            computed. Otherwise you can specify a sequence of the indices
            of the variables whose partials are to be computed
               0 -> w.r.t x only, 1 -> w.r.t y only, etc.

        h : float, optional, (default=Decimal(1E-8))
            Approximating infinitesimal.

        as_decimal : bool, optional (default=True)
            If True, f's arguments are passed as Decimal-type arrays. This
            improves numerical precision, but is not permitted by some functions.

        kwargs : Optional[Dict]

        Returns
        -------
        Tuple[Union[NoneType, numpy.ndarray], ...]
            df/dx0, df/dx1, ... - evaluated at (`x0`, `x1`, ... ).
        """

    if kwargs is None:
        kwargs = {}

    if not args:
        raise ValueError("At least one value must be passed to `args`")

    h = Decimal(h) if as_decimal else float(h)
    two_h = Decimal(2)*h if as_decimal else 2*h

    args = tuple(to_decimal_array(i) if as_decimal else i for i in args)

    grads = [None]*len(args)

    def gen_fwd_diff(i):
        # x1, ..., x_i + h, ..., xn
        return ((var if j != i else var + h) for j, var in enumerate(args))

    def gen_bkwd_diff(i):
        # x1, ..., x_i - h, ..., xn
        return ((var if j != i else var - h) for j, var in enumerate(args))

    for n in range(len(args)):
        if vary_ind is not None and n not in vary_ind:
            continue
        # central difference in variable n
        dvar = (f(*gen_fwd_diff(n), **kwargs) - f(*gen_bkwd_diff(n), **kwargs)) / (two_h)
        grads[n] = reduce_broadcast(back_grad * dvar.astype(float), args[n].shape)

    return grads


def numerical_gradient_full(f, *args, back_grad, as_decimal=True, kwargs=None, vary_ind=None) -> Tuple[np.ndarray, ...]:
    """ Computes numerical partial derivatives of f(x, y, ..., **kwargs), by
        varying each entry of x, y, ... independently producing a gradient
        in each variable.

        Parameters
        ----------
        f : Callable[[numpy.ndarray, ...], numpy.ndarray]
            f(x, ...) -> numpy.ndarray

        *args : numpy.ndarray
            The array(s) to be passed to f

        back_grad : numpy.ndarray
            The gradient being back-propagated to {x}, via f

        as_decimal : bool, optional (default=True)
            If True, f's arguments are passed as Decimal-type arrays. This
            improves numerical precision, but is not permitted by some functions.

        kwargs : Dict[str, Any], optional (default=dict())
            The keyword arguments to be passed to f.

        vary_ind : Optional[Tuple[int, ...]]
            If `None`, the partials of f with respect to all the inputs are.
            computed. Otherwise you can specify a sequence of the indices
            of the variables whose partials are to be computed
               0 -> w.r.t x only, 1 -> w.r.t y only, etc.

        Returns
        -------
        Tuple[numpy.ndarray, ...]
            df/dx, df/dy, ...
            df/dvar will be None if var was excluded via `vary_ind`
        """
    if kwargs is None:
        kwargs = {}

    args = tuple(to_decimal_array(i) if as_decimal else i for i in args)
    grads = [None] * len(args)  # type: List[Optional[np.ndarray]]
    if isinstance(vary_ind, int):
        vary_ind = [vary_ind]

    for n in range(len(args)):
        if vary_ind is not None and n not in vary_ind:
            continue

        def tmp_f(var: np.ndarray) -> np.ndarray:
            return f(*args[:n], var, *args[n+1:], **kwargs)

        grads[n] = _numerical_gradient_full(tmp_f,
                                            x=args[n],
                                            back_grad=back_grad,
                                            as_decimal=as_decimal)
    return tuple(grads)


def _numerical_gradient_full(f, *, x, back_grad, h=Decimal(1)/Decimal(int(1e8)), as_decimal=True):
    """ Computes numerical partial derivatives of f(x), by
        varying each entry of `x` independently.

        Parameters
        ----------
        f : Callable[[numpy.ndarray], numpy.ndarray]
            f(x) -> numpy.ndarray

        x : numpy.ndarray
            An array storing the sequence(s) of values in the array. More than once
            sequence may be designated, according to the `axis` argument of `f`.

        back_grad : numpy.ndarray
            The gradient being back-propagated to {x}, via f

        h : float, optional, (default=Decimal(1E-8))
            Approximating infinitesimal.

        as_decimal : bool, optional (default=True)
            If True, x is passed to f as a Decimal-type array. This
            improves numerical precision, but is not permitted by some functions.

        Returns
        -------
        numpy.ndarray
            df/dx
        """

    grad = np.empty_like(x)
    x = to_decimal_array(x)
    x_orig = np.copy(x)
    h = Decimal(h)
    back_grad = to_decimal_array(back_grad)

    for ind, val in np.ndenumerate(x):
        x_fwd = x
        x_fwd[ind] = x_orig[ind] + h
        f_fwd = to_decimal_array(f(x_fwd) if as_decimal else f(x_fwd.astype(np.float64)))

        x_bkwd = np.copy(x_fwd)
        x_bkwd[ind] = x_orig[ind] - h
        f_bkwd = to_decimal_array(f(x_bkwd) if as_decimal else f(x_bkwd.astype(np.float64)))

        df_dxi = to_decimal_array((f_fwd - f_bkwd) / (Decimal(2) * h))

        dl_dxi = (df_dxi * back_grad)
        grad[ind] = np.float64(dl_dxi.sum() if isinstance(dl_dxi, np.ndarray) else dl_dxi)

        # reset x
        x[ind] = x_orig[ind]
    return grad.astype(np.float64)
