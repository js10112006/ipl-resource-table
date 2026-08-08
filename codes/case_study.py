import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Case Study 1 Parameters ---
s1_total = 214  # GT First Innings Score (20 overs)
overs_shortened = 15.0

# DLS vs. Proposed Model Targets
dls_target = 171
dls_rrr = dls_target / overs_shortened  # 11.40 rpo

model_target = 197
model_rrr = model_target / overs_shortened  # 13.13 rpo

gt_rrr = s1_total / 20.0  # Original 1st innings rate (10.70 rpo)

# Overs array for 2nd innings (0 to 15 overs)
overs = np.linspace(0, 15, 16)

# Projected Cumulative Par Scores over 15 overs
gt_projected = gt_rrr * overs
dls_par = dls_rrr * overs
model_par = model_rrr * overs

# --- Figure Setup ---
plt.figure(figsize=(11, 6.2), dpi=300)
ax = plt.subplot(111)

ax.set_facecolor('#FFFFFF')
ax.grid(True, linestyle='--', linewidth=0.5, color='#E0E0E0', zorder=1)

# Color Scheme
color_gt = '#708090'       # Slate Gray (GT Benchmark)
color_dls = '#B22222'      # Crimson Red (Standard DLS)
color_model = '#1B365D'    # Deep Navy (Proposed Model)

# --- Plot Lines ---
# 1. First Innings Baseline Rate (GT 214/4 Pace)
ax.plot(overs, gt_projected, color=color_gt, linestyle=':', linewidth=1.8, label=f"GT 1st Innings Pace (214/4 in 20 ov | {gt_rrr:.2f} rpo)", zorder=2)

# 2. Standard DLS Target Path
ax.plot(overs, dls_par, color=color_dls, linestyle='--', linewidth=2.2, label=f"Standard DLS Par Path (Target: {dls_target} | {dls_rrr:.2f} rpo)", zorder=3)

# 3. Proposed Model Target Path
ax.plot(overs, model_par, color=color_model, linestyle='-', linewidth=2.5, label=f"Proposed Model Par Path (Target: {model_target} | {model_rrr:.2f} rpo)", zorder=4)

# --- Target Highlights at 15 Overs ---
# --- Target Highlights at 15 Overs (FIXED ANNOTATION PLACEMENT) ---

# Point marker for DLS
ax.scatter(15, dls_target, color=color_dls, s=70, zorder=5)
ax.annotate(
    f"Standard DLS Target\n{dls_target} Runs ({dls_rrr:.2f} rpo)", 
    xy=(15, dls_target), 
    xytext=(11.5, dls_target - 22),  # Shifted down/left to avoid arrow intersection
    fontsize=9.0, 
    fontweight='bold', 
    color=color_dls,
    arrowprops=dict(arrowstyle='->', color=color_dls, lw=1.2)
)

# Point marker for Proposed Model
ax.scatter(15, model_target, color=color_model, s=80, zorder=5)
ax.annotate(
    f"Proposed Model Target\n{model_target} Runs ({model_rrr:.2f} rpo)\n[+26 Runs Equity Adjustment]", 
    xy=(15, model_target), 
    xytext=(9.8, model_target + 8),  # Shifted left/down so it doesn't clip the top boundary
    fontsize=9.0, 
    fontweight='bold', 
    color=color_model,
    arrowprops=dict(arrowstyle='->', color=color_model, lw=1.2)
)
# --- Shade the DLS "Undervaluation Deficit" Zone ---
ax.fill_between(overs, dls_par, model_par, color=color_model, alpha=0.08, label="Model Equity Correction (+26 Runs)")

# --- Formatting ---
ax.set_xlabel("Overs Bowled in 2nd Innings", fontsize=10.5, fontweight="bold", color="#222222", labelpad=8)
ax.set_ylabel("Cumulative Runs Required", fontsize=10.5, fontweight="bold", color="#222222", labelpad=8)

ax.set_xlim(0, 15.2)
ax.set_ylim(0, 225)
ax.set_xticks(range(0, 16, 1))
ax.set_yticks(range(0, 226, 25))

# Border styling
for spine in ax.spines.values():
    spine.set_color('#CCCCCC')
    spine.set_linewidth(0.8)

# Legend
legend = ax.legend(loc="upper left", frameon=True, facecolor="#FFFFFF", edgecolor="#CCCCCC", fontsize=9.5)
legend.get_frame().set_linewidth(0.8)

plt.tight_layout()
plt.savefig("case_study_1_shortened_chase.png", dpi=300, bbox_inches="tight")

print("Case study chart successfully saved as 'case_study_1_shortened_chase.png'!")