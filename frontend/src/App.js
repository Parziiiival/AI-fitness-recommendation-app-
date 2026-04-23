import React, { useState } from "react";
import "./App.css";
import Navigation from "./components/Navigation";
import Form from "./components/Form";
import Result from "./components/Result";
import HealthInsights from "./components/HealthInsights";
import ProgressTracker from "./components/ProgressTracker";

function App() {
  const [activeTab, setActiveTab] = useState("recommend");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [userFormData, setUserFormData] = useState(null);

  const handleResult = (data) => setResult(data);
  const handleFormData = (data) => setUserFormData(data);

  return (
    <div className="app">
      {/* Navbar */}
      <nav className="navbar" id="main-navbar">
        <div className="nav-brand">
          <span className="brand-icon">💪</span>
          <h1>AI Fitness <span>Recommender</span></h1>
        </div>
        <Navigation activeTab={activeTab} setActiveTab={setActiveTab} />
      </nav>

      {/* Hero */}
      <header className="hero">
        <h1>Get Your Personalized Fitness Plan</h1>
        <p>Enter your details and let our AI recommend the best workout and diet for you.</p>
      </header>

      {/* Main */}
      <main className="main-content">
        {activeTab === "recommend" && (
          <>
            <Form setResult={handleResult} setError={setError} onFormData={handleFormData} />
            {error && <div className="error-message">⚠️ {error}</div>}
            <Result result={result} />
          </>
        )}
        {activeTab === "insights" && <HealthInsights userFormData={userFormData} />}
        {activeTab === "progress" && <ProgressTracker />}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        Built with <span>AI & Django</span> — Personalized fitness, powered by machine learning.
      </footer>
    </div>
  );
}

export default App;
