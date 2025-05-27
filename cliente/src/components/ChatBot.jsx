import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function ChatBot() {
  const [messages, setMessages] = useState([
    { from: "bot", text: "Olá! Como posso ajudar?" },
  ]);
  const [input, setInput] = useState("");
  const navigate = useNavigate();

  const usuaruiTexto = async () => {
    if (!input.trim()) return;
    const userMsg = { from: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    sendMessage();
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    try {
      const res = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: input }),
      });

      const data = await res.json();

      if (data.reply == "{}" || data.reply == "{ }") {
        sendMessage();
        return;
      }
      // Mostra resposta do bot
      if (data.reply) {
        setMessages((prev) => [...prev, { from: "bot", text: data.reply }]);
      }

      // Redireciona se tiver rota no backend
      if (data.app_rota) {
        setTimeout(() => navigate(`/${data.app_rota}`), 1000);
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { from: "bot", text: "Erro ao conectar com o servidor." },
      ]);
    }
  };

  return (
    <div
      style={{
        maxWidth: 400,
        margin: "0 auto",
        padding: 20,
        border: "1px solid #ccc",
      }}
    >
      <div
        style={{
          height: 300,
          overflowY: "auto",
          marginBottom: 10,
          padding: 10,
          background: "#f9f9f9",
        }}
      >
        {messages.map((m, i) => (
          <div
            key={i}
            style={{
              textAlign: m.from === "bot" ? "left" : "right",
              margin: "5px 0",
            }}
          >
            <strong>{m.from === "bot" ? "Bot:" : "Você:"}</strong> {m.text}
          </div>
        ))}
      </div>
      <div style={{ display: "flex" }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && usuaruiTexto()}
          placeholder="Digite sua mensagem..."
          style={{ flex: 1, padding: 8 }}
        />
        <button
          onClick={usuaruiTexto}
          style={{ marginLeft: 8, padding: "8px 12px" }}
        >
          Enviar
        </button>
      </div>
    </div>
  );
}
