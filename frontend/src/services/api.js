export async function sendMessage(message) {
  const res = await fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
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
