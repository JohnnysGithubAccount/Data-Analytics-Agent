import api from "../api";

// Upload a file with prompt
export const uploadDataset = async (file, prompt) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("prompt", prompt);

  const response = await api.post("/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
};

// Get a list of all uploaded files
export const listUploadedFiles = async () => {
  const response = await api.get("/uploaded-files"); // make sure backend has this endpoint
  return response.data; // e.g., { files: ["file1.csv", "file2.xlsx"] }
};

// Delete a specific file by filename
export const deleteFile = async (filename) => {
  const response = await api.delete(`/uploaded-files/${filename}`);
  return response.data;
};
