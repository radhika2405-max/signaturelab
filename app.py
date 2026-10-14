"""
SignatureLab — AI-Assisted Handwritten Signature Comparison
A focused, modern signature-comparison application that evaluates two handwritten signature
images using image preprocessing and high-dimensional vector similarity metrics.
"""

import os
import io
import datetime
import streamlit as st
import numpy as np
from PIL import Image
import plotly.express as px

from src.image_processing import (
    load_image_to_grayscale,
    extract_signature_bounding_box,
    aspect_preserving_resize,
    pad_to_canonical_canvas,
    to_foreground_representation,
    check_blank_or_uniform,
    ImageValidationError,
    DEFAULT_CANVAS_HEIGHT,
    DEFAULT_CANVAS_WIDTH,
    DEFAULT_MARGIN_PADDING,
)
from src.comparison import compare_signatures
from src.visualizations import plot_difference_heatmap
try:
    from core.ui_helper import init_session_state, render_header, render_privacy_footer
except ImportError:
    from core.ui_helper import init_session_state, render_header
    def render_privacy_footer():
        pass
from core.sample_generator import generate_all_sample_signatures

# Configure page layout
st.set_page_config(
    page_title="SignatureLab — Handwritten Signature Comparison",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state & samples
init_session_state()
generate_all_sample_signatures()

# Render top header
render_header()

# Sample data directory for quick testing
SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "sample_data")
SAMPLE_PRESETS = {
    "Select a preset sample...": None,
    "Author A: Genuine vs Genuine (Same Writer)": ("author_a_genuine_1.png", "author_a_genuine_2.png"),
    "Author A: Genuine vs Skilled Forgery": ("author_a_genuine_1.png", "author_a_forged.png"),
    "Author B: Genuine vs Genuine (Same Writer)": ("author_b_genuine_1.png", "author_b_genuine_2.png"),
    "Author A vs Author B (Different Writers)": ("author_a_genuine_1.png", "author_b_genuine_1.png"),
}

# --- Collapsible Advanced Settings ---
with st.expander("⚙️ Advanced Comparison & Preprocessing Settings", expanded=False):
    st.markdown(
        "<p style='color: #475569; font-size: 0.88rem; margin-bottom: 0.75rem;'>"
        "Optional parameters used for bounding box extraction, canonical canvas normalization, "
        "and similarity thresholding. Default settings are calibrated for standard handwritten signatures."
        "</p>",
        unsafe_allow_html=True
    )
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        canvas_choice = st.selectbox(
            "Canonical Canvas Dimensions (H × W)",
            ["128 × 256 (Standard)", "64 × 128 (Compact)", "256 × 512 (High Resolution)"],
            index=0,
            help="Images are proportionally resized and centered on this standard canvas."
        )
        if "128 × 256" in canvas_choice:
            st.session_state["canvas_height"] = 128
            st.session_state["canvas_width"] = 256
        elif "64 × 128" in canvas_choice:
            st.session_state["canvas_height"] = 64
            st.session_state["canvas_width"] = 128
        else:
            st.session_state["canvas_height"] = 256
            st.session_state["canvas_width"] = 512

    with col_s2:
        padding_choice = st.slider(
            "Stroke Margin Padding (pixels)",
            min_value=0,
            max_value=30,
            value=st.session_state.get("margin_padding", 10),
            step=5,
            help="Safety border added around detected signature ink bounding box."
        )
        st.session_state["margin_padding"] = padding_choice

    with col_s3:
        threshold_choice = st.slider(
            "Provisional Similarity Threshold (τ)",
            min_value=0.50,
            max_value=0.90,
            value=float(st.session_state.get("similarity_threshold", 0.70)),
            step=0.01,
            help="Provisional threshold for high-similarity classification."
        )
        st.session_state["similarity_threshold"] = threshold_choice

    st.markdown(
        "<div style='font-size: 0.8rem; color: #64748b; background: #f8fafc; padding: 6px 12px; border-radius: 6px;'>"
        "ℹ️ <b>Foreground Encoding:</b> Dark ink strokes are inverted and normalized to [0.0, 1.0], while background paper is set to 0.0. "
        "This ensures empty paper does not contribute positively to similarity metrics."
        "</div>",
        unsafe_allow_html=True
    )

# --- Preset Quick-Loader ---
preset_cols = st.columns([2, 1])
with preset_cols[0]:
    selected_preset = st.selectbox(
        "⚡ Quick Test with Built-in Signatures (Optional):",
        list(SAMPLE_PRESETS.keys()),
        index=0,
        help="Select a benchmark signature pair to instantly test the comparison pipeline without uploading files."
    )

if selected_preset != "Select a preset sample...":
    ref_file, test_file = SAMPLE_PRESETS[selected_preset]
    st.session_state["ref_image_source"] = os.path.join(SAMPLE_DIR, ref_file)
    st.session_state["test_image_source"] = os.path.join(SAMPLE_DIR, test_file)
    st.session_state["ref_image_name"] = f"Sample: {ref_file}"
    st.session_state["test_image_name"] = f"Sample: {test_file}"
    # Reset last comparison on preset switch
    st.session_state["last_comparison"] = None

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# --- Main Upload & Preview Cards (Side by Side) ---
card_col1, card_col2 = st.columns(2)

# --- CARD 1: REFERENCE SIGNATURE ---
with card_col1:
    with st.container(border=True):
        st.markdown(
            """
            <div class="upload-card-header">
                <div class="upload-card-title">
                    <span>1️⃣</span> Reference Signature
                </div>
                <span class="card-status-badge badge-ready">Baseline</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        uploaded_ref = st.file_uploader(
            "Upload reference signature (PNG, JPG, JPEG):",
            type=["png", "jpg", "jpeg"],
            key="uploader_ref",
            help="Drag and drop or browse for the baseline reference signature."
        )
        
        if uploaded_ref is not None:
            st.session_state["ref_image_source"] = uploaded_ref
            st.session_state["ref_image_name"] = uploaded_ref.name

        ref_ready = st.session_state.get("ref_image_source") is not None

        if ref_ready:
            st.caption(f"📁 **Active:** {st.session_state.get('ref_image_name', 'Reference Image')}")
            st.image(
                st.session_state["ref_image_source"],
                caption="Reference Signature Preview",
                use_container_width=True
            )
            btn_clear_ref = st.button("🗑️ Remove Reference", key="btn_clear_ref", use_container_width=True)
            if btn_clear_ref:
                st.session_state["ref_image_source"] = None
                st.session_state["ref_image_name"] = "Reference Signature"
                st.session_state["last_comparison"] = None
                st.rerun()
        else:
            st.info("Upload a reference signature above or choose a sample preset.")

# --- CARD 2: TEST SIGNATURE ---
with card_col2:
    with st.container(border=True):
        st.markdown(
            """
            <div class="upload-card-header">
                <div class="upload-card-title">
                    <span>2️⃣</span> Test Signature
                </div>
                <span class="card-status-badge badge-waiting">Comparison</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        uploaded_test = st.file_uploader(
            "Upload test signature (PNG, JPG, JPEG):",
            type=["png", "jpg", "jpeg"],
            key="uploader_test",
            help="Drag and drop or browse for the signature to compare against the reference."
        )
        
        if uploaded_test is not None:
            st.session_state["test_image_source"] = uploaded_test
            st.session_state["test_image_name"] = uploaded_test.name

        test_ready = st.session_state.get("test_image_source") is not None

        if test_ready:
            st.caption(f"📁 **Active:** {st.session_state.get('test_image_name', 'Test Image')}")
            st.image(
                st.session_state["test_image_source"],
                caption="Test Signature Preview",
                use_container_width=True
            )
            btn_clear_test = st.button("🗑️ Remove Test", key="btn_clear_test", use_container_width=True)
            if btn_clear_test:
                st.session_state["test_image_source"] = None
                st.session_state["test_image_name"] = "Test Signature"
                st.session_state["last_comparison"] = None
                st.rerun()
        else:
            st.info("Upload a test signature above or choose a sample preset.")

# --- COMPARE ACTION BUTTON ---
st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

both_images_ready = (st.session_state.get("ref_image_source") is not None and 
                     st.session_state.get("test_image_source") is not None)

btn_compare = st.button(
    "⚡ COMPARE SIGNATURES",
    type="primary",
    disabled=not both_images_ready,
    use_container_width=True
)

if not both_images_ready:
    st.caption("🔒 *Please provide both a Reference Signature and a Test Signature to enable comparison.*")

if btn_compare and both_images_ready:
    try:
        with st.spinner("Analyzing stroke geometry, performing aspect-preserving normalization, and computing vector metrics..."):
            result = compare_signatures(
                st.session_state["ref_image_source"],
                st.session_state["test_image_source"],
                canvas_height=st.session_state["canvas_height"],
                canvas_width=st.session_state["canvas_width"],
                margin_padding=st.session_state["margin_padding"],
                similarity_threshold=st.session_state["similarity_threshold"]
            )
            st.session_state["last_comparison"] = result
            st.session_state["comparisons_count"] += 1

            # Log to session history
            cosine_score = result["metrics"]["cosine_similarity"]
            euclidean_dist = result["metrics"]["euclidean_distance"]
            thresh = st.session_state["similarity_threshold"]

            if cosine_score >= thresh:
                cat_label = "High similarity"
            elif cosine_score >= 0.50:
                cat_label = "Moderate similarity"
            else:
                cat_label = "Low similarity"

            history_entry = {
                "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
                "ref_name": st.session_state.get("ref_image_name", "Ref"),
                "test_name": st.session_state.get("test_image_name", "Test"),
                "cosine": f"{cosine_score:.4f}",
                "euclidean": f"{euclidean_dist:.2f}",
                "category": cat_label
            }
            st.session_state["comparison_history"].append(history_entry)
            st.success("Comparison completed successfully.")

    except ImageValidationError as ive:
        st.session_state["last_comparison"] = {"error": str(ive)}
        st.error(f"⚠️ **Image Preprocessing Error:** {ive}")
    except Exception as exc:
        st.session_state["last_comparison"] = {"error": str(exc)}
        st.error(f"❌ **Comparison Pipeline Error:** {exc}")

# =========================================================================
# --- RESULTS SECTION ---
# =========================================================================
if st.session_state.get("last_comparison") is not None:
    comp = st.session_state["last_comparison"]
    st.markdown("<hr style='margin: 2rem 0 1.5rem 0; border: 0; border-top: 1px solid #e2e8f0;'/>", unsafe_allow_html=True)
    st.subheader("📊 Comparison Results")

    if "error" in comp:
        # Unable to compare state
        st.markdown(
            f"""
            <div class="outcome-banner outcome-unable">
                <div class="outcome-title">⚠️ Unable to Compare</div>
                <div class="outcome-desc">
                    The application could not complete the comparison because an input image failed validation:<br/>
                    <b>{comp['error']}</b><br/>
                    Please verify that both files are legible image files with clearly visible signature ink strokes.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        metrics = comp["metrics"]
        cos_score = float(metrics["cosine_similarity"])
        euc_dist = float(metrics["euclidean_distance"])
        tau = float(st.session_state.get("similarity_threshold", 0.70))

        # Categorize result
        if cos_score >= tau:
            outcome_class = "outcome-high"
            outcome_title = "✅ High Similarity"
            outcome_desc = (
                f"These signatures have a <b>high numerical similarity</b> (Cosine Similarity = <b>{cos_score:.4f}</b>) "
                f"under the selected comparison method. The preprocessed stroke vectors demonstrate strong spatial alignment."
            )
        elif cos_score >= 0.50:
            outcome_class = "outcome-moderate"
            outcome_title = "⚖️ Moderate Similarity"
            outcome_desc = (
                f"These signatures have a <b>moderate numerical similarity</b> (Cosine Similarity = <b>{cos_score:.4f}</b>) "
                f"under the selected comparison method. There is partial stroke overlap with observable spatial discrepancies."
            )
        else:
            outcome_class = "outcome-low"
            outcome_title = "❌ Low Similarity"
            outcome_desc = (
                f"These signatures have a <b>low numerical similarity</b> (Cosine Similarity = <b>{cos_score:.4f}</b>) "
                f"under the selected comparison method. The stroke representations diverge significantly in coordinate distribution."
            )

        # 1. Main Outcome Banner
        st.markdown(
            f"""
            <div class="outcome-banner {outcome_class}">
                <div class="outcome-title">{outcome_title}</div>
                <div class="outcome-desc">{outcome_desc}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # 2. Honest Authenticity Disclaimer
        st.markdown(
            """
            <div class="authenticity-notice">
                <b>Important Comparison Notice:</b> This result measures mathematical vector alignment between 
                preprocessed digital images. <b>This result alone does not establish that they were signed by the same person, 
                nor does it prove forgery or legal authenticity.</b> Natural intra-writer variation, scanning conditions, 
                pen pressure, and image orientation affect numerical similarity.
            </div>
            """,
            unsafe_allow_html=True
        )

        # 3. Two Prominent Metrics Cards
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.markdown(
                f"""
                <div class="metric-card-primary">
                    <div class="metric-card-label">Cosine Similarity</div>
                    <div class="metric-card-val" style="color: {'#15803d' if cos_score >= tau else ('#b45309' if cos_score >= 0.50 else '#b91c1c')};">
                        {cos_score:.4f}
                    </div>
                    <div class="metric-card-sub">
                        Measures how closely the numerical signature representations align (Range: 0.0000 to 1.0000).
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with m_col2:
            st.markdown(
                f"""
                <div class="metric-card-primary">
                    <div class="metric-card-label">Euclidean Distance</div>
                    <div class="metric-card-val" style="color: #0f172a;">
                        {euc_dist:.2f}
                    </div>
                    <div class="metric-card-sub">
                        Measures the numerical difference between processed image vectors. A smaller distance indicates closer numerical representations.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # 4. Optional Technical Details
        with st.expander("🔍 Optional Technical Vector Details", expanded=False):
            t_col1, t_col2, t_col3, t_col4 = st.columns(4)
            t_col1.metric("Vector Dimension", f"{metrics['dimension']:,}")
            t_col2.metric("Reference L2 Norm", f"{metrics['norm_u']:.3f}")
            t_col3.metric("Test L2 Norm", f"{metrics['norm_v']:.3f}")
            t_col4.metric("Subspace Angle (θ)", f"{metrics['angle_degrees']:.2f}°")

        # 5. Visual Image Comparison & Difference Image
        st.markdown("<br/>", unsafe_allow_html=True)
        st.subheader("🖼️ Preprocessed Canvas & Visual Difference")
        st.markdown(
            "<p style='color: #475569; font-size: 0.9rem; margin-bottom: 0.75rem;'>"
            "Below are the canonical preprocessed representations (strokes normalized to bright foreground, paper to background zero), "
            "alongside a spatial difference heatmap highlighting coordinate stroke discrepancies."
            "</p>",
            unsafe_allow_html=True
        )

        ref_fg = comp["ref_prep"]["foreground_matrix"]
        test_fg = comp["test_prep"]["foreground_matrix"]

        img_col1, img_col2, img_col3 = st.columns(3)
        with img_col1:
            st.image(
                ref_fg,
                caption=f"Reference Canonical Canvas ({comp['canvas_shape'][0]}×{comp['canvas_shape'][1]})",
                clamp=True,
                use_container_width=True
            )
        with img_col2:
            st.image(
                test_fg,
                caption=f"Test Canonical Canvas ({comp['canvas_shape'][0]}×{comp['canvas_shape'][1]})",
                clamp=True,
                use_container_width=True
            )
        with img_col3:
            fig_diff = plot_difference_heatmap(ref_fg, test_fg)
            st.plotly_chart(fig_diff, use_container_width=True)

        st.caption(
            "💡 **Understanding Difference Heatmaps:** Highlighted red pixels reflect coordinate variations between strokes. "
            "Differences can arise from handwriting speed, pen stroke thickness, scanner resolution, or slight rotational misalignment."
        )

        # 6. Action Buttons
        st.markdown("<br/>", unsafe_allow_html=True)
        act_col1, act_col2, act_col3, act_col4 = st.columns(4)
        with act_col1:
            if st.button("🔄 Compare Another Pair", use_container_width=True):
                st.session_state["ref_image_source"] = None
                st.session_state["test_image_source"] = None
                st.session_state["ref_image_name"] = "Reference Signature"
                st.session_state["test_image_name"] = "Test Signature"
                st.session_state["last_comparison"] = None
                st.rerun()

        with act_col2:
            if st.button("📁 Replace Reference Image", use_container_width=True):
                st.session_state["ref_image_source"] = None
                st.session_state["ref_image_name"] = "Reference Signature"
                st.session_state["last_comparison"] = None
                st.rerun()

        with act_col3:
            if st.button("📁 Replace Test Image", use_container_width=True):
                st.session_state["test_image_source"] = None
                st.session_state["test_image_name"] = "Test Signature"
                st.session_state["last_comparison"] = None
                st.rerun()

        with act_col4:
            if st.button("🗑️ Clear Comparison", use_container_width=True):
                st.session_state["last_comparison"] = None
                st.rerun()

        # 7. Download Comparison Reports
        st.markdown("<br/>", unsafe_allow_html=True)
        st.subheader("📄 Export Formal Academic Report")
        rep_col1, rep_col2 = st.columns(2)
        with rep_col1:
            try:
                from core.report_generator import generate_pdf_report
                report_data = {
                    **comp["metrics"],
                    "canvas_shape": f"{comp['canvas_shape'][0]} x {comp['canvas_shape'][1]}",
                }
                pdf_report_bytes = generate_pdf_report(report_data)
                st.download_button(
                    label="📥 Download Academic Report (PDF)",
                    data=pdf_report_bytes,
                    file_name=f"SignatureLab_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e_pdf:
                st.caption(f"PDF generation note: {e_pdf}")

        with rep_col2:
            try:
                from core.report_generator import generate_docx_report, DOCX_AVAILABLE
                if DOCX_AVAILABLE:
                    report_data = {
                        **comp["metrics"],
                        "canvas_shape": f"{comp['canvas_shape'][0]} x {comp['canvas_shape'][1]}",
                    }
                    docx_report_bytes = generate_docx_report(report_data)
                    st.download_button(
                        label="📥 Download Academic Report (Word DOCX)",
                        data=docx_report_bytes,
                        file_name=f"SignatureLab_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
            except Exception:
                pass

# =========================================================================
# --- SESSION COMPARISON HISTORY ---
# =========================================================================
if st.session_state.get("comparison_history"):
    st.markdown("<hr style='margin: 2rem 0 1.5rem 0; border: 0; border-top: 1px solid #e2e8f0;'/>", unsafe_allow_html=True)
    with st.expander(f"🕒 Recent Comparisons in this Session ({len(st.session_state['comparison_history'])})", expanded=False):
        st.markdown(
            "<p style='color: #64748b; font-size: 0.85rem;'>"
            "History is maintained only in memory for this active session. No images or logs are stored permanently."
            "</p>",
            unsafe_allow_html=True
        )
        h_cols = st.columns([1, 2, 2, 1, 1, 1.5])
        h_cols[0].markdown("**Time**")
        h_cols[1].markdown("**Reference**")
        h_cols[2].markdown("**Test**")
        h_cols[3].markdown("**Cosine**")
        h_cols[4].markdown("**Distance**")
        h_cols[5].markdown("**Outcome**")

        for item in reversed(st.session_state["comparison_history"]):
            r_cols = st.columns([1, 2, 2, 1, 1, 1.5])
            r_cols[0].write(item["timestamp"])
            r_cols[1].write(item["ref_name"])
            r_cols[2].write(item["test_name"])
            r_cols[3].write(item["cosine"])
            r_cols[4].write(item["euclidean"])
            r_cols[5].write(item["category"])

        if st.button("🗑️ Clear History", key="btn_clear_history"):
            st.session_state["comparison_history"] = []
            st.rerun()

# Render privacy notice and footer
render_privacy_footer()
