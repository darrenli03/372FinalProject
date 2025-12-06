export default function ResponseDisplay({ data }) {
  if (!data) {
    return (
      <div style={{ marginTop: 20, color: "#000" }}>
        No response yet.
      </div>
    );
  }

  return (
    <div style={{ marginTop: 20, color: "#000", display: "flex", flexDirection: "column", gap: 8 }}>
      <div style={{ marginBottom: 10 }}>
        <strong style={{ color: "#1e3a8a" }}>Answer:</strong>
        <div style={{ marginTop: 8, whiteSpace: "pre-wrap", background: "#f8fafc", padding: 12, borderRadius: 8, border: "1px solid #dbe3f1", color: "#000", width: "100%" }}>
          {data.response || data.answer || "(no answer)"}
        </div>
      </div>

      {data.excerpts && data.excerpts.length > 0 && (
        <div style={{ marginTop: 14 }}>
          <strong style={{ color: "#1e3a8a" }}>Excerpts:</strong>
          <ul style={{ marginTop: 8, paddingLeft: 18 }}>
            {data.excerpts.map((ex, i) => (
              <li key={i} style={{ marginBottom: 6 }}>
                <div style={{ whiteSpace: "pre-wrap", color: "#000" }}>{ex}</div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
