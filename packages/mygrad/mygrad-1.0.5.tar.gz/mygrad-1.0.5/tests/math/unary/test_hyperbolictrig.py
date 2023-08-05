from tests.wrappers.uber import fwdprop_test_factory, backprop_test_factory
from mygrad import sinh, cosh, tanh, csch, sech, coth

import numpy as np


def _is_nonzero(x):
    return np.all(np.abs(x.data) > 1e-8)


@fwdprop_test_factory(mygrad_func=sinh, true_func=np.sinh,
                      index_to_bnds={0: (-10, 10)}, num_arrays=1)
def test_sinh_fwd():
    pass


@backprop_test_factory(mygrad_func=sinh, true_func=np.sinh,
                       index_to_bnds={0: (-10, 10)}, num_arrays=1, as_decimal=False)
def test_sinh_backward():
    pass


@fwdprop_test_factory(mygrad_func=cosh, true_func=np.cosh, index_to_bnds={0: (-10, 10)}, num_arrays=1)
def test_cosh_fwd():
    pass


@backprop_test_factory(mygrad_func=cosh, true_func=np.cosh,
                       index_to_bnds={0: (-10, 10)}, atol=1e-5, num_arrays=1, as_decimal=False)
def test_cosh_backward():
    pass


@fwdprop_test_factory(mygrad_func=tanh, true_func=np.tanh, index_to_bnds={0: (-10, 10)}, num_arrays=1)
def test_tanh_fwd():
    pass


@backprop_test_factory(mygrad_func=tanh, true_func=np.tanh,
                       index_to_bnds={0: (-10, 10)}, atol=1e-5, num_arrays=1, as_decimal=False)
def test_tanh_backward():
    pass


@fwdprop_test_factory(mygrad_func=csch, true_func=lambda x: 1 / np.sinh(x), index_to_bnds={0: (.001, 10)}, num_arrays=1)
def test_csch_fwd():
    pass


@backprop_test_factory(mygrad_func=csch, true_func=lambda x: 1 / np.sinh(x),
                       index_to_bnds={0: (.001, 10)}, num_arrays=1, as_decimal=False)
def test_csch_backward():
    pass


@fwdprop_test_factory(mygrad_func=sech, true_func=lambda x: 1 / np.cosh(x),
                      index_to_bnds={0: (-10, 10)}, num_arrays=1)
def test_sech_fwd():
    pass


@backprop_test_factory(mygrad_func=sech, true_func=lambda x: 1 / np.cosh(x),
                       index_to_bnds={0: (.001, 10)}, atol=1e-5, num_arrays=1, as_decimal=False)
def test_sech_backward():
    pass


@fwdprop_test_factory(mygrad_func=coth, true_func=lambda x: 1 / np.tanh(x),
                      index_to_bnds={0: (-10, 10)}, assumptions=_is_nonzero, num_arrays=1)
def test_coth_fwd():
    pass


@backprop_test_factory(mygrad_func=coth, true_func=lambda x: 1 / np.tanh(x),
                       index_to_bnds={0: (.001, 10)},
                       atol=1e-5, num_arrays=1, as_decimal=False)
def test_coth_backward():
    pass
