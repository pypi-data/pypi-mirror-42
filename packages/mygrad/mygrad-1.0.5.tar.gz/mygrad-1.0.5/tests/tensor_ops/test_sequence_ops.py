from mygrad.tensor_base import Tensor
from mygrad import multiply_sequence, add_sequence
from numpy.testing import assert_allclose


def test_seq_add():
    a = Tensor(3)
    b = Tensor([1, 2, 3])
    c = Tensor([[1, 2, 3], [2, 3, 4]])
    f = add_sequence(a, b, c, constant=False)
    f.sum().backward()

    a1 = Tensor(3)
    b1 = Tensor([1, 2, 3])
    c1 = Tensor([[1, 2, 3], [2, 3, 4]])
    f1 = a1 + b1 + c1
    f1.sum().backward()

    assert_allclose(f.data, f1.data)
    assert_allclose(f.grad, f1.grad)
    assert_allclose(a.grad, a1.grad)
    assert_allclose(b.grad, b1.grad)
    assert_allclose(c.grad, c1.grad)


def test_seq_mult():
    a = Tensor(3.)
    b = Tensor([1., 2., 3.])
    c = Tensor([[1., 2., 3.], [2., 3., 4.]])
    f = multiply_sequence(a, b, c, constant=False)
    f.sum().backward()

    a1 = Tensor(3.)
    b1 = Tensor([1., 2., 3.])
    c1 = Tensor([[1., 2., 3.], [2., 3., 4.]])
    f1 = a1 * b1 * c1
    f1.sum().backward()

    assert_allclose(f.data, f1.data)
    assert_allclose(f.grad, f1.grad)
    assert_allclose(a.grad, a1.grad)
    assert_allclose(b.grad, b1.grad)
    assert_allclose(c.grad, c1.grad)
