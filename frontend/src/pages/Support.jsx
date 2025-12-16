// src/pages/Support.jsx
import React from "react";
import {
  MessageSquare,
  User,
  ShieldCheck,
  FileText,
  Zap,
  Download,
  ListChecks,
} from "lucide-react";
import Navbar from "../components/Navbar.jsx";
export default function Support() {
  // --- Data defining the loan process steps ---
  const loanProcessSteps = [
    {
      stage: "Stage 1: Sales Conversation & Needs Assessment",
      icon: MessageSquare,
      description:
        "The Master Agent and Sales Agent will interact with you to understand your financial goals, preferred loan amount, and repayment tenure.",
      action:
        "Action Required: Clearly state your desired loan amount (₹) and repayment period (in years).",
      documents: "None required. This stage is purely conversational.",
      color: "text-blue-600 bg-blue-50 border-blue-200",
    },
    {
      stage: "Stage 2: Identity Verification (KYC)",
      icon: ShieldCheck,
      description:
        "The Verification Agent cross-checks your personal details (Name, Age, Phone, City, Salary) against our CRM records and mock credit bureau data.",
      action:
        "Action Required: Confirm your personal details are accurate. You will then be prompted to upload required documents.",
      documents: "• PAN Card (PDF/Image) • Aadhaar Card (PDF/Image)",
      color: "text-purple-600 bg-purple-50 border-purple-200",
    },
    {
      stage: "Stage 3: Underwriting & Eligibility Check",
      icon: Zap,
      description:
        "The Underwriting Agent fetches your credit score and evaluates your application based on the pre-approved limit and EMI affordability criteria.",
      action:
        "Action Required: You may be asked to input your current monthly salary manually. If your loan request is above the pre-approved limit, you will be prompted for a salary slip.",
      documents:
        "Conditional: • Latest Salary Slip (PDF/Image) or Proof of Income (if requested by the Underwriting Agent).",
      color: "text-emerald-600 bg-emerald-50 border-emerald-200",
    },
    {
      stage: "Stage 4: Final Approval & Sanction",
      icon: Download,
      description:
        "Upon successful verification and eligibility clearance, the Sanction Letter Generator Agent will instantly create your final loan sanction letter.",
      action:
        "Action Required: Download your personalized sanction letter (PDF) to proceed with fund disbursement.",
      documents: "None required.",
      color: "text-red-600 bg-red-50 border-red-200",
    },
  ];

  return (
    <div className="max-w-6xl mx-auto py-16 px-4 sm:px-6 lg:px-8">
      <div className="fixed top-0 left-0 w-full z-50">
        <Navbar />
      </div>
      <header className="text-center mb-16 pt-10">
        <h1 className="text-4xl font-extrabold text-slate-900 mb-3">
          Loan Application Support & Help Center
        </h1>
        <p className="text-xl text-gray-600">
          A clear guide to the four stages of your personal loan application
          journey.
        </p>
      </header>

      {/* --- Document Checklist Header --- */}
      <section className="mb-12 p-6 bg-gray-100 rounded-xl shadow-inner border border-gray-200">
        <h2 className="text-2xl font-bold text-slate-800 flex items-center gap-3 mb-4">
          <ListChecks className="w-6 h-6 text-blue-600" /> Essential Documents
          Checklist
        </h2>
        <div className="flex flex-wrap gap-x-12 gap-y-2 text-md text-gray-700">
          <p>• PAN Card</p>
          <p>• Aadhaar Card</p>
          <p>• Salary Slip (Conditional)</p>
        </div>
      </section>

      {/* --- Workflow Diagram Trigger --- */}
      <div className="text-center my-12"></div>

      {/* --- Loan Process Steps --- */}
      <section className="space-y-8">
        {loanProcessSteps.map((step, index) => (
          <div
            key={index}
            className={`p-6 rounded-xl shadow-lg transition duration-300 hover:shadow-xl border-l-4 ${step.color.replace(
              "bg-",
              "border-"
            )}`}
            style={{ backgroundColor: step.color.split(" ")[1] }}
          >
            <div className="flex items-start gap-4">
              <div
                className={`p-3 rounded-full ${step.color.replace(
                  "text-",
                  "bg-"
                )}`}
              >
                <step.icon className={`w-6 h-6 ${step.color.split(" ")[0]}`} />
              </div>
              <div className="flex-1">
                <h3
                  className={`text-2xl font-bold ${
                    step.color.split(" ")[0]
                  } mb-2`}
                >
                  {step.stage}
                </h3>
                <p className="text-gray-700 mb-3">{step.description}</p>

                {/* Documents Required Section */}
                <div className="mt-4 p-3 rounded-lg bg-white border border-gray-200">
                  <p className="text-sm font-semibold text-slate-800">
                    <FileText className="w-4 h-4 inline mr-2 text-blue-500" />{" "}
                    Documents/Data Required:
                  </p>
                  <p className="text-sm text-gray-600 mt-1 pl-6">
                    {step.documents}
                  </p>
                </div>

                {/* Action Section */}
                <div className="mt-4 p-3 rounded-lg bg-white border border-gray-200">
                  <p className="text-sm font-semibold text-slate-800">
                    <User className="w-4 h-4 inline mr-2 text-blue-500" /> Your
                    Key Action:
                  </p>
                  <p className="text-sm text-gray-600 mt-1 pl-6 font-medium">
                    {step.action}
                  </p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </section>
    </div>
  );
}
