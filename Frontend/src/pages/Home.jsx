import React, { useEffect } from "react";
import AOS from "aos";
import "aos/dist/aos.css";

// Reusable blob shape component
const BlueShape = ({ top, left, rotate, scale, color }) => (
  <div
    className="absolute opacity-30 pointer-events-none"
    style={{
      top,
      left,
      transform: `rotate(${rotate}deg) scale(${scale})`,
      zIndex: 0,
    }}
  >
    <svg width="200" height="200" viewBox="0 0 200 200" fill="none">
      <path
        fill={color}
        d="M39.5,-56.6C52.6,-48.7,66.7,-39.3,69.6,-26.5C72.5,-13.7,64.1,2.5,57.8,18.7C51.5,34.8,47.2,50.9,36.8,59.2C26.3,67.4,9.7,67.9,-3.8,65C-17.3,62.1,-27.6,55.7,-37.7,47.2C-47.9,38.6,-57.9,28.1,-63.4,14.9C-68.9,1.8,-69.9,-13.9,-64.3,-27.6C-58.6,-41.2,-46.2,-52.8,-32.3,-60.5C-18.5,-68.3,-3.2,-72.2,10.3,-70.4C23.7,-68.6,35.4,-61.1,39.5,-56.6Z"
        transform="translate(100 100)"
      />
    </svg>
  </div>
);

const Home = () => {
  useEffect(() => {
    AOS.init({ duration: 1000 });
  }, []);

  return (
    <div className="w-full relative overflow-hidden text-gray-900 bg-white">
      {/* Decorative Shapes - Large & Small, Light & Dark */}
      {/* Light Blue Large */}
      <BlueShape top="5%" left="10%" rotate={40} scale={2.5} color="#3B82F6" />
      <BlueShape top="25%" left="80%" rotate={-25} scale={2.1} color="#3B82F6" />
      <BlueShape top="55%" left="5%" rotate={30} scale={2.6} color="#3B82F6" />
      <BlueShape top="85%" left="60%" rotate={-10} scale={2.2} color="#3B82F6" />


      {/* Dark Blue Small */}
      <BlueShape top="10%" left="60%" rotate={15} scale={0.6} color="#1E3A8A" />
      <BlueShape top="35%" left="40%" rotate={-35} scale={0.8} color="#1E3A8A" />
      <BlueShape top="65%" left="75%" rotate={45} scale={0.5} color="#1E3A8A" />
      <BlueShape top="90%" left="20%" rotate={-20} scale={0.7} color="#1E3A8A" />

      {/* Section 0: Hero */}
      <section className="relative z-10 min-h-[90vh] flex flex-col justify-center items-center text-center px-4">
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
      <section className="relative z-10 py-20 px-6 text-center" data-aos="fade-up">
        <h3 className="text-4xl font-bold text-blue-600 mb-8">Our Mission</h3>
        <p className="max-w-4xl mx-auto text-gray-700 text-lg">
          Saarthi is dedicated to enhancing road safety through real-time intelligence and smart support systems.
          We blend technology and empathy for a safer tomorrow.
        </p>
      </section>

      {/* Section 2: Features */}
      <section className="relative z-10 py-20 px-6 text-center" data-aos="fade-up">
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
      <section className="relative z-10 py-20 px-6 text-center" data-aos="fade-up">
        <h3 className="text-4xl font-bold text-blue-600 mb-10">How It Works</h3>
        <div className="max-w-4xl mx-auto space-y-8 text-gray-700 text-left">
          {[
            "📍 Step 1: Install the Saarthi App on your mobile device.",
            "🧠 Step 2: AI scans and monitors surroundings in real-time.",
            "📢 Step 3: Get alerts, updates, and insights instantly.",
            "🚀 Step 4: Drive smarter, safer, and stay informed.",
          ].map((step, i) => (
            <div key={i} className="bg-white border-l-4 border-blue-500 pl-4 py-2 rounded">
              <strong>{step.split(":")[0]}:</strong> {step.split(":")[1]}
            </div>
          ))}
        </div>
      </section>

      {/* Section 4: Call to Action */}
      <section className="relative z-10 py-20 px-6 text-center" data-aos="zoom-in">
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
