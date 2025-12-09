import { useState, useEffect } from "react";
import QueryForm from "./components/QueryForm";
import ResponseDisplay from "./components/ResponseDisplay";
import ContextPanel from "./components/ContextPanel";

function App() {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isMobile, setIsMobile] = useState(typeof window !== 'undefined' ? window.innerWidth <= 768 : false);

  useEffect(() => {
    const handleResize = () => setIsMobile(window.innerWidth <= 768);
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

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
        minHeight: "100dvh",
        width: "100%",
        boxSizing: 'border-box',
        background: "#060516",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "20px",
      }}
    >
      <div style={{ width: "100%", maxWidth: 1100 }}>
        <h1 style={{ color: "#e6eef8", marginBottom: "20px", textAlign: "center", fontWeight: "600" }}>
          Search the Commerce Control List!
        </h1>

        <div style={{ display: 'flex', gap: 16, flexDirection: isMobile ? 'column' : 'row' }}>
          {/* Left column: query + response */}
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ background: "#071129", padding: "18px", borderRadius: "12px", border: "1px solid #0f1724", boxShadow: "0 6px 18px rgba(2,6,23,0.6)", display: 'flex', flexDirection: 'column', gap: 12, maxHeight: isMobile ? '50vh' : '70vh', height: isMobile ? 'auto' : '70vh', boxSizing: 'border-box', overflow: 'hidden' }}>
              <div style={{ flex: '0 0 auto', width: '100%', display: 'flex', justifyContent: isMobile ? 'center' : 'flex-start' }}>
                <div style={{ width: '100%', maxWidth: isMobile ? 720 : '100%' }}>
                  <QueryForm onSend={sendQuery} />
                </div>
              </div>

              {loading && <div style={{ color: "#e6eef8" }}>Loading…</div>}
              {error && <div style={{ color: "#fca5a5" }}>Error: {error}</div>}

              <div style={{ flex: '1 1 auto', overflowY: 'auto', marginTop: 6, paddingRight: 4 }}>
                <ResponseDisplay data={response} />
              </div>
            </div>
          </div>

          {/* Right column: context/excerpts */}
          <div style={{ width: isMobile ? '100%' : 360, marginTop: isMobile ? 16 : 0, boxSizing: 'border-box' }}>
            <div style={{ maxHeight: isMobile ? '40vh' : '70vh', overflowY: isMobile ? 'auto' : 'hidden', overflowX: 'hidden' }}>
              <ContextPanel excerpts={response?.excerpts || []} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

