import React, { useState } from 'react';
import HeroSection from "./landing/HeroSection";
import FeatureSection from "./landing/FeatureSection";
import Workflow from "./landing/Workflow.jsx";
import Footer from "./landing/Footer";
import Pricing from "./landing/Pricing";
import Testimonials from "./landing/Testimonials";
import Navbar from '../components/Navbar.jsx';

const LandingPage = () => {
  return (
    <div className="overflow-x-hidden">
      <Navbar /> 
      <div className="max-w-7xl mx-auto pt-20 px-4 sm:px-6 lg:px-8">
        <HeroSection />
        <FeatureSection />
        <Workflow />
        <Pricing />
        <Testimonials />
        <Footer />
      </div>

     
    </div>
  );
};

export default LandingPage;