import { NavLink } from "react-router-dom";
import { FaUpload, FaChartBar, FaRobot, FaTable } from "react-icons/fa";
import "./Sidebar.css";

export default function Sidebar() {
  const links = [
    { name: "Upload", path: "/", icon: <FaUpload /> },
    { name: "Data Review", path: "/review", icon: <FaTable /> },
    { name: "Analysis", path: "/analysis", icon: <FaChartBar /> },
    { name: "Insights", path: "/insights", icon: <FaRobot /> },
  ];

  return (
    <aside className="sidebar">
      <nav>
        {links.map((link) => (
          <NavLink
            key={link.name}
            to={link.path}
            end
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            <span className="icon">{link.icon}</span>
            <span className="link-text">{link.name}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
