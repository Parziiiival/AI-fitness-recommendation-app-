import React, { useState, useEffect, useCallback } from "react";

function Form({ setResult, setError, onFormData }) {
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    age: "",
    gender: "male",
    height: "",
    weight: "",
    goal: "fat_loss",
    activity_level: "medium",
    experience_level: "beginner",
  });
  const [bmi, setBmi] = useState(null);

  // Auto-calculate BMI whenever height or weight changes
  const calculateBmi = useCallback(() => {
    const h = parseFloat(formData.height);
    const w = parseFloat(formData.weight);
    if (h > 0 && w > 0) {
      const heightM = h / 100;
      const value = (w / (heightM * heightM)).toFixed(1);
      setBmi(value);
    } else {
      setBmi(null);
    }
  }, [formData.height, formData.weight]);

  useEffect(() => {
    calculateBmi();
  }, [calculateBmi]);

  const getBmiCategory = (value) => {
    const v = parseFloat(value);
    if (v < 18.5) return "Underweight";
    if (v < 25) return "Normal";
    if (v < 30) return "Overweight";
    return "Obese";
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    // Build the payload with the auto-calculated BMI
    const payload = {
      ...formData,
      age: parseInt(formData.age, 10),
      height: parseFloat(formData.height),
      weight: parseFloat(formData.weight),
      bmi: bmi ? parseFloat(bmi) : 0,
    };

    try {
      const response = await fetch("/api/predict/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Something went wrong. Please try again.");
      } else {
        setResult(data);
        if (onFormData) onFormData(payload);
      }
    } catch (err) {
      setError("Could not connect to the server. Make sure the Django backend is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="glass-card" id="fitness-form-section">
      <div className="card-header">
        <div className="card-icon purple">📋</div>
        <div>
          <h2>Enter Your Details</h2>
          <p>Fill in your body metrics and fitness goal</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="form-grid" id="fitness-form">
        {/* Age */}
        <div className="form-group">
          <label htmlFor="age">Age</label>
          <input
            id="age"
            type="number"
            name="age"
            placeholder="e.g. 25"
            min="10"
            max="100"
            value={formData.age}
            onChange={handleChange}
            required
          />
        </div>

        {/* Gender */}
        <div className="form-group">
          <label htmlFor="gender">Gender</label>
          <select id="gender" name="gender" value={formData.gender} onChange={handleChange}>
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
        </div>

        {/* Height */}
        <div className="form-group">
          <label htmlFor="height">Height (cm)</label>
          <input
            id="height"
            type="number"
            name="height"
            placeholder="e.g. 175"
            min="100"
            max="250"
            step="0.1"
            value={formData.height}
            onChange={handleChange}
            required
          />
        </div>

        {/* Weight */}
        <div className="form-group">
          <label htmlFor="weight">Weight (kg)</label>
          <input
            id="weight"
            type="number"
            name="weight"
            placeholder="e.g. 70"
            min="20"
            max="300"
            step="0.1"
            value={formData.weight}
            onChange={handleChange}
            required
          />
        </div>

        {/* BMI Auto-calculated */}
        <div className="form-group full-width">
          <label>BMI (Auto-calculated)</label>
          <div className="bmi-display">
            <span className="bmi-label">Your BMI</span>
            <span className="bmi-value">{bmi || "—"}</span>
            {bmi && <span className="bmi-category">{getBmiCategory(bmi)}</span>}
          </div>
        </div>

        {/* Goal */}
        <div className="form-group">
          <label htmlFor="goal">Fitness Goal</label>
          <select id="goal" name="goal" value={formData.goal} onChange={handleChange}>
            <option value="fat_loss">Fat Loss</option>
            <option value="muscle_gain">Muscle Gain</option>
            <option value="maintenance">Maintenance</option>
          </select>
        </div>

        {/* Activity Level */}
        <div className="form-group">
          <label htmlFor="activity_level">Activity Level</label>
          <select
            id="activity_level"
            name="activity_level"
            value={formData.activity_level}
            onChange={handleChange}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        {/* Experience Level */}
        <div className="form-group full-width">
          <label htmlFor="experience_level">Experience Level</label>
          <select
            id="experience_level"
            name="experience_level"
            value={formData.experience_level}
            onChange={handleChange}
          >
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>

        {/* Submit */}
        <button type="submit" className="submit-btn" disabled={loading || !bmi} id="submit-btn">
          <span className="btn-content">
            {loading ? (
              <>
                <span className="spinner"></span>
                Analyzing...
              </>
            ) : (
              <>🚀 Get My Fitness Plan</>
            )}
          </span>
        </button>
      </form>
    </section>
  );
}

export default Form;
