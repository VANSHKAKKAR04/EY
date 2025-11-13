import React, { useState, useEffect } from 'react';
import { MessageCircle, Shield, Zap, CheckCircle, Clock, Users, X } from 'lucide-react';

export default function LoanLandingPage() {
  const [showChatPopup, setShowChatPopup] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setShowChatPopup(true), 3000);
    const handleScroll = () => setIsScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll);
    return () => {
      clearTimeout(timer);
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  const handleStartChat = () => {
    window.location.href = '/chat';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Navbar */}
      <nav className={`fixed w-full top-0 z-50 transition-all duration-300 ${
        isScrolled ? 'bg-white shadow-lg' : 'bg-transparent'
      }`}>
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg flex items-center justify-center">
              <MessageCircle className="w-6 h-6 text-white" />
            </div>
            <span className="text-2xl font-bold text-slate-800">SmartLoan</span>
          </div>
          <div className="hidden md:flex items-center gap-8">
            <a href="#home" className="text-slate-600 hover:text-blue-600 transition-colors">Home</a>
            <a href="#loans" className="text-slate-600 hover:text-blue-600 transition-colors">About Loans</a>
            <a href="#support" className="text-slate-600 hover:text-blue-600 transition-colors">Support</a>
            <a href="#login" className="text-slate-600 hover:text-blue-600 transition-colors">Login</a>
            <button 
              onClick={handleStartChat}
              className="px-6 py-2.5 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg font-semibold hover:shadow-lg hover:scale-105 transition-all duration-300"
            >
              Start Chat
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6">
        <div className="max-w-7xl mx-auto grid md:grid-cols-2 gap-12 items-center">
          <div className="space-y-6">
            <div className="inline-block px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-semibold">
              🤖 AI-Powered Loan Assistant
            </div>
            <h1 className="text-5xl md:text-6xl font-bold text-slate-900 leading-tight">
              Meet Your Smart Loan Assistant
            </h1>
            <p className="text-xl text-slate-600 leading-relaxed">
              Get <span className="font-semibold text-blue-600">Instant Personal Loans</span> in Minutes
            </p>
            <p className="text-lg text-slate-500">
              Chat with our AI-powered assistant to check eligibility, verify KYC, and get your sanction letter instantly.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 pt-4">
              <button 
                onClick={handleStartChat}
                className="px-8 py-4 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl font-semibold text-lg hover:shadow-2xl hover:scale-105 transition-all duration-300 flex items-center justify-center gap-2"
              >
                <MessageCircle className="w-5 h-5" />
                Start Your Loan Chat
              </button>
              <button className="px-8 py-4 bg-white text-slate-700 rounded-xl font-semibold text-lg border-2 border-slate-200 hover:border-blue-600 hover:text-blue-600 transition-all duration-300">
                Learn More
              </button>
            </div>
            <div className="flex items-center gap-8 pt-6">
              <div className="flex items-center gap-2">
                <CheckCircle className="w-5 h-5 text-green-500" />
                <span className="text-sm text-slate-600">No paperwork</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="w-5 h-5 text-green-500" />
                <span className="text-sm text-slate-600">Instant approval</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="w-5 h-5 text-green-500" />
                <span className="text-sm text-slate-600">100% digital</span>
              </div>
            </div>
          </div>
          
          {/* Animated AI Assistant */}
          <div className="relative">
            <div className="relative z-10">
              <ChatbotIllustration />
            </div>
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-blue-200 rounded-full blur-3xl opacity-30"></div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 px-6 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-4">
              How It Works
            </h2>
            <p className="text-xl text-slate-600">
              Get your personal loan in 3 simple steps
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <StepCard 
              number="01"
              icon={<MessageCircle className="w-8 h-8" />}
              title="Start Chat"
              description="Tell us your loan needs and preferred amount through our friendly AI assistant."
            />
            <StepCard 
              number="02"
              icon={<Zap className="w-8 h-8" />}
              title="AI Verification"
              description="Our AI verifies your details and evaluates eligibility in real-time with instant credit checks."
            />
            <StepCard 
              number="03"
              icon={<CheckCircle className="w-8 h-8" />}
              title="Get Approved"
              description="Receive your sanction letter instantly and get funds disbursed within 24 hours."
            />
          </div>
        </div>
      </section>

      {/* Trust Section */}
      <section className="py-20 px-6 bg-gradient-to-br from-slate-900 to-blue-900 text-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4">Trusted by Millions</h2>
            <p className="text-xl text-blue-200">Your security and trust is our priority</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8 mb-16">
            <TrustBadge 
              icon={<Shield className="w-12 h-12" />}
              title="Secure & RBI Compliant"
              description="Bank-grade security with full regulatory compliance"
            />
            <TrustBadge 
              icon={<Users className="w-12 h-12" />}
              title="1M+ Happy Customers"
              description="Join millions who trust us for their financial needs"
            />
            <TrustBadge 
              icon={<Clock className="w-12 h-12" />}
              title="Instant Decision Engine"
              description="Get approval decisions in under 2 minutes"
            />
          </div>

          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 max-w-3xl mx-auto border border-white/20">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-2xl">⭐</span>
              </div>
              <div>
                <p className="text-lg mb-4 italic">
                  "The AI chatbot made the entire loan process incredibly smooth. I got approved in minutes and the funds were in my account the next day. Highly recommend!"
                </p>
                <p className="font-semibold">— Priya Sharma</p>
                <p className="text-blue-200 text-sm">Small Business Owner, Mumbai</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 text-slate-300 py-12 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg flex items-center justify-center">
                  <MessageCircle className="w-6 h-6 text-white" />
                </div>
                <span className="text-2xl font-bold text-white">SmartLoan</span>
              </div>
              <p className="text-sm">Your trusted partner for instant personal loans powered by AI.</p>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Products</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-blue-400 transition-colors">Personal Loans</a></li>
                <li><a href="#" className="hover:text-blue-400 transition-colors">Business Loans</a></li>
                <li><a href="#" className="hover:text-blue-400 transition-colors">EMI Calculator</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Company</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-blue-400 transition-colors">About Us</a></li>
                <li><a href="#" className="hover:text-blue-400 transition-colors">Careers</a></li>
                <li><a href="#" className="hover:text-blue-400 transition-colors">Contact</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Legal</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-blue-400 transition-colors">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-blue-400 transition-colors">Terms & Conditions</a></li>
                <li><a href="#" className="hover:text-blue-400 transition-colors">Disclaimer</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-slate-700 pt-8 text-center text-sm">
            <p>© 2025 SmartLoan NBFC. All rights reserved. | RBI Registered NBFC</p>
            <p className="mt-2 text-xs text-slate-400">*Terms & Conditions Apply. Loans subject to approval.</p>
          </div>
        </div>
      </footer>

      {/* Floating Chat Popup */}
      {showChatPopup && (
        <div className="fixed bottom-6 right-6 z-50 animate-bounce">
          <div className="bg-white rounded-2xl shadow-2xl p-4 max-w-xs relative border-2 border-blue-500">
            <button 
              onClick={() => setShowChatPopup(false)}
              className="absolute -top-2 -right-2 w-6 h-6 bg-slate-600 text-white rounded-full flex items-center justify-center hover:bg-slate-700 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
            <div className="flex items-start gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-blue-800 rounded-full flex items-center justify-center flex-shrink-0">
                <MessageCircle className="w-6 h-6 text-white" />
              </div>
              <div className="flex-1">
                <p className="font-semibold text-slate-900 mb-1">💬 Hi there!</p>
                <p className="text-sm text-slate-600 mb-3">I'm your AI Loan Assistant. Want to check your eligibility?</p>
                <button 
                  onClick={handleStartChat}
                  className="w-full px-4 py-2 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg font-semibold text-sm hover:shadow-lg transition-all duration-300"
                >
                  Start Chat
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function ChatbotIllustration() {
  return (
    <div className="relative w-full h-96">
      {/* Main chatbot */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
        <div className="w-64 h-80 bg-gradient-to-br from-blue-600 to-blue-800 rounded-3xl shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-24 bg-gradient-to-b from-white/10 to-transparent"></div>
          
          {/* Screen */}
          <div className="absolute top-8 left-6 right-6 bottom-8 bg-white rounded-2xl p-4 space-y-3">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-blue-600 rounded-full"></div>
              <div className="flex-1 h-2 bg-slate-200 rounded"></div>
            </div>
            
            <ChatBubble align="left" delay={0} />
            <ChatBubble align="right" delay={1} />
            <ChatBubble align="left" delay={2} />
          </div>
          
          {/* Home button */}
          <div className="absolute bottom-3 left-1/2 -translate-x-1/2 w-12 h-1 bg-white/30 rounded-full"></div>
        </div>
      </div>
      
      {/* Floating elements */}
      <FloatingIcon icon="💰" delay={0} x={-100} y={-50} />
      <FloatingIcon icon="✅" delay={1} x={100} y={-80} />
      <FloatingIcon icon="⚡" delay={2} x={-80} y={100} />
      <FloatingIcon icon="🔒" delay={1.5} x={120} y={80} />
    </div>
  );
}

function ChatBubble({ align, delay }) {
  const [visible, setVisible] = useState(false);
  
  useEffect(() => {
    const timer = setTimeout(() => setVisible(true), delay * 1000);
    return () => clearTimeout(timer);
  }, [delay]);

  if (!visible) return null;

  return (
    <div className={`flex ${align === 'right' ? 'justify-end' : 'justify-start'} animate-fade-in`}>
      <div className={`max-w-[70%] h-8 rounded-2xl ${
        align === 'right' ? 'bg-blue-600' : 'bg-slate-200'
      }`}></div>
    </div>
  );
}

function FloatingIcon({ icon, delay, x, y }) {
  return (
    <div 
      className="absolute animate-float"
      style={{
        left: `calc(50% + ${x}px)`,
        top: `calc(50% + ${y}px)`,
        animationDelay: `${delay}s`
      }}
    >
      <div className="w-16 h-16 bg-white rounded-2xl shadow-lg flex items-center justify-center text-3xl">
        {icon}
      </div>
    </div>
  );
}

function StepCard({ number, icon, title, description }) {
  return (
    <div className="bg-gradient-to-br from-slate-50 to-blue-50 rounded-2xl p-8 hover:shadow-xl transition-all duration-300 hover:-translate-y-2 border border-slate-200">
      <div className="text-6xl font-bold text-blue-100 mb-4">{number}</div>
      <div className="w-16 h-16 bg-gradient-to-br from-blue-600 to-blue-800 rounded-xl flex items-center justify-center text-white mb-4">
        {icon}
      </div>
      <h3 className="text-2xl font-bold text-slate-900 mb-3">{title}</h3>
      <p className="text-slate-600 leading-relaxed">{description}</p>
    </div>
  );
}

function TrustBadge({ icon, title, description }) {
  return (
    <div className="text-center">
      <div className="w-24 h-24 bg-white/10 backdrop-blur-lg rounded-2xl flex items-center justify-center mx-auto mb-4 border border-white/20">
        <div className="text-blue-300">
          {icon}
        </div>
      </div>
      <h3 className="text-xl font-bold mb-2">{title}</h3>
      <p className="text-blue-200">{description}</p>
    </div>
  );
}

// Add custom animations
const style = document.createElement('style');
style.textContent = `
  @keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
  }
  @keyframes fade-in {
    from { opacity: 0; transform: scale(0.8); }
    to { opacity: 1; transform: scale(1); }
  }
  .animate-float {
    animation: float 3s ease-in-out infinite;
  }
  .animate-fade-in {
    animation: fade-in 0.5s ease-out;
  }
`;
document.head.appendChild(style);