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

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 8000);

    try {
      const response = await fetch("http://127.0.0.1:8000/compare", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        signal: controller.signal,
        body: JSON.stringify({
          prompt_version: promptVersion, // context hint
          question: question,
        }),
      });

      if (!response.ok) {
        throw new Error(`Backend error: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error("Request failed:", err);
      if (err.name === "AbortError") {
        setError("Request timed out. Backend may be down.");
      } else {
        setError("Failed to connect to backend.");
      }
    } finally {
      clearTimeout(timeoutId);
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Enterprise LLM Governance Console</h1>

      <label>Prompt Version (Reference)</label>
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
          <p style={{ color: "#555", fontSize: "14px" }}>
            Evaluated at: {new Date(result.timestamp).toLocaleString()}
          </p>

          <h2>Prompt Version Comparison</h2>

          {Object.entries(result.comparisons).map(([version, res]) => (
            <div key={version} style={{ marginBottom: "16px" }}>
              <strong>{version.toUpperCase()}</strong>
              <br />
              Risk: {res.risk}
              <br />
              Approved: {res.approved ? "Yes" : "No"}

              <ul>
                {res.reasons.map((r, i) => (
                  <li key={i}>
                    <div>
                      <b>{r.category}</b> ({r.severity}) — {r.message}
                    </div>
                    <small style={{ color: "#666" }}>Source: {r.evaluator}</small>
                  </li>
                ))}
              </ul>
            </div>
          ))}

          <h3>
            ✅ Recommended Prompt Version:{" "}
            {result.recommended_version.toUpperCase()}
          </h3>
        </div>
      )}
    </div>
  );
}

export default App;
