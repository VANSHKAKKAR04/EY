import React from "react";
import Navbar from "../components/Navbar.jsx";

const blogPosts = [
  {
    id: 1,
    title: "How to Improve Your Credit Score",
    category: "Credit",
    date: "Updated Guide",
    content: [
      "Pay all EMIs and credit card bills on time.",
      "Keep your credit utilization below 30%.",
      "Avoid applying for multiple loans at once.",
      "Maintain a healthy mix of secured and unsecured loans.",
      "Check your credit report regularly for errors.",
    ],
  },
  {
    id: 2,
    title: "Things to Check Before Taking a Personal Loan",
    category: "Loans",
    date: "Beginner Friendly",
    content: [
      "Compare interest rates across lenders.",
      "Understand processing fees and hidden charges.",
      "Choose a tenure that keeps EMIs affordable.",
      "Check prepayment or foreclosure penalties.",
      "Borrow only what you actually need.",
    ],
  },
  {
    id: 3,
    title: "Smart Budgeting Tips for Young Professionals",
    category: "Savings",
    date: "Popular",
    content: [
      "Follow the 50-30-20 budgeting rule.",
      "Track expenses using budgeting apps.",
      "Build an emergency fund of at least 6 months.",
      "Avoid lifestyle inflation after salary hikes.",
      "Automate savings every month.",
    ],
  },
  {
    id: 4,
    title: "Understanding Interest Rates and EMIs",
    category: "Education",
    date: "Must Read",
    content: [
      "Lower interest rates reduce total loan cost.",
      "Longer tenure lowers EMI but increases interest paid.",
      "Fixed rates offer stability; floating rates may change.",
      "Always calculate EMI before applying for a loan.",
      "Use EMI calculators to plan better.",
    ],
  },
  {
    id: 5,
    title: "Common Financial Mistakes to Avoid",
    category: "Awareness",
    date: "Expert Advice",
    content: [
      "Ignoring insurance and emergency planning.",
      "Relying only on credit cards for expenses.",
      "Not reading loan terms carefully.",
      "Delaying investments for too long.",
      "Borrowing beyond repayment capacity.",
    ],
  },
];

export default function Blog() {
  return (
    <div className="max-w-5xl mx-auto py-12 px-4">
      {/* Navbar */}
      <div className="fixed top-0 left-0 w-full z-50">
        <Navbar />
      </div>

      <div className="mt-20">
        <h1 className="text-3xl font-bold mb-2">Financial Blog</h1>
        <p className="text-gray-600 mb-8">
          Simple financial tips, loan guides, and money management advice to
          help you make better decisions.
        </p>

        <div className="space-y-6">
          {blogPosts.map((post) => (
            <div
              key={post.id}
              className="bg-white border rounded-lg shadow-sm p-6"
            >
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm text-blue-600 font-medium">
                  {post.category}
                </span>
                <span className="text-xs text-gray-500">{post.date}</span>
              </div>

              <h2 className="text-xl font-bold mb-4">{post.title}</h2>

              <ul className="list-disc pl-5 space-y-2 text-gray-700 text-sm">
                {post.content.map((point, index) => (
                  <li key={index}>{point}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
