import React, { useState } from "react";
import emailjs from "@emailjs/browser";
import { Mail, User, MessageCircle } from "lucide-react";

const Contact = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [isSent, setIsSent] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsSending(true);

    emailjs
      .send(
        "service_zd8j699", // Your EmailJS service ID
        "template_h47lvfd", // Your EmailJS template ID
        {
          from_name: name,
          email,
          message,
        },
        "qKgzsdh_j7Y3WDoxz" // Your EmailJS public key
      )
      .then(() => {
        setIsSending(false);
        setIsSent(true);
        setTimeout(() => window.location.reload(), 3000);
      })
      .catch((error) => {
        console.error("Email send error:", error);
        setIsSending(false);
      });
  };

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
          <form className="space-y-6" onSubmit={handleSubmit}>
            <div className="relative">
              <User className="absolute left-4 top-3.5 text-blue-400" />
              <input
                type="text"
                placeholder="Your Name"
                className="w-full pl-12 pr-4 py-3 border border-blue-200 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
            <div className="relative">
              <Mail className="absolute left-4 top-3.5 text-blue-400" />
              <input
                type="email"
                placeholder="Your Email"
                className="w-full pl-12 pr-4 py-3 border border-blue-200 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="relative">
              <MessageCircle className="absolute left-4 top-4 text-blue-400" />
              <textarea
                rows="4"
                placeholder="Your Message"
                className="w-full pl-12 pr-4 py-3 border border-blue-200 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 transition resize-none"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                required
              ></textarea>
            </div>
            <button
              type="submit"
              disabled={isSending || isSent}
              className={`w-full py-3 text-white font-semibold rounded-xl shadow-md transition transform hover:scale-105 ${
                isSent
                  ? "bg-green-600 hover:bg-green-700"
                  : "bg-blue-600 hover:bg-blue-700"
              }`}
            >
              {isSending ? "Sending..." : isSent ? "Sent!" : "Send Message"}
            </button>
          </form>
        </div>
      </div>
    </section>
  );
};

export default Contact;
