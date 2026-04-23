import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("fitness_dataset_300.csv")

# Create encoders
le = LabelEncoder()

# Convert categorical columns
df['gender'] = le.fit_transform(df['gender'])
df['goal'] = le.fit_transform(df['goal'])
df['activity_level'] = le.fit_transform(df['activity_level'])
df['experience_level'] = le.fit_transform(df['experience_level'])
df['workout_type'] = le.fit_transform(df['workout_type'])
df['diet_type'] = le.fit_transform(df['diet_type'])

# Define features (inputs)
X = df[['age', 'gender', 'height', 'weight', 'bmi',
        'goal', 'activity_level', 'experience_level']]

# Define labels (outputs)
y_workout = df['workout_type']
y_diet = df['diet_type']

print("Features:\n", X.head())
print("\nWorkout Labels:\n", y_workout.head())
