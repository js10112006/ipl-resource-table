import pandas as pd
import glob
import os

# 1. Setup paths
path = '/home/js_1010/Documents/coding/programming/DLS_2026/ipl_csv2' # Change this to your folder path
all_files = glob.glob(os.path.join(path, "*.csv"))
li = []

print(f"Starting to process {len(all_files)} files...")

for filename in all_files:
    if 'info' in filename: continue
    
    try:
        df = pd.read_csv(filename)
        
        # We only care about the first innings for the "Resource Base"
        df = df[df['innings'] == 1].copy()
        if df.empty: continue

        # A: Total runs on that specific ball (bat + extras)
        df['ball_runs'] = df['runs_off_bat'] + df['extras']
        
        # B: Current Wickets Lost (Cumulative)
        # Check 'player_dismissed' for any name entry
        df['is_wicket'] = df['player_dismissed'].notnull().astype(int)
        df['wickets_lost'] = df['is_wicket'].cumsum()
        
        # C: Convert Ball decimal to 'Balls Bowled' 
        # (Handles 0.1 through 19.6+)
        df['over_val'] = df['ball'].astype(int)
        df['ball_val'] = ((df['ball'] * 10) % 10).astype(int)
        df['total_balls_bowled'] = (df['over_val'] * 6) + df['ball_val']
        
        # D: Calculate Target (Runs to Come)
        total_score = df['ball_runs'].sum()
        df['runs_so_far'] = df['ball_runs'].cumsum()
        df['runs_to_come'] = total_score - df['runs_so_far'] + df['ball_runs'] # Include current ball asset
        
        
        # Normalize dynamically against THIS specific match's total score
        df['resource_pct'] = (df['runs_to_come'] / total_score) * 100
        # ------------------------------
        
        # E: Store features for ML matrix formatting
        li.append(df[['match_id', 'total_balls_bowled', 'wickets_lost', 'runs_to_come', 'resource_pct']])
        
    except Exception as e:
        print(f"Error processing {filename}: {e}")

# 2. Merge and Save
master_df = pd.concat(li, axis=0, ignore_index=True)

# Clean boundary clipping to maintain clean mathematical ranges
master_df['resource_pct'] = master_df['resource_pct'].clip(lower=0.0, upper=100.0)

master_df.to_csv('ipl_ml_master.csv', index=False)

print("Done! 'ipl_ml_master.csv' is ready for Approach B.")