import React from "react";

function Navigation({ activeTab, setActiveTab }) {
  const tabs = [
    { id: "recommend", label: "Get Plan", icon: "🚀" },
    { id: "insights", label: "Health Insights", icon: "📊" },
    { id: "progress", label: "Progress", icon: "📈" },
  ];

  return (
    <nav className="nav-tabs" id="main-navigation">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          className={`nav-tab ${activeTab === tab.id ? "active" : ""}`}
          onClick={() => setActiveTab(tab.id)}
          id={`nav-${tab.id}`}
        >
          <span className="nav-icon">{tab.icon}</span>
          <span className="nav-label">{tab.label}</span>
        </button>
      ))}
    </nav>
  );
}

export default Navigation;
