"""
Unit tests for src.image_processing
Explicitly verifies requirements 10 through 14:
10. Blank images (white and black)
11. Invalid image files (corrupt, wrong types, too small)
12. Consistent image dimensions (canonical canvas)
13. Empty foreground masks
14. Image preprocessing pipeline
"""

import pytest
import numpy as np
import cv2
from src.image_processing import (
    load_image_to_grayscale,
    extract_signature_bounding_box,
    aspect_preserving_resize,
    pad_to_canonical_canvas,
    to_foreground_representation,
    preprocess_signature_pipeline,
    check_blank_or_uniform,
    ImageValidationError,
)


def test_10_blank_images():
    """Requirement 10: Blank images (all white and all black)."""
    white_img = np.full((100, 100), 255, dtype=np.uint8)
    with pytest.raises(ImageValidationError):
        preprocess_signature_pipeline(white_img)
        
    black_img = np.full((100, 100), 0, dtype=np.uint8)
    with pytest.raises(ImageValidationError):
        preprocess_signature_pipeline(black_img)


def test_11_invalid_image_files():
    """Requirement 11: Invalid image files (corrupt bytes, tiny dimensions, None)."""
    with pytest.raises(ImageValidationError):
        load_image_to_grayscale(None)
        
    with pytest.raises(ImageValidationError):
        load_image_to_grayscale(b"CORRUPT_NOT_AN_IMAGE_STRING")
        
    tiny_img = np.full((3, 3), 100, dtype=np.uint8)
    with pytest.raises(ImageValidationError):
        load_image_to_grayscale(tiny_img)


def test_12_consistent_image_dimensions():
    """Requirement 12: Consistent image dimensions."""
    canvas1 = np.full((150, 300), 255, dtype=np.uint8)
    cv2.line(canvas1, (20, 50), (280, 50), 0, 3)
    
    canvas2 = np.full((80, 400), 255, dtype=np.uint8)
    cv2.circle(canvas2, (200, 40), 30, 0, 3)
    
    p1 = preprocess_signature_pipeline(canvas1, canvas_height=128, canvas_width=256)
    p2 = preprocess_signature_pipeline(canvas2, canvas_height=128, canvas_width=256)
    
    assert p1["canvas_shape"] == (128, 256)
    assert p2["canvas_shape"] == (128, 256)
    assert len(p1["vector"]) == 32768
    assert len(p2["vector"]) == 32768
    assert len(p1["vector"]) == len(p2["vector"])


def test_13_empty_foreground_masks():
    """Requirement 13: Empty foreground masks."""
    # Extremely subtle texture that falls below foreground threshold
    flat_paper = np.full((100, 100), 253, dtype=np.uint8)
    with pytest.raises(ImageValidationError):
        preprocess_signature_pipeline(flat_paper)


def test_14_image_preprocessing():
    """Requirement 14: Image preprocessing (verifying all stages)."""
    # Create valid synthetic signature
    img = np.full((200, 350), 255, dtype=np.uint8)
    cv2.line(img, (50, 100), (300, 120), 10, thickness=4)
    cv2.ellipse(img, (180, 110), (60, 40), 15, 0, 360, 10, thickness=3)
    
    res = preprocess_signature_pipeline(img, canvas_height=128, canvas_width=256)
    
    assert "original_gray" in res
    assert "bounding_box" in res
    assert "cropped_gray" in res
    assert "resized_img" in res
    assert "padded_canvas" in res
    assert "foreground_matrix" in res
    assert "vector" in res
    
    # Paper is 0 and strokes are > 0
    assert np.min(res["foreground_matrix"]) == 0.0
    assert np.max(res["foreground_matrix"]) > 0.5
