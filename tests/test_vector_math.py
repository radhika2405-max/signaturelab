"""
Unit tests for src.vector_math
Explicitly verifies:
1. Identical vectors
2. Different vectors
3. Orthogonal vectors
4. Zero vectors
5. Unequal vector dimensions
6. Dot-product calculations
7. Norm calculations
8. Euclidean-distance calculations
9. Cosine-similarity calculations
And hand-calculated expected values for A=(1,2,3), B=(2,3,4) + Eigendecomposition.
"""

import pytest
import numpy as np
from src.vector_math import (
    flatten_image_to_vector,
    vector_addition,
    scalar_multiplication,
    dot_product,
    euclidean_norm,
    euclidean_distance,
    cosine_similarity,
    orthogonal_projection,
    full_vector_comparison,
    compute_eigenspace_decomposition,
    solved_numerical_example,
)


def test_hand_calculated_worked_example():
    """
    Verifies Section 11 & Section 21 exact hand-calculated values:
    A = (1, 2, 3), B = (2, 3, 4)
    Dot product: 20
    Norm A: sqrt(14)
    Norm B: sqrt(29)
    Distance: sqrt(3) ~= 1.73205
    Cosine similarity: 20 / sqrt(406) ~= 0.99258
    """
    res = solved_numerical_example()
    assert res["dot_product"] == 20.0
    assert pytest.approx(res["norm_A"], 1e-4) == np.sqrt(14)
    assert pytest.approx(res["norm_B"], 1e-4) == np.sqrt(29)
    assert pytest.approx(res["euclidean_distance"], 1e-3) == 1.73205
    assert pytest.approx(res["cosine_similarity"], 1e-4) == 0.99258


def test_1_identical_vectors():
    """Requirement 1: Identical vectors."""
    u = np.array([3.0, 4.0, 5.0])
    v = np.array([3.0, 4.0, 5.0])
    assert euclidean_distance(u, v) == 0.0
    assert pytest.approx(cosine_similarity(u, v)) == 1.0
    assert pytest.approx(dot_product(u, v)) == euclidean_norm(u) ** 2


def test_2_different_vectors():
    """Requirement 2: Different vectors."""
    u = np.array([1.0, 2.0, 0.0])
    v = np.array([0.0, 2.0, 3.0])
    assert euclidean_distance(u, v) > 0.0
    sim = cosine_similarity(u, v)
    assert 0.0 < sim < 1.0


def test_3_orthogonal_vectors():
    """Requirement 3: Orthogonal vectors."""
    u = np.array([1.0, 0.0, 0.0])
    v = np.array([0.0, 5.0, 0.0])
    assert dot_product(u, v) == 0.0
    assert cosine_similarity(u, v) == 0.0
    proj, coord = orthogonal_projection(u, v)
    assert np.allclose(proj, 0.0)
    assert coord == 0.0


def test_4_zero_vectors():
    """Requirement 4: Zero vectors."""
    z = np.zeros(4)
    assert euclidean_norm(z) == 0.0
    u = np.ones(4)
    with pytest.raises(ValueError):
        cosine_similarity(z, u)
    with pytest.raises(ValueError):
        orthogonal_projection(u, z)


def test_5_unequal_vector_dimensions():
    """Requirement 5: Unequal vector dimensions."""
    u = np.array([1.0, 2.0])
    v = np.array([1.0, 2.0, 3.0])
    with pytest.raises(ValueError):
        dot_product(u, v)
    with pytest.raises(ValueError):
        euclidean_distance(u, v)
    with pytest.raises(ValueError):
        cosine_similarity(u, v)
    with pytest.raises(ValueError):
        vector_addition(u, v)


def test_6_dot_product_calculations():
    """Requirement 6: Dot-product calculations."""
    u = np.array([2.0, -3.0, 4.0])
    v = np.array([5.0, 1.0, 2.0])
    # 2*5 + (-3)*1 + 4*2 = 10 - 3 + 8 = 15
    assert dot_product(u, v) == 15.0


def test_7_norm_calculations():
    """Requirement 7: Norm calculations."""
    u = np.array([3.0, 4.0])
    # sqrt(3^2 + 4^2) = 5.0
    assert euclidean_norm(u) == 5.0


def test_8_euclidean_distance_calculations():
    """Requirement 8: Euclidean-distance calculations."""
    u = np.array([1.0, 1.0])
    v = np.array([4.0, 5.0])
    # sqrt((4-1)^2 + (5-1)^2) = sqrt(9 + 16) = 5.0
    assert euclidean_distance(u, v) == 5.0


def test_9_cosine_similarity_calculations():
    """Requirement 9: Cosine-similarity calculations."""
    u = np.array([1.0, 1.0])
    v = np.array([2.0, 0.0])
    # u . v = 2, ||u|| = sqrt(2), ||v|| = 2 -> cos = 2 / (2*sqrt(2)) = 1/sqrt(2) ~= 0.7071
    assert pytest.approx(cosine_similarity(u, v), 1e-4) == 1.0 / np.sqrt(2)


def test_vector_space_operations():
    """Tests vector addition and scalar multiplication."""
    u = np.array([1.0, 2.0])
    v = np.array([3.0, 4.0])
    assert np.array_equal(vector_addition(u, v), [4.0, 6.0])
    assert np.array_equal(scalar_multiplication(2.5, u), [2.5, 5.0])


def test_eigenspace_decomposition():
    """Tests eigenvalue decomposition and PCA on vector matrix."""
    X = np.array([
        [1.0, 2.0, 3.0, 4.0],
        [2.0, 3.0, 4.0, 5.0],
        [1.5, 2.5, 3.5, 4.5]
    ])
    res = compute_eigenspace_decomposition(X, n_components=2)
    assert res["num_samples"] == 3
    assert len(res["eigenvalues"]) == 2
    assert res["eigenvalues"][0] >= res["eigenvalues"][1]
    assert len(res["eigenvectors"]) == 2
