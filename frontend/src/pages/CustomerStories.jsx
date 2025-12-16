import React from "react";
import Navbar from "../components/Navbar.jsx";
import { testimonials } from "./landing/constants/index.jsx";

export default function CustomerStories() {
  // Pick a few strong testimonials for stories
  const stories = testimonials.slice(0, 4);

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      {/* Navbar */}
      <div className="fixed top-0 left-0 w-full z-50">
        <Navbar />
      </div>

      <div className="mt-20">
        {/* Header */}
        <div className="text-center mb-14">
          <h1 className="text-4xl font-bold mb-4">Customer Stories</h1>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Real people. Real financial journeys. See how our platform helped
            customers achieve their goals with confidence.
          </p>
        </div>

        {/* Featured Story */}
        <div className="bg-blue-50 border border-blue-200 rounded-xl p-8 mb-16">
          <div className="flex flex-col md:flex-row gap-8 items-center">
            <img
              src={stories[0].image}
              alt={stories[0].user}
              className="w-32 h-32 rounded-full border-4 border-white shadow"
            />

            <div>
              <h2 className="text-2xl font-bold mb-2">{stories[0].user}</h2>
              <p className="text-sm italic text-gray-600 mb-4">
                {stories[0].company}
              </p>
              <p className="text-gray-800 leading-relaxed">
                “{stories[0].text}”
              </p>
            </div>
          </div>
        </div>

        {/* Story Grid */}
        <div className="grid md:grid-cols-3 gap-8">
          {stories.slice(1).map((story, index) => (
            <div
              key={index}
              className="bg-white border rounded-xl p-6 shadow-sm hover:shadow-md transition"
            >
              <div className="flex items-center gap-4 mb-4">
                <img
                  src={story.image}
                  alt={story.user}
                  className="w-14 h-14 rounded-full border"
                />
                <div>
                  <h3 className="font-semibold">{story.user}</h3>
                  <span className="text-xs text-gray-500 italic">
                    {story.company}
                  </span>
                </div>
              </div>

              <p className="text-gray-700 text-sm leading-relaxed">
                “{story.text}”
              </p>
            </div>
          ))}
        </div>

        {/* Trust Section */}
        <div className="mt-20 bg-gray-900 text-white rounded-xl p-10 text-center">
          <h3 className="text-2xl font-bold mb-4">
            Trusted by Thousands of Customers
          </h3>
          <p className="text-gray-300 max-w-xl mx-auto mb-6">
            From first-time borrowers to experienced professionals, our platform
            empowers smarter financial decisions.
          </p>
          <a
            href="/chat"
            className="inline-block bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded"
          >
            Start Your Journey
          </a>
        </div>
      </div>
    </div>
  );
}
