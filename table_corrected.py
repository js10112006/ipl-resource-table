import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Paths
input_file = 'ipl_empirical_resource_table.csv'
corrected_output_file = 'ipl_empirical_table_corrected.csv'

def process_and_visualize():
    if not os.path.exists(input_file):
        print(f"Error: '{input_file}' not found. Please generate it first.")
        return

    # Load data
    res_df = pd.read_csv(input_file, index_col=0)
    
    # Force columns to look like clean string names to avoid type mismatch
    res_df.columns = [str(col).replace('Wickets Lost: ', '').strip() for col in res_df.columns]

    # ---------------------------------------------------------
    # PART 1: Monotonicity Boundary Correction
    # ---------------------------------------------------------
    print("Applying monotonicity bounds... Ensuring resources decay logically as wickets fall.")
    
    # Ball 1 must mathematically start at 100% across the board
    res_df.iloc[0, :] = 100.0
    
    # Loop over every ball delivery (rows) to smooth out inconsistencies
    for ball in res_df.index:
        for wkt in range(1, 10):
            current_val = res_df.loc[ball, str(wkt)]
            prev_wkt_val = res_df.loc[ball, str(wkt - 1)]
            
            if np.isnan(current_val) or np.isnan(prev_wkt_val):
                continue
                
            if current_val > prev_wkt_val:
                res_df.loc[ball, str(wkt)] = prev_wkt_val

    # Save your cleaned mathematical baseline
    res_df.to_csv(corrected_output_file)
    print(f"Corrected baseline saved to '{corrected_output_file}'")

    # ---------------------------------------------------------
    # PART 2: Generating Charts (Completely Explicit - No Loops!)
    # ---------------------------------------------------------
    print("Generating performance and decay comparison charts...")
    sns.set_theme(style="whitegrid")
    
    plt.figure(figsize=(12, 7), dpi=300)
    
    # Explicitly plotting each line independently so colors can never mix with dataframe columns
    plt.plot(res_df.index, res_df['0'], label='IPL Empirical (Wickets Lost: 0)', color='#1a73e8', linewidth=2.5)
    plt.plot(res_df.index, res_df['2'], label='IPL Empirical (Wickets Lost: 2)', color='#34a853', linewidth=2.5)
    plt.plot(res_df.index, res_df['5'], label='IPL Empirical (Wickets Lost: 5)', color='#fbbc05', linewidth=2.5)
    plt.plot(res_df.index, res_df['7'], label='IPL Empirical (Wickets Lost: 7)', color='#ea4335', linewidth=2.5)
        
    # Standard DLS Baseline Simulation Line for Reference (Wickets Lost: 0)
    dls_balls = np.arange(1, 121)
    dls_w0 = (((121 - dls_balls) / 120.0) ** 1.3) * 100
    plt.plot(dls_balls, dls_w0, label='Standard DLS Baseline (Wickets Lost: 0)', color='black', linestyle='--', linewidth=2)

    # Chart Styling
    plt.title('IPL Resource Decay Function vs. Standard DLS Baseline', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Balls Bowled (Progress of Innings)', fontsize=12)
    plt.ylabel('Resource Percentage Remaining (%)', fontsize=12)
    plt.xlim(1, 120)
    plt.ylim(-5, 105)
    plt.legend(loc='upper right', fontsize=10, frameon=True)
    
    # Presentation Annotation Hook
    plt.gca().text(
        0.05, 0.2, 
        'Notice the structural gaps (NaNs)\nin higher wicket tracks.\nThis justifies the entry of our Neural Network!', 
        transform=plt.gca().transAxes, 
        fontsize=11, 
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#fff3cd", edgecolor="#ffeeba", alpha=0.9)
    )

    plt.tight_layout()
    plt.savefig('ipl_resource_decay_chart.png')
    plt.close()
    print("Chart saved successfully as 'ipl_resource_decay_chart.png'")

if __name__ == "__main__":
    process_and_visualize()