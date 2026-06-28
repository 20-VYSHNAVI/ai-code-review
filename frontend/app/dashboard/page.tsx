"use client";
import { useState, useEffect } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";

export default function Dashboard() {
  const router = useRouter();
  const [reviews, setReviews] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [username, setUsername] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    const savedUsername = localStorage.getItem("username");
    if (!token) {
      router.push("/login");
      return;
    }
    setUsername(savedUsername || "");
    fetchHistory(token);
  }, []);

  const fetchHistory = async (token: string) => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8080/api/review/history?token=${token}`
      );
      setReviews(response.data.reviews);
    } catch (err) {
      console.error("Failed to fetch history");
    }
    setLoading(false);
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    router.push("/login");
  };

  return (
    <main className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-blue-400">Dashboard</h1>
            <p className="text-gray-400">Welcome, {username}!</p>
          </div>
          <div className="flex gap-4">
            <button
              onClick={() => router.push("/")}
              className="bg-blue-600 hover:bg-blue-700 rounded p-2 px-4 text-sm"
            >
              New Review
            </button>
            <button
              onClick={logout}
              className="bg-red-600 hover:bg-red-700 rounded p-2 px-4 text-sm"
            >
              Logout
            </button>
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-2xl font-bold mb-4 text-green-400">
            Review History
          </h2>

          {loading ? (
            <p className="text-gray-400">Loading...</p>
          ) : reviews.length === 0 ? (
            <p className="text-gray-400">
              No reviews yet. Go analyze some code!
            </p>
          ) : (
            <div className="space-y-4">
              {reviews.map((review: any) => (
                <div key={review.id} className="bg-gray-700 rounded-lg p-4">
                  <div className="flex justify-between items-center mb-2">
                    <h3 className="font-bold text-blue-400">
                      {review.filename}
                    </h3>
                    <span className={`px-3 py-1 rounded text-xs font-bold ${
                      review.severity === "Critical" ? "bg-red-600" :
                      review.severity === "Medium" ? "bg-yellow-600" :
                      "bg-green-600"
                    }`}>
                      {review.severity}
                    </span>
                  </div>
                  <div className="flex gap-4 text-sm text-gray-400">
                    <span>Overall Score: <span className="text-white font-bold">{review.overall_score}</span></span>
                    <span>Date: <span className="text-white">{new Date(review.created_at).toLocaleDateString()}</span></span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </main>
  );
}