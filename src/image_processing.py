"""
SignatureLab — Image Processing Pipeline
Implements 8-stage image preprocessing, validation, aspect-preserving canvas normalization,
foreground stroke extraction, and vector flattening.
"""

from typing import Dict, Any, Tuple, Optional, Union
import io
import os
import cv2
import numpy as np
from PIL import Image

DEFAULT_CANVAS_HEIGHT = 128
DEFAULT_CANVAS_WIDTH = 256
DEFAULT_MARGIN_PADDING = 10


class ImageValidationError(Exception):
    """Custom exception raised when an input image fails validation checks."""
    pass


def load_image_to_grayscale(
    image_input: Union[bytes, io.BytesIO, np.ndarray, Image.Image, str]
) -> np.ndarray:
    """
    Stage 1 & 2: Loads an image from various input sources and converts it to a 2D grayscale uint8 array.
    """
    if image_input is None:
        raise ImageValidationError("No image provided. Image input is None.")

    try:
        if isinstance(image_input, np.ndarray):
            if image_input.size == 0:
                raise ImageValidationError("Provided numpy array is empty.")
            if image_input.ndim == 3:
                if image_input.shape[2] == 4:
                    gray = cv2.cvtColor(image_input, cv2.COLOR_BGRA2GRAY)
                elif image_input.shape[2] == 3:
                    gray = cv2.cvtColor(image_input, cv2.COLOR_BGR2GRAY)
                else:
                    raise ImageValidationError(f"Unexpected number of channels: {image_input.shape[2]}")
            elif image_input.ndim == 2:
                gray = image_input.copy()
            else:
                raise ImageValidationError(f"Invalid image array dimension: {image_input.ndim}")
        elif isinstance(image_input, Image.Image):
            pil_gray = image_input.convert("L")
            gray = np.array(pil_gray, dtype=np.uint8)
        elif isinstance(image_input, (bytes, bytearray)):
            np_arr = np.frombuffer(image_input, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
            if img is None:
                raise ImageValidationError("Failed to decode image from bytes. File may be corrupted or unsupported.")
            gray = img
        elif hasattr(image_input, "read"):
            content = image_input.read()
            if hasattr(image_input, "seek"):
                image_input.seek(0)
            if not content:
                raise ImageValidationError("Uploaded image file is empty (0 bytes).")
            np_arr = np.frombuffer(content, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
            if img is None:
                try:
                    pil_img = Image.open(io.BytesIO(content)).convert("L")
                    img = np.array(pil_img, dtype=np.uint8)
                except Exception as exc:
                    raise ImageValidationError(f"Cannot decode image format: {exc}")
            gray = img
        elif isinstance(image_input, str):
            if not os.path.exists(image_input):
                raise ImageValidationError(f"Could not read image from path: {image_input}")
            try:
                with open(image_input, "rb") as f:
                    np_arr = np.frombuffer(f.read(), np.uint8)
                img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
            except Exception:
                img = cv2.imread(image_input, cv2.IMREAD_GRAYSCALE)
            if img is None:
                try:
                    pil_img = Image.open(image_input).convert("L")
                    img = np.array(pil_img, dtype=np.uint8)
                except Exception:
                    pass
            if img is None:
                raise ImageValidationError(f"Could not read image from path: {image_input}")
            gray = img
        else:
            raise ImageValidationError(f"Unsupported image input type: {type(image_input)}")

    except ImageValidationError:
        raise
    except Exception as e:
        raise ImageValidationError(f"Corrupt or unreadable image file: {str(e)}")

    if gray.shape[0] < 5 or gray.shape[1] < 5:
        raise ImageValidationError(f"Image too small ({gray.shape[1]}x{gray.shape[0]}). Must be at least 5x5 pixels.")

    return gray


def check_blank_or_uniform(gray: np.ndarray, std_threshold: float = 2.0) -> None:
    """
    Checks if an image is all-white, all-black, or nearly uniform blank paper.
    """
    std_val = float(np.std(gray))
    if std_val < std_threshold:
        mean_val = float(np.mean(gray))
        if mean_val > 240:
            raise ImageValidationError("Uploaded image appears completely blank/white (no signature strokes detected).")
        elif mean_val < 15:
            raise ImageValidationError("Uploaded image appears completely black (no signature strokes detectable).")
        else:
            raise ImageValidationError(f"Uploaded image is a solid flat color (std={std_val:.2f}). No signature detected.")


def extract_signature_bounding_box(
    gray: np.ndarray,
    margin_padding: int = DEFAULT_MARGIN_PADDING
) -> Tuple[np.ndarray, Tuple[int, int, int, int]]:
    """
    Stage 3: Locates the signature strokes using Otsu's binarization, removes excessive empty margins,
    and returns the cropped bounding region.
    """
    is_light_bg = np.mean(gray) > 127
    stroke_img = cv2.bitwise_not(gray) if is_light_bg else gray.copy()
        
    _, binary_mask = cv2.threshold(stroke_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    points = cv2.findNonZero(binary_mask)
    if points is None or len(points) < 15:
        h, w = gray.shape
        return gray.copy(), (0, 0, w, h)
        
    x, y, w, h = cv2.boundingRect(points)
    
    img_h, img_w = gray.shape
    x_start = max(0, x - margin_padding)
    y_start = max(0, y - margin_padding)
    x_end = min(img_w, x + w + margin_padding)
    y_end = min(img_h, y + h + margin_padding)
    
    cropped = gray[y_start:y_end, x_start:x_end]
    return cropped, (x_start, y_start, x_end - x_start, y_end - y_start)


def aspect_preserving_resize(
    img: np.ndarray,
    target_height: int = DEFAULT_CANVAS_HEIGHT,
    target_width: int = DEFAULT_CANVAS_WIDTH
) -> Tuple[np.ndarray, Tuple[int, int]]:
    """
    Stage 4: Resizes image to fit inside target_height x target_width preserving original aspect ratio.
    """
    h, w = img.shape[:2]
    if h == 0 or w == 0:
        raise ImageValidationError("Cannot resize image with zero height or width.")
        
    scale = min(target_width / w, target_height / h)
    new_w = max(1, int(round(w * scale)))
    new_h = max(1, int(round(h * scale)))
    
    interp = cv2.INTER_AREA if scale < 1.0 else cv2.INTER_CUBIC
    resized = cv2.resize(img, (new_w, new_h), interpolation=interp)
    return resized, (new_h, new_w)


def pad_to_canonical_canvas(
    resized_img: np.ndarray,
    target_height: int = DEFAULT_CANVAS_HEIGHT,
    target_width: int = DEFAULT_CANVAS_WIDTH,
    bg_color: int = 255
) -> np.ndarray:
    """
    Stage 5: Centers resized image on target canvas and pads borders with background color.
    """
    new_h, new_w = resized_img.shape[:2]
    canvas = np.full((target_height, target_width), bg_color, dtype=np.uint8)
    
    x_offset = (target_width - new_w) // 2
    y_offset = (target_height - new_h) // 2
    
    canvas[y_offset:y_offset + new_h, x_offset:x_offset + new_w] = resized_img
    return canvas


def to_foreground_representation(
    padded_canvas: np.ndarray,
    normalize_range: bool = True
) -> np.ndarray:
    """
    Stage 6: Converts padded canvas to foreground stroke representation.
    In raw scanned signatures, paper is white (255) and ink strokes are dark (0).
    In Linear Algebra vector space, background should be 0 so empty space does not
    contribute positively to the dot product or norm.
    """
    inverted = 255.0 - padded_canvas.astype(np.float64)
    inverted[inverted < 15.0] = 0.0
    
    if normalize_range:
        inverted = inverted / 255.0
        
    return inverted


def preprocess_signature_pipeline(
    image_input: Any,
    canvas_height: int = DEFAULT_CANVAS_HEIGHT,
    canvas_width: int = DEFAULT_CANVAS_WIDTH,
    margin_padding: int = DEFAULT_MARGIN_PADDING
) -> Dict[str, Any]:
    """
    Executes the complete, multi-stage image processing pipeline required by Sections 9 & 13:
    1. Read and validate uploaded image
    2. Convert to grayscale
    3. Check uniformity/blankness
    4. Detect signature region and crop empty margins
    5. Resize preserving aspect ratio
    6. Pad to fixed standard canvas (canvas_height x canvas_width)
    7. Generate documented foreground stroke representation
    8. Convert image matrix into high-dimensional vector in R^(mn)
    """
    raw_gray = load_image_to_grayscale(image_input)
    orig_height, orig_width = raw_gray.shape
    
    check_blank_or_uniform(raw_gray)
    
    cropped_gray, bbox = extract_signature_bounding_box(raw_gray, margin_padding=margin_padding)
    
    resized_img, (resized_h, resized_w) = aspect_preserving_resize(
        cropped_gray,
        target_height=canvas_height,
        target_width=canvas_width
    )
    
    padded_canvas = pad_to_canonical_canvas(
        resized_img,
        target_height=canvas_height,
        target_width=canvas_width,
        bg_color=255
    )
    
    foreground_matrix = to_foreground_representation(padded_canvas, normalize_range=True)
    
    if np.sum(foreground_matrix) < 1e-4:
        raise ImageValidationError("Signature strokes could not be isolated from image. Foreground is empty.")
        
    vector = foreground_matrix.flatten()
    
    return {
        "original_gray": raw_gray,
        "original_shape": (orig_height, orig_width),
        "bounding_box": bbox,
        "cropped_gray": cropped_gray,
        "cropped_shape": cropped_gray.shape,
        "resized_img": resized_img,
        "resized_shape": (resized_h, resized_w),
        "padded_canvas": padded_canvas,
        "foreground_matrix": foreground_matrix,
        "canvas_shape": (canvas_height, canvas_width),
        "vector": vector,
        "vector_dimension": len(vector),
    }
