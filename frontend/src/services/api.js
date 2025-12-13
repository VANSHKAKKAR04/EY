export async function sendMessage(message) {
  // include logged-in customer from localStorage if present
  const raw =
    typeof window !== "undefined" ? localStorage.getItem("customer") : null;
  const customer = raw ? JSON.parse(raw) : undefined;

  const res = await fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, customer }),
  });
  return res.json();
}

export async function uploadSalarySlip(file) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch("http://localhost:8000/upload-salary-slip", {
    method: "POST",
    body: formData,
  });
  return res.json();
}

// -----------------
// Auth endpoints (CRM mock server runs on 8001)
// -----------------
export async function signup(payload) {
  const res = await fetch("http://localhost:8001/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || JSON.stringify(data));
  return data;
}

export async function login(payload) {
  const res = await fetch("http://localhost:8001/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || JSON.stringify(data));
  return data;
}

// -----------------
// Offer Mart endpoints (runs on 8002)
// -----------------
export async function getUserLoans(userId) {
  const res = await fetch(`http://localhost:8002/user/${userId}/loans`);
  return res.json();
}
