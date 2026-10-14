"""
SignatureLab — Core Source Package (src)
Exports all linear algebra, preprocessing, comparison, experiment, visualization, and reporting modules.
"""

from .vector_math import (
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

from .image_processing import (
    load_image_to_grayscale,
    extract_signature_bounding_box,
    aspect_preserving_resize,
    pad_to_canonical_canvas,
    to_foreground_representation,
    preprocess_signature_pipeline,
    check_blank_or_uniform,
    ImageValidationError,
    DEFAULT_CANVAS_HEIGHT,
    DEFAULT_CANVAS_WIDTH,
)

from .comparison import compare_signatures

from .experiments import (
    load_pairs_from_csv,
    evaluate_batch_pairs,
    compute_biometric_performance_metrics,
    sweep_all_thresholds,
    BatchValidationError,
)

from .visualizations import (
    plot_difference_heatmap,
    plot_inner_product_energy,
    plot_confusion_matrix,
    plot_score_distributions,
    plot_far_frr_tradeoff,
)

from .report_generator import (
    generate_full_pdf_report,
    generate_full_docx_report,
    export_all_deliverables,
)

from .syllabus_mapping import (
    SYLLABUS_MAPPING_DATA,
    get_syllabus_mapping_dataframe,
)

__all__ = [
    "flatten_image_to_vector",
    "vector_addition",
    "scalar_multiplication",
    "dot_product",
    "euclidean_norm",
    "euclidean_distance",
    "cosine_similarity",
    "orthogonal_projection",
    "full_vector_comparison",
    "compute_eigenspace_decomposition",
    "solved_numerical_example",
    "load_image_to_grayscale",
    "extract_signature_bounding_box",
    "aspect_preserving_resize",
    "pad_to_canonical_canvas",
    "to_foreground_representation",
    "preprocess_signature_pipeline",
    "check_blank_or_uniform",
    "ImageValidationError",
    "compare_signatures",
    "load_pairs_from_csv",
    "evaluate_batch_pairs",
    "compute_biometric_performance_metrics",
    "sweep_all_thresholds",
    "BatchValidationError",
    "plot_difference_heatmap",
    "plot_inner_product_energy",
    "plot_confusion_matrix",
    "plot_score_distributions",
    "plot_far_frr_tradeoff",
    "generate_full_pdf_report",
    "generate_full_docx_report",
    "export_all_deliverables",
    "SYLLABUS_MAPPING_DATA",
    "get_syllabus_mapping_dataframe",
    "DEFAULT_CANVAS_HEIGHT",
    "DEFAULT_CANVAS_WIDTH",
]
