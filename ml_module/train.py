import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load dataset
df = pd.read_csv(os.path.join(BASE_DIR, "fitness_dataset_300.csv"))

# Use separate encoders for each column (important for reproducibility)
gender_le = LabelEncoder()
goal_le = LabelEncoder()
activity_le = LabelEncoder()
experience_le = LabelEncoder()
workout_le = LabelEncoder()
diet_le = LabelEncoder()

df['gender'] = gender_le.fit_transform(df['gender'])
df['goal'] = goal_le.fit_transform(df['goal'])
df['activity_level'] = activity_le.fit_transform(df['activity_level'])
df['experience_level'] = experience_le.fit_transform(df['experience_level'])
df['workout_type'] = workout_le.fit_transform(df['workout_type'])
df['diet_type'] = diet_le.fit_transform(df['diet_type'])

print("Gender classes:", list(gender_le.classes_))
print("Goal classes:", list(goal_le.classes_))
print("Activity classes:", list(activity_le.classes_))
print("Experience classes:", list(experience_le.classes_))
print("Workout classes:", list(workout_le.classes_))
print("Diet classes:", list(diet_le.classes_))

# Features
X = df[['age', 'gender', 'height', 'weight', 'bmi',
        'goal', 'activity_level', 'experience_level']]

# Targets
y_workout = df['workout_type']
y_diet = df['diet_type']

# -------- WORKOUT MODEL --------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_workout, test_size=0.2, random_state=42
)

workout_model = RandomForestClassifier()
workout_model.fit(X_train, y_train)

y_pred = workout_model.predict(X_test)
print("\nWorkout Accuracy:", accuracy_score(y_test, y_pred))

# -------- DIET MODEL --------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_diet, test_size=0.2, random_state=42
)

diet_model = RandomForestClassifier()
diet_model.fit(X_train, y_train)

y_pred = diet_model.predict(X_test)
print("Diet Accuracy:", accuracy_score(y_test, y_pred))

# -------- SAVE MODELS --------
joblib.dump(workout_model, os.path.join(BASE_DIR, "workout_model.pkl"))
joblib.dump(diet_model, os.path.join(BASE_DIR, "diet_model.pkl"))

print("\nModels saved successfully!")