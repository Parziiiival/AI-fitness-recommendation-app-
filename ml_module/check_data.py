import pandas as pd

df = pd.read_csv("fitness_dataset_300.csv")

print(df.head())
print("\nGoal distribution:\n", df['goal'].value_counts())
print("\nWorkout distribution:\n", df['workout_type'].value_counts())