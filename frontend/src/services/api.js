import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export const sendMessage = async (message) => {
  const res = await axios.post(`${API_URL}/sales`, { message });
  return res.data.response;
};
