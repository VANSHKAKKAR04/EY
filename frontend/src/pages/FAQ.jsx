import React, { useState } from "react";
import Navbar from "../components/Navbar.jsx";
import { ChevronDown, ChevronUp } from "lucide-react";

const faqs = [
  {
    id: 1,
    category: "Loans",
    question: "Who can apply for a loan on this platform?",
    answer:
      "Any salaried individual who meets the minimum eligibility criteria such as age, income stability, and credit score can apply for a loan through our platform.",
  },
  {
    id: 2,
    category: "Loans",
    question: "How long does loan approval take?",
    answer:
      "Most loan applications are reviewed instantly. In some cases, manual verification may take up to 24–48 hours.",
  },
  {
    id: 3,
    category: "Credit Score",
    question: "Does checking my credit score affect it?",
    answer:
      "No. Checking your credit score through our platform is considered a soft inquiry and does not impact your credit score.",
  },
  {
    id: 4,
    category: "Repayment",
    question: "Can I repay my loan before the tenure ends?",
    answer:
      "Yes. Prepayment or foreclosure is allowed, subject to the lender’s terms. Some loans may include a small prepayment fee.",
  },
  {
    id: 5,
    category: "Security",
    question: "Is my personal data safe?",
    answer:
      "Absolutely. We use industry-grade encryption and follow strict data protection policies to ensure your information remains secure.",
  },
  {
    id: 6,
    category: "General",
    question: "What documents are required to apply?",
    answer:
      "Typically, PAN card, Aadhaar card, salary slips, and bank statements are required. Document requirements may vary by lender.",
  },
];

export default function FAQ() {
  const [openId, setOpenId] = useState(null);

  const toggleFAQ = (id) => {
    setOpenId(openId === id ? null : id);
  };

  return (
    <div className="max-w-4xl mx-auto py-12 px-4">
      {/* Navbar */}
      <div className="fixed top-0 left-0 w-full z-50">
        <Navbar />
      </div>

      <div className="mt-20">
        <h1 className="text-3xl font-bold mb-2">Frequently Asked Questions</h1>
        <p className="text-gray-600 mb-8">
          Find quick answers to common questions about loans, credit scores, and
          your account.
        </p>

        <div className="space-y-4">
          {faqs.map((faq) => (
            <div key={faq.id} className="border rounded-lg bg-white shadow-sm">
              <button
                onClick={() => toggleFAQ(faq.id)}
                className="w-full flex justify-between items-center p-4 text-left"
              >
                <div>
                  <span className="text-xs text-blue-600 font-medium">
                    {faq.category}
                  </span>
                  <h3 className="font-semibold text-lg">{faq.question}</h3>
                </div>

                {openId === faq.id ? (
                  <ChevronUp className="w-5 h-5 text-blue-600" />
                ) : (
                  <ChevronDown className="w-5 h-5 text-gray-500" />
                )}
              </button>

              {openId === faq.id && (
                <div className="px-4 pb-4 text-gray-700 text-sm leading-relaxed">
                  {faq.answer}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Support CTA */}
        <div className="mt-10 bg-blue-50 border border-blue-200 rounded-lg p-6 text-center">
          <h3 className="text-xl font-bold mb-2">Still have questions?</h3>
          <p className="text-gray-600 mb-4">
            Our support team is always ready to help you.
          </p>
          <a
            href="/chat"
            className="inline-block bg-blue-600 text-white px-6 py-2 rounded"
          >
            Chat with Support
          </a>
        </div>
      </div>
    </div>
  );
}
