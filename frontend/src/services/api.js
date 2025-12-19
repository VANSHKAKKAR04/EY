// src/services/api.js

export const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

/* -----------------------------
   Chat
----------------------------- */
export async function sendMessage(message) {
  const raw =
    typeof window !== "undefined" ? localStorage.getItem("customer") : null;
  const customer = raw ? JSON.parse(raw) : undefined;

  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      customer,
    }),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "Failed to send message");
  }

  return data;
}

/* -----------------------------
   File uploads
----------------------------- */

export async function uploadSalarySlip(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/upload-salary-slip`, {
    method: "POST",
    body: formData,
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Upload failed");
  return data;
}

export async function uploadPan(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/upload-pan`, {
    method: "POST",
    body: formData,
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Upload failed");
  return data;
}

export async function uploadAadhaar(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/upload-aadhaar`, {
    method: "POST",
    body: formData,
  });

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
