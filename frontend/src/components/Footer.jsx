import "./Footer.css";
import { FaGithub, FaLinkedin, FaEnvelope } from "react-icons/fa";

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-links">
          <a
            href="https://github.com/yourusername"
            target="_blank"
            rel="noopener noreferrer"
          >
            <FaGithub className="icon" /> GitHub
          </a>
          <a
            href="https://linkedin.com/in/yourprofile"
            target="_blank"
            rel="noopener noreferrer"
          >
            <FaLinkedin className="icon" /> LinkedIn
          </a>
          <a href="mailto:taifa2907@gmail.com">
            <FaEnvelope className="icon" /> Email
          </a>
        </div>
      </div>
      <p className="footer-bottom">© {new Date().getFullYear()} Johnny. All rights reserved.</p>
    </footer>
  );
}
