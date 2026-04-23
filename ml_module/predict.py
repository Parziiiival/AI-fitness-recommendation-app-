import joblib
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

workout_model = joblib.load(os.path.join(BASE_DIR, "workout_model.pkl"))
diet_model = joblib.load(os.path.join(BASE_DIR, "diet_model.pkl"))

# --- Encoding maps (alphabetical order, matching LabelEncoder used during training) ---
GENDER_MAP = {"female": 0, "male": 1}
GOAL_MAP = {"fat_loss": 0, "maintenance": 1, "muscle_gain": 2}
ACTIVITY_LEVEL_MAP = {"high": 0, "low": 1, "medium": 2}
EXPERIENCE_LEVEL_MAP = {"advanced": 0, "beginner": 1, "intermediate": 2}

# --- Decoding maps for model output ---
WORKOUT_MAP = {
    0: "cardio",
    1: "hiit",
    2: "strength_training",
    3: "weight_training",
    4: "yoga"
}

DIET_MAP = {
    0: "balanced",
    1: "calorie_deficit",
    2: "high_protein",
    3: "low_carb"
}


def encode_input(data):
    """
    Accept either a dict with string values or a list of pre-encoded numbers.
    Returns a list of numeric values ready for the model.
    """
    if isinstance(data, dict):
        return [
            int(data['age']),
            GENDER_MAP.get(str(data['gender']).lower(), data['gender']),
            float(data['height']),
            float(data['weight']),
            float(data['bmi']),
            GOAL_MAP.get(str(data['goal']).lower(), data['goal']),
            ACTIVITY_LEVEL_MAP.get(str(data['activity_level']).lower(), data['activity_level']),
            EXPERIENCE_LEVEL_MAP.get(str(data['experience_level']).lower(), data['experience_level']),
        ]
    # Already a list of numbers (backward compatible)
    return data


def get_detailed_workout_plan(workout_type, experience_level):
    """Generates a detailed workout split and exercise list based on type and experience."""
    plans = {
        "weight_training": {
            "beginner": [
                {"day": "Day 1", "title": "Full Body A", "exercises": ["Squats (3x8-10)", "Bench Press (3x8-10)", "Bent Over Rows (3x8-10)"]},
                {"day": "Day 2", "title": "Rest", "exercises": ["Active recovery or walking"]},
                {"day": "Day 3", "title": "Full Body B", "exercises": ["Deadlifts (3x5-8)", "Overhead Press (3x8-10)", "Lat Pulldowns (3x10-12)"]},
                {"day": "Day 4", "title": "Rest", "exercises": ["Active recovery or walking"]},
                {"day": "Day 5", "title": "Full Body C", "exercises": ["Leg Press (3x10-12)", "Incline Dumbbell Press (3x10-12)", "Seated Cable Rows (3x10-12)"]},
                {"day": "Day 6", "title": "Rest", "exercises": ["Active recovery"]},
                {"day": "Day 7", "title": "Rest", "exercises": ["Active recovery"]}
            ],
            "intermediate": [
                {"day": "Day 1", "title": "Upper Body", "exercises": ["Bench Press (4x8)", "Pull-ups (4x8-10)", "Overhead Press (3x10)", "Bicep Curls (3x12)"]},
                {"day": "Day 2", "title": "Lower Body", "exercises": ["Squats (4x8)", "Romanian Deadlifts (3x10)", "Leg Press (3x12)", "Calf Raises (4x15)"]},
                {"day": "Day 3", "title": "Rest", "exercises": ["Active recovery"]},
                {"day": "Day 4", "title": "Upper Body", "exercises": ["Incline Bench (4x8)", "Barbell Rows (4x8)", "Lateral Raises (3x15)", "Tricep Extensions (3x12)"]},
                {"day": "Day 5", "title": "Lower Body", "exercises": ["Deadlifts (3x5)", "Leg Extensions (3x15)", "Leg Curls (3x15)", "Ab Rollouts (3x15)"]},
                {"day": "Day 6", "title": "Rest", "exercises": ["Active recovery"]},
                {"day": "Day 7", "title": "Rest", "exercises": ["Active recovery"]}
            ],
            "advanced": [
                {"day": "Day 1", "title": "Push", "exercises": ["Bench Press (4x6)", "Overhead Press (4x8)", "Incline DB Press (3x10)", "Tricep Pushdowns (4x12)"]},
                {"day": "Day 2", "title": "Pull", "exercises": ["Barbell Rows (4x6)", "Pull-ups (4x8)", "Face Pulls (3x15)", "Barbell Curls (4x10)"]},
                {"day": "Day 3", "title": "Legs", "exercises": ["Squats (4x6)", "Leg Press (3x10)", "Leg Extensions (3x15)", "Calf Raises (4x20)"]},
                {"day": "Day 4", "title": "Rest", "exercises": ["Active recovery"]},
                {"day": "Day 5", "title": "Push", "exercises": ["DB Shoulder Press (4x8)", "Dips (3x10)", "Chest Flyes (3x12)", "Skull Crushers (3x12)"]},
                {"day": "Day 6", "title": "Pull", "exercises": ["Deadlifts (1x5)", "Lat Pulldowns (4x10)", "Seated Rows (3x12)", "Hammer Curls (3x12)"]},
                {"day": "Day 7", "title": "Legs", "exercises": ["Bulgarian Split Squats (3x10)", "RDLs (3x10)", "Leg Curls (3x15)", "Hanging Leg Raises (3x15)"]}
            ]
        },
        "hiit": {
            "beginner": [
                {"day": "Day 1", "title": "HIIT Basics", "exercises": ["Jumping Jacks (30s on, 30s off) x 5", "High Knees (30s on, 30s off) x 5"]},
                {"day": "Day 2", "title": "Rest", "exercises": ["Light stretching"]},
                {"day": "Day 3", "title": "Core HIIT", "exercises": ["Mountain Climbers (30s on, 30s off) x 5", "Plank Hold (30s on, 30s off) x 5"]},
                {"day": "Day 4", "title": "Rest", "exercises": ["Light stretching"]},
                {"day": "Day 5", "title": "Full Body HIIT", "exercises": ["Burpees (20s on, 40s off) x 5", "Squat Jumps (20s on, 40s off) x 5"]},
                {"day": "Day 6", "title": "Rest", "exercises": ["Light stretching"]},
                {"day": "Day 7", "title": "Rest", "exercises": ["Light stretching"]}
            ],
            "intermediate": [
                {"day": "Day 1", "title": "HIIT Circuit", "exercises": ["Burpees, Mountain Climbers, Jump Squats (40s on, 20s off) x 4 rounds"]},
                {"day": "Day 2", "title": "Active Rest", "exercises": ["Light Jogging (20 mins)"]},
                {"day": "Day 3", "title": "Tabata", "exercises": ["Kettlebell Swings, Box Jumps (20s on, 10s off) x 8 rounds per exercise"]},
                {"day": "Day 4", "title": "Active Rest", "exercises": ["Yoga or stretching"]},
                {"day": "Day 5", "title": "Sprint Intervals", "exercises": ["Sprint (30s), Walk (60s) x 10 rounds"]},
                {"day": "Day 6", "title": "Core HIIT", "exercises": ["Bicycle Crunches, Russian Twists, Plank (45s on, 15s off) x 4 rounds"]},
                {"day": "Day 7", "title": "Rest", "exercises": ["Full Rest"]}
            ],
            "advanced": [
                {"day": "Day 1", "title": "Explosive Power", "exercises": ["Box Jumps, Burpee Pull-ups, Kettlebell Swings (45s on, 15s off) x 5 rounds"]},
                {"day": "Day 2", "title": "Sprint Intervals", "exercises": ["Sprint (20s), Walk (40s) x 15 rounds"]},
                {"day": "Day 3", "title": "Tabata Core", "exercises": ["V-ups, Mountain Climbers, Hollow Rocks (20s on, 10s off) x 8 rounds"]},
                {"day": "Day 4", "title": "Active Rest", "exercises": ["Light cycling or swimming"]},
                {"day": "Day 5", "title": "Endurance HIIT", "exercises": ["Rowing Machine or Bike (60s all out, 60s recovery) x 10 rounds"]},
                {"day": "Day 6", "title": "Metcon", "exercises": ["Thrusters, Jump Rope, Push-ups (40s on, 20s off) x 5 rounds"]},
                {"day": "Day 7", "title": "Rest", "exercises": ["Full Rest"]}
            ]
        },
        "cardio": {
            "beginner": [
                {"day": "Day 1", "title": "Steady State", "exercises": ["Brisk Walk or Light Jog (20-30 mins)"]},
                {"day": "Day 2", "title": "Rest", "exercises": ["Light stretching"]},
                {"day": "Day 3", "title": "Steady State", "exercises": ["Cycling or Elliptical (20-30 mins)"]},
                {"day": "Day 4", "title": "Rest", "exercises": ["Light stretching"]},
                {"day": "Day 5", "title": "Intervals", "exercises": ["Walk 2 mins, Jog 1 min (x 6 rounds)"]},
                {"day": "Day 6", "title": "Rest", "exercises": ["Light stretching"]},
                {"day": "Day 7", "title": "Rest", "exercises": ["Light stretching"]}
            ],
            "intermediate": [
                {"day": "Day 1", "title": "Steady State", "exercises": ["Jogging or Swimming (40 mins at moderate pace)"]},
                {"day": "Day 2", "title": "Cross Training", "exercises": ["Cycling or Elliptical (30 mins)"]},
                {"day": "Day 3", "title": "Intervals", "exercises": ["Run 3 mins, Walk 1 min (x 8 rounds)"]},
                {"day": "Day 4", "title": "Rest", "exercises": ["Light stretching or Yoga"]},
                {"day": "Day 5", "title": "Tempo Run", "exercises": ["Warm up, 20 mins brisk pace, Cool down"]},
                {"day": "Day 6", "title": "Long Distance", "exercises": ["Slow Jog or Hike (60+ mins)"]},
                {"day": "Day 7", "title": "Rest", "exercises": ["Full Rest"]}
            ],
            "advanced": [
                {"day": "Day 1", "title": "Tempo Run", "exercises": ["Warm up, 30 mins fast/threshold pace, Cool down"]},
                {"day": "Day 2", "title": "Recovery Run", "exercises": ["Easy Jog (30-40 mins)"]},
                {"day": "Day 3", "title": "Intervals", "exercises": ["400m Sprint, 90s Walk (x 8-10 rounds)"]},
                {"day": "Day 4", "title": "Cross Training", "exercises": ["Intense Cycling or Swimming (45 mins)"]},
                {"day": "Day 5", "title": "Fartlek Training", "exercises": ["Continuous run mixing fast and slow segments (45 mins)"]},
                {"day": "Day 6", "title": "Long Distance", "exercises": ["Long Run (90+ mins)"]},
                {"day": "Day 7", "title": "Rest", "exercises": ["Full Rest"]}
            ]
        },
        "strength_training": {
            "beginner": [
                {"day": "Day 1", "title": "Full Body Basics", "exercises": ["Bodyweight Squats (3x10)", "Push-ups (3xMax)", "Dumbbell Rows (3x10)"]},
                {"day": "Day 2", "title": "Rest", "exercises": ["Active recovery"]},
                {"day": "Day 3", "title": "Full Body Basics", "exercises": ["Lunges (3x10/leg)", "Plank (3x30s)", "Glute Bridges (3x12)"]},
                {"day": "Day 4", "title": "Rest", "exercises": ["Active recovery"]},
                {"day": "Day 5", "title": "Full Body Basics", "exercises": ["Goblet Squats (3x10)", "Dumbbell Overhead Press (3x10)", "Bird-Dog (3x10/side)"]},
                {"day": "Day 6", "title": "Rest", "exercises": ["Active recovery"]},
                {"day": "Day 7", "title": "Rest", "exercises": ["Active recovery"]}
            ],
            "intermediate": [
                {"day": "Day 1", "title": "Upper Body", "exercises": ["Barbell Bench Press (3x5)", "Weighted Pull-ups (3x5)", "Barbell Overhead Press (3x8)"]},
                {"day": "Day 2", "title": "Lower Body", "exercises": ["Back Squats (3x5)", "Romanian Deadlifts (3x8)", "Bulgarian Split Squats (3x8/leg)"]},
                {"day": "Day 3", "title": "Rest", "exercises": ["Active recovery"]},
                {"day": "Day 4", "title": "Upper Body", "exercises": ["Incline Dumbbell Press (3x8)", "Pendlay Rows (3x5)", "Dumbbell Lateral Raises (3x12)"]},
                {"day": "Day 5", "title": "Lower Body", "exercises": ["Deadlifts (1x5)", "Front Squats (3x8)", "Hanging Leg Raises (3x10)"]},
                {"day": "Day 6", "title": "Rest", "exercises": ["Active recovery"]},
                {"day": "Day 7", "title": "Rest", "exercises": ["Active recovery"]}
            ],
            "advanced": [
                {"day": "Day 1", "title": "Heavy Push", "exercises": ["Bench Press (5x5)", "Overhead Press (4x6)", "Weighted Dips (3x8)"]},
                {"day": "Day 2", "title": "Heavy Pull", "exercises": ["Weighted Pull-ups (5x5)", "Barbell Rows (4x6)", "Barbell Shrugs (3x10)"]},
                {"day": "Day 3", "title": "Heavy Legs", "exercises": ["Squats (5x5)", "Leg Press (4x8)", "Calf Raises (4x15)"]},
                {"day": "Day 4", "title": "Rest", "exercises": ["Active recovery"]},
                {"day": "Day 5", "title": "Hypertrophy Push/Pull", "exercises": ["Incline Bench (3x10)", "Seated Cable Rows (3x10)", "Lateral Raises (3x15)"]},
                {"day": "Day 6", "title": "Heavy Deadlift & Accessories", "exercises": ["Deadlifts (3x3)", "Front Squats (3x8)", "Ab Rollouts (3x15)"]},
                {"day": "Day 7", "title": "Rest", "exercises": ["Active recovery"]}
            ]
        },
        "yoga": {
            "beginner": [
                {"day": "Day 1", "title": "Foundations", "exercises": ["Sun Salutations A (5 rounds)", "Downward Dog (Hold 5 breaths)", "Child's Pose (Hold 1 min)"]},
                {"day": "Day 2", "title": "Rest/Light Walk", "exercises": ["Active recovery"]},
                {"day": "Day 3", "title": "Balance & Core", "exercises": ["Tree Pose (Hold 30s/leg)", "Plank (Hold 30s)", "Bridge Pose (Hold 5 breaths)"]},
                {"day": "Day 4", "title": "Rest", "exercises": ["Active recovery"]},
                {"day": "Day 5", "title": "Flexibility", "exercises": ["Seated Forward Fold (Hold 1 min)", "Pigeon Pose (Hold 1 min/leg)", "Supine Twist (Hold 1 min/side)"]},
                {"day": "Day 6", "title": "Rest", "exercises": ["Active recovery"]},
                {"day": "Day 7", "title": "Rest", "exercises": ["Active recovery"]}
            ],
            "intermediate": [
                {"day": "Day 1", "title": "Vinyasa Flow", "exercises": ["Sun Salutations A & B (45 mins continuous flow)", "Chaturanga Practice"]},
                {"day": "Day 2", "title": "Hatha Yoga", "exercises": ["Warrior I, II, III (Hold 1 min each)", "Triangle Pose (Hold 1 min/side)"]},
                {"day": "Day 3", "title": "Core & Inversions", "exercises": ["Boat Pose (Hold 1 min)", "Crow Pose Practice (5 attempts)", "Headstand Prep"]},
                {"day": "Day 4", "title": "Rest", "exercises": ["Meditation or Light stretching"]},
                {"day": "Day 5", "title": "Power Yoga", "exercises": ["Dynamic Flow integrating lunges and twists (45 mins)"]},
                {"day": "Day 6", "title": "Yin Yoga", "exercises": ["Deep holds in Pigeon, Frog, and Dragon poses (3-5 mins each)"]},
                {"day": "Day 7", "title": "Rest", "exercises": ["Meditation"]}
            ],
            "advanced": [
                {"day": "Day 1", "title": "Ashtanga Primary Series", "exercises": ["Full Primary Series practice (60-90 mins)"]},
                {"day": "Day 2", "title": "Advanced Inversions", "exercises": ["Handstand Practice", "Forearm Stand (Pincha Mayurasana)", "Headstand Variations"]},
                {"day": "Day 3", "title": "Deep Backbends", "exercises": ["Wheel Pose (Urdhva Dhanurasana)", "Camel Pose (Ustrasana)", "Bow Pose (Dhanurasana)"]},
                {"day": "Day 4", "title": "Rest/Pranayama", "exercises": ["Breathing exercises and meditation"]},
                {"day": "Day 5", "title": "Power Vinyasa", "exercises": ["60 mins fast-paced flow with arm balances integrated"]},
                {"day": "Day 6", "title": "Yin & Restorative", "exercises": ["Long holds (5+ mins) for deep connective tissue release"]},
                {"day": "Day 7", "title": "Rest", "exercises": ["Full Rest"]}
            ]
        }
    }
    
    level = experience_level.lower() if experience_level else "beginner"
    if level not in ["beginner", "intermediate", "advanced"]:
        level = "beginner"
        
    workout = workout_type.lower() if workout_type else "weight_training"
    if workout not in plans:
        workout = "weight_training"
        
    return plans[workout][level]


def predict_plan(data):
    """
    Predict workout and diet plan from user data.
    `data` can be a dict with human-readable keys or a list of 8 numeric values.
    """
    encoded = encode_input(data)

    columns = ['age', 'gender', 'height', 'weight', 'bmi',
               'goal', 'activity_level', 'experience_level']

    df = pd.DataFrame([encoded], columns=columns)

    workout_pred = workout_model.predict(df)[0]
    diet_pred = diet_model.predict(df)[0]
    
    workout_type = WORKOUT_MAP.get(workout_pred, str(workout_pred))
    diet_type = DIET_MAP.get(diet_pred, str(diet_pred))
    
    experience_level = "beginner"
    if isinstance(data, dict) and 'experience_level' in data:
        experience_level = str(data['experience_level']).lower()
        
    workout_plan = get_detailed_workout_plan(workout_type, experience_level)

    return {
        "workout": workout_type,
        "diet": diet_type,
        "workout_plan": workout_plan
    }