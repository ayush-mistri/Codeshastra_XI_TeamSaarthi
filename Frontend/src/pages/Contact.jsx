import React from "react";
import { Mail, User, MessageCircle } from "lucide-react";

const Contact = () => {
  return (
    <section className="min-h-screen bg-gradient-to-br from-white via-blue-50 to-white flex items-center justify-center px-4 sm:px-6 py-12">
      <div className="bg-white/90 backdrop-blur-md rounded-3xl shadow-2xl max-w-5xl w-full grid md:grid-cols-2 overflow-hidden border border-blue-100">
        {/* Left Image Section */}
        <div className="hidden md:block">
          <img
            src="https://cdn3d.iconscout.com/3d/free/thumb/free-contact-us-3d-illustration-download-in-png-blend-fbx-gltf-file-formats--phone-telephone-communication-empty-state-pack-seo-web-illustrations-2969399.png?f=webp"
            alt="Contact illustration"
            className="h-full w-full object-cover"
          />
        </div>

        {/* Right Form Section */}
        <div className="p-8 sm:p-12">
          <h2 className="text-4xl font-extrabold text-blue-600 text-center mb-8">
            Get in Touch
          </h2>
          <form className="space-y-6">
            <div className="relative">
              <User className="absolute left-4 top-3.5 text-blue-400" />
              <input
                type="text"
                placeholder="Your Name"
                className="w-full pl-12 pr-4 py-3 border border-blue-200 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
              />
            </div>
            <div className="relative">
              <Mail className="absolute left-4 top-3.5 text-blue-400" />
              <input
                type="email"
                placeholder="Your Email"
                className="w-full pl-12 pr-4 py-3 border border-blue-200 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
              />
            </div>
            <div className="relative">
              <MessageCircle className="absolute left-4 top-4 text-blue-400" />
              <textarea
                rows="4"
                placeholder="Your Message"
                className="w-full pl-12 pr-4 py-3 border border-blue-200 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 transition resize-none"
              ></textarea>
            </div>
            <button
              type="submit"
              className="w-full py-3 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 shadow-md transition transform hover:scale-105"
            >
              Send Message
            </button>
          </form>
        </div>
      </div>
    </section>
  );
};

export default Contact;
