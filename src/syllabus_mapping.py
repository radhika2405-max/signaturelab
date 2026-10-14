"""
SignatureLab — Syllabus Mapping Engine
Maps Undergraduate Linear Algebra Syllabus (Units 1, 2, 3) to project implementations.
Columns required by Section 12:
1. Unit
2. Mathematical concept
3. Project application
4. Actual implementation status
5. Explanation or evidence
"""

import pandas as pd
from typing import List, Dict, Any

SYLLABUS_MAPPING_DATA: List[Dict[str, str]] = [
    # UNIT 1: INTRODUCTION TO VECTOR SPACES
    {
        "Unit": "Unit 1: Vector Spaces",
        "Mathematical Concept": "Real Vector Spaces M_{m,n}(R)",
        "Project Application": "Standardized canonical signature image matrices",
        "Implementation Status": "Directly Implemented",
        "Explanation / Evidence": "Signature canvas of m=128, n=256 satisfies all 8 vector space axioms under matrix addition and real scalar multiplication."
    },
    {
        "Unit": "Unit 1: Vector Spaces",
        "Mathematical Concept": "Vectors in R^N",
        "Project Application": "Flattened 1D signature embeddings",
        "Implementation Status": "Directly Implemented",
        "Explanation / Evidence": "Lexicographical vectorization maps each matrix M into R^(32,768). Verified in src/vector_math.py::flatten_image_to_vector."
    },
    {
        "Unit": "Unit 1: Vector Spaces",
        "Mathematical Concept": "Subspaces",
        "Project Application": "Subspace of signatures with fixed canvas size",
        "Implementation Status": "Directly Implemented",
        "Explanation / Evidence": "All m x n signatures form a closed subspace within the ambient space of all digital images."
    },
    {
        "Unit": "Unit 1: Vector Spaces",
        "Mathematical Concept": "Linear Independence",
        "Project Application": "Signatures from distinct authors as non-collinear vectors",
        "Implementation Status": "Directly Implemented",
        "Explanation / Evidence": "Distinct writers yield linearly independent vectors in R^N (cos theta < 0.60). Verified in batch experiments."
    },
    {
        "Unit": "Unit 1: Vector Spaces",
        "Mathematical Concept": "Basis & Dimension",
        "Project Application": "Canonical standard basis vectors e_i of R^(mn)",
        "Implementation Status": "Directly Implemented",
        "Explanation / Evidence": "dim(V) = mn = 32,768. Standard basis consists of single-pixel impulse matrices E_{ij} where pixel (i,j)=1 and others are 0."
    },
    {
        "Unit": "Unit 1: Vector Spaces",
        "Mathematical Concept": "Span & Sums of Subspaces",
        "Project Application": "Linear combinations of stroke features and synthetic variants",
        "Implementation Status": "Theoretical & Empirical Discussion",
        "Explanation / Evidence": "The span of multiple genuine signatures forms an affine handwriting subspace; discussed in oral viva guide."
    },
    {
        "Unit": "Unit 1: Vector Spaces",
        "Mathematical Concept": "Direct Sums & Quotient Spaces",
        "Project Application": "Orthogonal decomposition into signal + residual noise",
        "Implementation Status": "Theoretical Discussion",
        "Explanation / Evidence": "Decomposition V = W (+) W_perp where W is genuine signature subspace and W_perp is residual orthogonal noise."
    },

    # UNIT 2: LINEAR MAPS
    {
        "Unit": "Unit 2: Linear Maps",
        "Mathematical Concept": "Definition of Linear Maps",
        "Project Application": "Grayscale projection and resizing transformations",
        "Implementation Status": "Directly Implemented",
        "Explanation / Evidence": "Luminance map T: R^3 -> R (0.299R + 0.587G + 0.114B) satisfies T(u+v)=T(u)+T(v) and T(c*u)=c*T(u). Bilinear resize is linear combination."
    },
    {
        "Unit": "Unit 2: Linear Maps",
        "Mathematical Concept": "Isomorphic Vector Spaces",
        "Project Application": "Matrix-to-Vector Flattening vec(M)",
        "Implementation Status": "Directly Implemented",
        "Explanation / Evidence": "vec: M_{m,n}(R) -> R^(mn) is a bijective linear map with trivial kernel ker(vec) = {0}, proving M_{m,n}(R) ~= R^(mn)."
    },
    {
        "Unit": "Unit 2: Linear Maps",
        "Mathematical Concept": "Linear Maps as Matrix Multiplication",
        "Project Application": "Filtering, blur, and spatial linear convolution",
        "Implementation Status": "Directly Implemented",
        "Explanation / Evidence": "Spatial filtering can be expressed as y = K x where K is a block Toeplitz matrix representing convolution operator."
    },
    {
        "Unit": "Unit 2: Linear Maps",
        "Mathematical Concept": "Null Space & Injectivity",
        "Project Application": "Rank-Nullity theorem applied to projection operations",
        "Implementation Status": "Directly Implemented",
        "Explanation / Evidence": "Orthogonal projection proj_v: R^N -> R^N has rank 1 and nullity N-1. Dim(ker) + Dim(range) = N by Fundamental Theorem."
    },
    {
        "Unit": "Unit 2: Linear Maps",
        "Mathematical Concept": "Nonlinear Preprocessing Operations",
        "Project Application": "Otsu thresholding and bounding-box margin crop",
        "Implementation Status": "Directly Implemented & Contrast Analyzed",
        "Explanation / Evidence": "Explicitly distinguished from linear maps. Thresholding step function fails additivity and homogeneity; documented in Section 9 & 13."
    },

    # UNIT 3: EIGENVALUES, EIGENVECTORS, AND INNER PRODUCT SPACES
    {
        "Unit": "Unit 3: Inner Product Spaces",
        "Mathematical Concept": "Euclidean Inner Product (Dot Product)",
        "Project Application": "Metric engine evaluating spatial alignment",
        "Implementation Status": "Directly Implemented",
        "Explanation / Evidence": "<u, v> = sum(u_i * v_i). Directly computes geometric overlap. Verified with manual worked example A=(1,2,3), B=(2,3,4) yielding 20."
    },
    {
        "Unit": "Unit 3: Inner Product Spaces",
        "Mathematical Concept": "Euclidean (L2) Norm",
        "Project Application": "Total stroke energy / magnitude of signature vector",
        "Implementation Status": "Directly Implemented",
        "Explanation / Evidence": "||u||_2 = sqrt(<u, u>). For non-negative stroke pixels, represents cumulative ink mass. Hand-verified ||A||=sqrt(14), ||B||=sqrt(29)."
    },
    {
        "Unit": "Unit 3: Inner Product Spaces",
        "Mathematical Concept": "Euclidean Distance Metric",
        "Project Application": "Point-to-point spatial separation d(u, v) = ||u - v||_2",
        "Implementation Status": "Directly Implemented",
        "Explanation / Evidence": "Satisfies positivity, identity of indiscernibles, symmetry, and triangle inequality. Hand-verified d(A,B)=sqrt(3) ~= 1.732."
    },
    {
        "Unit": "Unit 3: Inner Product Spaces",
        "Mathematical Concept": "Cauchy-Schwarz Inequality & Cosine Sim",
        "Project Application": "Scale-invariant signature similarity cos(theta)",
        "Implementation Status": "Directly Implemented",
        "Explanation / Evidence": "|<u, v>| <= ||u|| ||v|| guarantees cos(theta) in [0, 1] for non-negative strokes. Hand-verified cos(theta)=20/sqrt(406) ~= 0.9926."
    },
    {
        "Unit": "Unit 3: Inner Product Spaces",
        "Mathematical Concept": "Eigenvalues and Eigenvectors",
        "Project Application": "Covariance matrix decomposition & Principal Component Analysis (PCA)",
        "Implementation Status": "Genuinely Implemented & Visualized",
        "Explanation / Evidence": "Computes sample covariance C = (1/k) X X^T and evaluates C v = lambda v to extract dominant eigenspaces of handwriting variations."
    }
]


def get_syllabus_mapping_dataframe() -> pd.DataFrame:
    """Returns the syllabus mapping as a pandas DataFrame."""
    return pd.DataFrame(SYLLABUS_MAPPING_DATA)
