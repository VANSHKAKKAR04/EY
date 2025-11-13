import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ChatWindow from "./components/ChatWindow";
import LoanLandingPage from "./pages/LandingPage";
import LandingPage from "./pages/LandingPage2";

export default function App() {
  return (
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/chat" element={<ChatWindow />} />
      </Routes>
  );
}