"""
SignatureLab — Core Package
"""
from .linear_algebra import (
    flatten_image_to_vector,
    dot_product,
    euclidean_norm,
    euclidean_distance,
    cosine_similarity,
    orthogonal_projection,
    full_vector_comparison,
    solved_numerical_example,
)
from .image_processing import (
    load_image_to_grayscale,
    extract_signature_bounding_box,
    aspect_preserving_resize_and_pad,
    to_foreground_representation,
    preprocess_signature_pipeline,
    ImageValidationError,
)

__all__ = [
    "flatten_image_to_vector",
    "dot_product",
    "euclidean_norm",
    "euclidean_distance",
    "cosine_similarity",
    "orthogonal_projection",
    "full_vector_comparison",
    "solved_numerical_example",
    "load_image_to_grayscale",
    "extract_signature_bounding_box",
    "aspect_preserving_resize_and_pad",
    "to_foreground_representation",
    "preprocess_signature_pipeline",
    "ImageValidationError",
]
