import { Routes, Route } from "react-router-dom";
import ChatWindow from "./components/ChatWindow";
import LoanLandingPage from "./pages/LandingPage";
import LandingPage from "./pages/LandingPage2";
import Signup from "./pages/Signup";
import Login from "./pages/Login";
import Profile from "./pages/Profile";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/chat" element={<ChatWindow />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/login" element={<Login />} />
      <Route path="/profile" element={<Profile />} />
    </Routes>
  );
}
