import "./Insights.css";
import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";

export default function InsightsWithCharts() {
  const [insight, setInsight] = useState("");
  const [charts, setCharts] = useState([]);

  useEffect(() => {
    // Load insights
    fetch("http://localhost:8000/insights")
      .then((res) => res.json())
      .then((data) => setInsight(data.content))
      .catch(console.error);

    // Load chart list
    fetch("http://localhost:8000/analysis")
      .then((res) => res.json())
      .then((data) => setCharts(data.results || []))
      .catch(console.error);
  }, []);

  return (
    <div className="insights-container">
      <h2 className="insights-title">AI Insights & Charts</h2>
      <p className="insights-subtitle">
        Explore professional insights alongside the charts.
      </p>

      <div className="insights-content-row">
        <div className="insights-card">
          <div className="insights-content">
            <ReactMarkdown>{insight}</ReactMarkdown>
          </div>
        </div>

        <div className="insights-charts-column">
          {charts.map((item) => (
            <div key={item.name} className="insights-chart-card">
              <img
                src={`http://localhost:8000${item.chart}`}
                alt={item.name}
                className="insights-chart-img"
              />
              <div className="insights-chart-caption">{item.name}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
