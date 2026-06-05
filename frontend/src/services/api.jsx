import axios from "axios";

const api = axios.create({
  baseURL: "ai-procurement-intelligence-agent-production.up.railway.app"
});

export default api;