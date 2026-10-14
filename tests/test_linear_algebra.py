"""
Unit tests for core.linear_algebra
Validates the mathematical engine, solved numerical examples,
norms, dot products, distances, and edge cases.
"""

import pytest
import numpy as np
from core.linear_algebra import (
    flatten_image_to_vector,
    dot_product,
    euclidean_norm,
    euclidean_distance,
    cosine_similarity,
    orthogonal_projection,
    full_vector_comparison,
    solved_numerical_example,
)


def test_solved_numerical_example_exact_values():
    """
    Validates Section 11 from the prompt:
    A = (1, 2, 3), B = (2, 3, 4)
    A . B = 20
    ||A|| = sqrt(14)
    ||B|| = sqrt(29)
    d(A, B) = sqrt(3) ~= 1.732
    cos(theta) = 20 / sqrt(406) ~= 0.9926
    """
    ex = solved_numerical_example()
    assert ex["dot_product"] == 20.0
    assert pytest.approx(ex["norm_A"], 1e-4) == np.sqrt(14)
    assert pytest.approx(ex["norm_B"], 1e-4) == np.sqrt(29)
    assert pytest.approx(ex["euclidean_distance"], 1e-3) == 1.73205
    assert pytest.approx(ex["cosine_similarity"], 1e-4) == 0.99258


def test_flatten_image_to_vector():
    """
    Validates matrix flattening from R^(m x n) to R^(mn).
    """
    matrix = np.array([[1, 2], [3, 4]], dtype=np.float32)
    vector = flatten_image_to_vector(matrix)
    assert vector.shape == (4,)
    assert np.array_equal(vector, [1, 2, 3, 4])


def test_dot_product_properties():
    """
    Tests symmetry and linearity of dot product.
    """
    u = np.array([2.0, -1.0, 3.0])
    v = np.array([1.0, 4.0, 2.0])
    # Symmetry: u . v == v . u
    assert pytest.approx(dot_product(u, v)) == dot_product(v, u)
    assert pytest.approx(dot_product(u, v)) == (2*1 + (-1)*4 + 3*2) # 2 - 4 + 6 = 4.0


def test_cauchy_schwarz_inequality():
    """
    Verifies Cauchy-Schwarz: |u . v| <= ||u|| * ||v||
    and equality iff u and v are linearly dependent.
    """
    u = np.array([3.0, 4.0, 5.0])
    v = np.array([1.0, 2.0, -1.0])
    dot_uv = dot_product(u, v)
    norm_u = euclidean_norm(u)
    norm_v = euclidean_norm(v)
    assert abs(dot_uv) <= norm_u * norm_v
    
    # Linearly dependent: v = 2 * u -> cos(theta) == 1.0
    v_dep = 2.0 * u
    assert pytest.approx(cosine_similarity(u, v_dep)) == 1.0


def test_orthogonal_vectors():
    """
    Tests orthogonal vectors (perpendicular): dot product is 0, cosine similarity is 0.
    """
    u = np.array([1.0, 0.0])
    v = np.array([0.0, 1.0])
    assert dot_product(u, v) == 0.0
    assert cosine_similarity(u, v) == 0.0
    proj, coord = orthogonal_projection(u, v)
    assert np.allclose(proj, 0.0)
    assert coord == 0.0


def test_dimension_mismatch_raises_error():
    """
    Tests that unequal vector dimensions raise ValueError.
    """
    u = np.array([1.0, 2.0])
    v = np.array([1.0, 2.0, 3.0])
    with pytest.raises(ValueError):
        dot_product(u, v)
    with pytest.raises(ValueError):
        euclidean_distance(u, v)
    with pytest.raises(ValueError):
        cosine_similarity(u, v)


def test_zero_vector_norm_and_cosine():
    """
    Tests zero vector handling.
    """
    z = np.zeros(5)
    u = np.ones(5)
    assert euclidean_norm(z) == 0.0
    with pytest.raises(ValueError):
        cosine_similarity(z, u)
