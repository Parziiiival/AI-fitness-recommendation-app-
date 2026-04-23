from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from ml_module.predict import predict_plan
from .models import FitnessRecord
from .serializers import FitnessRecordSerializer
import math


def _get_session_key(request):
    """Get or create a session key for anonymous tracking."""
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


# ─────────────────────────────────────────────────
# 1. PREDICT — Get AI recommendation
# ─────────────────────────────────────────────────
@csrf_exempt
@api_view(['GET', 'POST'])
def get_recommendation(request):
    """API endpoint to get workout and diet recommendations."""

    if request.method == 'GET':
        return Response({
            "message": "AI Fitness Recommendation API",
            "usage": "Send a POST request with JSON body containing: "
                     "age, gender, height, weight, bmi, goal, "
                     "activity_level, experience_level",
            "example": {
                "age": 25,
                "gender": "male",
                "height": 175,
                "weight": 70,
                "bmi": 22.9,
                "goal": "muscle_gain",
                "activity_level": "high",
                "experience_level": "intermediate"
            }
        })

    # POST request handling
    data = request.data

    # Validate required fields
    required_fields = [
        'age', 'gender', 'height', 'weight',
        'bmi', 'goal', 'activity_level', 'experience_level'
    ]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return Response(
            {"error": f"Missing required fields: {', '.join(missing)}"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        result = predict_plan(data)

        # Save to database for progress tracking
        session_key = _get_session_key(request)
        FitnessRecord.objects.create(
            age=int(data['age']),
            gender=str(data['gender']),
            height=float(data['height']),
            weight=float(data['weight']),
            bmi=float(data['bmi']),
            goal=str(data['goal']),
            activity_level=str(data['activity_level']),
            experience_level=str(data['experience_level']),
            workout=result['workout'],
            diet=result['diet'],
            session_key=session_key,
        )

        return Response(result)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ─────────────────────────────────────────────────
# 2. HISTORY — Progress tracking
# ─────────────────────────────────────────────────
@csrf_exempt
@api_view(['GET', 'DELETE'])
def get_history(request):
    """Get the user's recommendation history for progress tracking."""
    session_key = _get_session_key(request)

    if request.method == 'DELETE':
        FitnessRecord.objects.filter(session_key=session_key).delete()
        return Response({"message": "History cleared."})

    records = FitnessRecord.objects.filter(session_key=session_key)[:50]
    serializer = FitnessRecordSerializer(records, many=True)
    return Response({
        "count": records.count(),
        "records": serializer.data,
    })


# ─────────────────────────────────────────────────
# 3. INSIGHTS — Health analytics
# ─────────────────────────────────────────────────
@csrf_exempt
@api_view(['POST'])
def get_insights(request):
    """Generate health insights based on user data."""
    data = request.data

    required_fields = ['age', 'gender', 'height', 'weight', 'bmi',
                       'goal', 'activity_level']
    missing = [f for f in required_fields if f not in data]
    if missing:
        return Response(
            {"error": f"Missing fields: {', '.join(missing)}"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        age = int(data['age'])
        gender = str(data['gender']).lower()
        height = float(data['height'])
        weight = float(data['weight'])
        bmi = float(data['bmi'])
        goal = str(data['goal']).lower()
        activity_level = str(data['activity_level']).lower()

        # ── BMI Analysis ──
        if bmi < 18.5:
            bmi_category = "Underweight"
            bmi_color = "blue"
            bmi_advice = "Consider a calorie surplus with nutrient-dense foods to reach a healthy weight."
        elif bmi < 25:
            bmi_category = "Normal"
            bmi_color = "green"
            bmi_advice = "Great job! Maintain your current habits with balanced nutrition and regular exercise."
        elif bmi < 30:
            bmi_category = "Overweight"
            bmi_color = "orange"
            bmi_advice = "A moderate calorie deficit combined with regular cardio and strength training can help."
        else:
            bmi_category = "Obese"
            bmi_color = "red"
            bmi_advice = "Consult a healthcare provider. Start with low-impact exercises and gradual dietary changes."

        # ── BMR (Mifflin-St Jeor) ──
        if gender == "male":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161

        # ── TDEE ──
        activity_multipliers = {
            "low": 1.375,
            "medium": 1.55,
            "high": 1.725,
        }
        multiplier = activity_multipliers.get(activity_level, 1.55)
        tdee = round(bmr * multiplier)

        # ── Calorie Target based on Goal ──
        if goal == "fat_loss":
            calorie_target = round(tdee - 500)
            calorie_note = "500 calorie deficit for steady fat loss (~0.45 kg/week)"
        elif goal == "muscle_gain":
            calorie_target = round(tdee + 400)
            calorie_note = "400 calorie surplus to support muscle growth"
        else:
            calorie_target = tdee
            calorie_note = "Maintenance calories to sustain current weight"

        # ── Macronutrient Split ──
        if goal == "muscle_gain":
            protein_pct, carb_pct, fat_pct = 30, 45, 25
        elif goal == "fat_loss":
            protein_pct, carb_pct, fat_pct = 35, 35, 30
        else:
            protein_pct, carb_pct, fat_pct = 25, 45, 30

        protein_g = round((calorie_target * protein_pct / 100) / 4)
        carb_g = round((calorie_target * carb_pct / 100) / 4)
        fat_g = round((calorie_target * fat_pct / 100) / 9)

        # ── Water Intake ──
        water_liters = round(weight * 0.033, 1)

        # ── Ideal Weight Range (BMI 18.5 - 24.9) ──
        height_m = height / 100
        ideal_weight_low = round(18.5 * height_m * height_m, 1)
        ideal_weight_high = round(24.9 * height_m * height_m, 1)

        # ── Health Score (0-100) ──
        health_score = 100
        # BMI penalty
        if bmi < 18.5:
            health_score -= min(20, (18.5 - bmi) * 5)
        elif bmi > 25:
            health_score -= min(30, (bmi - 25) * 3)
        # Age factor
        if age > 50:
            health_score -= (age - 50) * 0.3
        # Activity bonus
        activity_bonus = {"low": -10, "medium": 0, "high": 10}
        health_score += activity_bonus.get(activity_level, 0)
        health_score = max(0, min(100, round(health_score)))

        # ── Weekly Exercise Recommendation ──
        if activity_level == "low":
            exercise_days = 3
            exercise_note = "Start with 3 days/week and gradually increase"
        elif activity_level == "medium":
            exercise_days = 4
            exercise_note = "Maintain 4-5 days/week for optimal results"
        else:
            exercise_days = 5
            exercise_note = "5-6 days/week with adequate rest and recovery"

        # ── Progress Tracking Stats ──
        session_key = _get_session_key(request)
        total_records = FitnessRecord.objects.filter(session_key=session_key).count()

        return Response({
            "bmi_analysis": {
                "value": bmi,
                "category": bmi_category,
                "color": bmi_color,
                "advice": bmi_advice,
                "ideal_weight_range": {
                    "low": ideal_weight_low,
                    "high": ideal_weight_high,
                },
            },
            "calories": {
                "bmr": round(bmr),
                "tdee": tdee,
                "target": calorie_target,
                "note": calorie_note,
            },
            "macros": {
                "protein": {"grams": protein_g, "percent": protein_pct},
                "carbs": {"grams": carb_g, "percent": carb_pct},
                "fat": {"grams": fat_g, "percent": fat_pct},
            },
            "hydration": {
                "liters": water_liters,
                "glasses": round(water_liters / 0.25),
            },
            "exercise": {
                "days_per_week": exercise_days,
                "note": exercise_note,
            },
            "health_score": health_score,
            "total_records": total_records,
        })

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )