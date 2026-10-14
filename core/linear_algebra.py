"""
SignatureLab — Linear Algebra Verification Studio
Core Mathematical Engine

Implements vector space operations, inner products (dot product),
Euclidean norms, Euclidean distances, and cosine similarity for
flattened image matrices in R^(mn).
"""

from typing import Dict, Any, Tuple
import numpy as np


def flatten_image_to_vector(image_matrix: np.ndarray) -> np.ndarray:
    """
    Flattens an m x n 2D image matrix into an mn-dimensional column/row vector in R^(mn).
    
    Parameters:
        image_matrix: 2D numpy array of shape (m, n)
        
    Returns:
        1D numpy float64 array of length m*n
    """
    if not isinstance(image_matrix, np.ndarray):
        raise TypeError("Input image must be a numpy ndarray.")
    if image_matrix.ndim != 2:
        raise ValueError(f"Expected 2D image matrix, got shape {image_matrix.shape}")
    
    # Flatten in row-major (C-style) order and cast to float64 for precision
    vector = image_matrix.astype(np.float64).flatten()
    return vector


def dot_product(u: np.ndarray, v: np.ndarray) -> float:
    """
    Computes standard inner product (dot product) of two vectors u, v in R^N:
    <u, v> = u . v = sum_{i=1}^N (u_i * v_i)
    
    Parameters:
        u: 1D numpy array
        v: 1D numpy array
        
    Returns:
        float: dot product value
    """
    u = np.asarray(u, dtype=np.float64)
    v = np.asarray(v, dtype=np.float64)
    
    if u.ndim != 1 or v.ndim != 1:
        raise ValueError("Both inputs must be 1D vectors.")
    if u.shape[0] != v.shape[0]:
        raise ValueError(f"Vector dimensions must match. Got {u.shape[0]} and {v.shape[0]}.")
    if not np.all(np.isfinite(u)) or not np.all(np.isfinite(v)):
        raise ValueError("Vectors contain non-finite numbers (NaN or Inf).")
        
    return float(np.dot(u, v))


def euclidean_norm(u: np.ndarray) -> float:
    """
    Computes Euclidean norm (L2 norm) induced by standard inner product:
    ||u||_2 = sqrt(<u, u>) = sqrt(sum_{i=1}^N u_i^2)
    
    Parameters:
        u: 1D numpy array
        
    Returns:
        float: Euclidean norm (non-negative)
    """
    u = np.asarray(u, dtype=np.float64)
    if u.ndim != 1:
        raise ValueError("Input must be a 1D vector.")
    if not np.all(np.isfinite(u)):
        raise ValueError("Vector contains non-finite numbers (NaN or Inf).")
        
    norm_val = np.linalg.norm(u, ord=2)
    return float(norm_val)


def euclidean_distance(u: np.ndarray, v: np.ndarray) -> float:
    """
    Computes Euclidean distance between two vectors u, v:
    d(u, v) = ||u - v||_2 = sqrt(sum_{i=1}^N (u_i - v_i)^2)
    
    Parameters:
        u: 1D numpy array
        v: 1D numpy array
        
    Returns:
        float: Euclidean distance
    """
    u = np.asarray(u, dtype=np.float64)
    v = np.asarray(v, dtype=np.float64)
    
    if u.shape != v.shape:
        raise ValueError(f"Dimension mismatch for distance: {u.shape} vs {v.shape}")
    if not np.all(np.isfinite(u)) or not np.all(np.isfinite(v)):
        raise ValueError("Vectors contain non-finite numbers (NaN or Inf).")
        
    diff = u - v
    return float(np.linalg.norm(diff, ord=2))


def cosine_similarity(u: np.ndarray, v: np.ndarray, eps: float = 1e-12) -> float:
    """
    Computes Cosine Similarity between two vectors u, v:
    cos(theta) = (u . v) / (||u||_2 * ||v||_2)
    
    Measures the directional alignment of vectors in high-dimensional space,
    invariant to positive scalar multiplication (overall stroke intensity).
    
    Parameters:
        u: 1D numpy array
        v: 1D numpy array
        eps: small epsilon to guard against division by zero
        
    Returns:
        float: Cosine similarity in range [-1.0, 1.0] (or [0.0, 1.0] for non-negative vectors)
    """
    u = np.asarray(u, dtype=np.float64)
    v = np.asarray(v, dtype=np.float64)
    
    if u.shape != v.shape:
        raise ValueError(f"Dimension mismatch: {u.shape} vs {v.shape}")
        
    norm_u = euclidean_norm(u)
    norm_v = euclidean_norm(v)
    
    if norm_u < eps or norm_v < eps:
        raise ValueError(
            "Cannot compute cosine similarity: one or both vectors have zero norm (blank image)."
        )
        
    dot_val = dot_product(u, v)
    denom = norm_u * norm_v
    
    cos_sim = dot_val / denom
    # Clip to theoretical bounds [-1.0, 1.0] to eliminate float precision anomalies
    return float(np.clip(cos_sim, -1.0, 1.0))


def orthogonal_projection(u: np.ndarray, v: np.ndarray, eps: float = 1e-12) -> Tuple[np.ndarray, float]:
    """
    Computes orthogonal projection of vector u onto vector v:
    proj_v(u) = ((u . v) / ||v||^2) * v
    
    Returns:
        Tuple[np.ndarray, float]: (projection vector, projection scalar coordinate)
    """
    v = np.asarray(v, dtype=np.float64)
    u = np.asarray(u, dtype=np.float64)
    
    norm_v = euclidean_norm(v)
    if norm_v < eps:
        raise ValueError("Cannot project onto zero vector.")
        
    scalar_coord = dot_product(u, v) / (norm_v ** 2)
    proj_vector = scalar_coord * v
    return proj_vector, float(scalar_coord)


def full_vector_comparison(u: np.ndarray, v: np.ndarray) -> Dict[str, Any]:
    """
    Computes all linear algebra comparison metrics between two vectors u and v.
    
    Returns a comprehensive dictionary with both exact numerical values
    and step-by-step breakdown data for display and educational explanation.
    """
    u = np.asarray(u, dtype=np.float64)
    v = np.asarray(v, dtype=np.float64)
    
    dim = int(u.shape[0])
    dot_val = dot_product(u, v)
    norm_u = euclidean_norm(u)
    norm_v = euclidean_norm(v)
    dist_val = euclidean_distance(u, v)
    cos_sim = cosine_similarity(u, v)
    
    # Angle theta in radians and degrees
    theta_rad = float(np.arccos(np.clip(cos_sim, -1.0, 1.0)))
    theta_deg = float(np.degrees(theta_rad))
    
    # Normalized Euclidean distance (distance divided by max possible distance given norms)
    # ||u - v||^2 = ||u||^2 + ||v||^2 - 2(u . v)
    max_theoretical_dist = norm_u + norm_v
    norm_dist_ratio = float(dist_val / max_theoretical_dist) if max_theoretical_dist > 0 else 0.0

    return {
        "dimension": dim,
        "dot_product": dot_val,
        "norm_u": norm_u,
        "norm_v": norm_v,
        "euclidean_distance": dist_val,
        "normalized_distance": norm_dist_ratio,
        "cosine_similarity": cos_sim,
        "angle_radians": theta_rad,
        "angle_degrees": theta_deg,
        "product_of_norms": norm_u * norm_v,
    }


def solved_numerical_example() -> Dict[str, Any]:
    """
    Returns the exact solved numerical example required by Section 11 of the syllabus:
    A = (1, 2, 3), B = (2, 3, 4)
    """
    A = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    B = np.array([2.0, 3.0, 4.0], dtype=np.float64)
    
    dot_val = 1 * 2 + 2 * 3 + 3 * 4  # 2 + 6 + 12 = 20
    norm_A = np.sqrt(1**2 + 2**2 + 3**2)  # sqrt(14)
    norm_B = np.sqrt(2**2 + 3**2 + 4**2)  # sqrt(29)
    dist = np.sqrt((1 - 2)**2 + (2 - 3)**2 + (3 - 4)**2)  # sqrt(3)
    cos_sim = 20.0 / (norm_A * norm_B)  # 20 / sqrt(406)
    
    # 2x2 matrix illustration
    M_A = np.array([[10, 20], [30, 40]], dtype=np.float64)
    M_B = np.array([[15, 25], [35, 45]], dtype=np.float64)
    v_A = flatten_image_to_vector(M_A)
    v_B = flatten_image_to_vector(M_B)
    
    matrix_example_metrics = full_vector_comparison(v_A, v_B)
    
    return {
        "vector_A": [1, 2, 3],
        "vector_B": [2, 3, 4],
        "dot_product": dot_val,
        "norm_A": norm_A,
        "norm_A_exact": "√14",
        "norm_B": norm_B,
        "norm_B_exact": "√29",
        "euclidean_distance": dist,
        "euclidean_distance_exact": "√3",
        "cosine_similarity": cos_sim,
        "cosine_similarity_exact": "20 / √406",
        "matrix_2x2_A": M_A.tolist(),
        "matrix_2x2_B": M_B.tolist(),
        "matrix_vector_A": v_A.tolist(),
        "matrix_vector_B": v_B.tolist(),
        "matrix_metrics": matrix_example_metrics,
    }
