import React, { useState } from "react";
import {
  Send,
  Upload,
  Loader2,
  CheckCircle2,
  AlertCircle,
  Download,
} from "lucide-react";
import { sendMessage, uploadSalarySlip } from "../services/api";

export default function ChatWindow() {
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hello! Welcome to our loan application service. How can I assist you today?",
    },
  ]);

  const [input, setInput] = useState("");
  const [stage, setStage] = useState("greeting");
  const [awaitingSalarySlip, setAwaitingSalarySlip] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [sending, setSending] = useState(false);

  // -----------------------------------------------------------
  // SEND MESSAGE TO BACKEND
  // -----------------------------------------------------------
  const handleSend = async () => {
    if (!input.trim() || sending) return;

    const msg = input;
    setMessages((prev) => [...prev, { sender: "user", text: msg }]);
    setInput("");
    setSending(true);

    try {
      const {
        message,
        stage: newStage,
        awaitingSalarySlip: awaiting,
        file,
      } = await sendMessage(msg);

      setMessages((prev) => [...prev, { sender: "bot", text: message, file }]);
      setStage(newStage);
      setAwaitingSalarySlip(awaiting);
    } finally {
      setSending(false);
    }
  };

  // -----------------------------------------------------------
  // HANDLE SALARY SLIP UPLOAD
  // -----------------------------------------------------------
  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);

    try {
      const {
        message,
        stage: newStage,
        awaitingSalarySlip: awaiting,
        file: fileLink,
      } = await uploadSalarySlip(file);

      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: message, file: fileLink },
      ]);
      setStage(newStage);
      setAwaitingSalarySlip(awaiting);
    } finally {
      setUploading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // -----------------------------------------------------------
  // HANDLE SANCTION LETTER DOWNLOAD
  // -----------------------------------------------------------
  const downloadFile = (filename) => {
    window.open(
      `http://localhost:8000/download-sanction/${filename}`,
      "_blank"
    );
  };

  return (
    <div className="w-full max-w-2xl mx-auto h-screen flex flex-col bg-gradient-to-br from-slate-50 to-slate-100 p-4">
      {/* HEADER */}
      <div className="bg-white rounded-t-2xl shadow-sm border border-slate-200 p-4 flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center text-white font-semibold">
          LA
        </div>
        <div>
          <h2 className="font-semibold text-slate-800">Loan Assistant</h2>
          <p className="text-xs text-slate-500">Online • Ready to help</p>
        </div>
      </div>

      {/* MESSAGES */}
      <div className="flex-1 overflow-y-auto bg-white border-x border-slate-200 p-4 space-y-3">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`flex ${
              m.sender === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[75%] rounded-2xl px-4 py-2.5 shadow-sm ${
                m.sender === "user"
                  ? "bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-br-md"
                  : "bg-slate-100 text-slate-800 rounded-bl-md"
              }`}
            >
              <p className="text-sm leading-relaxed">{m.text}</p>
              {m.file && (
                <button
                  onClick={() => downloadFile(m.file)}
                  className="mt-2 flex items-center gap-1 text-blue-600 text-sm font-medium"
                >
                  <Download className="w-4 h-4" />
                  Download Sanction Letter
                </button>
              )}
            </div>
          </div>
        ))}

        {sending && (
          <div className="flex justify-start">
            <div className="bg-slate-100 rounded-2xl rounded-bl-md px-4 py-3 shadow-sm">
              <div className="flex gap-1.5">
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
                <div
                  className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"
                  style={{ animationDelay: "150ms" }}
                ></div>
                <div
                  className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"
                  style={{ animationDelay: "300ms" }}
                ></div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* SALARY SLIP UPLOAD */}
      {awaitingSalarySlip && stage === "salary_slip" && (
        <div className="bg-white border-x border-slate-200 px-4 py-3">
          <div className="bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 rounded-xl p-4">
            <div className="flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-amber-600 mt-0.5" />
              <div className="flex-1">
                <h3 className="font-semibold text-amber-900 text-sm mb-1">
                  Upload Required
                </h3>
                <p className="text-xs text-amber-700 mb-3">
                  Please upload your salary slip to proceed.
                </p>

                {uploading ? (
                  <div className="flex items-center gap-2 text-blue-600">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span className="text-sm font-medium">
                      Uploading document...
                    </span>
                  </div>
                ) : (
                  <label className="flex items-center gap-2 px-4 py-2 bg-white border border-amber-300 rounded-lg cursor-pointer hover:bg-amber-50 transition-colors">
                    <Upload className="w-4 h-4 text-amber-600" />
                    <span className="text-sm font-medium text-amber-700">
                      Upload Salary Slip
                    </span>
                    <input
                      type="file"
                      accept=".pdf,.png,.jpg"
                      onChange={handleUpload}
                      className="hidden"
                    />
                  </label>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* UNDERWRITING BANNER */}
      {stage === "underwriting" && (
        <div className="bg-white border-x border-slate-200 px-4 py-3">
          <div className="bg-gradient-to-r from-emerald-50 to-green-50 border border-emerald-200 rounded-xl p-4 flex items-start gap-3">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 mt-0.5" />
            <div>
              <h3 className="font-semibold text-emerald-900 text-sm mb-1">
                Underwriting in Progress
              </h3>
              <p className="text-xs text-emerald-700">
                We’re evaluating your profile. This usually takes a few moments.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* INPUT BAR */}
      <div className="bg-white rounded-b-2xl shadow-sm border border-slate-200 p-4">
        <div className="flex gap-2">
          <input
            className="flex-1 border border-slate-300 rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            disabled={sending}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || sending}
            className="px-5 py-2.5 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-xl font-medium hover:from-blue-600 hover:to-blue-700 disabled:opacity-50"
          >
            {sending ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
