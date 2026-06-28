
"use client";
import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [code, setCode] = useState("");
  const [token, setToken] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeCode = async () => {
    if (!code || !token) {
      setError("Please enter code and token");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const response = await axios.post("http://127.0.0.1:8080/api/review/analyze", {
        code,
        filename: "code.py",
        token,
      });
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Something went wrong");
    }
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-2 text-blue-400">
          AI Code Review Assistant
        </h1>
        <p className="text-center text-gray-400 mb-8">
          Multi-agent AI system for code quality, security and bug detection
        </p>

        <div className="bg-gray-800 rounded-lg p-6 mb-6">
          <label className="block text-sm font-medium mb-2">JWT Token</label>
          <input
            type="text"
            value={token}
            onChange={(e) => setToken(e.target.value)}
            placeholder="Paste your token here after login"
            className="w-full bg-gray-700 rounded p-3 text-sm mb-4"
          />

          <label className="block text-sm font-medium mb-2">Python Code</label>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="Paste your Python code here..."
            rows={10}
            className="w-full bg-gray-700 rounded p-3 text-sm font-mono mb-4"
          />

          {error && <p className="text-red-400 mb-4">{error}</p>}

          <button
            onClick={analyzeCode}
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 rounded p-3 font-bold text-lg disabled:opacity-50"
          >
            {loading ? "Analyzing... Please wait" : "Analyze Code"}
          </button>
        </div>

        {result && (
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-2xl font-bold mb-4 text-green-400">Review Results</h2>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div className="bg-gray-700 rounded p-4 text-center">
                <p className="text-gray-400 text-sm">Quality</p>
                <p className="text-3xl font-bold text-blue-400">{result.scores.quality}</p>
              </div>
              <div className="bg-gray-700 rounded p-4 text-center">
                <p className="text-gray-400 text-sm">Security</p>
                <p className="text-3xl font-bold text-green-400">{result.scores.security}</p>
              </div>
              <div className="bg-gray-700 rounded p-4 text-center">
                <p className="text-gray-400 text-sm">Readability</p>
                <p className="text-3xl font-bold text-yellow-400">{result.scores.readability}</p>
              </div>
              <div className="bg-gray-700 rounded p-4 text-center">
                <p className="text-gray-400 text-sm">Overall</p>
                <p className="text-3xl font-bold text-purple-400">{result.scores.overall}</p>
              </div>
            </div>

            <div className="mb-4">
              <span className={`px-3 py-1 rounded text-sm font-bold ${
                result.severity === "Critical" ? "bg-red-600" :
                result.severity === "Medium" ? "bg-yellow-600" : "bg-green-600"
              }`}>
                Severity: {result.severity}
              </span>
            </div>

            <div className="mb-6">
              <h3 className="text-lg font-bold mb-2 text-red-400">Issues Found</h3>
              <ul className="space-y-2">
                {result.issues.map((issue: string, i: number) => (
                  <li key={i} className="bg-gray-700 rounded p-3 text-sm">
                    ⚠️ {issue}
                  </li>
                ))}
              </ul>
            </div>

            <div className="mb-6">
              <h3 className="text-lg font-bold mb-2 text-blue-400">Suggestions</h3>
              <ul className="space-y-2">
                {result.suggestions.map((s: string, i: number) => (
                  <li key={i} className="bg-gray-700 rounded p-3 text-sm">
                    💡 {s}
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="text-lg font-bold mb-2 text-yellow-400">Learning Tips</h3>
              <ul className="space-y-2">
                {result.learning_tips.map((tip: string, i: number) => (
                  <li key={i} className="bg-gray-700 rounded p-3 text-sm">
                    📚 {tip}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}