import { Routes, Route } from "react-router-dom";
import ChatWindow from "./components/ChatWindow";
import LoanLandingPage from "./pages/LandingPage";
import LandingPage from "./pages/LandingPage2";
import Signup from "./pages/Signup";
import Login from "./pages/Login";
import Profile from "./pages/Profile";
import AboutUs from "./pages/AboutUs";
import Support from "./pages/Support.jsx";
import Blog from "./pages/Blog.jsx";
import FAQ from "./pages/FAQ.jsx";
import CustomerStories from "./pages/CustomerStories.jsx";
export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/chat" element={<ChatWindow />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/login" element={<Login />} />
      <Route path="/about" element={<AboutUs />} />
      <Route path="/support" element={<Support />} />
      <Route path="/blog" element={<Blog />} />
      <Route path="/faqs" element={<FAQ />} />
      <Route path="/customer-stories" element={<CustomerStories />} />
      <Route path="/profile" element={<Profile />} />
    </Routes>
  );
}
