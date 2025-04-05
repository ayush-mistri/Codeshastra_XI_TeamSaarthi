import { Link } from "react-router-dom";
import { FaChartLine } from "react-icons/fa";

export default function Footer() {
  return (
    <footer className="bg-gradient-to-tl from-blue-800 to-blue-300 text-white pt-12 pb-6">
      <div className="max-w-7xl mx-auto px-4">
        {/* Top Footer */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-10 border-b border-blue-100 pb-10">
          <div>
            <h3 className="font-bold text-lg mb-4">Product</h3>
            <ul className="space-y-2 text-sm">
              <li><Link to="#" className="hover:underline">Features</Link></li>
              <li><Link to="#" className="hover:underline">Pricing</Link></li>
              <li><Link to="#" className="hover:underline">Testimonials</Link></li>
              <li><Link to="#" className="hover:underline">FAQ</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="font-bold text-lg mb-4">Company</h3>
            <ul className="space-y-2 text-sm">
              <li><Link to="#" className="hover:underline">About</Link></li>
              <li><Link to="#" className="hover:underline">Blog</Link></li>
              <li><Link to="#" className="hover:underline">Careers</Link></li>
              <li><Link to="#" className="hover:underline">Contact</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="font-bold text-lg mb-4">Resources</h3>
            <ul className="space-y-2 text-sm">
              <li><Link to="#" className="hover:underline">Documentation</Link></li>
              <li><Link to="#" className="hover:underline">Guides</Link></li>
              <li><Link to="#" className="hover:underline">API Reference</Link></li>
              <li><Link to="#" className="hover:underline">Support</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="font-bold text-lg mb-4">Legal</h3>
            <ul className="space-y-2 text-sm">
              <li><Link to="#" className="hover:underline">Privacy</Link></li>
              <li><Link to="#" className="hover:underline">Terms</Link></li>
              <li><Link to="#" className="hover:underline">Security</Link></li>
              <li><Link to="#" className="hover:underline">Cookies</Link></li>
            </ul>
          </div>
        </div>

        {/* Bottom Footer */}
        <div className="flex flex-col md:flex-row justify-between items-center mt-6 text-sm text-blue-100">
          <p>© {new Date().getFullYear()} Team Saarthi. All rights reserved.</p>
          <div className="flex gap-4 mt-2 md:mt-0">
            <Link to="#" className="hover:underline">Privacy Policy</Link>
            <Link to="#" className="hover:underline">Terms of Use</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
