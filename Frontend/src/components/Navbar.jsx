import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="bg-white/60 backdrop-blur-md shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-blue-600">
          <Link to="/">Team Saarthi</Link>
        </h1>
        <ul className="hidden md:flex gap-6 text-gray-600 font-medium items-center">
          <li>
            <Link to="/" className="hover:text-blue-500 transition">Home</Link>
          </li>
          <li>
            <Link to="/about" className="hover:text-blue-500 transition">About</Link>
          </li>
          <li>
            <Link to="/contact" className="hover:text-blue-500 transition">Contact</Link>
          </li>
          <li>
            <Link
              to="/login"
              className="px-4 py-2 border border-blue-500 text-blue-500 rounded-md hover:bg-blue-500 hover:text-white transition"
            >
              Login
            </Link>
          </li>
          <li>
            <Link
              to="/signup"
              className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition"
            >
              Signup
            </Link>
          </li>

        </ul>
        <button className="md:hidden text-blue-600 text-2xl">☰</button>
      </div>
    </nav>

  );
};

export default Navbar;
