import { Link } from "react-router-dom";
import { FaArrowLeft } from "react-icons/fa";

export default function NotFound() {
  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-r from-white to-blue-50 px-6 text-center">
      <h1 className="text-[120px] md:text-[160px] font-black text-blue-600 drop-shadow-lg leading-none">
        404
      </h1>
      <h2 className="text-3xl md:text-4xl font-semibold text-gray-800 mt-2">
        Oops! Page Not Found
      </h2>
      <p className="text-gray-600 mt-4 max-w-md">
        The page you're looking for doesn’t exist or has been moved. Let’s get you back home.
      </p>

      <Link to="/" className="mt-8">
        <button className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition duration-300 shadow-md text-sm md:text-base">
          <FaArrowLeft className="w-4 h-4" />
          Back to Home
        </button>
      </Link>
    </div>
  );
}
