import { useState } from "react";

export default function QueryForm({ onSend }) {
  const [query, setQuery] = useState("");

  const handleSend = () => {
    const trimmed = query.trim();
    if (!trimmed) return;
    onSend(trimmed);
  };

  const onKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div>
      <label style={{ display: "block", marginBottom: 8, color: "#1e3a8a", fontWeight: 600 }}>
        Enter a component/product to be queried:
      </label>
      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={onKeyDown}
        rows={4}
        placeholder='(e.g. "night vision goggles")'
        style={{
          width: "100%",
          padding: 12,
          borderRadius: 8,
          border: "1px solid #cbd5e1",
          resize: "vertical",
          background: "#f8fafc",
          color: "black",
        }}
      />

      <button
        onClick={handleSend}
        style={{
          marginTop: 12,
          width: "100%",
          padding: 12,
          borderRadius: 8,
          border: "none",
          background: "#2563eb",
          color: "white",
          fontSize: 16,
          fontWeight: 600,
          cursor: "pointer",
        }}
      >
        Send
      </button>
    </div>
  );
}
