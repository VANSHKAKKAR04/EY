import React, { useState } from "react";
import { login } from "../services/api";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [form, setForm] = useState({ email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const res = await login({ email: form.email, password: form.password });
      localStorage.setItem("customer", JSON.stringify(res.customer));
      navigate("/profile");
    } catch (err) {
      setError(err.message || String(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white p-8 rounded shadow">
        <h2 className="text-2xl font-bold mb-4">Log in</h2>
        {error && <div className="mb-3 text-red-600">{error}</div>}
        <form onSubmit={handleSubmit} className="space-y-3">
          <input
            name="email"
            placeholder="Email"
            value={form.email}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          />
          <input
            name="password"
            placeholder="Password"
            type="password"
            value={form.password}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          />
          <button
            disabled={loading}
            className="w-full bg-blue-600 text-white p-2 rounded"
          >
            {loading ? "Logging..." : "Log in"}
          </button>
        </form>
        <div className="mt-3 text-sm text-slate-600">
          Don't have an account?{" "}
          <a href="/signup" className="text-blue-600">
            Sign up
          </a>
        </div>
      </div>
    </div>
  );
}
