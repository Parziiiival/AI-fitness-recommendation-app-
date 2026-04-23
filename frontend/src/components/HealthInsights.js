import React, { useState, useEffect } from "react";

function HealthInsights({ userFormData }) {
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (
      userFormData &&
      userFormData.height &&
      userFormData.weight &&
      userFormData.age
    ) {
      fetchInsights(userFormData);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [userFormData]);

  const fetchInsights = async (data) => {
    setLoading(true);
    setError(null);
    try {
      const heightM = parseFloat(data.height) / 100;
      const bmi = (
        parseFloat(data.weight) /
        (heightM * heightM)
      ).toFixed(1);

      const response = await fetch("/api/insights/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...data, bmi: parseFloat(bmi) }),
      });
      const result = await response.json();
      if (!response.ok) {
        setError(result.error || "Failed to get insights");
      } else {
        setInsights(result);
      }
    } catch (err) {
      setError("Could not connect to the server.");
    } finally {
      setLoading(false);
    }
  };

  if (!userFormData || !userFormData.age) {
    return (
      <section className="glass-card" id="insights-empty">
        <div className="card-header">
          <div className="card-icon blue">📊</div>
          <div>
            <h2>Health Insights</h2>
            <p>Fill in your details on the "Get Plan" tab first</p>
          </div>
        </div>
        <div className="empty-state">
          <span className="empty-icon">🔬</span>
          <p>Enter your body metrics to unlock personalized health analytics including calorie needs, macronutrient breakdown, and health score.</p>
        </div>
      </section>
    );
  }

  if (loading) {
    return (
      <section className="glass-card">
        <div className="card-header">
          <div className="card-icon blue">📊</div>
          <div>
            <h2>Health Insights</h2>
            <p>Analyzing your health data...</p>
          </div>
        </div>
        <div className="loading-state">
          <div className="spinner large"></div>
          <p>Calculating your health metrics...</p>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="glass-card">
        <div className="error-message">⚠️ {error}</div>
      </section>
    );
  }

  if (!insights) return null;

  const { bmi_analysis, calories, macros, hydration, exercise, health_score } =
    insights;

  return (
    <div className="insights-container animate-in" id="insights-section">
      {/* Health Score */}
      <section className="glass-card health-score-card">
        <div className="card-header">
          <div className="card-icon green">💚</div>
          <div>
            <h2>Health Score</h2>
            <p>Overall assessment based on your metrics</p>
          </div>
        </div>
        <div className="score-display">
          <div className="score-ring">
            <svg viewBox="0 0 120 120" className="score-svg">
              <circle
                cx="60"
                cy="60"
                r="52"
                fill="none"
                stroke="rgba(255,255,255,0.06)"
                strokeWidth="8"
              />
              <circle
                cx="60"
                cy="60"
                r="52"
                fill="none"
                stroke={
                  health_score >= 80
                    ? "#10b981"
                    : health_score >= 60
                    ? "#f97316"
                    : "#ef4444"
                }
                strokeWidth="8"
                strokeLinecap="round"
                strokeDasharray={`${(health_score / 100) * 327} 327`}
                transform="rotate(-90 60 60)"
                className="score-progress"
              />
            </svg>
            <div className="score-value">{health_score}</div>
            <div className="score-label">/ 100</div>
          </div>
          <div className="score-details">
            <div className="score-tag" style={{
              background: health_score >= 80 ? 'rgba(16,185,129,0.15)' : health_score >= 60 ? 'rgba(249,115,22,0.15)' : 'rgba(239,68,68,0.15)',
              color: health_score >= 80 ? '#10b981' : health_score >= 60 ? '#f97316' : '#ef4444',
            }}>
              {health_score >= 80 ? "Excellent" : health_score >= 60 ? "Good" : "Needs Improvement"}
            </div>
          </div>
        </div>
      </section>

      {/* BMI Analysis */}
      <section className="glass-card">
        <div className="card-header">
          <div className="card-icon orange">⚖️</div>
          <div>
            <h2>BMI Analysis</h2>
            <p>Body Mass Index breakdown</p>
          </div>
        </div>
        <div className="bmi-analysis">
          <div className="bmi-big-value">
            <span className="bmi-number">{bmi_analysis.value}</span>
            <span
              className="bmi-tag"
              data-color={bmi_analysis.color}
            >
              {bmi_analysis.category}
            </span>
          </div>
          <div className="bmi-scale">
            <div className="scale-bar">
              <div className="scale-segment underweight"></div>
              <div className="scale-segment normal"></div>
              <div className="scale-segment overweight"></div>
              <div className="scale-segment obese"></div>
            </div>
            <div className="scale-labels">
              <span>&lt;18.5</span>
              <span>18.5-24.9</span>
              <span>25-29.9</span>
              <span>30+</span>
            </div>
          </div>
          <p className="bmi-advice">{bmi_analysis.advice}</p>
          <div className="ideal-weight">
            <span className="iw-label">Ideal weight range:</span>
            <span className="iw-value">
              {bmi_analysis.ideal_weight_range.low} – {bmi_analysis.ideal_weight_range.high} kg
            </span>
          </div>
        </div>
      </section>

      {/* Calorie & Macro Cards */}
      <div className="insights-grid">
        {/* Calories */}
        <section className="glass-card compact">
          <div className="mini-header">🔥 Daily Calories</div>
          <div className="calorie-stack">
            <div className="calorie-row">
              <span className="cal-label">BMR</span>
              <span className="cal-value">{calories.bmr}</span>
            </div>
            <div className="calorie-row">
              <span className="cal-label">TDEE</span>
              <span className="cal-value">{calories.tdee}</span>
            </div>
            <div className="calorie-row target">
              <span className="cal-label">Target</span>
              <span className="cal-value highlight">{calories.target}</span>
            </div>
          </div>
          <p className="cal-note">{calories.note}</p>
        </section>

        {/* Macros */}
        <section className="glass-card compact">
          <div className="mini-header">🥗 Macronutrients</div>
          <div className="macro-bars">
            <div className="macro-item">
              <div className="macro-info">
                <span className="macro-name">Protein</span>
                <span className="macro-grams">{macros.protein.grams}g</span>
              </div>
              <div className="macro-bar-bg">
                <div
                  className="macro-bar-fill protein"
                  style={{ width: `${macros.protein.percent}%` }}
                ></div>
              </div>
              <span className="macro-pct">{macros.protein.percent}%</span>
            </div>
            <div className="macro-item">
              <div className="macro-info">
                <span className="macro-name">Carbs</span>
                <span className="macro-grams">{macros.carbs.grams}g</span>
              </div>
              <div className="macro-bar-bg">
                <div
                  className="macro-bar-fill carbs"
                  style={{ width: `${macros.carbs.percent}%` }}
                ></div>
              </div>
              <span className="macro-pct">{macros.carbs.percent}%</span>
            </div>
            <div className="macro-item">
              <div className="macro-info">
                <span className="macro-name">Fat</span>
                <span className="macro-grams">{macros.fat.grams}g</span>
              </div>
              <div className="macro-bar-bg">
                <div
                  className="macro-bar-fill fat"
                  style={{ width: `${macros.fat.percent}%` }}
                ></div>
              </div>
              <span className="macro-pct">{macros.fat.percent}%</span>
            </div>
          </div>
        </section>

        {/* Hydration */}
        <section className="glass-card compact">
          <div className="mini-header">💧 Daily Hydration</div>
          <div className="hydration-display">
            <span className="hydration-value">{hydration.liters}L</span>
            <span className="hydration-glasses">{hydration.glasses} glasses</span>
          </div>
        </section>

        {/* Exercise */}
        <section className="glass-card compact">
          <div className="mini-header">🏋️ Weekly Exercise</div>
          <div className="exercise-display">
            <span className="exercise-days">{exercise.days_per_week}</span>
            <span className="exercise-unit">days / week</span>
          </div>
          <p className="cal-note">{exercise.note}</p>
        </section>
      </div>
    </div>
  );
}

export default HealthInsights;
