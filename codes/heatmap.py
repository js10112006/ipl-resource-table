import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load Data
df_model = pd.read_csv("ipl_final_exponential_table.csv")
df_original = pd.read_csv("original_ball_by_ball.csv")

# 2. Process Overs Columns
if "Balls Bowled" in df_model.columns:
    df_model["Overs Remaining"] = (120 - df_model["Balls Bowled"]) / 6.0
elif "Overs Remaining" not in df_model.columns:
    df_model["Overs Remaining"] = df_model.iloc[:, 0]

# Standardize columns
model_rename = {f"Wickets Lost: {i}": str(i) for i in range(10)}
df_model.rename(columns=model_rename, inplace=True)

# 3. Filter down to integer overs (1 to 20 overs remaining)
df_model["Over_Int"] = df_model["Overs Remaining"].round()
df_orig_int = df_original.copy()
df_orig_int["Over_Int"] = df_orig_int["Overs Remaining"].round()

# Group by integer overs
model_overs = df_model.groupby("Over_Int")[[str(i) for i in range(10)]].mean()
orig_overs = df_orig_int.groupby("Over_Int")[[str(i) for i in range(10)]].mean()

# Align range (1 to 20 overs)
overs_range = range(1, 21)
model_overs = model_overs.reindex(overs_range)
orig_overs = orig_overs.reindex(overs_range)

# 4. Compute Absolute Resource Difference (%)
# Difference = Proposed IPL Model - Original DLS Model
diff_matrix = model_overs - orig_overs

# 5. Figure Setup
plt.figure(figsize=(12, 7), dpi=300)
ax = plt.subplot(111)

# Generate Heatmap (Diverging Color Map: Blue = Higher IPL Resources, Red = Lower)
sns.heatmap(
    diff_matrix.T,  # Transpose so Wickets Lost is on Y-axis and Overs on X-axis
    annot=False, 
    fmt=".1f", 
    cmap="vlag", 
    center=0,
    cbar_kws={'label': 'Resource Difference (%) [IPL Model - Original DLS]'},
    linewidths=0.5,
    linecolor="#FFFFFF",
    ax=ax
)

# 6. Formatting & Titles
ax.set_title("Resource Allocation Variance Heatmap (IPL Model vs. Standard DLS)", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Overs Remaining in Innings", fontsize=10.5, fontweight="bold", labelpad=8)
ax.set_ylabel("Wickets Lost", fontsize=10.5, fontweight="bold", labelpad=8)

# Set Y-axis labels from 0 to 9 wickets
ax.set_yticklabels(range(10), rotation=0)

plt.tight_layout()
plt.savefig("resource_difference_heatmap.png", dpi=300, bbox_inches="tight")

print("Heatmap saved successfully as 'resource_difference_heatmap.png'!")