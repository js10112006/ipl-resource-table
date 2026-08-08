import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Load CSV Files
df_model = pd.read_csv("ipl_final_exponential_table.csv")
df_original = pd.read_csv("original_ball_by_ball.csv")

# 2. Process IPL Model DataFrame
if "Balls Bowled" in df_model.columns:
    df_model["Overs Remaining"] = (120 - df_model["Balls Bowled"]) / 6.0
elif "Overs Remaining" not in df_model.columns:
    df_model["Overs Remaining"] = df_model.iloc[:, 0]

# Standardize column names to '0' through '9'
model_rename_map = {f"Wickets Lost: {i}": str(i) for i in range(10)}
df_model.rename(columns=model_rename_map, inplace=True)

# 3. Sort both DataFrames (Overs Remaining: 0 -> 20)
df_model = df_model.sort_values(by="Overs Remaining", ascending=True).reset_index(drop=True)
df_original = df_original.sort_values(by="Overs Remaining", ascending=True).reset_index(drop=True)

# 4. Professional Figure Setup
plt.figure(figsize=(11, 6.2), dpi=300)
ax = plt.subplot(111)

# Set base whitegrid background manually for clean report aesthetic
ax.set_facecolor('#FFFFFF')
ax.grid(True, linestyle='--', linewidth=0.5, color='#E0E0E0', zorder=1)

# Color Schemes:
# IPL Model: Deep Blue/Navy (#1B365D)
# Original DLS: Dark Crimson Red (#B22222)
color_ipl = '#1B365D'
color_dls = '#B22222'

# 5. Plot Curves for Wickets 0 through 9
for w in range(10):
    w_str = str(w)
    
    # Calculate opacity decay per wicket lost
    alpha_val = 1.0 - (w * 0.075)  # Ranges from 1.0 down to ~0.32
    
    # --- IPL Model (Solid Navy Lines) ---
    if w_str in df_model.columns:
        ax.plot(
            df_model["Overs Remaining"], 
            df_model[w_str], 
            color=color_ipl, 
            linestyle="-",
            linewidth=2.0, 
            alpha=alpha_val,
            zorder=3,
            label="IPL Exponential Model" if w == 0 else "" # Single legend entry
        )
        
    # --- Original DLS Model (Dashed Red Lines) ---
    if w_str in df_original.columns:
        ax.plot(
            df_original["Overs Remaining"], 
            df_original[w_str], 
            color=color_dls, 
            linestyle="--", 
            linewidth=1.4, 
            alpha=alpha_val * 0.85, 
            zorder=2,
            label="Original DLS Model" if w == 0 else "" # Single legend entry
        )

# 6. Professional Axis Typography & Formatting
ax.set_xlabel("Overs Remaining in Innings", fontsize=10.5, fontweight="bold", color="#222222", labelpad=8)
ax.set_ylabel("Resource Percentage Remaining (%)", fontsize=10.5, fontweight="bold", color="#222222", labelpad=8)

# 7. Axes Boundaries & Spines Formatting
ax.set_xlim(0, 20)
ax.set_ylim(-2, 103)
ax.set_xticks(range(0, 21, 2))
ax.set_yticks(range(0, 101, 10))

# Clean box border
for spine in ax.spines.values():
    spine.set_color('#CCCCCC')
    spine.set_linewidth(0.8)

# 8. Clean Custom Legend
legend = ax.legend(
    loc="upper left", 
    frameon=True, 
    facecolor="#FFFFFF", 
    edgecolor="#CCCCCC", 
    fontsize=9.5
)
legend.get_frame().set_linewidth(0.8)

# 9. Overwrite the Monochrome Image File Directly
plt.tight_layout()
plt.savefig("ipl_dls_comparison_monochrome.png", dpi=300, bbox_inches="tight")

print("Successfully updated and replaced 'ipl_dls_comparison_monochrome.png'!")