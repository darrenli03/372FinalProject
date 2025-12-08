import { useState } from "react";
import QueryForm from "./components/QueryForm";
import ResponseDisplay from "./components/ResponseDisplay";

function App() {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendQuery = async (text) => {
    setLoading(true);
    setError(null);
    setResponse(null);
    try {
      const encoded = encodeURIComponent(text);
      const res = await fetch(`https://api.export.darrenli.org:443/query_single?search_query=${encoded}`, {
        method: "POST",
      });

      if (!res.ok) {
        const err = await res.json().catch(() => null);
        throw new Error(err?.detail || `${res.status} ${res.statusText}`);
      }

      const data = await res.json();
      // The backend returns {query, response, excerpts}
      setResponse({ response: data.response || data.answer, excerpts: data.excerpts || [] });
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        height: "100vh",
        width: "100vw",
        background: "#f3f6fb",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "20px",
      }}
    >
      <div
        style={{
          background: "white",
          padding: "24px",
          width: "600px",
          borderRadius: "12px",
          boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
          border: "1px solid #e6e9f0",
          display: "flex",
          flexDirection: "column",
          gap: 12,
          maxHeight: "80vh",
        }}
      >
        <h2 style={{ color: "#1e3a8a", marginBottom: "20px", textAlign: "center", fontWeight: "600" }}>
          Search the Commerce Control List!
        </h2>

        <div style={{ flex: "0 0 auto" }}>
          <QueryForm onSend={sendQuery} />
        </div>

        <div style={{ minHeight: 8 }} />

        {loading && <div style={{ color: "#0f172a" }}>Loading…</div>}
        {error && <div style={{ color: "#b91c1c" }}>Error: {error}</div>}

        <div style={{ flex: "1 1 auto", overflowY: "auto", marginTop: 6 }}>
          <ResponseDisplay data={response} />
        </div>
      </div>
    </div>
  );
}

export default App;

