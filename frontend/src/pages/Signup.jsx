import React, { useState } from "react";
import { signup } from "../services/api";
import { useNavigate } from "react-router-dom";

export default function Signup() {
  const [form, setForm] = useState({
    name: "",
    age: "",
    city: "",
    phone: "",
    salary: "",
    email: "",
    password: "",
    pan_number: "",
    aadhaar_number: "",
  });
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
      const payload = {
        name: form.name,
        age: Number(form.age),
        city: form.city,
        phone: form.phone,
        salary: Number(form.salary),
        email: form.email,
        password: form.password,
        pan_number: form.pan_number,
        aadhaar_number: form.aadhaar_number,
      };
      const res = await signup(payload);
      // store customer locally
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
        <h2 className="text-2xl font-bold mb-4">Sign up</h2>
        {error && <div className="mb-3 text-red-600">{error}</div>}
        <form onSubmit={handleSubmit} className="space-y-3">
          <input
            name="name"
            placeholder="Full name"
            value={form.name}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          />
          <div className="grid grid-cols-2 gap-2">
            <input
              name="age"
              placeholder="Age"
              value={form.age}
              onChange={handleChange}
              className="p-2 border rounded"
            />
            <input
              name="city"
              placeholder="City"
              value={form.city}
              onChange={handleChange}
              className="p-2 border rounded"
            />
          </div>
          <input
            name="phone"
            placeholder="Phone"
            value={form.phone}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          />
          <input
            name="salary"
            placeholder="Salary"
            value={form.salary}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          />
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
          <input
            name="pan_number"
            placeholder="PAN Number"
            value={form.pan_number}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          />
          <input
            name="aadhaar_number"
            placeholder="Aadhaar Number"
            value={form.aadhaar_number}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          />

          <button
            disabled={loading}
            className="w-full bg-blue-600 text-white p-2 rounded"
          >
            {loading ? "Creating..." : "Create account"}
          </button>
        </form>
        <div className="mt-3 text-sm text-slate-600">
          Already have an account?{" "}
          <a href="/login" className="text-blue-600">
            Log in
          </a>
        </div>
      </div>
    </div>
  );
}
