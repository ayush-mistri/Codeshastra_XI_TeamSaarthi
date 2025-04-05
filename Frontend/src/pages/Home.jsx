import React, { useEffect } from "react";
import AOS from "aos";
import "aos/dist/aos.css";

const GradientOverlay = ({ position }) => {
  const isLeft = position === "left";
  return (
    <div className={`absolute ${isLeft ? "left-0" : "right-0"} top-0 opacity-20`}>
      <svg width="600" height="600" viewBox="0 0 600 600" fill="none">
        <circle cx="300" cy="300" r="300" fill="url(#radial)" />
        <defs>
          <radialGradient
            id="radial"
            cx="0"
            cy="0"
            r="1"
            gradientUnits="userSpaceOnUse"
            gradientTransform="translate(300 300) rotate(90) scale(300)"
          >
            <stop stopColor="#3B82F6" />
            <stop offset="1" stopColor="#3B82F6" stopOpacity="0" />
          </radialGradient>
        </defs>
      </svg>
    </div>
  );
};

const Home = () => {
  useEffect(() => {
    AOS.init({ duration: 1000 });
  }, []);

  return (
    <div className="w-full text-gray-900 relative overflow-hidden">
      {/* Section 0: Hero */}
      <section className="relative min-h-[90vh] flex flex-col justify-center items-center text-center px-4 bg-white">
        <GradientOverlay position="right" />
        <h2 className="text-4xl md:text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-blue-400 mb-6">
          Welcome to Team Saarthi
        </h2>
        <p className="text-lg text-gray-700 max-w-2xl mb-8">
          Empowering road safety and awareness with intelligent technology and real-time support.
        </p>
        <button className="px-8 py-3 text-lg bg-gradient-to-r from-blue-600 to-blue-400 text-white rounded-xl shadow-xl hover:from-blue-700 hover:to-blue-500 transition-all duration-300">
          Get Started
        </button>
      </section>

      {/* Section 1: Mission */}
      <section className="relative py-20 px-6 bg-white text-center" data-aos="fade-up">
        <GradientOverlay position="left" />
        <h3 className="text-4xl font-bold text-blue-600 mb-8">Our Mission</h3>
        <p className="max-w-4xl mx-auto text-gray-700 text-lg">
          Saarthi is dedicated to enhancing road safety through real-time intelligence and smart support systems.
          We blend technology and empathy for a safer tomorrow.
        </p>
      </section>

      {/* Section 2: Features */}
      <section className="relative py-20 px-6 bg-white text-center" data-aos="fade-up">
        <GradientOverlay position="right" />
        <h3 className="text-4xl font-bold text-blue-600 mb-12">Key Features</h3>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
          {[
            { icon: "🚨", title: "AI Detection", desc: "Detects real-time road hazards using AI." },
            { icon: "📡", title: "Live Alerts", desc: "Receive live traffic and incident notifications." },
            { icon: "📈", title: "Driving Insights", desc: "Get performance stats and driving tips." },
            { icon: "🆘", title: "SOS Help", desc: "Emergency SOS integration for quick support." },
          ].map((f, idx) => (
            <div
              key={idx}
              className="bg-gradient-to-br from-blue-50 via-white to-blue-100 border border-blue-200 rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all"
              data-aos="zoom-in"
            >
              <div className="text-4xl mb-3">{f.icon}</div>
              <h4 className="text-xl font-semibold text-blue-700 mb-2">{f.title}</h4>
              <p className="text-gray-600">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Section 3: How It Works */}
      <section className="relative py-20 px-6 bg-white text-center" data-aos="fade-up">
        <GradientOverlay position="left" />
        <h3 className="text-4xl font-bold text-blue-600 mb-10">How It Works</h3>
        <div className="max-w-4xl mx-auto space-y-8 text-gray-700 text-left">
          {[
            "📍 Step 1: Install the Saarthi App on your mobile device.",
            "🧠 Step 2: AI scans and monitors surroundings in real-time.",
            "📢 Step 3: Get alerts, updates, and insights instantly.",
            "🚀 Step 4: Drive smarter, safer, and stay informed.",
          ].map((step, i) => (
            <div key={i} className="bg-white border-l-4 border-blue-500 pl-4 py-2">
              <strong>{step.split(":")[0]}:</strong> {step.split(":")[1]}
            </div>
          ))}
        </div>
      </section>

      {/* Section 4: Call to Action */}
      <section className="relative py-20 px-6 bg-white text-center" data-aos="zoom-in">
        <GradientOverlay position="right" />
        <h3 className="text-4xl font-bold text-blue-600 mb-6">Join Team Saarthi</h3>
        <p className="max-w-3xl mx-auto text-gray-700 mb-8">
          Become a part of the movement toward safer roads and smarter driving.
        </p>
        <button className="px-8 py-3 text-lg bg-gradient-to-r from-blue-500 to-indigo-500 text-white rounded-xl shadow-lg hover:from-blue-600 hover:to-indigo-600 transition-all duration-300">
          Become a Saarthi
        </button>
      </section>
    </div>
  );
};

export default Home;
