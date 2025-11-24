import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please upload a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await res.text();
    setResponse(data);
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
          padding: "40px",
          width: "450px",
          borderRadius: "12px",
          boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
          border: "1px solid #e6e9f0",
        }}
      >
        <h2
          style={{
            color: "#1e3a8a",
            marginBottom: "20px",
            textAlign: "center",
            fontWeight: "600",
          }}
        >
          Upload Excel File
        </h2>

        <input
          type="file"
          accept=".xlsx,.xls"
          onChange={handleFileChange}
          style={{
            width: "100%",
            padding: "12px",
            borderRadius: "8px",
            border: "1px solid #cbd5e1",
            background: "#f8fafc",
          }}
        />

        <button
          onClick={handleUpload}
          style={{
            marginTop: "20px",
            width: "100%",
            padding: "14px",
            borderRadius: "8px",
            border: "none",
            background: "#2563eb",
            color: "white",
            fontSize: "16px",
            fontWeight: "600",
            cursor: "pointer",
          }}
        >
          Send Query
        </button>

        <div
          style={{
            marginTop: "30px",
            background: "#f8fafc",
            border: "1px solid #dbe3f1",
            padding: "20px",
            borderRadius: "8px",
            minHeight: "100px",
          }}
        >
          <strong style={{ color: "#1e3a8a" }}>Response:</strong>
          <p style={{ marginTop: "10px", whiteSpace: "pre-wrap" }}>
            {response}
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
