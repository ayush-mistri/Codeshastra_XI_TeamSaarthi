import { FaChartLine, FaBell, FaCog, FaUser, FaBars } from "react-icons/fa";
import { MdDashboard } from "react-icons/md";
import { useState } from "react";

export default function Dashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex flex-col h-screen">
      {/* Top Bar */}
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
        <button className="p-2 rounded-full bg-gray-100 hover:bg-gray-200">
          <FaUser size={18} />
        </button>
      </header>

      {/* Main Layout */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <aside
          className={`bg-blue-700 text-white w-64 p-6 space-y-6 lg:block ${
            sidebarOpen ? "block" : "hidden"
          }`}
        >
          <h2 className="text-2xl font-bold flex items-center gap-2 mb-10">
            <FaChartLine /> DashPro
          </h2>
          <nav className="space-y-4">
            <SidebarItem icon={<MdDashboard />} label="Dashboard" active />
            <SidebarItem icon={<FaChartLine />} label="Analytics" />
            <SidebarItem icon={<FaBell />} label="Notifications" />
            <SidebarItem icon={<FaCog />} label="Settings" />
          </nav>

          <div className="mt-10 flex items-center gap-3">
            <div className="bg-white text-blue-700 rounded-full p-2">
              <FaUser />
            </div>
            <div>
              <p className="font-semibold">Essam Mohamed</p>
              <p className="text-sm text-gray-300">Essam@example.com</p>
            </div>
          </div>
        </aside>

        {/* Content */}
        <main className="flex-1 p-6 overflow-y-auto bg-gray-50">
          <h2 className="text-2xl font-bold mb-4 block lg:hidden">Dashboard</h2>
          <p className="text-gray-600 mb-6">View your analytics and track your business performance.</p>

          {/* Stats */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
            <StatCard title="Total Revenue" value="$45,231.89" change="+20.1% from last month" />
            <StatCard title="Subscriptions" value="+2350" change="+180.1%" />
            <StatCard title="Sales" value="+12,234" change="+19%" />
            <StatCard title="Active Now" value="+573" change="-201" isNegative />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Chart */}
            <div className="col-span-2 bg-white p-6 rounded-lg shadow-sm">
              <h3 className="font-semibold text-lg mb-2">Overview</h3>
              <p className="text-sm text-gray-500 mb-4">Monthly revenue overview for the current year.</p>
              <div className="h-64 bg-gray-100 flex items-center justify-center rounded">
                Chart Visualization
              </div>
            </div>

            {/* Recent Activity */}
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <h3 className="font-semibold text-lg mb-2">Recent Activity</h3>
              <p className="text-sm text-gray-500 mb-4">Your recent activity and events.</p>
              <ul className="space-y-4 text-sm">
                {Array.from({ length: 5 }).map((_, i) => (
                  <li className="flex justify-between" key={i}>
                    <span>New subscription from Customer #{i + 1}</span>
                    <span className="font-medium">+${(i + 1) * 100}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

function SidebarItem({ icon, label, active }) {
  return (
    <div
      className={`flex items-center gap-2 px-4 py-2 rounded cursor-pointer ${
        active ? "bg-blue-600 font-semibold" : "hover:bg-blue-600"
      }`}
    >
      {icon}
      {label}
    </div>
  );
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
