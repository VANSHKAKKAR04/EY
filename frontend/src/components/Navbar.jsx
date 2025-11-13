import React, { useState, useEffect } from 'react';
import { MessageCircle, Menu, X, User, BadgeIndianRupee } from 'lucide-react';

export default function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [productsOpen, setProductsOpen] = useState(false);
  const [resourcesOpen, setResourcesOpen] = useState(false);
  const [accountOpen, setAccountOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const closeAllDropdowns = () => {
    setProductsOpen(false);
    setResourcesOpen(false);
    setAccountOpen(false);
  };

  useEffect(() => {
    const handleClickOutside = () => closeAllDropdowns();
    
    if (productsOpen || resourcesOpen || accountOpen) {
      document.addEventListener('click', handleClickOutside);
      return () => document.removeEventListener('click', handleClickOutside);
    }
  }, [productsOpen, resourcesOpen, accountOpen]);

  return (
    <nav className={`fixed w-full top-0 z-[100] transition-all duration-300 ${
      isScrolled ? 'bg-white shadow-lg' : 'bg-white/95 backdrop-blur-sm'
    }`}>
      <div className="max-w-7xl mx-auto px-6 py-4 relative">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <a href="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
              <BadgeIndianRupee className="w-6 h-6 text-white" />
            </div>
            <span className="text-2xl font-bold text-slate-800">FinWise</span>
          </a>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex items-center gap-8">
            <a href="/" className="text-slate-600 hover:text-blue-600 transition-colors font-medium">
              Home
            </a>

            {/* Products Dropdown */}
            <div className="relative static">
              <button 
                onClick={(e) => {
                  e.stopPropagation();
                  setProductsOpen(!productsOpen);
                  setResourcesOpen(false);
                  setAccountOpen(false);
                }}
                className={`text-slate-600 hover:text-blue-600 transition-colors font-medium ${
                  productsOpen ? 'text-blue-600' : ''
                }`}
              >
                Products ▾
              </button>
              
              {productsOpen && (
                <div 
                  onClick={(e) => e.stopPropagation()}
                  className="fixed mt-2 w-56 bg-white rounded-xl shadow-xl border border-slate-200 overflow-hidden z-[110]"
                  style={{
                    top: '60px',
                    left: 'calc(50% - 350px + 60px)'
                  }}
                >
                  <a href="/personal-loans" className="block px-4 py-3 hover:bg-blue-50 transition-colors border-b border-slate-100">
                    <div className="font-semibold text-slate-800">Personal Loans</div>
                    <div className="text-sm text-slate-500">Quick & easy loans</div>
                  </a>
                  <a href="/business-loans" className="block px-4 py-3 hover:bg-blue-50 transition-colors border-b border-slate-100">
                    <div className="font-semibold text-slate-800">Business Loans</div>
                    <div className="text-sm text-slate-500">Grow your business</div>
                  </a>
                  <a href="/education-loans" className="block px-4 py-3 hover:bg-blue-50 transition-colors border-b border-slate-100">
                    <div className="font-semibold text-slate-800">Education Loans</div>
                    <div className="text-sm text-slate-500">Invest in your future</div>
                  </a>
                  <a href="/loan-calculator" className="block px-4 py-3 hover:bg-blue-50 transition-colors">
                    <div className="font-semibold text-slate-800">EMI Calculator</div>
                    <div className="text-sm text-slate-500">Calculate your EMI</div>
                  </a>
                </div>
              )}
            </div>

            <a href="/eligibility" className="text-slate-600 hover:text-blue-600 transition-colors font-medium">
              Check Eligibility
            </a>

            {/* Resources Dropdown */}
            <div className="relative static">
              <button 
                onClick={(e) => {
                  e.stopPropagation();
                  setResourcesOpen(!resourcesOpen);
                  setProductsOpen(false);
                  setAccountOpen(false);
                }}
                className={`text-slate-600 hover:text-blue-600 transition-colors font-medium ${
                  resourcesOpen ? 'text-blue-600' : ''
                }`}
              >
                Resources ▾
              </button>
              
              {resourcesOpen && (
                <div 
                  onClick={(e) => e.stopPropagation()}
                  className="fixed mt-2 w-56 bg-white rounded-xl shadow-xl border border-slate-200 overflow-hidden z-[110]"
                  style={{
                    top: '60px',
                    left: 'calc(50% - 350px + 300px)'
                  }}
                >
                  <a href="/blog" className="block px-4 py-3 hover:bg-blue-50 transition-colors border-b border-slate-100">
                    <div className="font-semibold text-slate-800">Blog</div>
                    <div className="text-sm text-slate-500">Financial tips & guides</div>
                  </a>
                  <a href="/faqs" className="block px-4 py-3 hover:bg-blue-50 transition-colors border-b border-slate-100">
                    <div className="font-semibold text-slate-800">FAQs</div>
                    <div className="text-sm text-slate-500">Common questions</div>
                  </a>
                  <a href="/how-it-works" className="block px-4 py-3 hover:bg-blue-50 transition-colors border-b border-slate-100">
                    <div className="font-semibold text-slate-800">How It Works</div>
                    <div className="text-sm text-slate-500">Learn about our process</div>
                  </a>
                  <a href="/customer-stories" className="block px-4 py-3 hover:bg-blue-50 transition-colors">
                    <div className="font-semibold text-slate-800">Customer Stories</div>
                    <div className="text-sm text-slate-500">Success stories</div>
                  </a>
                </div>
              )}
            </div>

            <a href="/support" className="text-slate-600 hover:text-blue-600 transition-colors font-medium">
              Support
            </a>

            <a href="/about" className="text-slate-600 hover:text-blue-600 transition-colors font-medium">
              About Us
            </a>

            {/* Account Dropdown */}
            <div className="relative static">
              <button 
                onClick={(e) => {
                  e.stopPropagation();
                  setAccountOpen(!accountOpen);
                  setProductsOpen(false);
                  setResourcesOpen(false);
                }}
                className={`flex items-center gap-2 text-slate-600 hover:text-blue-600 transition-colors font-medium ${
                  accountOpen ? 'text-blue-600' : ''
                }`}
              >
                <User className="w-5 h-5" />
                Account ▾
              </button>
              
              {accountOpen && (
                <div 
                  onClick={(e) => e.stopPropagation()}
                  className="fixed mt-2 w-48 bg-white rounded-xl shadow-xl border border-slate-200 overflow-hidden z-[110]"
                  style={{
                    top: '60px',
                    left: '50%+ 600px'
                  }}
                >
                  <a href="/dashboard" className="block px-4 py-3 hover:bg-blue-50 transition-colors text-slate-700 border-b border-slate-100">
                    Dashboard
                  </a>
                  <a href="/my-loans" className="block px-4 py-3 hover:bg-blue-50 transition-colors text-slate-700 border-b border-slate-100">
                    My Loans
                  </a>
                  <a href="/profile" className="block px-4 py-3 hover:bg-blue-50 transition-colors text-slate-700 border-b border-slate-100">
                    Profile Settings
                  </a>
                  <a href="/documents" className="block px-4 py-3 hover:bg-blue-50 transition-colors text-slate-700">
                    Documents
                  </a>
                </div>
              )}
            </div>

            {/* CTA Button */}
            <button
              onClick={() => window.location.href = '/chat'}
              className="flex items-center gap-2 bg-gradient-to-r from-blue-600 to-blue-700 text-white px-5 py-2.5 rounded-lg hover:shadow-lg hover:scale-105 transition-all duration-200 font-medium"
            >
              <MessageCircle className="w-5 h-5" />
              Get Started
            </button>
          </div>

          {/* Mobile Menu Button */}
          <button 
            className="lg:hidden p-2 text-slate-600 hover:text-blue-600 transition-colors"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Menu */}
        <div className={`lg:hidden overflow-hidden transition-all duration-300 ${
          mobileMenuOpen ? 'max-h-[800px] opacity-100' : 'max-h-0 opacity-0'
        }`}>
          <div className="pt-4 pb-4 border-t border-slate-200 space-y-2">
            <a href="/" className="block px-4 py-3 text-slate-600 hover:bg-blue-50 rounded-lg transition-colors">
              Home
            </a>
            
            {/* Products Mobile */}
            <div className="px-4 py-2">
              <div className="font-semibold text-slate-800 mb-2 flex items-center gap-2">
                Products
                <div className="h-px flex-1 bg-slate-200"></div>
              </div>
              <div className="pl-4 space-y-2">
                <a href="/personal-loans" className="block py-2 text-slate-600 hover:text-blue-600 transition-colors">
                  Personal Loans
                </a>
                <a href="/business-loans" className="block py-2 text-slate-600 hover:text-blue-600 transition-colors">
                  Business Loans
                </a>
                <a href="/education-loans" className="block py-2 text-slate-600 hover:text-blue-600 transition-colors">
                  Education Loans
                </a>
                <a href="/loan-calculator" className="block py-2 text-slate-600 hover:text-blue-600 transition-colors">
                  EMI Calculator
                </a>
              </div>
            </div>

            <a href="/eligibility" className="block px-4 py-3 text-slate-600 hover:bg-blue-50 rounded-lg transition-colors">
              Check Eligibility
            </a>

            {/* Resources Mobile */}
            <div className="px-4 py-2">
              <div className="font-semibold text-slate-800 mb-2 flex items-center gap-2">
                Resources
                <div className="h-px flex-1 bg-slate-200"></div>
              </div>
              <div className="pl-4 space-y-2">
                <a href="/blog" className="block py-2 text-slate-600 hover:text-blue-600 transition-colors">
                  Blog
                </a>
                <a href="/faqs" className="block py-2 text-slate-600 hover:text-blue-600 transition-colors">
                  FAQs
                </a>
                <a href="/how-it-works" className="block py-2 text-slate-600 hover:text-blue-600 transition-colors">
                  How It Works
                </a>
                <a href="/customer-stories" className="block py-2 text-slate-600 hover:text-blue-600 transition-colors">
                  Customer Stories
                </a>
              </div>
            </div>

            <a href="/support" className="block px-4 py-3 text-slate-600 hover:bg-blue-50 rounded-lg transition-colors">
              Support
            </a>

            <a href="/about" className="block px-4 py-3 text-slate-600 hover:bg-blue-50 rounded-lg transition-colors">
              About Us
            </a>

            {/* Account Mobile */}
            <div className="px-4 py-2">
              <div className="font-semibold text-slate-800 mb-2 flex items-center gap-2">
                <User className="w-4 h-4" />
                Account
                <div className="h-px flex-1 bg-slate-200"></div>
              </div>
              <div className="pl-4 space-y-2">
                <a href="/dashboard" className="block py-2 text-slate-600 hover:text-blue-600 transition-colors">
                  Dashboard
                </a>
                <a href="/my-loans" className="block py-2 text-slate-600 hover:text-blue-600 transition-colors">
                  My Loans
                </a>
                <a href="/profile" className="block py-2 text-slate-600 hover:text-blue-600 transition-colors">
                  Profile Settings
                </a>
                <a href="/documents" className="block py-2 text-slate-600 hover:text-blue-600 transition-colors">
                  Documents
                </a>
              </div>
            </div>

            <button
              onClick={() => window.location.href = '/chat'}
              className="w-full mt-4 flex items-center justify-center gap-2 bg-gradient-to-r from-blue-600 to-blue-700 text-white px-5 py-3 rounded-lg hover:shadow-lg transition-all duration-200 font-medium"
            >
              <MessageCircle className="w-5 h-5" />
              Get Started
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}