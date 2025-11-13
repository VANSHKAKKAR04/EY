import { Rocket, Shield, Star, LineChart,RefreshCcw, Users, Cpu, User, Bell, Grid, Link, CheckCircle, ShieldCheck, FileText  } from 'lucide-react';

import user1 from "../assets/user1.jpg";
import user2 from "../assets/user2.jpg";
import user3 from "../assets/user3.jpg";
import user4 from "../assets/user4.jpg";
import user5 from "../assets/user5.jpg";
import user6 from "../assets/user6.jpg";

export const navItems = [
  { label: "Features", href: "#" },
  { label: "Workflow", href: "#" },
  { label: "Pricing", href: "#" },
  { label: "Testimonials", href: "#" },
];export const testimonials = [
  {
    user: "Aarav Mehta",
    company: "CrediCore Pvt. Ltd.",
    image: user1,
    text: "Finwise completely transformed how I manage my finances. The AI insights are accurate, and the planning tools are simple yet powerful. Highly recommended!",
  },
  {
    user: "Neha Sharma",
    company: "BluePeak Analytics",
    image: user2,
    text: "Using Finwise has made budgeting and goal tracking effortless. I love how it connects all my bank accounts seamlessly and offers real-time insights.",
  },
  {
    user: "Rohan Gupta",
    company: "NextWave Capital",
    image: user3,
    text: "Finwise is the smartest financial assistant I’ve used. The personalized recommendations and loan eligibility checks save me so much time and stress.",
  },
  {
    user: "Simran Kaur",
    company: "BrightLedger Solutions",
    image: user4,
    text: "The app’s design and intelligence are exceptional. Finwise’s AI helps me make smarter investment choices and stay on top of my spending habits easily.",
  },
  {
    user: "Arjun Patel",
    company: "WealthSync Advisors",
    image: user5,
    text: "Finwise helped me organize my savings, track expenses, and plan better for future investments. A must-have for anyone serious about financial health.",
  },
  {
    user: "Priya Nair",
    company: "Nova Financials",
    image: user6,
    text: "I’ve tried many finance apps, but Finwise stands out for its clarity and intelligence. It gives practical insights and makes managing money stress-free.",
  },
];

  

export const features = [
  {
    icon: <Cpu />,
    text: "AI-Powered Financial Insights",
    description:
      "Harness advanced AI to analyze your spending, savings, and investment patterns for smarter decision-making.",
  },
  {
    icon: <User />,
    text: "Personalized Financial Planning",
    description:
      "Get customized budgeting, saving, and investment plans designed around your goals and financial behavior.",
  },
  {
    icon: <Link />,
    text: "Seamless Bank Integration",
    description:
      "Securely connect multiple bank accounts and wallets to manage your finances effortlessly in one place.",
  },
  {
    icon: <CheckCircle />,
    text: "Instant Loan Eligibility Check",
    description:
      "Quickly assess your loan eligibility and discover the best offers tailored to your credit profile.",
  },
  {
    icon: <ShieldCheck />,
    text: "Automated KYC & Verification",
    description:
      "Verify identity and documents seamlessly through AI-based KYC, ensuring security and compliance.",
  },
  {
    icon: <FileText />,
    text: "Smart Document Handling",
    description:
      "Upload, store, and retrieve all financial documents securely with automated data extraction and tagging.",
  },
];




export const checklistItems = [
    {
        title: "Quick and Secure Login",
        description:
          "Start by logging in and setting up your FinWise profile effortlessly.",
      }, 
    {
      title: "Connect Your Bank Accounts",
      description:
        "Link your bank account to enable real-time analysis.",
    },
    {
      title: "Chat with Our AI Assistant",
      description:
        "Our AI chatbot provides instant, data-driven insights.",
    },
    {
      title: "Get Personalized Financial Plan",
      description:
        "Receive tailored budgeting, investment, and saving strategies.",
    },
    {
      title: "Check Loan Eligibility & KYC Status",
      description:
        "verify your KYC and check your loan eligibility in seconds.",
    },
    {
      title: "Track and Improve Your Finances",
      description:
        "Monitor spending, credit score, and performance trends to make smarter financial moves.",
    }
  ];
  
export const pricingOptions = [
  {
    title: "Basic",
    price: "₹0",
    features: [
      "AI-powered financial insights",
      "Personalized budgeting",
      "Access to savings & investment tools",
      "Secure account and data management",
    ],
  },
  {
    title: "Standard",
    price: "₹299.99",
    features: [
      "Advanced financial planning with smart analytics",
      "Real-time expense tracking and alerts",
      "Loan eligibility and KYC verification",
      "Priority chatbot assistance",
    ],
  },
  {
    title: "Premium",
    price: "₹499.99",
    features: [
      "Portfolio management",
      "Automated investment recommendations",
      "Seamless multi-bank integration",
      "Dedicated 24/7 financial advisor support",
    ],
  },
];


export const resourcesLinks = [
  { href: "#", text: "Getting Started" },
  { href: "#", text: "Documentation" },
  { href: "#", text: "Tutorials" },
  { href: "#", text: "API Reference" },
  { href: "#", text: "Community Forums" },
];

export const platformLinks = [
  { href: "#", text: "Features" },
  { href: "#", text: "Supported Devices" },
  { href: "#", text: "System Requirements" },
  { href: "#", text: "Downloads" },
  { href: "#", text: "Release Notes" },
];

export const communityLinks = [
  { href: "#", text: "Events" },
  { href: "#", text: "Meetups" },
  { href: "#", text: "Conferences" },
  { href: "#", text: "Hackathons" },
  { href: "#", text: "Jobs" },
];