import "./Upload.css";
import { useState, useEffect } from "react";
import { uploadDataset, listUploadedFiles, deleteFile } from "../api/upload";

export default function Upload() {
  const [prompt, setPrompt] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [successMessage, setSuccessMessage] = useState("");
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [selectedUploadedFile, setSelectedUploadedFile] = useState("");
  
  // Fetch uploaded files from server
  const fetchUploadedFiles = async () => {
    try {
      const res = await listUploadedFiles();
      setUploadedFiles(res.files || []);
    } catch (err) {
      console.error(err);
    }
  };

  // Auto-fetch files on mount and every 1 second
  useEffect(() => {
    fetchUploadedFiles(); // initial fetch

    const interval = setInterval(() => {
      fetchUploadedFiles();
    }, 1000); // fetch every 1 second

    return () => clearInterval(interval); // cleanup on unmount
  }, []);

  // Handle file selection
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);

    if (file) {
      setSuccessMessage(`✅ Selected file: ${file.name}`);
      // Optimistically add to uploadedFiles if not already present
      // setUploadedFiles((prev) =>
      //   prev.includes(file.name) ? prev : [file.name, ...prev]
      // );
    } else {
      setSuccessMessage("");
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return alert("Please select a file!");

    setLoading(true);
    setResult(null);

    try {
      const data = await uploadDataset(selectedFile, prompt);
      setResult(data);
      setSuccessMessage(`✅ File analyzed successfully: ${selectedFile.name}`);
      setSelectedFile(null);
      setPrompt("");
      // Immediately fetch to ensure consistency
      await fetchUploadedFiles();
    } catch (err) {
      console.error(err);
      alert("Upload failed, check console.");
    } finally {
      setLoading(false);
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
          <input
            type="file"
            accept=".csv,.xlsx"
            onChange={handleFileChange}
          />
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

      {/* Uploaded Files Panel */}
      <div className="uploaded-files-panel">
        <h4>Uploaded Files</h4>
        <ul>
          {uploadedFiles.map((file) => (
            <li key={file} className="uploaded-file-item">
              <span
                className={selectedUploadedFile === file ? "selected" : ""}
                onClick={() => {
                  setSelectedUploadedFile(file);
                  setSelectedFile({ name: file }); // set clicked file as "selectedFile"
                }}
              >
                {file}
              </span>
              <button className="delete-btn" onClick={() => handleDelete(file)}>×</button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
