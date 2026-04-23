import React from "react";

const WORKOUT_INFO = {
  cardio: {
    icon: "🏃",
    description: "Cardiovascular exercises like running, cycling, and swimming to improve heart health and burn calories.",
  },
  hiit: {
    icon: "⚡",
    description: "High-Intensity Interval Training — short bursts of intense exercise alternated with recovery periods.",
  },
  strength_training: {
    icon: "💪",
    description: "Resistance exercises using bodyweight, bands, or machines to build muscular strength and endurance.",
  },
  weight_training: {
    icon: "🏋️",
    description: "Progressive overload with free weights and machines to build muscle mass and increase power.",
  },
  yoga: {
    icon: "🧘",
    description: "Mind-body practice combining poses, breathing, and meditation for flexibility and stress relief.",
  },
};

const DIET_INFO = {
  balanced: {
    icon: "🥗",
    description: "A well-rounded diet with proportional macros — ideal for maintaining overall health and energy.",
  },
  calorie_deficit: {
    icon: "📉",
    description: "Reduced calorie intake while maintaining nutrition — designed for steady and healthy weight loss.",
  },
  high_protein: {
    icon: "🥩",
    description: "Protein-rich meals to support muscle repair, growth, and recovery after intense training.",
  },
  low_carb: {
    icon: "🥑",
    description: "Reduced carbohydrate intake, focusing on proteins and healthy fats for sustained energy.",
  },
};

function formatLabel(value) {
  if (!value) return "";
  return value
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

function Result({ result }) {
  if (!result) return null;

  const workout = WORKOUT_INFO[result.workout] || { icon: "🏅", description: "" };
  const diet = DIET_INFO[result.diet] || { icon: "🍽️", description: "" };

  return (
    <section className="glass-card animate-in" id="results-section">
      <div className="card-header">
        <div className="card-icon green">✨</div>
        <div>
          <h2>Your Personalized Plan</h2>
          <p>Based on your metrics, here's what we recommend</p>
        </div>
      </div>

      <div className="results-grid">
        {/* Workout Card */}
        <div className="result-card workout" id="workout-result">
          <span className="result-icon">{workout.icon}</span>
          <div className="result-label">Recommended Workout</div>
          <div className="result-value">{formatLabel(result.workout)}</div>
          <p className="result-description">{workout.description}</p>
        </div>

        {/* Diet Card */}
        <div className="result-card diet" id="diet-result">
          <span className="result-icon">{diet.icon}</span>
          <div className="result-label">Recommended Diet</div>
          <div className="result-value">{formatLabel(result.diet)}</div>
          <p className="result-description">{diet.description}</p>
        </div>
      </div>

      {result.workout_plan && (
        <div className="detailed-plan-section animate-in">
          <div className="plan-header">
            <span className="plan-icon">📅</span>
            <h3>Your 7-Day Workout Split</h3>
          </div>
          <div className="workout-plan-grid">
            {result.workout_plan.map((dayPlan, index) => (
              <div key={index} className={`day-card ${dayPlan.title.includes('Rest') ? 'rest-day' : 'active-day'}`}>
                <div className="day-header">
                  <span className="day-name">{dayPlan.day}</span>
                  <span className="day-title">{dayPlan.title}</span>
                </div>
                <ul className="exercise-list">
                  {dayPlan.exercises.map((exercise, i) => (
                    <li key={i}>
                      <span className="bullet">•</span>
                      {exercise}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}

export default Result;
