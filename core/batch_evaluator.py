"""
SignatureLab — Batch Evaluator & Experiment Engine
Runs systematic comparisons over multiple signature pairs, sweeps decision thresholds,
and computes binary classification metrics (TP, FP, TN, FN, Accuracy, Precision, Recall).
"""

from typing import List, Dict, Any, Tuple
import os
import numpy as np
import pandas as pd
from .image_processing import preprocess_signature_pipeline
from .linear_algebra import full_vector_comparison


def run_pair_comparison(
    path_ref: str,
    path_test: str,
    pair_label: str = "Unknown",
    expected_match: bool = True,
    canvas_height: int = 128,
    canvas_width: int = 256
) -> Dict[str, Any]:
    """
    Compares a single pair of signature images from files.
    """
    prep_ref = preprocess_signature_pipeline(path_ref, canvas_height, canvas_width)
    prep_test = preprocess_signature_pipeline(path_test, canvas_height, canvas_width)
    
    metrics = full_vector_comparison(prep_ref["vector"], prep_test["vector"])
    
    return {
        "pair_label": pair_label,
        "ref_path": path_ref,
        "test_path": path_test,
        "ref_name": os.path.basename(path_ref),
        "test_name": os.path.basename(path_test),
        "expected_match": expected_match,
        "cosine_similarity": metrics["cosine_similarity"],
        "euclidean_distance": metrics["euclidean_distance"],
        "dot_product": metrics["dot_product"],
        "norm_ref": metrics["norm_u"],
        "norm_test": metrics["norm_v"],
        "angle_degrees": metrics["angle_degrees"],
    }


def evaluate_batch(
    pairs_config: List[Dict[str, Any]],
    canvas_height: int = 128,
    canvas_width: int = 256
) -> pd.DataFrame:
    """
    Evaluates a list of signature pairs.
    Each item in pairs_config should have:
    - 'ref_path': str
    - 'test_path': str
    - 'pair_label': str
    - 'expected_match': bool
    """
    records = []
    for item in pairs_config:
        try:
            res = run_pair_comparison(
                path_ref=item["ref_path"],
                path_test=item["test_path"],
                pair_label=item.get("pair_label", "Unnamed Pair"),
                expected_match=item.get("expected_match", True),
                canvas_height=canvas_height,
                canvas_width=canvas_width
            )
            records.append(res)
        except Exception as e:
            records.append({
                "pair_label": item.get("pair_label", "Error Pair"),
                "ref_name": os.path.basename(item.get("ref_path", "")),
                "test_name": os.path.basename(item.get("test_path", "")),
                "expected_match": item.get("expected_match", True),
                "cosine_similarity": None,
                "euclidean_distance": None,
                "error": str(e)
            })
            
    return pd.DataFrame(records)


def compute_threshold_metrics(
    df: pd.DataFrame,
    threshold: float
) -> Dict[str, Any]:
    """
    Computes classification metrics for a given cosine similarity threshold.
    Match predicted if cosine_similarity >= threshold.
    """
    valid_df = df.dropna(subset=["cosine_similarity", "expected_match"]).copy()
    if len(valid_df) == 0:
        return {"error": "No valid comparisons"}
        
    y_true = valid_df["expected_match"].astype(bool).values
    y_scores = valid_df["cosine_similarity"].astype(float).values
    y_pred = y_scores >= threshold
    
    tp = int(np.sum((y_true == True) & (y_pred == True)))
    tn = int(np.sum((y_true == False) & (y_pred == False)))
    fp = int(np.sum((y_true == False) & (y_pred == True)))
    fn = int(np.sum((y_true == True) & (y_pred == False)))
    
    total = tp + tn + fp + fn
    accuracy = (tp + tn) / total if total > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        "threshold": threshold,
        "TP": tp,
        "TN": tn,
        "FP": fp,
        "FN": fn,
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
        "total_pairs": total
    }


def sweep_thresholds(df: pd.DataFrame, steps: int = 50) -> pd.DataFrame:
    """
    Sweeps thresholds from 0.0 to 1.0 to generate an ROC / precision-recall exploration table.
    """
    thresholds = np.linspace(0.0, 1.0, steps)
    metrics_list = []
    for t in thresholds:
        m = compute_threshold_metrics(df, t)
        if "error" not in m:
            metrics_list.append(m)
    return pd.DataFrame(metrics_list)
