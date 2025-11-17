// Upload.jsx
import "./Upload.css";
import { useState, useEffect } from "react";
import { uploadDataset, listUploadedFiles, deleteFile } from "../api/upload";
import GraphPopup from "./GraphOverlay";
import { streamGraph } from "../api/graph_overlay";

export default function Upload() {
  const [prompt, setPrompt] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [selectedUploadedFile, setSelectedUploadedFile] = useState("");
  const [showGraphPopup, setShowGraphPopup] = useState(false);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [activeNodeId, setActiveNodeId] = useState(null);

  // Fetch uploaded files from server
  const fetchUploadedFiles = async () => {
    try {
      const res = await listUploadedFiles();
      setUploadedFiles(res.files || []);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchUploadedFiles(); // initial fetch
    const interval = setInterval(fetchUploadedFiles, 1000);
    return () => clearInterval(interval);
  }, []);

  // Handle file selection
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
    if (file) setSuccessMessage(`✅ Selected file: ${file.name}`);
    else setSuccessMessage("");
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return alert("Please select a file!");

    // Restrict multiple streams
    if (loading) return; // prevent re-entry if analysis is already running

    setShowGraphPopup(true);
    setLoading(true);
    setAnalysisLoading(true);
    setActiveNodeId(null);
    setSuccessMessage("");

    try {
      // Upload the file first
      await uploadDataset(selectedFile, prompt);

      // Stream the graph nodes with a try/catch to safely handle SSE errors
      await new Promise((resolve, reject) => {
        let resolved = false; // ensure we resolve/reject only once

        const sse = streamGraph(
          selectedFile?.name || selectedUploadedFile,
          prompt,
          (node_name) => {
            setActiveNodeId(node_name);
          },
          () => {
            if (!resolved) {
              resolved = true;
              resolve(); // finished
            }
          }
        );

        sse.onerror = (err) => {
          console.error("SSE error:", err);
          if (!resolved) {
            resolved = true;
            reject(err); // reject only once
          }
        };

        // Optional: add a timeout so stream doesn’t run forever
        setTimeout(() => {
          if (!resolved) {
            resolved = true;
            sse.close();
            console.warn("StreamGraph timeout: closing connection.");
            resolve();
          }
        }, 300_000); // 60s max per stream
      });

      setSuccessMessage(`✅ Analysis finished for: ${selectedFile.name}`);
    } catch (err) {
      console.error(err);
      alert("Analysis failed. Check console.");
      setLoading(false);
      setAnalysisLoading(false);
      setShowGraphPopup(false);
    } finally {
      setLoading(false);
      setAnalysisLoading(false);
      setShowGraphPopup(false);
    }
  };

  const handleDelete = async (filename) => {
    if (!window.confirm(`Are you sure you want to delete ${filename}?`)) return;
    try {
      await deleteFile(filename);
      setUploadedFiles(uploadedFiles.filter(f => f !== filename));
      if (selectedUploadedFile === filename) setSelectedUploadedFile("");
    } catch (err) {
      console.error(err);
      alert("Failed to delete file.");
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload Your Data</h2>
      <p>Select a CSV or Excel file to begin analysis.</p>

      <div className="file-input-wrapper">
        <label className="custom-file-button">
          {selectedFile ? selectedFile.name : "Choose File"}
          <input type="file" accept=".csv,.xlsx" onChange={handleFileChange} />
        </label>
      </div>

      <label htmlFor="prompt" className="prompt-label">
        Add instructions or context for the agent:
      </label>
      <textarea
        id="prompt"
        placeholder="Describe what the agent should do with this data..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        rows={5}
      />

      <button onClick={handleAnalyze} disabled={loading}>
        {loading ? "Processing..." : "Analyze"}
      </button>

      {successMessage && <div className="upload-success">{successMessage}</div>}

      <div className="uploaded-files-panel">
        <h4>Uploaded Files</h4>
        <ul>
          {uploadedFiles.map((file) => (
            <li key={file} className="uploaded-file-item">
              <span
                className={selectedUploadedFile === file ? "selected" : ""}
                onClick={() => {
                  setSelectedUploadedFile(file);
                  setSelectedFile({ name: file });
                }}
              >
                {file}
              </span>
              <button className="delete-btn" onClick={() => handleDelete(file)}>×</button>
            </li>
          ))}
        </ul>
      </div>

      {/* Popup with analysis status and graph */}
      {showGraphPopup && (
        <div className="graph-popup">
          <div className="graph-popup-content">
            <h3>Analysis Process</h3>
            {analysisLoading ? (
              <p>Analysis in progress... Please wait.</p>
            ) : (
              <p>Analysis finished!</p>
            )}
            <div className="graph-placeholder">
              <GraphPopup
                activeNodeId={activeNodeId} // Highlight nodes in real-time
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
