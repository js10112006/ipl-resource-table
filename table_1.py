import pandas as pd
import numpy as np
import os

# Configuration
input_file = 'ipl_ml_master.csv'
output_table_file = 'ipl_empirical_resource_table.csv'

def generate_empirical_base_table():
    if not os.path.exists(input_file):
        print(f"Error: '{input_file}' not found. Please run your master generation script first.")
        return

    print("Loading optimized IPL master dataset...")
    df = pd.read_csv(input_file)

    print("Computing historical averages grouped by Ball and Wicket state...")
    # 1. Group by the delivery sequence and the current step-wise wickets lost count
    # Then calculate the mathematical mean of your individual-match normalized resource percentages
    grouped = df.groupby(['total_balls_bowled', 'wickets_lost'])['resource_pct'].mean().reset_index()

    # 2. Pivot the long-form data into a structured 2D matrix layout
    # Rows will be Balls Bowled (1 to 120), Columns will be Wickets Lost (0 to 9)
    resource_table = grouped.pivot(
        index='total_balls_bowled', 
        columns='wickets_lost', 
        values='resource_pct'
    )

    # 3. Ensure all standard T20 structural dimensions are present (1 to 120 balls)
    # If a certain high-wicket state never happened early in an innings, it automatically stays blank (NaN)
    all_balls = list(range(1, 121))
    all_wickets = list(range(0, 10)) # 0 down to 9 down
    
    resource_table = resource_table.reindex(index=all_balls, columns=all_wickets)

    
    # 4. Enforce strict boundary conditions for physical reality consistency
    # At ball 120 (end of over 20), the resource remaining must logically be 0% across all states
    if 120 in resource_table.index:
        resource_table.loc[120, :] = 0.0  # Uses bracket indexing to modify the row values smoothly

    # Rename headers for clean presentation in your research paper
    resource_table.index.name = 'Balls Bowled'
    resource_table.columns = [f'Wickets Lost: {w}' for w in resource_table.columns]

    # Save to your working directory
    resource_table.to_csv(output_table_file)
    
    print("\n--- MATRIX GENERATION SUCCESSFUL ---")
    print(f"Empirical Resource Table saved to: '{output_table_file}'")
    print("\nFirst 10 rows preview (Initial match states):")
    print(resource_table.head(10).round(2)) # Rounded to 2 decimals for clean console view

if __name__ == "__main__":
    generate_empirical_base_table()