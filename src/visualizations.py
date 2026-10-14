"""
SignatureLab — Data Visualizations & Analytics
Generates publication-quality charts using Plotly and Matplotlib satisfying all requirements of Section 17:
- Meaningful title
- Axis labels
- Appropriate legends
- Readable values
- Short interpretation
"""

from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_difference_heatmap(mat_ref: np.ndarray, mat_test: np.ndarray) -> go.Figure:
    """
    Computes and plots the absolute spatial residual error matrix |M_ref - M_test|.
    """
    diff = np.abs(mat_ref.astype(np.float64) - mat_test.astype(np.float64))
    fig = px.imshow(
        diff,
        color_continuous_scale="Reds",
        title="Spatial Residual Error Heatmap: |M_ref - M_test|",
        labels=dict(x="Canvas Columns (x)", y="Canvas Rows (y)", color="Stroke Error")
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        height=320,
        annotations=[
            dict(
                text="Interpretation: Red pixels pinpoint exact coordinate discrepancies between ink strokes.",
                xref="paper", yref="paper",
                x=0.5, y=-0.22, showarrow=False,
                font=dict(size=11, color="#64748b")
            )
        ]
    )
    return fig


def plot_inner_product_energy(mat_ref: np.ndarray, mat_test: np.ndarray) -> go.Figure:
    """
    Plots the Hadamard element-wise product matrix M_ref * M_test.
    """
    hadamard = mat_ref.astype(np.float64) * mat_test.astype(np.float64)
    fig = px.imshow(
        hadamard,
        color_continuous_scale="Viridis",
        title="Inner Product Overlap Energy: u_i × v_i Summand Heatmap",
        labels=dict(x="Canvas Columns (x)", y="Canvas Rows (y)", color="Product Energy")
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        height=320,
        annotations=[
            dict(
                text="Interpretation: Bright cells highlight exact overlapping stroke regions that sum to <u, v>.",
                xref="paper", yref="paper",
                x=0.5, y=-0.22, showarrow=False,
                font=dict(size=11, color="#64748b")
            )
        ]
    )
    return fig


def plot_confusion_matrix(metrics: Dict[str, Any]) -> go.Figure:
    """
    Plots a 2x2 Confusion Matrix heatmap from evaluation metrics.
    """
    cm_data = [[metrics["TP"], metrics["FN"]], [metrics["FP"], metrics["TN"]]]
    fig = px.imshow(
        cm_data,
        labels=dict(x="Predicted Outcome", y="Ground Truth Class", color="Pair Count"),
        x=["Predicted Match", "Predicted Non-Match"],
        y=["Actual Genuine", "Actual Impostor/Forged"],
        text_auto=True,
        color_continuous_scale="Blues",
        title=f"Verification Confusion Matrix (Threshold τ = {metrics['threshold']:.2f})"
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=40),
        height=320,
        annotations=[
            dict(
                text=f"Interpretation: TP={metrics['TP']} | TN={metrics['TN']} | FP={metrics['FP']} | FN={metrics['FN']} (Accuracy={metrics['accuracy']*100:.1f}%)",
                xref="paper", yref="paper",
                x=0.5, y=-0.25, showarrow=False,
                font=dict(size=11, color="#334155")
            )
        ]
    )
    return fig


def plot_score_distributions(df: pd.DataFrame, threshold: float) -> go.Figure:
    """
    Plots score distribution comparing Genuine vs Impostor pairs.
    """
    valid = df.dropna(subset=["cosine_similarity", "expected_match"]).copy()
    valid["Category"] = valid["expected_match"].apply(lambda x: "Genuine" if x else "Impostor/Forged")
    
    fig = px.box(
        valid,
        x="Category",
        y="cosine_similarity",
        color="Category",
        color_discrete_map={"Genuine": "#16a34a", "Impostor/Forged": "#dc2626"},
        points="all",
        title="Cosine Similarity Score Distribution by Verification Category",
        labels={"cosine_similarity": "Cosine Similarity (cos θ)", "Category": "Claimed Category"}
    )
    fig.add_hline(
        y=threshold,
        line_dash="dash",
        line_color="#2563eb",
        annotation_text=f"Decision Threshold τ = {threshold:.2f}"
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=30),
        height=350,
        showlegend=False
    )
    return fig


def plot_far_frr_tradeoff(sweep_df: pd.DataFrame, current_threshold: float) -> go.Figure:
    """
    Plots FAR (False Acceptance Rate) vs FRR (False Rejection Rate) trade-off curve.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sweep_df["threshold"], y=sweep_df["FAR"],
        mode="lines+markers", name="FAR (False Acceptance Rate)",
        line=dict(color="#dc2626", width=2.5)
    ))
    fig.add_trace(go.Scatter(
        x=sweep_df["threshold"], y=sweep_df["FRR"],
        mode="lines+markers", name="FRR (False Rejection Rate)",
        line=dict(color="#2563eb", width=2.5)
    ))
    fig.add_trace(go.Scatter(
        x=sweep_df["threshold"], y=sweep_df["accuracy"],
        mode="lines", name="Overall Accuracy",
        line=dict(color="#16a34a", width=2, dash="dot")
    ))
    fig.add_vline(
        x=current_threshold,
        line_dash="dash", line_color="#7c3aed",
        annotation_text=f"Active τ = {current_threshold:.2f}"
    )
    fig.update_layout(
        title="Biometric Tradeoff: FAR vs FRR across Decision Thresholds",
        xaxis_title="Cosine Similarity Threshold (τ)",
        yaxis_title="Rate (0.0 to 1.0)",
        margin=dict(l=20, r=20, t=40, b=40),
        height=360,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig
