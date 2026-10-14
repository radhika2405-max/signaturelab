"""
Unit tests for core.batch_evaluator and report generator.
"""

import pytest
import os
import pandas as pd
from core.batch_evaluator import (
    run_pair_comparison,
    evaluate_batch,
    compute_threshold_metrics,
    sweep_thresholds
)
from core.report_generator import generate_pdf_report, generate_docx_report


def test_batch_evaluation_on_sample_signatures():
    """
    Runs batch evaluator across generated sample signatures.
    """
    ref_path = "assets/sample_signatures/author_a_genuine_1.png"
    test_gen_path = "assets/sample_signatures/author_a_genuine_2.png"
    test_forged_path = "assets/sample_signatures/author_a_forged.png"
    
    assert os.path.exists(ref_path)
    assert os.path.exists(test_gen_path)
    assert os.path.exists(test_forged_path)
    
    pairs = [
        {
            "pair_label": "Author A: Genuine vs Genuine",
            "ref_path": ref_path,
            "test_path": test_gen_path,
            "expected_match": True,
        },
        {
            "pair_label": "Author A: Genuine vs Forged",
            "ref_path": ref_path,
            "test_path": test_forged_path,
            "expected_match": False,
        }
    ]
    
    df = evaluate_batch(pairs)
    assert len(df) == 2
    assert "cosine_similarity" in df.columns
    assert "euclidean_distance" in df.columns
    
    # Check that genuine vs genuine has higher cosine similarity than genuine vs forged
    gen_score = df[df["expected_match"] == True]["cosine_similarity"].values[0]
    forged_score = df[df["expected_match"] == False]["cosine_similarity"].values[0]
    assert gen_score > forged_score
    
    # Check threshold metrics
    metrics = compute_threshold_metrics(df, threshold=0.7)
    assert "accuracy" in metrics
    assert metrics["total_pairs"] == 2
    
    # Check sweep
    sweep_df = sweep_thresholds(df, steps=10)
    assert len(sweep_df) == 10


def test_pdf_report_generation():
    """
    Verifies that PDF report generates non-empty valid PDF bytes.
    """
    sample_data = {
        "canvas_shape": "128 x 256",
        "dimension": 32768,
        "dot_product": 124.5,
        "norm_u": 15.2,
        "norm_v": 14.8,
        "euclidean_distance": 5.4,
        "cosine_similarity": 0.8842,
        "angle_degrees": 27.8,
    }
    pdf_bytes = generate_pdf_report(sample_data)
    assert len(pdf_bytes) > 1000
    assert pdf_bytes.startswith(b"%PDF")


def test_docx_report_generation():
    """
    Verifies that DOCX report generates valid document bytes.
    """
    sample_data = {
        "canvas_shape": "128 x 256",
        "dimension": 32768,
        "dot_product": 124.5,
        "norm_u": 15.2,
        "norm_v": 14.8,
        "euclidean_distance": 5.4,
        "cosine_similarity": 0.8842,
        "angle_degrees": 27.8,
    }
    docx_bytes = generate_docx_report(sample_data)
    assert len(docx_bytes) > 1000
    # ZIP signature for docx: PK..
    assert docx_bytes.startswith(b"PK")
