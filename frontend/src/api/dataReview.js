import api from "../api";

export const fetchDataPreview = async (filename) => {
  const res = await api.get("/data-review", { params: { filename } });
  return res.data;
};

export const fetchUploadedFiles = async () => {
  const res = await api.get("/uploaded-files");
  return res.data.files;
};
