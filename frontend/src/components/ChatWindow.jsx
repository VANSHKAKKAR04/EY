import React, { useState } from "react";
import { sendMessage } from "../services/api";

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    const userMsg = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);

    const reply = await sendMessage(input);
    const botMsg = { sender: "bot", text: reply };
    setMessages((prev) => [...prev, botMsg]);
    setInput("");
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
