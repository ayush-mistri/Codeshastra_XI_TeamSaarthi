import React from "react";
import { Link, useNavigate } from "react-router-dom";

const Login = () => {
    const navigate = useNavigate();

    const handleGoogleSignIn = () => {
        // Add your Google Sign-In logic here (Firebase/Auth0/etc.)
        console.log("Google Sign-In clicked");
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-white to-blue-50 p-4">
            {/* Back Button */}
            <button
                onClick={() => navigate(-1)}
                className="absolute top-4 left-4 bg-blue-600 hover:bg-blue-700 text-white rounded-full w-10 h-10 flex items-center justify-center shadow-md transition z-10"
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

            {/* Main Card */}
            <div className="w-full max-w-5xl bg-white rounded-3xl shadow-2xl overflow-hidden border border-gray-200 grid grid-cols-1 md:grid-cols-2">
                {/* Left Side */}
                <div className="hidden md:flex flex-col justify-center items-center bg-gradient-to-br from-blue-800 via-blue-600 to-blue-400 text-white p-12">
                    <h2 className="text-4xl font-bold mb-4">Welcome Back 👋</h2>
                    <p className="text-lg text-center max-w-sm">
                        Join the mission to make roads safer. Login and take control of your road safety journey with Team Saarthi.
                    </p>
                </div>

                {/* Right Side with Card */}
                <div className="flex items-center justify-center p-10 bg-gray-50">
                    <div className="w-full bg-white rounded-2xl shadow-md p-8 border border-gray-100">
                        <h2 className="text-3xl font-bold text-blue-600 text-center mb-6">Login to Team Saarthi</h2>
                        <form className="space-y-4">
                            <input
                                type="email"
                                placeholder="Email"
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                            />
                            <input
                                type="password"
                                placeholder="Password"
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                            />
                            <button
                                type="submit"
                                className="w-full py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
                            >
                                Login
                            </button>
                        </form>

                        <div className="text-center mt-4">
                            <p className="text-sm text-gray-500 mb-2">Or sign in with</p>
                            <button
                                onClick={handleGoogleSignIn}
                                className="w-full flex items-center justify-center gap-3 py-2 border rounded-lg text-gray-700 hover:bg-gray-100 transition"
                            >
                                <img src="https://www.svgrepo.com/show/475656/google-color.svg" alt="Google" className="w-5 h-5" />
                                Sign in with Google
                            </button>
                        </div>

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
