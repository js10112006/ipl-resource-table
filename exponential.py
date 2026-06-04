import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit
import os

# Configuration paths
master_file = 'ipl_ml_master.csv'
final_output_table = 'ipl_final_exponential_table.csv'
final_output_chart = 'ipl_exponential_decay_chart.png'

def dls_decay_formula(b, F, lam):
    """
    Standard Exponential Decay Function
    b: Balls remaining in the innings
    """
    return F * (1.0 - np.exp(-b / lam))

def generate_exponential_model():
    if not os.path.exists(master_file):
        print(f"Error: '{master_file}' not found. Please ensure it exists in your directory.")
        return

    print("Step 1: Loading raw IPL master dataset...")
    df = pd.read_csv(master_file)
    
    # Calculate balls remaining as our independent tracking variable
    df['balls_remaining'] = 120 - df['total_balls_bowled']
    
    fitted_F = {}
    fitted_lambda = {}
    
    # Explicit independent variables to hold Wicket-0 parameters safely
    safe_F0 = 100.0
    safe_lam0 = 50.0
    
    print("Step 2: Fitting exponential curves directly to actual historical data clusters...")
    for wkt in range(0, 10):
        wkt_data = df[df['wickets_lost'] == wkt]
        
        # Fallback parameters if any high-wicket group is extremely sparse
        if len(wkt_data) < 15:
            f_val = float(100.0 * ((10 - wkt) / 10.0))
            l_val = float(max(10.0, 50.0 - (wkt * 3)))
        else:
            X_data = wkt_data['balls_remaining'].values
            y_data = wkt_data['resource_pct'].values
            
            try:
                # Sensible baseline initialization guesses [F, lambda]
                p0 = [100.0 * ((10 - wkt) / 10.0), 40.0] 
                bounds = ([0.0, 1.0], [150.0, 200.0])
                
                popt, _ = curve_fit(dls_decay_formula, X_data, y_data, p0=p0, bounds=bounds, maxfev=10000)
                f_val = float(popt)
                l_val = float(popt[1])
            except Exception:
                f_val = float(100.0 * ((10 - wkt) / 10.0))
                l_val = float(max(10.0, 50.0 - (wkt * 3)))
                
        # Assign values directly to tracking dictionaries
        fitted_F[wkt] = f_val
        fitted_lambda[wkt] = l_val
        
        # Cache wicket-0 variables strictly outside of dictionary logic
        if wkt == 0:
            safe_F0 = f_val
            safe_lam0 = l_val

    print("\n--- Optimized Parametric Results ---")
    print(f"{'Wickets':<10}{'Resource Factor (F)':<25}{'Decay Scale (lambda)':<20}")
    for wkt in range(10):
        print(f"{wkt:<10}{fitted_F[wkt]:<25.4f}{fitted_lambda[wkt]:<20.4f}")

    print("\nStep 3: Compiling continuous matrix using optimized equations...")
    grid_data = {wkt: [] for wkt in range(0, 10)}
    
    # ADJUSTED AXIS: Start loop from 0 balls bowled up to 120 balls bowled
    balls_axis = list(range(0, 121))
    
    # Baseline unscaled value sampled at match start (120 balls remaining)
    initial_0_wkt_val = dls_decay_formula(120, safe_F0, safe_lam0)

    for ball in balls_axis:
        balls_remaining = 120 - ball
        for wkt in range(0, 10):
            if balls_remaining == 0:
                grid_data[wkt].append(0.0)
                continue
                
            current_F = float(fitted_F[wkt])
            current_lam = float(fitted_lambda[wkt])
            
            # Compute raw mathematical value from curve optimization
            val = dls_decay_formula(balls_remaining, current_F, current_lam)
            
            # Proportional scale for the 0-wicket curve to elegantly hit 100% at ball 0
            if wkt == 0:
                val = (val / initial_0_wkt_val) * 100.0
                
            grid_data[wkt].append(val)

    # Convert to standard DataFrame
    res_df = pd.DataFrame(grid_data, index=balls_axis)
    
    print("Step 4: Executing dimensional consistency sorting...")
    for ball in res_df.index:
        for wkt in range(1, 10):
            if res_df.loc[ball, wkt] > res_df.loc[ball, wkt - 1]:
                res_df.loc[ball, wkt] = res_df.loc[ball, wkt - 1]

    res_df = res_df.clip(lower=0.0, upper=100.0)
    
    # Save clean table to CSV
    save_df = res_df.copy()
    save_df.index.name = 'Balls Bowled'
    save_df.columns = [f'Wickets Lost: {w}' for w in save_df.columns]
    save_df.to_csv(final_output_table)
    print(f"Optimized Lookup table saved successfully to: '{final_output_table}'")

    # ---------------------------------------------------------
    # PART 5: Traditional DLS Chart Generation (Overs Remaining)
    # ---------------------------------------------------------
    print("Step 5: Plotting smooth resource decay curves against overs remaining...")
    sns.set_theme(style="whitegrid")
    
    fig, ax = plt.subplots(figsize=(13, 8), dpi=300)
    
    # Convert balls axis into match OVERS REMAINING (20.0 down to 0.0)
    overs_remaining_axis = (120 - np.array(res_df.index)) / 6.0
    
    palette = sns.color_palette("turbo", 10)
    
    for wkt in range(0, 10):
        ax.plot(
            overs_remaining_axis, 
            res_df[wkt], 
            label=f'Wickets Lost: {wkt}', 
            color=palette[wkt], 
            linewidth=2.4,
            alpha=0.9
        )
        
    # Chart Styling
    ax.set_title('IPL Resource Curves Against Overs Remaining (Proportionally Scaled)', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Overs Remaining in Innings', fontsize=12)
    ax.set_ylabel('Resource Percentage Remaining (%)', fontsize=12)
    
    ax.set_xlim(0, 20)
    ax.set_xticks(range(0, 21, 2)) 
    ax.set_ylim(-5, 105)
    
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1.0), title="Wicket States", title_fontsize=11, fontsize=10, frameon=True)
    
    plt.tight_layout()
    plt.savefig(final_output_chart)
    plt.close()
    print(f"Publication-ready chart saved successfully as: '{final_output_chart}'")

if __name__ == "__main__":
    generate_exponential_model()