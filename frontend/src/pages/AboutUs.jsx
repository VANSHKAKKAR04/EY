// src/pages/AboutUs.jsx
import React from "react";
import { Target, Zap, UserCheck, Banknote, FileText } from "lucide-react";
import Navbar from "../components/Navbar.jsx";
// Color Mapping based on chat interface/buttons:
// Primary Blue: text-blue-600, bg-blue-50
// Accent Green/Emerald: text-emerald-600, bg-emerald-50
// Accent Amber/Orange: text-amber-600, bg-amber-50

// --- Helper component for a colored feature card ---
const FeatureCard = ({ icon: Icon, title, description, color }) => (
  <div
    className={`p-6 rounded-xl shadow-lg border ${color.bg} ${color.border}`}
  >
    <Icon className={`w-8 h-8 mb-4 ${color.text}`} />
    <h3 className={`text-xl font-semibold mb-2 ${color.text}`}>{title}</h3>
    <p className="text-gray-700">{description}</p>
  </div>
);

export default function AboutUs() {
  return (
    <div className="max-w-7xl mx-auto py-16 px-4 sm:px-6 lg:px-8">
      <div className="fixed top-0 left-0 w-full z-50">
        <Navbar />
      </div>
      <header className="text-center mb-16 pt-10">
        <h1 className="text-5xl font-extrabold text-slate-900 mb-4">
          About FinWise: Your Trusted Financial AI Assistant
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Empowering customers through intelligent, conversational finance,
          simplifying the entire personal loan journey from initial inquiry to
          final sanction.
        </p>
      </header>

      {/* --- Section 1: Our Mission --- */}
      <section className="mb-20">
        <h2 className="text-3xl font-bold text-center text-blue-600 mb-8">
          Our Core Mission & Challenge
        </h2>
        <div className="bg-white p-8 rounded-2xl shadow-xl border border-slate-200">
          <p className="text-lg text-gray-700 leading-relaxed mb-6">
            FinWise was developed as a solution to **Challenge II: Banking,
            Financial Services, and Insurance (BFSI)**, addressing the need for
            a seamless, personalized, and efficient loan application process
            within the NBFC sector.
          </p>
          <p className="text-lg text-gray-700 leading-relaxed">
            Our primary goal is to **improve the sales success rate for personal
            loans** by simulating a human-like, expert sales experience,
            providing end-to-end service from conversation and verification to
            credit evaluation and approval.
          </p>
        </div>
      </section>

      {/* --- Section 2: The FinWise Advantage (Agentic AI) --- */}
      <section className="mb-20">
        <h2 className="text-3xl font-bold text-center text-blue-600 mb-12">
          The FinWise Advantage: Agentic AI Orchestration
        </h2>

        {/* Visual Representation of Agentic Structure */}
        <div className="text-center mb-10"></div>

        <div className="grid md:grid-cols-3 gap-8">
          <FeatureCard
            icon={Target}
            title="Master Agent (Orchestrator)"
            description="Manages the entire conversation flow, coordinates tasks among Worker Agents, and ensures a seamless transition through all stages of the loan process."
            color={{
              text: "text-blue-600",
              bg: "bg-blue-50",
              border: "border-blue-200",
            }}
          />

          <FeatureCard
            icon={Zap}
            title="Sales Agent"
            description="Handles negotiations, discusses customer needs, and finalizes key loan terms (amount, tenure, and proposed interest rates)."
            color={{
              text: "text-amber-600",
              bg: "bg-amber-50",
              border: "border-amber-200",
            }}
          />

          <FeatureCard
            icon={UserCheck}
            title="Verification Agent"
            description="Confirms and validates customer KYC details, including identity and address, against mock CRM server data."
            color={{
              text: "text-purple-600",
              bg: "bg-purple-50",
              border: "border-purple-200",
            }}
          />
        </div>
      </section>

      {/* --- Section 3: Specialized Worker Agents --- */}
      <section className="mb-20">
        <h2 className="text-3xl font-bold text-center text-blue-600 mb-12">
          Specialized Worker Functions
        </h2>
        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          <FeatureCard
            icon={Banknote}
            title="Underwriting Agent"
            description={
              <>
                Fetches mock credit scores and validates eligibility based on
                strict criteria: instant approval if within pre-approved limit;
                conditional approval (requiring salary slip) if within 2&times;
                limit; and outright rejection for low score or high amount.
              </>
            }
            color={{
              text: "text-emerald-600",
              bg: "bg-emerald-50",
              border: "border-emerald-200",
            }}
          />

          <FeatureCard
            icon={FileText}
            title="Sanction Letter Generator"
            description="Automatically generates and provides the official PDF sanction letter to the customer immediately upon successful approval, closing the loop on the application process."
            color={{
              text: "text-red-600",
              bg: "bg-red-50",
              border: "border-red-200",
            }}
          />
        </div>
      </section>

      {/* --- Section 4: Project Context --- */}
      <footer className="text-center border-t pt-8 mt-10">
        <h3 className="text-2xl font-semibold text-slate-800 mb-4">
          Built for the Future of Finance
        </h3>
        <p className="text-md text-gray-600">
          FinWise is a testament to the power of conversational and Agentic AI
          in transforming the customer journey in the BFSI domain.
        </p>
      </footer>
    </div>
  );
}
