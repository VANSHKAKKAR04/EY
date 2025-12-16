import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getUserLoans } from "../services/api";
import Navbar from "../components/Navbar.jsx";
import { ChevronDown, ChevronUp } from "lucide-react";

export default function Profile() {
  const navigate = useNavigate();

  const [customer, setCustomer] = useState(null);
  const [loans, setLoans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loansOpen, setLoansOpen] = useState(false);

  useEffect(() => {
    const raw = localStorage.getItem("customer");
    const storedCustomer = raw ? JSON.parse(raw) : null;

    if (!storedCustomer) {
      setLoading(false);
      return;
    }

    fetch(`http://localhost:8000/profile/${storedCustomer.id}`)
      .then((res) => res.json())
      .then((data) => {
        if (!data?.error) {
          setCustomer(data);
          localStorage.setItem("customer", JSON.stringify(data));
        } else {
          setCustomer(storedCustomer);
        }
      })
      .catch(() => setCustomer(storedCustomer))
      .finally(() => {
        getUserLoans(storedCustomer.id)
          .then((data) => {
            if (data?.loans) {
              setLoans(data.loans);
            }
          })
          .catch(console.error)
          .finally(() => setLoading(false));
      });
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("customer");
    navigate("/");
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        Loading profile...
      </div>
    );
  }

  if (!customer) {
    return (
      <div className="min-h-screen flex items-center justify-center text-center">
        <p className="mb-4">Not logged in.</p>
        <a href="/login" className="text-blue-600 underline">
          Go to login
        </a>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto py-12 px-4">
      <div className="fixed top-0 left-0 w-full z-50">
        <Navbar />
      </div>

      <div className="bg-white p-8 rounded shadow mt-16">
        <h2 className="text-2xl font-bold mb-6">Your Profile</h2>

        {/* Profile Details */}
        <div className="grid grid-cols-2 gap-4 text-sm">
          <ProfileItem label="Name" value={customer.name} />
          <ProfileItem label="Email" value={customer.email} />
          <ProfileItem label="City" value={customer.city} />
          <ProfileItem label="Phone" value={customer.phone} />
          <ProfileItem label="Age" value={customer.age} />
          <ProfileItem label="Salary" value={customer.salary} />
          <ProfileItem
            label="Credit Score"
            value={customer.credit_score || "N/A"}
          />
          <ProfileItem
            label="Preapproved Limit"
            value={customer.preapproved_limit}
          />
          <ProfileItem label="Existing Loans" value={customer.existing_loans} />
          <ProfileItem label="PAN Number" value={customer.pan_number} />
          <ProfileItem label="Aadhaar Number" value={customer.aadhaar_number} />
        </div>

        {/* Loan Requests */}
        <div className="mt-8 border-t pt-4">
          <button
            onClick={() => setLoansOpen(!loansOpen)}
            className="w-full flex justify-between items-center text-xl font-bold hover:text-blue-600"
          >
            <span>Your Loan Requests ({loans.length})</span>
            {loansOpen ? (
              <ChevronUp className="w-5 h-5" />
            ) : (
              <ChevronDown className="w-5 h-5" />
            )}
          </button>
        </div>

        {loansOpen && (
          <div className="mt-4 space-y-4">
            {loans.length === 0 ? (
              <p className="text-gray-600">No loan requests found.</p>
            ) : (
              loans.map((loan) => (
                <div
                  key={loan.id}
                  className="border rounded-lg p-4 bg-gray-50 shadow-sm"
                >
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <ProfileItem label="Loan Name" value={loan.name} />
                    <ProfileItem label="Type" value={loan.type} />
                    <ProfileItem
                      label="Amount"
                      value={`₹${loan.amount.toLocaleString()}`}
                    />
                    <ProfileItem
                      label="Interest Rate"
                      value={`${loan.interest_rate}%`}
                    />
                    <ProfileItem
                      label="Tenure"
                      value={`${loan.tenure_months} months`}
                    />
                    <ProfileItem
                      label="Status"
                      value={loan.status}
                      valueClass={
                        loan.status === "sanctioned"
                          ? "text-green-600"
                          : "text-red-600"
                      }
                    />
                  </div>

                  {loan.sanction_letter_path && (
                    <div className="mt-4">
                      <a
                        href={`http://localhost:8002/${loan.sanction_letter_path}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 underline"
                      >
                        Download Sanction Letter
                      </a>
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        )}

        {/* Actions */}
        <div className="mt-6 flex gap-3">
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

/* ---------- Reusable Component ---------- */

function ProfileItem({ label, value, valueClass = "" }) {
  return (
    <div>
      <strong>{label}</strong>
      <div className={valueClass}>{value}</div>
    </div>
  );
}
