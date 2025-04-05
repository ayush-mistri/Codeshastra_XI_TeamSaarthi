import React, { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";

const Navbar = () => {
  const location = useLocation();
  const currentPath = location.pathname;
  const [isOpen, setIsOpen] = useState(false);

  // Close drawer on route change
  useEffect(() => {
    setIsOpen(false);
  }, [location.pathname]);

  const linkClasses = (path) =>
    `transition ${
      currentPath === path
        ? "text-blue-600 underline underline-offset-4"
        : "text-gray-600 hover:text-blue-500 hover:underline underline-offset-4"
    }`;

  return (
    <>
      <nav className="bg-white/60 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-blue-600">
            <Link to="/">Team Saarthi</Link>
          </h1>

          {/* Desktop Links */}
          <ul className="hidden md:flex gap-6 font-medium items-center">
            <li>
              <Link to="/" className={linkClasses("/")}>
                Home
              </Link>
            </li>
            <li>
              <Link to="/about" className={linkClasses("/about")}>
                About
              </Link>
            </li>
            <li>
              <Link to="/contact" className={linkClasses("/contact")}>
                Contact
              </Link>
            </li>
            <li>
              <Link
                to="/login"
                className={`px-4 py-2 border rounded-md transition ${
                  currentPath === "/login"
                    ? "bg-blue-500 text-white border-blue-500"
                    : "text-blue-500 border-blue-500 hover:bg-blue-500 hover:text-white"
                }`}
              >
                Login
              </Link>
            </li>
            <li>
              <Link
                to="/signup"
                className={`px-4 py-2 rounded-md transition ${
                  currentPath === "/signup"
                    ? "bg-blue-600 text-white"
                    : "bg-blue-500 text-white hover:bg-blue-600"
                }`}
              >
                Signup
              </Link>
            </li>
          </ul>

          {/* Mobile Hamburger */}
          <button
            onClick={() => setIsOpen(true)}
            className="md:hidden text-blue-600 text-xl p-2"
          >
            ☰
          </button>
        </div>
      </nav>

      {/* Mobile Drawer */}
      <div
        className={`fixed top-0 left-0 w-full h-[50vh] bg-white shadow-lg z-50 transition-transform duration-300 ease-in-out ${
          isOpen ? "translate-y-0" : "-translate-y-full"
        } md:hidden`}
      >
        <div className="flex justify-between items-center p-4 border-b">
          <h2 className="text-xl font-bold text-blue-600">Menu</h2>
          <button
            onClick={() => setIsOpen(false)}
            className="text-2xl text-blue-600"
          >
            ✕
          </button>
        </div>
        <ul className="flex flex-col items-center p-2 gap-3 text-gray-700 font-medium">
          <li className="w-full text-center py-2">
            <Link to="/" className={linkClasses("/")}>
              Home
            </Link>
          </li>
          <li className="w-full text-center py-2">
            <Link to="/about" className={linkClasses("/about")}>
              About
            </Link>
          </li>
          <li className="w-full text-center py-2">
            <Link to="/contact" className={linkClasses("/contact")}>
              Contact
            </Link>
          </li>
          <li className="w-full text-center py-2">
            <Link
              to="/login"
              className={`px-4 py-2 border rounded-md transition ${
                currentPath === "/login"
                  ? "bg-blue-500 text-white border-blue-500"
                  : "text-blue-500 border-blue-500 hover:bg-blue-500 hover:text-white"
              }`}
            >
              Login
            </Link>
          </li>
          <li className="w-full text-center py-2">
            <Link
              to="/signup"
              className={`px-4 py-2 rounded-md transition ${
                currentPath === "/signup"
                  ? "bg-blue-600 text-white"
                  : "bg-blue-500 text-white hover:bg-blue-600"
              }`}
            >
              Signup
            </Link>
          </li>
        </ul>
      </div>

      {/* Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-30 z-40 md:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  );
};

export default Navbar;
