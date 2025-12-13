import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getUserLoans } from "../services/api";

export default function Profile() {
  const navigate = useNavigate();
  const [customer, setCustomer] = useState(null);
  const [loans, setLoans] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const raw = localStorage.getItem("customer");
    const storedCustomer = raw ? JSON.parse(raw) : null;

    if (!storedCustomer) {
      setLoading(false);
      return;
    }

    // Fetch updated profile from backend
    fetch(`http://localhost:8000/profile/${storedCustomer.id}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          console.error(data.error);
          setCustomer(storedCustomer); // fallback to stored
        } else {
          setCustomer(data);
          // Update localStorage with fresh data
          localStorage.setItem("customer", JSON.stringify(data));
        }
      })
      .catch((err) => {
        console.error("Failed to fetch profile:", err);
        setCustomer(storedCustomer); // fallback
      })
      .finally(() => {
        // Fetch loans after profile
        if (storedCustomer) {
          getUserLoans(storedCustomer.id)
            .then((data) => {
              if (data.loans) {
                setLoans(data.loans);
              }
            })
            .catch((err) => console.error("Failed to fetch loans:", err))
            .finally(() => setLoading(false));
        } else {
          setLoading(false);
        }
      });
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("customer");
    navigate("/");
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div>Loading profile...</div>
      </div>
    );
  }

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
    <div className="max-w-4xl mx-auto py-12 px-4">
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
          <div>
            <strong>Credit score</strong>
            <div>{customer.credit_score}</div>
          </div>
        </div>

        <div className="mt-8">
          <h3 className="text-xl font-bold mb-4">Your Loan Requests</h3>
          {loans.length === 0 ? (
            <p>No loan requests found.</p>
          ) : (
            <div className="space-y-4">
              {loans.map((loan) => (
                <div key={loan.id} className="border p-4 rounded">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <strong>Loan Name</strong>
                      <div>{loan.name}</div>
                    </div>
                    <div>
                      <strong>Type</strong>
                      <div>{loan.type}</div>
                    </div>
                    <div>
                      <strong>Amount</strong>
                      <div>₹{loan.amount.toLocaleString()}</div>
                    </div>
                    <div>
                      <strong>Interest Rate</strong>
                      <div>{loan.interest_rate}%</div>
                    </div>
                    <div>
                      <strong>Tenure</strong>
                      <div>{loan.tenure_months} months</div>
                    </div>
                    <div>
                      <strong>Status</strong>
                      <div
                        className={
                          loan.status === "sanctioned"
                            ? "text-green-600"
                            : "text-red-600"
                        }
                      >
                        {loan.status}
                      </div>
                    </div>
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
              ))}
            </div>
          )}
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
