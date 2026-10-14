"""
Unit tests for src.experiments & CSV validation
Verifies requirements 15 through 20:
15. Correct result-table generation
16. Threshold boundary conditions
17. Invalid thresholds
18. Batch processing errors
19. CSV export
20. Empty-data behavior
"""

import pytest
import os
import pandas as pd
import numpy as np
from src.experiments import (
    load_pairs_from_csv,
    evaluate_batch_pairs,
    compute_biometric_performance_metrics,
    sweep_all_thresholds,
    BatchValidationError,
)


def test_15_correct_result_table_generation():
    """Requirement 15: Correct result-table generation."""
    csv_path = "sample_data/pairs.csv"
    assert os.path.exists(csv_path)
    
    # Map filenames to sample paths
    imgs = {
        f: os.path.join("sample_data", f)
        for f in os.listdir("sample_data")
        if f.endswith(".png")
    }
    
    pairs = load_pairs_from_csv(csv_path, imgs)
    df = evaluate_batch_pairs(pairs, canvas_height=128, canvas_width=256, similarity_threshold=0.75)
    
    assert len(df) == len(pairs)
    expected_cols = [
        "pair_id", "pair_label", "reference_image", "test_image",
        "dot_product", "ref_norm", "test_norm", "euclidean_distance",
        "cosine_similarity", "decision"
    ]
    for col in expected_cols:
        assert col in df.columns
    assert not df["cosine_similarity"].isnull().any()


def test_16_threshold_boundary_conditions():
    """Requirement 16: Threshold boundary conditions (0.0 and 1.0)."""
    df = pd.DataFrame([
        {"cosine_similarity": 0.85, "euclidean_distance": 3.0, "expected_match": True},
        {"cosine_similarity": 0.30, "euclidean_distance": 12.0, "expected_match": False}
    ])
    
    # Boundary threshold = 0.0 -> all accepted as matches
    m0 = compute_biometric_performance_metrics(df, threshold=0.0)
    assert m0["TP"] == 1
    assert m0["FP"] == 1
    assert m0["FN"] == 0
    assert m0["TN"] == 0
    assert m0["FAR"] == 1.0
    
    # Boundary threshold = 1.0 -> all rejected (unless exact identical vector)
    m1 = compute_biometric_performance_metrics(df, threshold=1.0)
    assert m1["TP"] == 0
    assert m1["FP"] == 0
    assert m1["FN"] == 1
    assert m1["TN"] == 1
    assert m1["FRR"] == 1.0


def test_17_invalid_thresholds():
    """Requirement 17: Invalid thresholds handling."""
    df = pd.DataFrame([
        {"cosine_similarity": 0.85, "euclidean_distance": 3.0, "expected_match": True}
    ])
    # Threshold outside [0, 1] behaves safely
    m_high = compute_biometric_performance_metrics(df, threshold=1.5)
    assert m_high["TP"] == 0
    m_low = compute_biometric_performance_metrics(df, threshold=-0.5)
    assert m_low["TP"] == 1


def test_18_batch_processing_errors():
    """Requirement 18: Batch processing errors (missing files in CSV)."""
    bad_df = pd.DataFrame([
        {"pair_id": "99", "reference_image": "NON_EXISTENT_REF.png", "test_image": "author_a_genuine_1.png"}
    ])
    available = {"author_a_genuine_1.png": "dummy_path"}
    with pytest.raises(BatchValidationError) as exc_info:
        load_pairs_from_csv(bad_df, available)
    assert "unavailable images" in str(exc_info.value)


def test_19_csv_export():
    """Requirement 19: CSV export."""
    df = pd.DataFrame([
        {"pair_id": "1", "cosine_similarity": 0.884, "decision": "Match"}
    ])
    csv_out = "outputs/test_export.csv"
    df.to_csv(csv_out, index=False)
    assert os.path.exists(csv_out)
    loaded = pd.read_csv(csv_out)
    assert len(loaded) == 1
    assert loaded["decision"].values[0] == "Match"
    os.remove(csv_out)


def test_20_empty_data_behavior():
    """Requirement 20: Empty-data behavior."""
    empty_df = pd.DataFrame(columns=["cosine_similarity", "euclidean_distance", "expected_match"])
    m_empty = compute_biometric_performance_metrics(empty_df, threshold=0.75)
    assert "error" in m_empty
    
    sweep_empty = sweep_all_thresholds(empty_df)
    assert sweep_empty.empty
