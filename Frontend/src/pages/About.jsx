import React, { useEffect } from "react";
import { FaUserAlt } from "react-icons/fa";
import AOS from "aos";
import "aos/dist/aos.css";

const About = () => {
  useEffect(() => {
    AOS.init({ duration: 1000 });
  }, []);

  return (
    <section className="bg-gradient-to-br from-blue-50 via-white to-blue-50 px-6 pt-24 pb-20">
      <div className="max-w-4xl mx-auto text-center mb-20">
        <h2 className="text-4xl font-bold text-blue-600 mb-4">About Team Auralytics</h2>
        <p className="text-gray-700 text-lg leading-relaxed">
          Team Auralytics is committed to enhancing road safety and awareness through intelligent technology.
          Our mission is to provide real-time support, guidance, and resources to road users, helping reduce accidents and save lives.
        </p>
      </div>

      {/* Team Members Section */}
      <div className="text-center" data-aos="fade-up">
        <h3 className="text-5xl font-bold text-blue-600 mb-16">Team Members</h3>

        <div className="grid sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-7xl mx-auto px-6">
          {[
            { name: "Sujal Vekariya", role: "Full Stack Developer" },
            { name: "Ayush Mistri", role: "Full Stack Developer" },
            { name: "Krish Mavani", role: "ML Engineer" },
            { name: "Apurv Chudasama", role: "ML Engineer" },
          ].map((member, idx) => (
            <div
              key={idx}
              className="bg-gradient-to-br from-blue-100 via-white to-blue-200 border border-blue-200 rounded-2xl w-64 h-70 px-6 py-8 shadow-lg hover:shadow-xl transition-all flex flex-col items-center justify-start"
              data-aos="zoom-in"
            >
              <div className="text-7xl text-blue-700 mb-4">
                <FaUserAlt />
              </div>
              <h4 className="text-xl font-semibold text-blue-700 mb-1">{member.name}</h4>
              <p className="text-gray-700 text-lg">{member.role}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default About;
