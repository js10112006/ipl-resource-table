import pandas as pd

# 1. Complete Table 2 Data (0-9 Wickets)
table2_data = {
    "Overs Available": [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
    "0": [100.0, 96.1, 92.2, 88.2, 84.1, 79.9, 75.4, 71.0, 66.4, 61.7, 56.7, 51.8, 46.6, 41.3, 35.9, 30.4, 24.6, 18.7, 12.7, 6.4],
    "1": [96.8, 93.3, 89.6, 85.7, 81.8, 77.9, 73.7, 69.4, 65.0, 60.4, 55.8, 51.1, 45.9, 40.8, 35.5, 30.0, 24.4, 18.6, 12.5, 6.4],
    "2": [92.0, 88.9, 85.6, 82.1, 78.5, 74.8, 70.9, 66.9, 62.7, 58.4, 54.0, 49.5, 44.7, 39.8, 34.8, 29.5, 24.0, 18.3, 12.4, 6.3],
    "3": [84.9, 82.2, 79.4, 76.4, 73.3, 70.0, 66.6, 63.0, 59.2, 55.3, 51.3, 47.1, 42.7, 38.2, 33.5, 28.5, 23.3, 17.8, 12.2, 6.3],
    "4": [76.0, 73.8, 71.5, 69.0, 66.4, 63.6, 60.7, 57.6, 54.3, 50.9, 47.4, 43.7, 39.8, 35.7, 31.4, 26.9, 22.1, 17.0, 11.7, 6.1],
    "5": [68.2, 66.6, 65.0, 63.3, 61.3, 59.2, 56.9, 54.4, 51.9, 49.1, 46.1, 42.8, 39.4, 35.5, 31.4, 27.2, 22.4, 17.5, 12.0, 6.2],
    "6": [53.5, 52.4, 51.2, 49.9, 48.5, 47.0, 45.4, 43.6, 41.7, 39.7, 37.5, 35.1, 32.5, 29.7, 26.6, 23.3, 19.6, 15.6, 11.1, 6.0],
    "7": [37.7, 37.1, 36.4, 35.6, 34.8, 33.9, 32.9, 31.8, 30.6, 29.3, 27.9, 26.3, 24.6, 22.7, 20.6, 18.2, 15.6, 12.7, 9.3, 5.3],
    "8": [21.8, 21.6, 21.3, 21.0, 20.6, 20.2, 19.8, 19.3, 18.7, 18.1, 17.4, 16.6, 15.7, 14.7, 13.5, 12.2, 10.7, 8.9, 6.7, 4.0],
    "9": [8.3, 8.3, 8.3, 8.3, 8.3, 8.3, 8.3, 8.3, 8.3, 8.3, 8.3, 8.3, 8.3, 8.3, 8.1, 8.1, 8.0, 7.4, 6.5, 4.4]
}

df2 = pd.DataFrame(table2_data)

# Add 0 Overs remaining (0.0% resources across all wickets)
zero_row = pd.DataFrame([{"Overs Available": 0, **{str(w): 0.0 for w in range(10)}}])
df2 = pd.concat([df2, zero_row], ignore_index=True)

# 2. Build ball-by-ball list (20.0 down to 0.0)
balls_remaining = []
for over in range(20, 0, -1):
    balls_remaining.append(float(over))
    for ball in range(5, 0, -1):
        balls_remaining.append(round((over - 1) + (ball / 6), 2))
balls_remaining.append(0.0)

df2_ball_by_ball = pd.DataFrame({"Overs Remaining": balls_remaining})

# Explicit datatype conversion prevents Pandas UserWarning
df2["Overs Available"] = df2["Overs Available"].astype(float)
df2_ball_by_ball["Overs Remaining"] = df2_ball_by_ball["Overs Remaining"].astype(float)

# 3. Merge and interpolate linearly
df2_ball_by_ball = pd.merge(df2_ball_by_ball, df2, left_on="Overs Remaining", right_on="Overs Available", how="left")
df2_ball_by_ball.drop(columns=["Overs Available"], inplace=True)
df2_ball_by_ball = df2_ball_by_ball.interpolate(method="linear")

# Save final CSV
df2_ball_by_ball.to_csv("original_ball_by_ball.csv", index=False)
print("Ball-by-ball table created successfully without warnings!")
