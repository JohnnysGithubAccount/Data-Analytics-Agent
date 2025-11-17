import api from "../api";

export const getAnalysis = async () => {
  const response = await api.get("/analysis");
  return response.data;
};
