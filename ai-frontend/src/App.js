import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL = "http://127.0.0.1:8000/chat-stream";
const API_KEY = "my-secret-key";

function App() {

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {

    if (!input) return;

    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    let botMessage = { role: "assistant", content: "" };
    setMessages([...newMessages, botMessage]);

    try {

      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": API_KEY
        },
        body: JSON.stringify({ message: input })
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let result = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        result += chunk;

        botMessage.content = result;
        setMessages([...newMessages, { ...botMessage }]);
      }

    } catch (error) {
      botMessage.content = "⚠️ Error connecting to API";
      setMessages([...newMessages, botMessage]);
    }

    setLoading(false);
  };

  return (
    <div className="app">

      <h1>🤖 AI Assistant</h1>

      <div className="chat-box">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
      </div>

      <div className="input-box">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something..."
        />
        <button onClick={sendMessage} disabled={loading}>
          Send
        </button>
      </div>

    </div>
  );
}

export default App;