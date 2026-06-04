import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
import os

# Configuration paths
master_file = 'ipl_ml_master.csv'
final_output_table = 'ipl_final_nn_optimized_table.csv'

def train_resource_model():
    if not os.path.exists(master_file):
        print(f"Error: '{master_file}' not found. Please run your data processing script first.")
        return

    print("Step 1: Loading and preparing IPL master dataset...")
    df = pd.read_csv(master_file)
    
    # Extract training features (X) and target outputs (y)
    X = df[['total_balls_bowled', 'wickets_lost']].values
    y = df['resource_pct'].values

    print("Step 2: Building Neural Network Architecture...")
    # A deep MLP structure designed to learn complex, non-linear decay curves
    model = keras.Sequential([
        keras.layers.Input(shape=(2,)),                 # Input: [Balls Bowled, Wickets Lost]
        keras.layers.Dense(128, activation='relu'),     # Hidden Layer 1
        keras.layers.Dense(64, activation='relu'),      # Hidden Layer 2
        keras.layers.Dense(32, activation='relu'),      # Hidden Layer 3
        keras.layers.Dense(1, activation='linear')      # Output Layer: Predicted Resource %
    ])

    print("Step 3: Compiling Model with standard Mean Squared Error loss...")
    # Using 'mse' because its string alias is completely universal across all Keras editions
    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mae']
    )

    print("Step 4: Training the model on historic patterns...")
    # Training for 15 epochs with a batch size of 64 to ensure smooth convergence
    model.fit(X, y, epochs=15, batch_size=64, verbose=1, validation_split=0.1)

    print("Step 5: Using model inference to generate a 100% complete resource grid...")
    
    # Create an empty dictionary structure to hold our clean 120x10 matrix predictions
    grid_data = {wkt: [] for wkt in range(0, 10)}
    balls_axis = list(range(1, 121))
    
    # Loop through every single structural coordinate to predict values
    for ball in balls_axis:
        for wkt in range(0, 10):
            # Special Rule: Ball 1 with 0 Wickets lost must absolutely anchor at 100%
            if ball == 1 and wkt == 0:
                grid_data[wkt].append(100.0)
                continue
                
            # Special Rule: Ball 120 (End of Innings) must absolutely anchor at 0%
            if ball == 120:
                grid_data[wkt].append(0.0)
                continue

            # Pass the coordinate to the trained network for inference
            input_state = np.array([[ball, wkt]])
            predicted_resource = model.predict(input_state, verbose=0)
            grid_data[wkt].append(predicted_resource)

    # Convert the predictions dictionary into a structured pandas DataFrame
    nn_table = pd.DataFrame(grid_data, index=balls_axis)
    
    print("Step 6: Applying final boundary sanitization constraints...")
    # Force logical sorting across columns (Wickets) to guarantee resource decay
    for ball in nn_table.index:
        for wkt in range(1, 10):
            if nn_table.loc[ball, wkt] > nn_table.loc[ball, wkt - 1]:
                nn_table.loc[ball, wkt] = nn_table.loc[ball, wkt - 1]

    # Clip values to ensure no mathematical anomalies outside range
    nn_table = nn_table.clip(lower=0.0, upper=100.0)
    
    # Format layout for presentation
    nn_table.index.name = 'Balls Bowled'
    nn_table.columns = [f'Wickets Lost: {w}' for w in nn_table.columns]
    
    # Save to directory
    nn_table.to_csv(final_output_table)
    print(f"\n--- SUCCESS! ---")
    print(f"Your neural-network-smoothed lookup matrix has been saved to: '{final_output_table}'")
    print("\nFirst 10 rows preview of the AI-filled model:")
    print(nn_table.head(10).round(2))

if __name__ == "__main__":
    train_resource_model()