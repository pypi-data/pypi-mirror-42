# This file is part of the pyMOR project (http://www.pymor.org).
# Copyright 2013-2018 pyMOR developers and contributors. All rights reserved.
# License: BSD 2-Clause License (http://opensource.org/licenses/BSD-2-Clause)

import numpy as np

from pymor.algorithms.basic import almost_equal
from pymor.algorithms.gram_schmidt import gram_schmidt, gram_schmidt_biorth
from pymortests.fixtures.operator import operator_with_arrays_and_products
from pymortests.fixtures.vectorarray import vector_array, vector_array_without_reserve


def test_gram_schmidt(vector_array):
    U = vector_array

    V = U.copy()
    onb = gram_schmidt(U, copy=True)
    assert np.all(almost_equal(U, V))
    assert np.allclose(onb.dot(onb), np.eye(len(onb)))
    assert np.all(almost_equal(U, onb.lincomb(U.dot(onb)), rtol=1e-13))

    onb2 = gram_schmidt(U, copy=False)
    assert np.all(almost_equal(onb, onb2))
    assert np.all(almost_equal(onb, U))


def test_gram_schmidt_with_product(operator_with_arrays_and_products):
    _, _, U, _, p, _ = operator_with_arrays_and_products

    V = U.copy()
    onb = gram_schmidt(U, product=p, copy=True)
    assert np.all(almost_equal(U, V))
    assert np.allclose(p.apply2(onb, onb), np.eye(len(onb)))
    assert np.all(almost_equal(U, onb.lincomb(p.apply2(U, onb)), rtol=1e-13))

    onb2 = gram_schmidt(U, product=p, copy=False)
    assert np.all(almost_equal(onb, onb2))
    assert np.all(almost_equal(onb, U))


def test_gram_schmidt_biorth(vector_array):
    U = vector_array
    if U.dim < 2:
        return
    l = len(U) // 2
    l = min((l, U.dim - 1))
    if l < 1:
        return
    U1 = U[:l].copy()
    U2 = U[l:2 * l].copy()

    V1 = U1.copy()
    V2 = U2.copy()
    A1, A2 = gram_schmidt_biorth(U1, U2, copy=True)
    assert np.all(almost_equal(U1, V1))
    assert np.all(almost_equal(U2, V2))
    assert np.allclose(A2.dot(A1), np.eye(len(A1)))
    c = np.linalg.cond(A1.to_numpy()) * np.linalg.cond(A2.to_numpy())
    assert np.all(almost_equal(U1, A1.lincomb(U1.dot(A2)), rtol=c * 1e-14))
    assert np.all(almost_equal(U2, A2.lincomb(U2.dot(A1)), rtol=c * 1e-14))

    B1, B2 = gram_schmidt_biorth(U1, U2, copy=False)
    assert np.all(almost_equal(A1, B1))
    assert np.all(almost_equal(A2, B2))
    assert np.all(almost_equal(A1, U1))
    assert np.all(almost_equal(A2, U2))


def test_gram_schmidt_biorth_with_product(operator_with_arrays_and_products):
    _, _, U, _, p, _ = operator_with_arrays_and_products
    if U.dim < 2:
        return
    l = len(U) // 2
    l = min((l, U.dim - 1))
    if l < 1:
        return
    U1 = U[:l].copy()
    U2 = U[l:2 * l].copy()

    V1 = U1.copy()
    V2 = U2.copy()
    A1, A2 = gram_schmidt_biorth(U1, U2, product=p, copy=True)
    assert np.all(almost_equal(U1, V1))
    assert np.all(almost_equal(U2, V2))
    assert np.allclose(p.apply2(A2, A1), np.eye(len(A1)))
    c = np.linalg.cond(A1.to_numpy()) * np.linalg.cond(p.apply(A2).to_numpy())
    assert np.all(almost_equal(U1, A1.lincomb(p.apply2(U1, A2)), rtol=c * 1e-14))
    assert np.all(almost_equal(U2, A2.lincomb(p.apply2(U2, A1)), rtol=c * 1e-14))

    B1, B2 = gram_schmidt_biorth(U1, U2, product=p, copy=False)
    assert np.all(almost_equal(A1, B1))
    assert np.all(almost_equal(A2, B2))
    assert np.all(almost_equal(A1, U1))
    assert np.all(almost_equal(A2, U2))
