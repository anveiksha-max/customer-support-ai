import axios from "axios";

// In production (Vercel), set VITE_API_URL to your deployed backend URL.
// Locally, it falls back to your FastAPI dev server.
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// Attach the logged-in user's token to every request automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("techmart_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export async function sendMessage(sessionId, message) {
  const response = await api.post("/chat", {
    session_id: sessionId,
    message,
  });
  return response.data;
}

export async function getHistory(sessionId) {
  const response = await api.get(`/history/${sessionId}`);
  return response.data;
}

export async function sendFeedback(sessionId, agent, rating) {
  const response = await api.post("/feedback", { session_id: sessionId, agent, rating });
  return response.data;
}

export async function getAnalytics() {
  const response = await api.get("/analytics");
  return response.data;
}

export default api;
