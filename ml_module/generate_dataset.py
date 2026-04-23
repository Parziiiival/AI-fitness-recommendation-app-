import pandas as pd
import random

data = []

goals = ["fat_loss", "muscle_gain", "maintenance"]
activity_levels = ["low", "medium", "high"]
experience_levels = ["beginner", "intermediate", "advanced"]
genders = ["male", "female"]

def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)

def assign_plan(bmi, goal):
    if goal == "fat_loss":
        if bmi >= 25:
            return "cardio", "calorie_deficit"
        else:
            return "hiit", "low_carb"
    elif goal == "muscle_gain":
        if bmi < 22:
            return "weight_training", "high_protein"
        else:
            return "strength_training", "balanced"
    else:
        return "yoga", "balanced"

for _ in range(300):
    age = random.randint(18, 50)
    gender = random.choice(genders)
    height = round(random.uniform(1.5, 1.9), 2)
    weight = random.randint(50, 100)
    
    bmi = calculate_bmi(weight, height)
    
    goal = random.choice(goals)
    activity = random.choice(activity_levels)
    experience = random.choice(experience_levels)
    
    workout, diet = assign_plan(bmi, goal)
    
    data.append([
        age, gender, height, weight, bmi,
        goal, activity, experience,
        workout, diet
    ])

columns = [
    "age", "gender", "height", "weight", "bmi",
    "goal", "activity_level", "experience_level",
    "workout_type", "diet_type"
]

df = pd.DataFrame(data, columns=columns)

df.to_csv("fitness_dataset_300.csv", index=False)

print("Dataset generated successfully!")