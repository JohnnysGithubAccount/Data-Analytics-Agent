import "./Analysis.css";
import { useEffect, useState } from "react";
import { getAnalysis } from "../api/analysis";
import ReactMarkdown from "react-markdown";

export default function Analysis() {
  const [data, setData] = useState([]);
  const markdown = '# Hello, *world*!';

  useEffect(() => {
    getAnalysis()
      .then((res) => setData(res.results))
      .catch(console.error);
  }, []);

  return (
    <div className="analysis-container">
      <h2 className="analysis-title">Data Analysis</h2>

      <div className="analysis-list">
        {data.map((item) => (        
          console.log("Analysis value:", item.analysis, "Type:", typeof item.analysis),
          
          <div key={item.name} className="analysis-row">
            <img src={`http://localhost:8000${item.chart}`} alt={item.name} className="chart-img" />

            <div className="analysis-text">
              <h3>{item.name}</h3>
              <ReactMarkdown>{String(item.analysis)}</ReactMarkdown>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
