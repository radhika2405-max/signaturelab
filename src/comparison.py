"""
SignatureLab — Comparison Module
Coordinates the end-to-end comparison between a reference signature and a test signature,
combining image preprocessing with the linear algebra vector engine.
"""

from typing import Dict, Any, Optional
from .image_processing import preprocess_signature_pipeline, ImageValidationError
from .vector_math import full_vector_comparison


def compare_signatures(
    ref_image: Any,
    test_image: Any,
    canvas_height: int = 128,
    canvas_width: int = 256,
    margin_padding: int = 10,
    similarity_threshold: Optional[float] = 0.75,
    distance_threshold: Optional[float] = 5.0
) -> Dict[str, Any]:
    """
    Executes end-to-end comparison between reference and test signature inputs.
    
    Returns a comprehensive result dictionary with preprocessing artifacts,
    computed linear algebra metrics, and provisional matching decisions.
    """
    # Preprocess reference signature
    ref_prep = preprocess_signature_pipeline(
        ref_image,
        canvas_height=canvas_height,
        canvas_width=canvas_width,
        margin_padding=margin_padding
    )
    
    # Preprocess test signature
    test_prep = preprocess_signature_pipeline(
        test_image,
        canvas_height=canvas_height,
        canvas_width=canvas_width,
        margin_padding=margin_padding
    )
    
    # Check vector dimension equality
    if len(ref_prep["vector"]) != len(test_prep["vector"]):
        raise ValueError(
            f"Dimension mismatch: Reference vector has {len(ref_prep['vector'])} components, "
            f"Test vector has {len(test_prep['vector'])} components."
        )
        
    # Evaluate metrics
    metrics = full_vector_comparison(ref_prep["vector"], test_prep["vector"])
    
    # Evaluate threshold decisions
    sim_match = None
    if similarity_threshold is not None:
        sim_match = bool(metrics["cosine_similarity"] >= similarity_threshold)
        
    dist_match = None
    if distance_threshold is not None:
        dist_match = bool(metrics["euclidean_distance"] <= distance_threshold)

    return {
        "ref_prep": ref_prep,
        "test_prep": test_prep,
        "metrics": metrics,
        "canvas_shape": (canvas_height, canvas_width),
        "similarity_threshold": similarity_threshold,
        "distance_threshold": distance_threshold,
        "similarity_decision": sim_match,
        "distance_decision": dist_match,
    }
