import { Routes, Route, useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import Footer from "./components/Footer";

import Upload from "./pages/Upload";
import Analysis from "./pages/Analysis";
import Insights from "./pages/Insights";
import DataReview from "./pages/DataReview";

// Wrapper component for page animations
function PageWrapper({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.5, ease: "easeInOut" }}
      style={{ height: "100%" }}
    >
      {children}
    </motion.div>
  );
}

export default function App() {
  const location = useLocation();

  return (
    <div className="app-container">
      <Header />
      <div className="main-layout">
        <Sidebar />
        <main className="content">
          <AnimatePresence mode="wait">
            <Routes location={location} key={location.pathname}>
              <Route
                path="/"
                element={
                  <PageWrapper>
                    <Upload />
                  </PageWrapper>
                }
              />
              <Route
                path="/review"
                element={
                  <PageWrapper>
                    <DataReview />
                  </PageWrapper>
                }
              />
              <Route
                path="/analysis"
                element={
                  <PageWrapper>
                    <Analysis />
                  </PageWrapper>
                }
              />
              <Route
                path="/insights"
                element={
                  <PageWrapper>
                    <Insights />
                  </PageWrapper>
                }
              />
            </Routes>
          </AnimatePresence>
        </main>
      </div>
      <Footer />
    </div>
  );
}
