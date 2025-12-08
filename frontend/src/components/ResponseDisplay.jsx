import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function ResponseDisplay({ data }) {
  if (!data) {
    return (
      <div style={{ marginTop: 20, color: "#e6eef8" }}>
        No response yet.
      </div>
    );
  }

  const raw = (data.response || data.answer || "(no answer)").toString();

  // Extract 'Final Answer: Yes' or 'Final Answer: No' (or any value after the label)
  const finalMatch = raw.match(/Final Answer:\s*(.+)/i);
  const finalAnswer = finalMatch ? finalMatch[1].trim() : null;

  // Remove the Final Answer line from the body for markdown rendering
  // let body = raw;
  // if (finalMatch) {
  //   body = raw.replace(finalMatch[0], "").trim();
  // }

  // render the original response using react-markdown 

  return (
    <div style={{ marginTop: 20, color: "#000", display: "flex", flexDirection: "column", gap: 8, minWidth: 0}}>
      {finalAnswer && (
        <div style={{ marginBottom: 6 }}>
          <h2 style={{ fontWeight: 700, color: finalAnswer.toLowerCase().includes('yes') ? '#12bd12ff' : '#c71b1bff' }}>
            Restricted Under the CCL? {finalAnswer}
          </h2>
        </div>
      )}

      <div style={{ marginBottom: 10 }}>
        <strong style={{ color: "#4EE7FF" }}>LLM Response:</strong>
        <div style={{ marginTop: 8, background: "#060516", padding: 12, borderRadius: 8, border: "1px solid #111827", color: "#e6eef8", width: "100%", boxSizing: 'border-box', overflowWrap: 'anywhere' }}>
          <div style={{ color: '#e6eef8', wordBreak: 'break-word' }}>
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{raw}</ReactMarkdown>
          </div>
        </div>
      </div>
    </div>
  );
}
