import { useState } from "react";
import "./index.css";

function App() {
  const [promptVersion, setPromptVersion] = useState("v1");
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleEvaluate = async () => {
    setError(null);
    setResult(null);

    if (!question.trim()) {
      alert("Please enter a business question");
      return;
    }

    setLoading(true);
    console.log("Sending request to backend...");

    try {
      const response = await fetch("http://localhost:8000/evaluate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          prompt_version: promptVersion,
          question: question
        })
      });

      console.log("HTTP status:", response.status);

      if (!response.ok) {
        throw new Error(`Backend error: ${response.status}`);
      }

      const data = await response.json();
      console.log("Backend response:", data);

      setResult(data);
    } catch (err) {
      console.error("Fetch error:", err);
      setError("Failed to connect to backend. Check console.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Enterprise LLM Governance Console</h1>

      <label>Prompt Version</label>
      <select
        value={promptVersion}
        onChange={(e) => setPromptVersion(e.target.value)}
      >
        <option value="v1">v1 – Creative</option>
        <option value="v2">v2 – Conservative</option>
        <option value="v3">v3 – Strict</option>
      </select>

      <label>Business Question</label>
      <textarea
        rows="5"
        placeholder="Enter compliance or business query..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={handleEvaluate} disabled={loading}>
        {loading ? "Evaluating..." : "Evaluate"}
      </button>

      {error && (
        <div className="result" style={{ background: "#ffe6e6" }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="result">
          <h2>Decision</h2>
          <p><strong>Risk Level:</strong> {result.risk_level}</p>
          <p><strong>Approved:</strong> {result.approved ? "Yes" : "No"}</p>

          <ul>
            {result.reasons.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
