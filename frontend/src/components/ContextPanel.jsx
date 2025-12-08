export default function ContextPanel({ excerpts }) {
  if (!excerpts || excerpts.length === 0) {
    return (
      <div style={{ padding: 12, color: '#cbd5e1' }}>
        No context available.
      </div>
    );
  }

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <div style={{ overflowY: 'auto', padding: 12, background: '#071028', borderRadius: 8, border: '1px solid #0f1724' }}>
        <div style={{ fontWeight: 600, color: '#4EE7FF', marginBottom: 8 }}>Retrieved Context</div>

        <div style={{ marginTop: 8, background: "#060516", padding: 12, borderRadius: 8, border: "1px solid #111827", color: "#e6eef8", width: "100%", boxSizing: 'border-box', overflowWrap: 'anywhere' }}>

            <ul style={{ margin: 0, paddingLeft: 16 }}>
            {excerpts.map((ex, i) => (
                <li key={i} style={{ marginBottom: 10, color: '#e6eef8', whiteSpace: 'pre-wrap' }}>
                {ex}
                </li>
            ))}
            </ul>
        </div>
      </div>
    </div>
  );
}
