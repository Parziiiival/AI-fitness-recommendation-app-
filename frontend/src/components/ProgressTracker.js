import React, { useState, useEffect, useCallback } from "react";

function ProgressTracker() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchHistory = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch("/api/history/");
      const data = await response.json();
      if (!response.ok) {
        setError(data.error || "Failed to load history");
      } else {
        setHistory(data.records || []);
      }
    } catch (err) {
      setError("Could not connect to the server.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  const clearHistory = async () => {
    if (!window.confirm("Are you sure you want to clear all progress history?")) return;
    try {
      await fetch("/api/history/", { method: "DELETE" });
      setHistory([]);
    } catch (err) {
      setError("Failed to clear history.");
    }
  };

  const formatDate = (dateStr) => {
    const d = new Date(dateStr);
    return d.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const formatLabel = (value) => {
    if (!value) return "";
    return value
      .split("_")
      .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
      .join(" ");
  };

  // Get unique BMI values for the chart
  const chartData = [...history].reverse().slice(-10);

  if (loading) {
    return (
      <section className="glass-card">
        <div className="card-header">
          <div className="card-icon blue">📈</div>
          <div>
            <h2>Progress Tracking</h2>
            <p>Loading your history...</p>
          </div>
        </div>
        <div className="loading-state">
          <div className="spinner large"></div>
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

  return (
    <div className="progress-container animate-in" id="progress-section">
      {/* Stats Overview */}
      <section className="glass-card">
        <div className="card-header">
          <div className="card-icon blue">📈</div>
          <div>
            <h2>Progress Tracking</h2>
            <p>Your fitness journey over time</p>
          </div>
          {history.length > 0 && (
            <button className="clear-btn" onClick={clearHistory} id="clear-history-btn">
              🗑️ Clear
            </button>
          )}
        </div>

        {history.length === 0 ? (
          <div className="empty-state">
            <span className="empty-icon">📊</span>
            <p>No records yet. Get your first AI recommendation on the "Get Plan" tab to start tracking progress!</p>
          </div>
        ) : (
          <>
            {/* Summary Stats */}
            <div className="stats-grid">
              <div className="stat-card">
                <span className="stat-number">{history.length}</span>
                <span className="stat-label">Total Plans</span>
              </div>
              <div className="stat-card">
                <span className="stat-number">
                  {history[0] ? history[0].bmi : "—"}
                </span>
                <span className="stat-label">Latest BMI</span>
              </div>
              <div className="stat-card">
                <span className="stat-number">
                  {history[0] ? history[0].weight : "—"}
                </span>
                <span className="stat-label">Latest Weight (kg)</span>
              </div>
              <div className="stat-card">
                <span className="stat-number">
                  {history.length >= 2
                    ? (history[0].weight - history[history.length - 1].weight).toFixed(1)
                    : "—"}
                </span>
                <span className="stat-label">Weight Change (kg)</span>
              </div>
            </div>

            {/* BMI Chart */}
            {chartData.length > 1 && (
              <div className="chart-section">
                <h3 className="chart-title">BMI Trend</h3>
                <div className="simple-chart">
                  {(() => {
                    const bmis = chartData.map((r) => parseFloat(r.bmi));
                    const min = Math.min(...bmis) - 1;
                    const max = Math.max(...bmis) + 1;
                    const range = max - min || 1;
                    return chartData.map((record, i) => {
                      const pct = ((parseFloat(record.bmi) - min) / range) * 100;
                      return (
                        <div key={i} className="chart-bar-wrapper" title={`BMI: ${record.bmi}`}>
                          <div className="chart-bar-value">{record.bmi}</div>
                          <div className="chart-bar-track">
                            <div
                              className="chart-bar-fill"
                              style={{ height: `${Math.max(pct, 8)}%` }}
                            ></div>
                          </div>
                          <div className="chart-bar-label">
                            {new Date(record.created_at).toLocaleDateString("en-US", { month: "short", day: "numeric" })}
                          </div>
                        </div>
                      );
                    });
                  })()}
                </div>
              </div>
            )}

            {/* History Table */}
            <div className="history-table-wrapper">
              <h3 className="chart-title">History</h3>
              <div className="history-table">
                <div className="table-header">
                  <span>Date</span>
                  <span>Weight</span>
                  <span>BMI</span>
                  <span>Goal</span>
                  <span>Workout</span>
                  <span>Diet</span>
                </div>
                {history.map((record) => (
                  <div key={record.id} className="table-row">
                    <span className="cell-date">{formatDate(record.created_at)}</span>
                    <span>{record.weight} kg</span>
                    <span>{record.bmi}</span>
                    <span className="cell-badge">{formatLabel(record.goal)}</span>
                    <span className="cell-badge workout">{formatLabel(record.workout)}</span>
                    <span className="cell-badge diet">{formatLabel(record.diet)}</span>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
      </section>
    </div>
  );
}

export default ProgressTracker;
