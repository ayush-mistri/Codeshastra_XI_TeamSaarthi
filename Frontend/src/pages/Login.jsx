import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { FaEye, FaEyeSlash } from "react-icons/fa";

const Login = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:5000/api/auth/login", formData);
      const { token, user } = res.data;

      localStorage.setItem("token", token);
      localStorage.setItem("user", JSON.stringify(user));

      toast.success("Login Successful!", {
        position: "top-right",
        autoClose: 3000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        style: {
          backgroundColor: "#ffffff",
          color: "#3B82F6",
          fontWeight: "bold",
        },
      });
  
      setTimeout(() => navigate("/Dashboard/Upload"), 1500);
    } catch (err) {
      const msg = err.response?.data?.message || "Login failed";
      setError(msg);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-white to-blue-50 px-4 py-10">
      <ToastContainer />

      <button
        onClick={() => navigate(-1)}
        className="fixed top-4 left-4 border-2 border-blue-600 text-blue-600 hover:bg-blue-100 rounded-full w-10 h-10 flex items-center justify-center shadow-sm transition z-10 md:absolute"
        title="Go back"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth="2"
          stroke="currentColor"
          className="w-5 h-5"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
      </button>

      {/* Card container - adjusted height */}
      <div className="w-full max-w-4xl h-[500px] bg-white rounded-3xl shadow-2xl overflow-hidden border border-gray-200 grid grid-cols-1 md:grid-cols-2">
        {/* Left Panel */}
        <div className="hidden md:flex flex-col justify-center items-center bg-gradient-to-br from-blue-800 via-blue-600 to-blue-400 text-white p-8 md:p-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4 text-center">Welcome Back 👋</h2>
          <p className="text-base md:text-lg text-center max-w-sm">
            Join the mission to make roads safer. Login and take control of your road safety journey with Auralytics.
          </p>
        </div>

        {/* Right Panel (Form) */}
        <div className="flex items-center justify-center p-6 sm:p-10 bg-gray-50">
          <div className="w-full bg-white rounded-2xl shadow-md p-6 sm:p-8 border border-gray-100">
            <h2 className="text-2xl sm:text-3xl font-bold text-blue-600 text-center mb-6">
              Login to Auralytics
            </h2>

            <form className="space-y-4" onSubmit={handleSubmit}>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="Email"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 text-sm"
                required
              />

              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="Password"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 text-sm pr-10"
                  required
                />
                <span
                  className="absolute top-1/2 right-3 transform -translate-y-1/2 cursor-pointer text-gray-500"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? <FaEyeSlash /> : <FaEye />}
                </span>
              </div>

              <button
                type="submit"
                className="w-full py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition text-sm font-medium"
              >
                Login
              </button>
            </form>

            {error && (
              <p className="text-red-500 text-sm text-center mt-2">{error}</p>
            )}

            <p className="text-center text-sm text-gray-500 mt-6">
              Don’t have an account?{" "}
              <Link to="/signup" className="text-blue-600 hover:underline">
                Sign up
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
