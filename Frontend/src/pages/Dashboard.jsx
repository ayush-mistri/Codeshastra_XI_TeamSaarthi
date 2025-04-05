import { FaBars, FaUser, FaChartLine } from "react-icons/fa";
import { MdDashboard } from "react-icons/md";
import { useEffect, useState } from "react";
import { NavLink, Routes, Route, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

export default function Dashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const navigate = useNavigate();


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
    }
  }, []);

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
    { label: "Dashboard", path: "/dashboard", icon: <MdDashboard /> },
    { label: "Analytics", path: "/dashboard/analytics", icon: <FaChartLine /> },
    { label: "Anomaly", path: "/dashboard/anomaly", icon: <FaChartLine /> },
  ];

  return (
    <div className="flex flex-col h-screen">
      {/* Top Navigation */}
      <header className="flex justify-between items-center px-6 py-4 bg-white shadow-md">
        <div className="flex items-center gap-4">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="text-blue-600 lg:hidden"
          >
            <FaBars size={20} />
          </button>
          <h1 className="text-2xl font-bold text-blue-600 hidden lg:block">Dashboard</h1>
        </div>
        <button
          onClick={handleLogout}
          className="px-4 py-2 rounded-lg bg-red-500 text-white hover:bg-red-600 transition"
          title="Logout"
        >
          Logout
        </button>
      </header>

      {/* Layout */}
      <div className="flex flex-1 overflow-hidden">
        {/* Mobile Overlay */}
        {sidebarOpen && (
          <div
            className="fixed inset-0 bg-black bg-opacity-40 z-40 lg:hidden"
            onClick={() => setSidebarOpen(false)}
          />
        )}

        {/* Sidebar */}
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
                    `flex items-center gap-2 px-4 py-2 rounded transition ${
                      isActive ? "bg-blue-600 font-semibold" : "hover:bg-blue-600"
                    }`
                  }
                >
                  {icon}
                  {label}
                </NavLink>
              ))}
            </nav>

            {/* User Info */}
            <div className="mt-6 pt-6 border-t border-blue-600 flex items-center gap-3">
              <div className="bg-white text-blue-700 rounded-full p-2">
                <FaUser />
              </div>
              <div>
                <p className="font-semibold">Essam Mohamed</p>
                <p className="text-sm text-gray-300">Essam@example.com</p>
              </div>
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-6 overflow-y-auto bg-gray-50">
          <Routes>
            <Route
              path="/"
              element={
                <DashboardHome />
              }
            />
            <Route
              path="/analytics"
              element={
                <AnalyticsPage />
              }
            />
            <Route
              path="/anomaly"
              element={
                <AnomalyPage />
              }
            />
          </Routes>
        </main>
      </div>
    </div>
  );
}

function DashboardHome() {
  return (
    <>
      <h2 className="text-2xl font-bold mb-4">Dashboard</h2>
      <p className="text-gray-600 mb-6">
        View your analytics and track your business performance.
      </p>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <StatCard title="Total Revenue" value="$45,231.89" change="+20.1% from last month" />
        <StatCard title="Subscriptions" value="+2350" change="+180.1%" />
        <StatCard title="Sales" value="+12,234" change="+19%" />
        <StatCard title="Active Now" value="+573" change="-201" isNegative />
      </div>
    </>
  );
}

function AnalyticsPage() {
  return (
    <>
      <h2 className="text-2xl font-bold mb-4">Analytics</h2>
      <p className="text-gray-600 mb-4">
        Insights and trends from your application usage.
      </p>
      <div className="h-64 bg-gray-100 rounded flex items-center justify-center">
        [Analytics Chart Placeholder]
      </div>
    </>
  );
}

function AnomalyPage() {
  return (
    <>
      <h2 className="text-2xl font-bold mb-4">Anomaly Detection</h2>
      <p className="text-gray-600 mb-4">
        Monitoring and detection of unusual patterns.
      </p>
      <div className="h-64 bg-gray-100 rounded flex items-center justify-center">
        [Anomaly Detection Graph]
      </div>
    </>
  );
}

function StatCard({ title, value, change, isNegative }) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-sm">
      <h4 className="text-sm text-gray-500 mb-2">{title}</h4>
      <p className="text-2xl font-bold">{value}</p>
      <p className={`text-sm ${isNegative ? "text-red-500" : "text-green-600"}`}>
        {change}
      </p>
      <div className="h-1 bg-gray-200 mt-2">
        <div
          className={`h-full ${isNegative ? "bg-red-400" : "bg-blue-500"}`}
          style={{ width: isNegative ? "30%" : "70%" }}
        />
      </div>
    </div>
  );
}
