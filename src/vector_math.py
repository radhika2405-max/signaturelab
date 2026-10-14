"""
SignatureLab — Vector Math & Linear Algebra Engine
Implements Vector Spaces (Unit 1), Linear Maps (Unit 2), and Inner Product Spaces & Eigendecompositions (Unit 3).
"""

from typing import Dict, Any, Tuple, List, Optional
import numpy as np


def flatten_image_to_vector(image_matrix: np.ndarray) -> np.ndarray:
    """
    Unit 1: Maps an m x n matrix M in M_{m,n}(R) isomorphically into R^(mn).
    """
    if not isinstance(image_matrix, np.ndarray):
        raise TypeError("Input must be a numpy ndarray.")
    if image_matrix.ndim != 2:
        raise ValueError(f"Expected 2D matrix, got shape {image_matrix.shape}")
        
    return image_matrix.astype(np.float64).flatten()


def vector_addition(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    """
    Unit 1: Entrywise vector addition in R^N: (u + v)_i = u_i + v_i.
    """
    u = np.asarray(u, dtype=np.float64)
    v = np.asarray(v, dtype=np.float64)
    if u.shape != v.shape:
        raise ValueError(f"Dimension mismatch in vector addition: {u.shape} vs {v.shape}")
    return u + v


def scalar_multiplication(alpha: float, u: np.ndarray) -> np.ndarray:
    """
    Unit 1: Scalar multiplication in R^N: (alpha * u)_i = alpha * u_i.
    """
    u = np.asarray(u, dtype=np.float64)
    return float(alpha) * u


def dot_product(u: np.ndarray, v: np.ndarray) -> float:
    """
    Unit 3: Standard Euclidean inner product in R^N:
    <u, v> = u . v = sum_{i=1}^N (u_i * v_i)
    """
    u = np.asarray(u, dtype=np.float64)
    v = np.asarray(v, dtype=np.float64)
    
    if u.ndim != 1 or v.ndim != 1:
        raise ValueError("Inputs to dot_product must be 1D vectors.")
    if u.shape[0] != v.shape[0]:
        raise ValueError(f"Vector dimensions must match. Got {u.shape[0]} and {v.shape[0]}.")
    if not np.all(np.isfinite(u)) or not np.all(np.isfinite(v)):
        raise ValueError("Vectors contain non-finite numbers (NaN or Inf).")
        
    return float(np.dot(u, v))


def euclidean_norm(u: np.ndarray) -> float:
    """
    Unit 3: Euclidean norm induced by inner product:
    ||u||_2 = sqrt(<u, u>) = sqrt(sum_{i=1}^N u_i^2)
    """
    u = np.asarray(u, dtype=np.float64)
    if u.ndim != 1:
        raise ValueError("Input must be a 1D vector.")
    if not np.all(np.isfinite(u)):
        raise ValueError("Vector contains non-finite numbers (NaN or Inf).")
        
    return float(np.linalg.norm(u, ord=2))


def euclidean_distance(u: np.ndarray, v: np.ndarray) -> float:
    """
    Unit 3: Euclidean distance metric:
    d(u, v) = ||u - v||_2 = sqrt(sum_{i=1}^N (u_i - v_i)^2)
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
    Unit 3: Cosine Similarity measuring directional alignment:
    cos(theta) = (u . v) / (||u||_2 * ||v||_2)
    """
    u = np.asarray(u, dtype=np.float64)
    v = np.asarray(v, dtype=np.float64)
    
    if u.shape != v.shape:
        raise ValueError(f"Dimension mismatch: {u.shape} vs {v.shape}")
        
    norm_u = euclidean_norm(u)
    norm_v = euclidean_norm(v)
    
    if norm_u < eps or norm_v < eps:
        raise ValueError(
            "Cannot compute cosine similarity: one or both vectors have zero norm (zero vector / blank image)."
        )
        
    dot_val = dot_product(u, v)
    denom = norm_u * norm_v
    cos_val = dot_val / denom
    return float(np.clip(cos_val, -1.0, 1.0))


def orthogonal_projection(u: np.ndarray, v: np.ndarray, eps: float = 1e-12) -> Tuple[np.ndarray, float]:
    """
    Unit 2 & 3: Orthogonal projection of vector u onto vector v:
    proj_v(u) = ((u . v) / ||v||^2) * v
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
    Computes all linear algebra metrics between vectors u and v.
    """
    u = np.asarray(u, dtype=np.float64)
    v = np.asarray(v, dtype=np.float64)
    
    dim = int(u.shape[0])
    dot_val = dot_product(u, v)
    norm_u = euclidean_norm(u)
    norm_v = euclidean_norm(v)
    dist_val = euclidean_distance(u, v)
    cos_sim = cosine_similarity(u, v)
    
    theta_rad = float(np.arccos(np.clip(cos_sim, -1.0, 1.0)))
    theta_deg = float(np.degrees(theta_rad))
    
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


def compute_eigenspace_decomposition(
    vectors_matrix: np.ndarray,
    n_components: int = 3
) -> Dict[str, Any]:
    """
    Unit 3: Genuinely implemented Eigenvalue & Eigenvector Decomposition (Section 12, Unit 3).
    Computes sample covariance matrix C = (1/N) * X_centered^T * X_centered
    and solves the characteristic eigenvalue equation:
        C * v_k = lambda_k * v_k
    
    Parameters:
        vectors_matrix: 2D array of shape (num_samples, num_features)
        n_components: number of top eigenvectors/eigenspaces to extract
        
    Returns:
        Dict with eigenvalues, eigenvectors, explained_variance_ratio, and mean_vector.
    """
    X = np.asarray(vectors_matrix, dtype=np.float64)
    if X.ndim != 2:
        raise ValueError("Input must be a 2D matrix of samples x features.")
    num_samples, num_features = X.shape
    if num_samples < 2:
        raise ValueError("At least 2 samples required to compute covariance matrix and eigenvalues.")
        
    # Center vectors
    mean_vec = np.mean(X, axis=0)
    X_centered = X - mean_vec
    
    # Dual covariance method for high-dimensional efficiency (num_features >> num_samples):
    # Small matrix K = (1 / (num_samples - 1)) * (X_centered @ X_centered.T)
    K = np.dot(X_centered, X_centered.T) / (num_samples - 1)
    
    eigenvalues_K, eigenvectors_K = np.linalg.eigh(K)
    
    # Sort eigenvalues in descending order
    idx = np.argsort(eigenvalues_K)[::-1]
    eigenvalues = np.maximum(eigenvalues_K[idx], 0.0) # Clip numerical precision noise
    
    # Reconstruct feature-space eigenvectors: V = X_centered^T @ eigenvectors_K
    eigenvectors = []
    for i in range(min(n_components, len(idx))):
        val = eigenvalues[i]
        if val > 1e-10:
            vec_k = np.dot(X_centered.T, eigenvectors_K[:, idx[i]])
            vec_k = vec_k / np.linalg.norm(vec_k)
        else:
            vec_k = np.zeros(num_features)
        eigenvectors.append(vec_k)
        
    eigenvectors = np.array(eigenvectors)
    total_var = np.sum(eigenvalues)
    var_ratios = (eigenvalues / total_var) if total_var > 0 else np.zeros_like(eigenvalues)

    return {
        "num_samples": num_samples,
        "num_features": num_features,
        "eigenvalues": eigenvalues[:n_components].tolist(),
        "eigenvectors": eigenvectors,
        "explained_variance_ratio": var_ratios[:n_components].tolist(),
        "mean_vector": mean_vec,
    }


def solved_numerical_example() -> Dict[str, Any]:
    """
    Section 11 & Section 21 Verification Benchmark:
    A = (1, 2, 3), B = (2, 3, 4)
    A . B = 20
    ||A|| = sqrt(14)
    ||B|| = sqrt(29)
    d(A, B) = sqrt(3) ~= 1.732
    cos(theta) = 20 / sqrt(406) ~= 0.9926
    """
    A = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    B = np.array([2.0, 3.0, 4.0], dtype=np.float64)
    
    dot_val = 1.0 * 2.0 + 2.0 * 3.0 + 3.0 * 4.0 # 20.0
    norm_A = np.sqrt(1.0**2 + 2.0**2 + 3.0**2) # sqrt(14)
    norm_B = np.sqrt(2.0**2 + 3.0**2 + 4.0**2) # sqrt(29)
    dist = np.sqrt((1.0 - 2.0)**2 + (2.0 - 3.0)**2 + (3.0 - 4.0)**2) # sqrt(3)
    cos_sim = dot_val / (norm_A * norm_B) # 20 / sqrt(406)
    
    # 2x2 matrix illustration
    M_A = np.array([[10, 20], [30, 40]], dtype=np.float64)
    M_B = np.array([[15, 25], [35, 45]], dtype=np.float64)
    v_A = flatten_image_to_vector(M_A)
    v_B = flatten_image_to_vector(M_B)
    matrix_metrics = full_vector_comparison(v_A, v_B)

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
        "matrix_metrics": matrix_metrics,
    }
