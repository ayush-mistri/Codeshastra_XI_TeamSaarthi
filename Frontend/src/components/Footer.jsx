import { Link } from "react-router-dom";
import { FaChartLine } from "react-icons/fa";

export default function Footer() {
  return (
    <footer className="border-t border-gray-200 py-12">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-8">
          <div>
            <h3 className="font-bold mb-4">Product</h3>
            <ul className="space-y-2">
              <li>
                <Link to="#" className="text-gray-500 hover:text-blue-600">
                  Features
                </Link>
              </li>
              <li>
                <Link to="#" className="text-gray-500 hover:text-blue-600">
                  Pricing
                </Link>
              </li>
              <li>
                <Link to="#" className="text-gray-500 hover:text-blue-600">
                  Testimonials
                </Link>
              </li>
              <li>
                <Link to="#" className="text-gray-500 hover:text-blue-600">
                  FAQ
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <h3 className="font-bold mb-4">Company</h3>
            <ul className="space-y-2">
              <li>
                <Link to="#" className="text-gray-500 hover:text-blue-600">
                  About
                </Link>
              </li>
              <li>
                <Link to="#" className="text-gray-500 hover:text-blue-600">
                  Blog
                </Link>
              </li>
              <li>
                <Link to="#" className="text-gray-500 hover:text-blue-600">
                  Careers
                </Link>
              </li>
              <li>
                <Link to="#" className="text-gray-500 hover:text-blue-600">
                  Contact
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <h3 className="font-bold mb-4">Resources</h3>
            <ul className="space-y-2">
              <li>
                <Link to="#" className="text-gray-500 hover:text-blue-600">
                  Documentation
                </Link>
              </li>
              <li>
                <Link to="#" className="text-gray-500 hover:text-blue-600">
                  Guides
                </Link>
              </li>
              <li>
                <Link to="#" className="text-gray-500 hover:text-blue-600">
                  API Reference
                </Link>
              </li>
              <li>
                <Link to="#" className="text-gray-500 hover:text-blue-600">
                  Support
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <h3 className="font-bold mb-4">Legal</h3>
            <ul className="space-y-2">
              <li>
                <Link to="#" className="text-gray-500 hover:text-blue-600">
                  Privacy
                </Link>
              </li>
              <li>
                <Link to="#" className="text-gray-500 hover:text-blue-600">
                  Terms
                </Link>
              </li>
              <li>
                <Link to="#" className="text-gray-500 hover:text-blue-600">
                  Security
                </Link>
              </li>
              <li>
                <Link to="#" className="text-gray-500 hover:text-blue-600">
                  Cookies
                </Link>
              </li>
            </ul>
          </div>
        </div>
        
      </div>
    </footer>
  );
}
