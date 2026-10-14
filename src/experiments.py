"""
SignatureLab — Batch Experiments & Statistical Evaluation Engine
Implements batch evaluations, CSV metadata parsing and validation,
threshold sweeping, and binary biometric performance metrics (FAR, FRR, F1, Accuracy).
"""

from typing import List, Dict, Any, Tuple, Optional
import os
import io
import pandas as pd
import numpy as np

from .image_processing import preprocess_signature_pipeline, ImageValidationError
from .vector_math import full_vector_comparison


class BatchValidationError(Exception):
    """Raised when batch data or CSV metadata fails validation."""
    pass


def load_pairs_from_csv(
    csv_input: Any,
    available_images_dict: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Parses a CSV metadata file containing:
    pair_id, reference_image, test_image, pair_label, [optional: expected_match]
    
    Validates that all referenced image filenames exist in available_images_dict.
    If any image is missing, raises BatchValidationError listing missing files.
    """
    if hasattr(csv_input, "read"):
        df = pd.read_csv(csv_input)
    elif isinstance(csv_input, str):
        if not os.path.exists(csv_input):
            raise BatchValidationError(f"CSV file not found: {csv_input}")
        df = pd.read_csv(csv_input)
    elif isinstance(csv_input, pd.DataFrame):
        df = csv_input.copy()
    else:
        raise BatchValidationError(f"Unsupported CSV input type: {type(csv_input)}")

    required_cols = ["pair_id", "reference_image", "test_image"]
    for col in required_cols:
        if col not in df.columns:
            raise BatchValidationError(
                f"Missing required CSV column '{col}'. Required headers are: pair_id, reference_image, test_image, pair_label"
            )

    missing_refs = []
    pairs = []
    for idx, row in df.iterrows():
        p_id = str(row["pair_id"]).strip()
        ref_name = str(row["reference_image"]).strip()
        test_name = str(row["test_image"]).strip()
        pair_label = str(row.get("pair_label", f"Pair {p_id}")).strip()
        
        # Determine expected_match ground truth if present
        expected_match = None
        if "expected_match" in row:
            val = str(row["expected_match"]).lower().strip()
            expected_match = val in ["true", "1", "yes", "genuine", "match"]
        elif "genuine" in pair_label.lower():
            expected_match = True
        elif "forg" in pair_label.lower() or "different" in pair_label.lower() or "cross" in pair_label.lower():
            expected_match = False

        # Validate that image files are available
        ref_obj = available_images_dict.get(ref_name) or available_images_dict.get(os.path.basename(ref_name))
        test_obj = available_images_dict.get(test_name) or available_images_dict.get(os.path.basename(test_name))

        if ref_obj is None:
            missing_refs.append(f"Row {idx+1} (Pair {p_id}): Reference '{ref_name}' not found")
        if test_obj is None:
            missing_refs.append(f"Row {idx+1} (Pair {p_id}): Test '{test_name}' not found")

        pairs.append({
            "pair_id": p_id,
            "pair_label": pair_label,
            "ref_name": ref_name,
            "test_name": test_name,
            "ref_image": ref_obj,
            "test_image": test_obj,
            "expected_match": expected_match
        })

    if missing_refs:
        raise BatchValidationError(
            f"CSV references unavailable images ({len(missing_refs)} errors):\n" + "\n".join(missing_refs[:10])
        )

    return pairs


def evaluate_batch_pairs(
    pairs: List[Dict[str, Any]],
    canvas_height: int = 128,
    canvas_width: int = 256,
    similarity_threshold: Optional[float] = 0.75,
    distance_threshold: Optional[float] = None
) -> pd.DataFrame:
    """
    Evaluates a list of signature pairs.
    Returns a pandas DataFrame with all required Section 14 columns:
    - pair_id
    - pair_label
    - dot_product
    - ref_norm
    - test_norm
    - euclidean_distance
    - cosine_similarity
    - decision (if threshold configured)
    """
    results = []
    for item in pairs:
        p_id = item["pair_id"]
        label = item["pair_label"]
        ref_name = item.get("ref_name", "")
        test_name = item.get("test_name", "")
        ref_img = item["ref_image"]
        test_img = item["test_image"]
        expected = item.get("expected_match")

        try:
            p_ref = preprocess_signature_pipeline(ref_img, canvas_height, canvas_width)
            p_test = preprocess_signature_pipeline(test_img, canvas_height, canvas_width)
            metrics = full_vector_comparison(p_ref["vector"], p_test["vector"])

            cos_sim = metrics["cosine_similarity"]
            dist = metrics["euclidean_distance"]

            # Evaluate decision
            decision = None
            if similarity_threshold is not None:
                decision = "Match" if cos_sim >= similarity_threshold else "Non-Match"
            elif distance_threshold is not None:
                decision = "Match" if dist <= distance_threshold else "Non-Match"

            results.append({
                "pair_id": p_id,
                "pair_label": label,
                "reference_image": ref_name,
                "test_image": test_name,
                "dot_product": metrics["dot_product"],
                "ref_norm": metrics["norm_u"],
                "test_norm": metrics["norm_v"],
                "euclidean_distance": dist,
                "cosine_similarity": cos_sim,
                "angle_degrees": metrics["angle_degrees"],
                "decision": decision,
                "expected_match": expected,
                "status": "Success"
            })
        except Exception as e:
            results.append({
                "pair_id": p_id,
                "pair_label": label,
                "reference_image": ref_name,
                "test_image": test_name,
                "dot_product": None,
                "ref_norm": None,
                "test_norm": None,
                "euclidean_distance": None,
                "cosine_similarity": None,
                "angle_degrees": None,
                "decision": "Error",
                "expected_match": expected,
                "status": f"Error: {str(e)}"
            })

    return pd.DataFrame(results)


def compute_biometric_performance_metrics(
    df: pd.DataFrame,
    threshold: float,
    metric_type: str = "similarity"
) -> Dict[str, Any]:
    """
    Calculates binary classification performance metrics (Section 18):
    - True Positives (TP)
    - True Negatives (TN)
    - False Positives (FP)
    - False Negatives (FN)
    - Accuracy
    - Precision
    - Recall (Sensitivity / True Acceptance Rate)
    - F1-Score
    - False Acceptance Rate (FAR = FP / (FP + TN))
    - False Rejection Rate (FRR = FN / (FN + TP))
    
    Class Definition: Genuine matches are considered POSITIVE (True).
    Impostors/forgeries are considered NEGATIVE (False).
    """
    valid = df.dropna(subset=["cosine_similarity", "euclidean_distance", "expected_match"]).copy()
    if len(valid) == 0:
        return {"error": "No labeled evaluation data available."}

    y_true = valid["expected_match"].astype(bool).values

    if metric_type == "similarity":
        y_scores = valid["cosine_similarity"].astype(float).values
        y_pred = y_scores >= threshold
    else: # distance-based
        y_scores = valid["euclidean_distance"].astype(float).values
        y_pred = y_scores <= threshold

    tp = int(np.sum((y_true == True) & (y_pred == True)))
    tn = int(np.sum((y_true == False) & (y_pred == False)))
    fp = int(np.sum((y_true == False) & (y_pred == True)))
    fn = int(np.sum((y_true == True) & (y_pred == False)))

    total = tp + tn + fp + fn
    accuracy = (tp + tn) / total if total > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    # Biometric specific metrics
    total_impostors = fp + tn
    far = (fp / total_impostors) if total_impostors > 0 else 0.0

    total_genuines = fn + tp
    frr = (fn / total_genuines) if total_genuines > 0 else 0.0

    return {
        "threshold": threshold,
        "metric_type": metric_type,
        "TP": tp,
        "TN": tn,
        "FP": fp,
        "FN": fn,
        "total_pairs": total,
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
        "FAR": float(far),
        "FRR": float(frr),
    }


def sweep_all_thresholds(
    df: pd.DataFrame,
    metric_type: str = "similarity",
    steps: int = 50
) -> pd.DataFrame:
    """
    Sweeps thresholds across valid range to generate full sensitivity tradeoff curve.
    """
    valid = df.dropna(subset=["cosine_similarity", "euclidean_distance", "expected_match"])
    if len(valid) == 0:
        return pd.DataFrame()

    if metric_type == "similarity":
        thresholds = np.linspace(0.0, 1.0, steps)
    else:
        min_d = float(valid["euclidean_distance"].min())
        max_d = float(valid["euclidean_distance"].max())
        thresholds = np.linspace(min_d * 0.8, max_d * 1.2, steps)

    records = []
    for t in thresholds:
        m = compute_biometric_performance_metrics(valid, t, metric_type=metric_type)
        if "error" not in m:
            records.append(m)

    return pd.DataFrame(records)
