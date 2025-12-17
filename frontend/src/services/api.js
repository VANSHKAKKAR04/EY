// src/services/api.js

export const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
/* -----------------------------
   Session helpers
----------------------------- */
function getSessionId() {
  return typeof window !== "undefined"
    ? localStorage.getItem("session_id")
    : null;
}

function saveSessionId(sessionId) {
  if (typeof window !== "undefined" && sessionId) {
    localStorage.setItem("session_id", sessionId);
  }
}

/* -----------------------------
   Chat
----------------------------- */
export async function sendMessage(message) {
  const raw =
    typeof window !== "undefined" ? localStorage.getItem("customer") : null;
  const customer = raw ? JSON.parse(raw) : undefined;

  const session_id = getSessionId();

  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      customer,
      session_id,
    }),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "Failed to send message");
  }

  if (data.session_id) {
    saveSessionId(data.session_id);
  }

  return data;
}

/* -----------------------------
   File uploads
----------------------------- */
export async function uploadSalarySlip(file) {
  const session_id = getSessionId();
  if (!session_id) throw new Error("Session not found");

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(
    `${API_BASE}/upload-salary-slip?session_id=${session_id}`,
    {
      method: "POST",
      body: formData,
    }
  );

  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Upload failed");
  return data;
}

export async function uploadPan(file) {
  const session_id = getSessionId();
  if (!session_id) throw new Error("Session not found");

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/upload-pan?session_id=${session_id}`, {
    method: "POST",
    body: formData,
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Upload failed");
  return data;
}

export async function uploadAadhaar(file) {
  const session_id = getSessionId();
  if (!session_id) throw new Error("Session not found");

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(
    `${API_BASE}/upload-aadhaar?session_id=${session_id}`,
    {
      method: "POST",
      body: formData,
    }
  );

  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Upload failed");
  return data;
}

/* -----------------------------
   CRM Auth
----------------------------- */
export async function signup(payload) {
  const res = await fetch(`${API_BASE}/crm/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || JSON.stringify(data));
  return data;
}

export async function login(payload) {
  const res = await fetch(`${API_BASE}/crm/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || JSON.stringify(data));

  if (data.customer) {
    localStorage.setItem("customer", JSON.stringify(data.customer));
  }

  return data;
}

/* -----------------------------
   Offer Mart
----------------------------- */
export async function getUserLoans(userId) {
  const res = await fetch(`${API_BASE}/offer-mart/user/${userId}/loans`);

  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || "Failed to fetch loans");
  }

  return data;
}
