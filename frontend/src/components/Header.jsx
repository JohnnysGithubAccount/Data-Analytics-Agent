import { useState, useEffect } from "react";
import "./Header.css";

export default function Header() {
  const fullText = "Data Analysis Agent";
  const [displayText, setDisplayText] = useState("");
  const [typing, setTyping] = useState(true);

  useEffect(() => {
    let timeout;
    if (typing) {
      if (displayText.length < fullText.length) {
        timeout = setTimeout(() => {
          setDisplayText(fullText.slice(0, displayText.length + 1));
        }, 120);
      } else {
        timeout = setTimeout(() => setTyping(false), 2000);
      }
    } else {
      if (displayText.length > 0) {
        timeout = setTimeout(() => {
          setDisplayText(fullText.slice(0, displayText.length - 1));
        }, 60);
      } else {
        setTyping(true);
      }
    }
    return () => clearTimeout(timeout);
  }, [displayText, typing]);

  return (
    <header className="header">
      <div className="header-left">
        <h1 className="logo">
          <span className="robot-icon">🤖</span>
          {displayText}
          <span className="cursor">_</span>
        </h1>
      </div>
      <nav className="header-nav">
        <a href="https://github.com/yourname" target="_blank" rel="noopener noreferrer">GitHub</a>
        <a href="#">Docs</a>
        <a href="#">About</a>
      </nav>
    </header>
  );
}
