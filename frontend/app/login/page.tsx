"use client";
import { useState } from "react";
import axios from "axios";

export default function LoginPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!username || !password) {
      setError("Please fill all fields");
      return;
    }
    setLoading(true);
    setError("");
    try {
      if (isLogin) {
        const response = await axios.post("http://127.0.0.1:8080/api/auth/login", {
          username,
          password,
        });
        localStorage.setItem("token", response.data.access_token);
        localStorage.setItem("username", username);
        window.location.href = "/";
      } else {
        if (!email) {
          setError("Please enter email");
          setLoading(false);
          return;
        }
        await axios.post("http://127.0.0.1:8080/api/auth/register", {
          username,
          email,
          password,
        });
        setIsLogin(true);
        setError("Registered successfully! Please login.");
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || "Something went wrong");
    }
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
      <div className="bg-gray-800 rounded-lg p-8 w-full max-w-md">
        <h1 className="text-3xl font-bold text-center mb-2 text-blue-400">
          AI Code Review
        </h1>
        <p className="text-center text-gray-400 mb-8">
          {isLogin ? "Login to your account" : "Create new account"}
        </p>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              className="w-full bg-gray-700 rounded p-3 text-sm"
            />
          </div>

          {!isLogin && (
            <div>
              <label className="block text-sm font-medium mb-2">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter email"
                className="w-full bg-gray-700 rounded p-3 text-sm"
              />
            </div>
          )}

          <div>
            <label className="block text-sm font-medium mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              className="w-full bg-gray-700 rounded p-3 text-sm"
            />
          </div>

          {error && (
            <p className={`text-sm ${error.includes("successfully") ? "text-green-400" : "text-red-400"}`}>
              {error}
            </p>
          )}

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 rounded p-3 font-bold