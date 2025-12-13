import React from "react";
import { useNavigate } from "react-router-dom";

export default function Profile() {
  const navigate = useNavigate();
  const raw = localStorage.getItem("customer");
  const customer = raw ? JSON.parse(raw) : null;

  const handleLogout = () => {
    localStorage.removeItem("customer");
    navigate("/");
  };

  if (!customer) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="mb-4">Not logged in.</p>
          <a href="/login" className="text-blue-600">
            Go to login
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto py-12 px-4">
      <div className="bg-white p-8 rounded shadow">
        <h2 className="text-2xl font-bold mb-4">Your profile</h2>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <strong>Name</strong>
            <div>{customer.name}</div>
          </div>
          <div>
            <strong>Email</strong>
            <div>{customer.email}</div>
          </div>
          <div>
            <strong>City</strong>
            <div>{customer.city}</div>
          </div>
          <div>
            <strong>Phone</strong>
            <div>{customer.phone}</div>
          </div>
          <div>
            <strong>Age</strong>
            <div>{customer.age}</div>
          </div>
          <div>
            <strong>Salary</strong>
            <div>{customer.salary}</div>
          </div>
          <div>
            <strong>Preapproved limit</strong>
            <div>{customer.preapproved_limit}</div>
          </div>
          <div>
            <strong>Existing loans</strong>
            <div>{customer.existing_loans}</div>
          </div>
        </div>

        <div className="mt-6 flex gap-2">
          <button
            onClick={() => navigate("/chat")}
            className="bg-blue-600 text-white px-4 py-2 rounded"
          >
            Go to chat
          </button>
          <button
            onClick={handleLogout}
            className="bg-gray-200 px-4 py-2 rounded"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  );
}
