import React, { useState } from "react";
import { sendMessage, uploadSalarySlip } from "../services/api";

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [stage, setStage] = useState("greeting");
  const [uploading, setUploading] = useState(false);

  const handleSend = async () => {
    const userMsg = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);

    const { response, stage: newStage } = await sendMessage(input);
    setMessages((prev) => [...prev, { sender: "bot", text: response }]);
    setStage(newStage);
    setInput("");
  };

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    const res = await uploadSalarySlip(file);
    setMessages((prev) => [
      ...prev,
      { sender: "bot", text: res.message || res.error },
    ]);
    setUploading(false);
  };

  return (
    <div className="w-full max-w-md mx-auto p-4 border rounded-lg">
      <div className="h-96 overflow-y-auto mb-3 bg-gray-50 p-2 rounded">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`my-1 p-2 rounded ${
              m.sender === "user"
                ? "bg-blue-100 text-right"
                : "bg-gray-200 text-left"
            }`}
          >
            {m.text}
          </div>
        ))}
      </div>

      {/* KYC Progress Section */}
      {stage === "kyc" && (
        <div className="mb-3 p-2 text-sm bg-yellow-50 border rounded">
          🔍 KYC verification in progress...
          {uploading ? (
            <p className="text-blue-500 mt-1">Uploading salary slip...</p>
          ) : (
            <div className="mt-2">
              <label className="block text-sm font-medium text-gray-700">
                Upload Salary Slip:
              </label>
              <input
                type="file"
                accept=".pdf,.jpg,.png"
                onChange={handleUpload}
                className="mt-1"
              />
            </div>
          )}
        </div>
      )}

      {stage === "underwriting" && (
        <div className="mb-3 p-2 text-sm bg-green-50 border rounded">
          📊 Underwriting in progress... Evaluating eligibility and risk
          profile.
        </div>
      )}

      <div className="flex">
        <input
          className="flex-1 border rounded p-2"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
        />
        <button
          onClick={handleSend}
          className="ml-2 px-4 py-2 bg-blue-600 text-white rounded"
        >
          Send
        </button>
      </div>
    </div>
  );
}
