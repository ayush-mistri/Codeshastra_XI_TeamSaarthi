import React from "react";

const About = () => {
  return (
    <section className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50 flex items-center justify-center px-6">
      <div className="max-w-4xl text-center">
        <h2 className="text-4xl font-bold text-blue-600 mb-4">About Team Saarthi</h2>
        <p className="text-gray-700 text-lg leading-relaxed">
          Team Saarthi is committed to enhancing road safety and awareness through intelligent technology.
          Our mission is to provide real-time support, guidance, and resources to road users, helping reduce accidents and save lives.
          <br />
          <br />
          We use modern tools and AI-driven solutions to empower communities with fast, responsive, and safe travel options.
        </p>
      </div>
    </section>
  );
};

export default About;
