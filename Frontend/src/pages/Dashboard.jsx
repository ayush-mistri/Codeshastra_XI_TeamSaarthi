import { FaBars, FaUser, FaChartLine } from "react-icons/fa";
import { useEffect, useState } from "react";
import React, { useRef } from "react";
import { NavLink, Routes, Route, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import axios from "axios";
import { MdCloudUpload } from "react-icons/md";
import { AiOutlineAreaChart } from "react-icons/ai";
import { BiErrorAlt } from "react-icons/bi";
import { jsPDF } from "jspdf";

// Shared data storage object
const reportData = {
  analytics: null,
  anomaly: null,
};

export default function Dashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      toast.warn("Please login first.", {
        position: "top-right",
        autoClose: 2000,
        hideProgressBar: true,
        style: {
          backgroundColor: "#fef3c7",
          color: "#92400e",
          fontWeight: "bold",
        },
      });
      navigate("/");
    } else {
      const fetchUser = async () => {
        try {
          const { data } = await axios.get("http://localhost:5000/api/user", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          console.log("Fetched user data:", data);
          setUser(data.user);
        } catch (error) {
          console.error("Failed to fetch user:", error);
          if (error.response?.status === 403) {
            toast.error("Authentication failed. Please log in again.", {
              position: "top-right",
              autoClose: 3000,
            });
            localStorage.removeItem("token");
            navigate("/login");
          }
        }
      };

      fetchUser();
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    toast.info("Logged out successfully!", {
      position: "top-right",
      autoClose: 2000,
      hideProgressBar: true,
      style: {
        backgroundColor: "#f3f4f6",
        color: "#111827",
        fontWeight: "bold",
      },
    });
    setTimeout(() => navigate("/login"), 1000);
  };

  useEffect(() => {
    document.body.style.overflow = sidebarOpen ? "hidden" : "auto";
  }, [sidebarOpen]);

  const navLinks = [
    { label: "Upload", path: "/Dashboard/Upload", icon: <MdCloudUpload /> },
    { label: "Analytics", path: "/Dashboard/Analytics", icon: <AiOutlineAreaChart /> },
    { label: "Anomaly", path: "/Dashboard/anomaly", icon: <BiErrorAlt /> },
  ];

  return (
    <div className="flex flex-col h-screen">
      <header className="flex justify-between items-center px-6 py-4 bg-white shadow-md">
        <div className="flex items-center gap-4">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="text-blue-600 lg:hidden"
          >
            <FaBars size={20} />
          </button>
          <h1 className="text-2xl font-bold text-blue-600 hidden lg:block">
            Auralytics
          </h1>
        </div>
        <button
          onClick={handleLogout}
          className="px-4 py-2 rounded-lg bg-red-500 text-white hover:bg-red-600 transition"
          title="Logout"
        >
          Logout
        </button>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {sidebarOpen && (
          <div
            className="fixed inset-0 bg-black bg-opacity-40 z-40 lg:hidden"
            onClick={() => setSidebarOpen(false)}
          />
        )}

        <aside
          className={`fixed top-0 left-0 z-50 h-full w-64 bg-blue-700 text-white p-6 transform transition-transform duration-300 ease-in-out 
            ${sidebarOpen ? "translate-x-0" : "-translate-x-full"} 
            lg:static lg:translate-x-0 lg:flex`}
        >
          <div className="flex flex-col justify-between h-full w-full">
            <nav className="space-y-4">
              {navLinks.map(({ label, path, icon }) => (
                <NavLink
                  key={label}
                  to={path}
                  end={path === "/dashboard"}
                  onClick={() => setSidebarOpen(false)}
                  className={({ isActive }) =>
                    `flex items-center gap-3 px-4 py-2 rounded transition ${
                      isActive ? "bg-blue-600 font-semibold" : "hover:bg-blue-600"
                    }`
                  }
                >
                  <span className="text-2xl">{icon}</span>
                  {label}
                </NavLink>
              ))}
            </nav>

            {user && (
              <div className="mt-6 pt-6 border-t border-blue-600 flex items-center gap-3">
                <div className="bg-white text-blue-700 rounded-full p-2">
                  <FaUser />
                </div>
                <div>
                  <p className="font-semibold">{user.fullName}</p>
                  <p className="text-sm text-gray-300">{user.email}</p>
                </div>
              </div>
            )}
          </div>
        </aside>

        <main className="flex-1 p-6 overflow-y-auto bg-gray-50">
          <Routes>
            <Route path="/upload" element={<DashboardHome />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
            <Route path="/anomaly" element={<AnomalyPage />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area,
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Label,
} from "recharts";

function AnalyticsPage() {
  const [anomalies, setAnomalies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchAnomalies = async () => {
      try {
        const token = localStorage.getItem("token");
        const { data } = await axios.get("http://localhost:5000/api/Anamoly", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const anomaliesData = data.anomalies[0]?.anomalies || [];
        setAnomalies(anomaliesData);
        reportData.analytics = anomaliesData;
        console.log("Analytics data stored:", reportData.analytics);
        setLoading(false);
      } catch (err) {
        setError("Failed to load dashboard data.");
        console.error("Analytics fetch error:", err);
        setLoading(false);
      }
    };

    fetchAnomalies();
  }, []);

  const anomalyTypeMap = {};
  anomalies.forEach((anomaly) => {
    const type = anomaly.type || "Unknown";
    if (!anomalyTypeMap[type]) anomalyTypeMap[type] = 0;
    anomalyTypeMap[type] += 1;
  });

  const anomalyTypeData = Object.entries(anomalyTypeMap).map(([type, count]) => ({
    type,
    count,
  }));

  const severityDistribution = anomalies.reduce((acc, curr) => {
    const bucket = Math.floor(curr.severity / 10) * 10;
    const existing = acc.find((item) => item.severity === bucket);
    if (existing) {
      existing.frequency += 1;
    } else {
      acc.push({ severity: bucket, frequency: 1 });
    }
    return acc;
  }, []);

  const sortedSeverity = severityDistribution.sort((a, b) => a.severity - b.severity);

  const avgSeverityPerType = Object.entries(
    anomalies.reduce((acc, { type, severity }) => {
      const key = type || "Unknown";
      if (!acc[key]) acc[key] = { count: 0, total: 0 };
      acc[key].count += 1;
      acc[key].total += severity;
      return acc;
    }, {})
  ).map(([type, { count, total }]) => ({
    type,
    avgSeverity: parseFloat((total / count).toFixed(1)),
  }));

  if (loading) return <p>Loading dashboard...</p>;
  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <div className="space-y-10 p-4 md:p-8">
      <section className="bg-white p-6 rounded-2xl shadow-md">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">Anomaly Type Distribution</h3>
        <div className="w-full h-80">
          <ResponsiveContainer>
            <BarChart data={anomalyTypeData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#d1d5db" />
              <XAxis dataKey="type" stroke="#374151">
                <Label value="Anomaly Type" offset={-5} position="insideBottom" fill="#374151" />
              </XAxis>
              <YAxis stroke="#374151">
                <Label value="Count" angle={-90} position="insideLeft" fill="#374151" />
              </YAxis>
              <Tooltip />
              <Bar dataKey="count" fill="#10b981" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section className="bg-white p-6 rounded-2xl shadow-md">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">Severity Score Distribution</h3>
        <div className="w-full h-80">
          <ResponsiveContainer>
            <LineChart data={sortedSeverity}>
              <CartesianGrid strokeDasharray="3 3" stroke="#d1d5db" />
              <XAxis dataKey="severity" stroke="#374151">
                <Label value="Severity Score" offset={-5} position="insideBottom" fill="#374151" />
              </XAxis>
              <YAxis stroke="#374151">
                <Label value="Frequency" angle={-90} position="insideLeft" fill="#374151" />
              </YAxis>
              <Tooltip />
              <Line type="monotone" dataKey="frequency" stroke="#f59e0b" strokeWidth={3} dot={{ r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section className="bg-white p-6 rounded-2xl shadow-md">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">
          Anomaly Type Proportion & Average Severity by Type
        </h3>
        <div className="flex justify-between items-center space-x-4">
          <div className="w-1/2 h-80">
            <ResponsiveContainer>
              <PieChart>
                <Pie data={anomalyTypeData} dataKey="count" nameKey="type" cx="50%" cy="50%" outerRadius={100} fill="#8884d8" label>
                  {anomalyTypeData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={["#0ea5e9", "#10b981", "#facc15", "#f43f5e", "#6366f1"][index % 5]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="w-1/2 h-80">
            <ResponsiveContainer>
              <RadarChart data={avgSeverityPerType} cx="50%" cy="50%" outerRadius="80%">
                <PolarGrid />
                <PolarAngleAxis dataKey="type" />
                <PolarRadiusAxis />
                <Radar dataKey="avgSeverity" stroke="#f97316" fill="#fdba74" fillOpacity={0.6} />
                <Tooltip />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>

      <section className="bg-white p-6 rounded-2xl shadow-md">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">Cumulative Severity Trend</h3>
        <div className="w-full h-80">
          <ResponsiveContainer>
            <AreaChart data={anomalies.map((a, i) => ({ ...a, index: i + 1 }))}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="index" stroke="#374151" />
              <YAxis stroke="#374151" />
              <Tooltip />
              <Area type="monotone" dataKey="severity" stroke="#34d399" fill="#a7f3d0" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </section>
    </div>
  );
}

import * as XLSX from "xlsx";

function DashboardHome() {
  const [message, setMessage] = useState("");
  const [recentFiles, setRecentFiles] = useState([]);
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const handleFile = (file) => {
    const fileExtension = file.name.split(".").pop().toLowerCase();

    if (fileExtension === "csv" || fileExtension === "xlsx") {
      const reader = new FileReader();

      reader.onload = (event) => {
        const data = new Uint8Array(event.target.result);
        const workbook = XLSX.read(data, { type: "array" });
        const sheetName = workbook.SheetNames[0];
        const sheet = workbook.Sheets[sheetName];
        const jsonData = XLSX.utils.sheet_to_json(sheet, { header: 1 });

        console.log("Parsed Data:", jsonData);
        setMessage("File uploaded and parsed successfully!");

        const newFile = {
          name: file.name,
          size: `${(file.size / 1024).toFixed(2)} KB`,
          date: new Date().toLocaleString(),
        };

        setRecentFiles((prev) => {
          const updated = [newFile, ...prev];
          return updated.slice(0, 5);
        });
      };

      reader.readAsArrayBuffer(file);
    } else {
      setMessage("Wrong format. Please upload a .csv or .xlsx file.");
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files.length > 0) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = () => {
    setDragOver(false);
  };

  const handleFileUpload = (e) => {
    if (e.target.files.length > 0) {
      handleFile(e.target.files[0]);
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="w-full px-4 py-8 flex flex-col items-center">
      <div className="w-full max-w-4xl bg-white rounded-lg border flex flex-col items-center justify-center shadow p-4">
        <div
          className={`w-full max-w-xl h-48 sm:h-60 md:h-52 rounded-xl border-2 border-dashed flex flex-col items-center justify-center cursor-pointer transition-colors ${
            dragOver ? "border-blue-400 bg-blue-100" : "border-gray-300 bg-blue-50"
          }`}
          onClick={triggerFileInput}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
        >
          <p className="text-gray-700 font-medium text-center px-4">
            Click or drag a .csv or .xlsx file here
          </p>
          <p className="text-sm text-gray-500 mt-2 text-center px-2">
            (Only CSV or Excel files allowed)
          </p>
          <input
            type="file"
            accept=".csv, .xlsx"
            ref={fileInputRef}
            onChange={handleFileUpload}
            className="hidden"
          />
        </div>
        {message && <p className="text-sm text-blue-600 mt-4 text-center">{message}</p>}
      </div>

      {recentFiles.length > 0 && (
        <div className="w-full max-w-4xl mt-8 bg-white border rounded-lg shadow overflow-x-auto">
          <h3 className="text-lg font-semibold text-gray-800 px-4 py-3 border-b">Recent Uploads</h3>
          <table className="min-w-full text-sm text-left text-gray-700">
            <thead className="bg-gray-100 Китая

text-gray-600 uppercase text-xs">
              <tr>
                <th className="px-4 py-2">File Name</th>
                <th className="px-4 py-2">Size</th>
                <th className="px-4 py-2">Uploaded At</th>
              </tr>
            </thead>
            <tbody>
              {recentFiles.map((file, index) => (
                <tr key={index} className="border-t">
                  <td className="px-4 py-2 truncate max-w-xs">{file.name}</td>
                  <td className="px-4 py-2">{file.size}</td>
                  <td className="px-4 py-2">{file.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

function AnomalyPage() {
  const [anomalyData, setAnomalyData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem("token");
        const { data } = await axios.get("http://localhost:5000/api/Anamoly", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const anomaly = data.anomalies[0];
        const analytics = data.anomalies[0]?.anomalies || [];
        
        setAnomalyData(anomaly);
        reportData.anomaly = anomaly;
        reportData.analytics = analytics;
        
        console.log("Anomaly data stored:", reportData.anomaly);
        console.log("Analytics data stored from AnomalyPage:", reportData.analytics);
        setLoading(false);
      } catch (err) {
        setError("Failed to load anomalies.");
        console.error("Anomaly fetch error:", err);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <p>Loading anomalies...</p>;
  if (error) return <p className="text-red-500">{error}</p>;
  if (!anomalyData) return <p>No data available.</p>;

  return (
    <div>
      <h2 className="text-3xl font-bold text-blue-700 mb-4">Anomaly Detection</h2>
      <div className="flex justify-between items-center mb-6 text-gray-700">
        <div>
          <p>
            <span className="font-semibold">Total Anomalies:</span> {anomalyData.metadata?.total_anomalies || "N/A"}
          </p>
          <p className="text-sm mt-1 italic text-gray-600">{anomalyData.metadata?.recommendation || "No recommendation"}</p>
        </div>
        <button
          className="px-4 py-2 bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700 transition"
          onClick={() => {
            console.log("Download button clicked, reportData:", reportData);
            DownloadReport(reportData);
          }}
        >
          Download Report
        </button>
      </div>

      <div className="overflow-auto rounded-lg shadow-xl ring-1 ring-gray-200">
        <table className="min-w-full bg-white text-sm text-gray-800">
          <thead className="bg-blue-600 text-white sticky top-0 z-10">
            <tr>
              <th className="px-4 py-3 text-left">Column</th>
              <th className="px-4 py-3 text-left">Type</th>
              <th className="px-4 py-3 text-left">Count</th>
              <th className="px-4 py-3 text-left">Severity</th>
              <th className="px-4 py-3 text-left">Explanation</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {anomalyData.anomalies.map((anomaly, index) => (
              <tr key={index} className="hover:bg-gray-50 even:bg-gray-50 transition-colors">
                <td className="px-4 py-3 font-medium">{anomaly.column || "Not Specified"}</td>
                <td className="px-4 py-3">{anomaly.type === "LSTM" ? "AI Detected" : anomaly.type}</td>
                <td className="px-4 py-3">{anomaly.count || 1}</td>
                <td
                  className={`px-4 py-3 font-semibold ${
                    anomaly.severity > 60
                      ? "text-red-600"
                      : anomaly.severity > 40
                      ? "text-yellow-600"
                      : "text-green-600"
                  }`}
                >
                  {anomaly.severity > 60 ? "High" : anomaly.severity > 40 ? "Medium" : "Low"}
                </td>
                <td className="px-4 py-3 max-w-md break-words whitespace-pre-line text-gray-600">
                  {anomaly.explanation}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function DownloadReport(data) {
  console.log("DownloadReport called with data:", data);

  try {
    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();
    const margin = 10;
    let yPosition = margin;

    // Header
    doc.setFontSize(22);
    doc.setTextColor(29, 78, 216); // Blue-700
    doc.text("Auralytics Report", margin, yPosition);
    yPosition += 15;

    // Anomaly Section
    if (data.anomaly) {
      doc.setFontSize(16);
      doc.text("Anomaly Detection", margin, yPosition);
      yPosition += 10;

      doc.setFontSize(12);
      doc.setTextColor(55, 65, 81); // Gray-700
      doc.text(`Total Anomalies: ${data.anomaly.metadata?.total_anomalies || "N/A"}`, margin, yPosition);
      yPosition += 7;
      doc.setFontSize(10);
      doc.setTextColor(75, 85, 99); // Gray-600
      doc.text(data.anomaly.metadata?.recommendation || "No recommendation available", margin, yPosition, { maxWidth: pageWidth - 2 * margin });
      yPosition += 15;

      // Anomaly Table Header
      doc.setFillColor(37, 99, 235); // Blue-600
      doc.rect(margin, yPosition, pageWidth - 2 * margin, 8, "F");
      doc.setTextColor(255, 255, 255);
      doc.setFontSize(10);
      doc.text("Column", margin + 2, yPosition + 6);
      doc.text("Type", margin + 40, yPosition + 6);
      doc.text("Count", margin + 80, yPosition + 6);
      doc.text("Severity", margin + 100, yPosition + 6);
      doc.text("Explanation", margin + 130, yPosition + 6);
      yPosition += 8;

      // Anomaly Table Rows
      doc.setFontSize(10);
      if (data.anomaly.anomalies && Array.isArray(data.anomaly.anomalies)) {
        data.anomaly.anomalies.forEach((anomaly, index) => {
          if (yPosition > doc.internal.pageSize.getHeight() - 20) {
            doc.addPage();
            yPosition = margin;
          }

          doc.setTextColor(31, 41, 55); // Gray-800
          const bgColor = index % 2 === 0 ? [243, 244, 246] : [255, 255, 255];
          doc.setFillColor(...bgColor);
          doc.rect(margin, yPosition, pageWidth - 2 * margin, 10, "F");

          doc.text(String(anomaly.column || "Not Specified"), margin + 2, yPosition + 7);
          doc.text(anomaly.type === "LSTM" ? "AI Detected" : String(anomaly.type || "Unknown"), margin + 40, yPosition + 7);
          doc.text(String(anomaly.count || 1), margin + 80, yPosition + 7);

          const severityText = anomaly.severity > 60 ? "High" : anomaly.severity > 40 ? "Medium" : "Low";
          doc.setTextColor(anomaly.severity > 60 ? [220, 38, 38] : anomaly.severity > 40 ? [202, 138, 4] : [22, 163, 74]);
          doc.text(severityText, margin + 100, yPosition + 7);

          doc.setTextColor(75, 85, 99); // Gray-600
          doc.text(String(anomaly.explanation || "No explanation"), margin + 130, yPosition + 7, { maxWidth: 60 });
          yPosition += 10;
        });
      } else {
        doc.setTextColor(31, 41, 55);
        doc.text("No anomaly data available", margin, yPosition);
        yPosition += 10;
      }
      yPosition += 15;
    } else {
      doc.setFontSize(16);
      doc.setTextColor(29, 78, 216);
      doc.text("Anomaly Detection", margin, yPosition);
      yPosition += 10;
      doc.setFontSize(12);
      doc.setTextColor(55, 65, 81);
      doc.text("No anomaly data available", margin, yPosition);
      yPosition += 15;
    }

    // Analytics Section
    if (data.analytics && Array.isArray(data.analytics)) {
      if (yPosition > doc.internal.pageSize.getHeight() - 40) {
        doc.addPage();
        yPosition = margin;
      }

      doc.setFontSize(16);
      doc.setTextColor(29, 78, 216); // Blue-700
      doc.text("Analytics Summary", margin, yPosition);
      yPosition += 10;

      const anomalyTypeMap = {};
      data.analytics.forEach((anomaly) => {
        const type = anomaly.type || "Unknown";
        anomalyTypeMap[type] = (anomalyTypeMap[type] || 0) + 1;
      });

      doc.setFontSize(12);
      doc.setTextColor(31, 41, 55); // Gray-800
      doc.text("Anomaly Type Distribution", margin, yPosition);
      yPosition += 7;

      doc.setFontSize(10);
      Object.entries(anomalyTypeMap).forEach(([type, count]) => {
        doc.text(`${type}: ${count}`, margin + 5, yPosition);
        yPosition += 6;
      });
      yPosition += 10;

      const severityDistribution = data.analytics.reduce((acc, curr) => {
        const bucket = Math.floor(curr.severity / 10) * 10;
        acc[bucket] = (acc[bucket] || 0) + 1;
        return acc;
      }, {});

      doc.setFontSize(12);
      doc.text("Severity Distribution", margin, yPosition);
      yPosition += 7;

      doc.setFontSize(10);
      Object.entries(severityDistribution).forEach(([severity, freq]) => {
        doc.text(`${severity}-${parseInt(severity) + 9}: ${freq}`, margin + 5, yPosition);
        yPosition += 6;
      });
    } else {
      if (yPosition > doc.internal.pageSize.getHeight() - 40) {
        doc.addPage();
        yPosition = margin;
      }
      doc.setFontSize(16);
      doc.setTextColor(29, 78, 216);
      doc.text("Analytics Summary", margin, yPosition);
      yPosition += 10;
      doc.setFontSize(12);
      doc.setTextColor(55, 65, 81);
      doc.text("No analytics data available", margin, yPosition);
      yPosition += 15;
    }

    // Footer
    doc.setFontSize(8);
    doc.setTextColor(107, 114, 128); // Gray-500
    doc.text(`Generated on: ${new Date().toLocaleString()}`, margin, doc.internal.pageSize.getHeight() - margin);

    console.log("PDF generation completed, saving...");
    doc.save("Auralytics_Report.pdf");
  } catch (error) {
    console.error("Error generating PDF:", error);
    toast.error("Failed to generate report. Please try again.", {
      position: "top-right",
      autoClose: 3000,
    });
  }
}

function StatCard({ title, value, change, isNegative }) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-sm">
      <h4 className="text-sm text-gray-500 mb-2">{title}</h4>
      <p className="text-2xl font-bold">{value}</p>
      <p className={`text-sm ${isNegative ? "text-red-500" : "text-green-600"}`}>{change}</p>
      <div className="h-1 bg-gray-200 mt-2">
        <div
          className={`h-full ${isNegative ? "bg-red-400" : "bg-blue-500"}`}
          style={{ width: isNegative ? "30%" : "70%" }}
        />
      </div>
    </div>
  );
}