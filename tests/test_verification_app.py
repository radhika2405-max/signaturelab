"""
Tests for transformed SignatureLab Application:
Validates the end-to-end comparison pipeline, edge cases, error handling,
and verification requirements specified in the Master Prompt.
"""

import os
import io
import pytest
import numpy as np
from PIL import Image

from src.comparison import compare_signatures
from src.image_processing import (
    preprocess_signature_pipeline,
    load_image_to_grayscale,
    check_blank_or_uniform,
    ImageValidationError,
    DEFAULT_CANVAS_HEIGHT,
    DEFAULT_CANVAS_WIDTH,
)
from src.vector_math import full_vector_comparison


@pytest.fixture
def sample_paths():
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_data")
    return {
        "author_a_1": os.path.join(base_dir, "author_a_genuine_1.png"),
        "author_a_2": os.path.join(base_dir, "author_a_genuine_2.png"),
        "author_a_forged": os.path.join(base_dir, "author_a_forged.png"),
        "author_b_1": os.path.join(base_dir, "author_b_genuine_1.png"),
        "author_b_2": os.path.join(base_dir, "author_b_genuine_2.png"),
    }


def test_identical_signatures_yield_perfect_similarity(sample_paths):
    """Confirm that comparing an image against itself yields Cosine = 1.0 and Distance = 0.0."""
    res = compare_signatures(
        sample_paths["author_a_1"],
        sample_paths["author_a_1"],
        canvas_height=128,
        canvas_width=256
    )
    cos_sim = res["metrics"]["cosine_similarity"]
    euc_dist = res["metrics"]["euclidean_distance"]
    assert pytest.approx(cos_sim, abs=1e-5) == 1.0
    assert pytest.approx(euc_dist, abs=1e-5) == 0.0


def test_genuine_vs_genuine_has_high_similarity(sample_paths):
    """Confirm that two genuine signatures from the same author have high similarity (> 0.65)."""
    res = compare_signatures(
        sample_paths["author_a_1"],
        sample_paths["author_a_2"],
        canvas_height=128,
        canvas_width=256
    )
    cos_sim = res["metrics"]["cosine_similarity"]
    euc_dist = res["metrics"]["euclidean_distance"]
    assert cos_sim > 0.65
    assert euc_dist > 0.0


def test_genuine_vs_forged_has_lower_similarity(sample_paths):
    """Confirm that genuine vs forged signature has significantly lower similarity."""
    res_gen = compare_signatures(
        sample_paths["author_a_1"],
        sample_paths["author_a_2"],
        canvas_height=128,
        canvas_width=256
    )
    res_forged = compare_signatures(
        sample_paths["author_a_1"],
        sample_paths["author_a_forged"],
        canvas_height=128,
        canvas_width=256
    )
    assert res_gen["metrics"]["cosine_similarity"] > res_forged["metrics"]["cosine_similarity"]
    assert res_forged["metrics"]["cosine_similarity"] < 0.60


def test_cross_author_signatures_have_lower_similarity(sample_paths):
    """Confirm that cross-author signatures diverge noticeably."""
    res_cross = compare_signatures(
        sample_paths["author_a_1"],
        sample_paths["author_b_1"],
        canvas_height=128,
        canvas_width=256
    )
    assert res_cross["metrics"]["cosine_similarity"] < 0.60


def test_blank_white_image_rejected():
    """Confirm that an all-white image raises an ImageValidationError."""
    blank_white = Image.new("RGB", (200, 100), color=(255, 255, 255))
    buf = io.BytesIO()
    blank_white.save(buf, format="PNG")
    buf.seek(0)
    with pytest.raises(ImageValidationError):
        preprocess_signature_pipeline(buf)


def test_blank_black_image_rejected():
    """Confirm that an all-black image raises an ImageValidationError."""
    blank_black = Image.new("RGB", (200, 100), color=(0, 0, 0))
    buf = io.BytesIO()
    blank_black.save(buf, format="PNG")
    buf.seek(0)
    with pytest.raises(ImageValidationError):
        preprocess_signature_pipeline(buf)


def test_corrupt_bytes_rejected():
    """Confirm that corrupt/random bytes raise an ImageValidationError."""
    corrupt_bytes = b"NOT_A_VALID_IMAGE_DATA_123456789"
    with pytest.raises(ImageValidationError):
        preprocess_signature_pipeline(corrupt_bytes)


def test_tiny_image_rejected():
    """Confirm that images smaller than 5x5 pixels are safely rejected."""
    tiny_img = Image.new("RGB", (3, 3), color=(200, 200, 200))
    with pytest.raises(ImageValidationError):
        preprocess_signature_pipeline(tiny_img)


def test_no_educational_pages_remain_in_workspace():
    """Confirm that the pages/ directory contains no leftover syllabus/viva/doc files."""
    pages_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "pages")
    if os.path.exists(pages_dir):
        files = [f for f in os.listdir(pages_dir) if f.endswith(".py")]
        assert len(files) == 0, f"Found unexpected pages in {pages_dir}: {files}"


def test_app_py_contains_no_academic_study_portal_text():
    """Confirm that app.py does not contain academic syllabus or course metadata text."""
    app_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app.py")
    with open(app_path, "r", encoding="utf-8") as f:
        content = f.read().lower()

    banned_phrases = [
        "linear algebra syllabus integration",
        "unit 1: vector spaces",
        "unit 2: linear maps",
        "unit 3: inner products and eigenspaces",
        "viva preparation",
        "max marks: 20",
        "submission deadline",
        "group size: 2",
    ]
    for phrase in banned_phrases:
        assert phrase not in content, f"Found banned educational phrase in app.py: '{phrase}'"


def test_streamlit_app_comparison_flow():
    """Verify that Streamlit app renders, loads presets, and runs comparison without exceptions."""
    from streamlit.testing.v1 import AppTest
    app_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app.py")
    at = AppTest.from_file(app_path)
    at.run(timeout=30)
    assert len(at.exception) == 0, f"App load exceptions: {[e.value for e in at.exception]}"

    # Select Author A genuine pair preset
    assert len(at.selectbox) >= 2
    at.selectbox[1].select("Author A: Genuine vs Genuine (Same Writer)")
    at.run(timeout=30)
    assert len(at.exception) == 0

    # Click COMPARE SIGNATURES button
    compare_btn = None
    for b in at.button:
        if "COMPARE SIGNATURES" in b.label:
            compare_btn = b
            break
    assert compare_btn is not None
    compare_btn.click()
    at.run(timeout=30)
    assert len(at.exception) == 0, f"Compare exceptions: {[e.value for e in at.exception]}"

