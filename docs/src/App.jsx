import React from "react";
import Header from "./Components/Header";
import Footer from "./Components/Footer";
import ServicesSection from "./Components/ServicesSection";
import { LanguageProvider } from "./context/LanguageContext";
import Informesstional from "./Components/Informesstional";
import ChatBotWidget from "./pages/ChatBotWidget";

const PageStyles = () => (
  <style>{`
    .hero {
      position: relative;
      background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
      color: #ffffff;
      padding: 80px 40px;
      overflow: hidden;
    }

    .hero-content {
      max-width: 1200px;
      margin: auto;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 40px;
      align-items: center;
    }

    .hero-text h1 {
      font-size: 3.2rem;
      font-weight: 700;
      margin-bottom: 20px;
    }

    .hero-text p {
      font-size: 1.1rem;
      line-height: 1.7;
      color: #e0e0e0;
      margin-bottom: 30px;
    }

    .cta-button {
      display: inline-block;
      padding: 14px 28px;
      background: #00c853;
      color: #fff;
      border-radius: 30px;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.3s ease;
    }

    .cta-button:hover {
      background: #00a844;
      transform: translateY(-2px);
    }

    .image-grid {
      display: grid;
      grid-template-columns: 2fr 1fr;
      grid-template-rows: 1fr 1fr;
      gap: 15px;
    }

    .img-large {
      grid-row: span 2;
      width: 100%;
      height: 100%;
      object-fit: cover;
      border-radius: 16px;
    }

    .img-small-1,
    .img-small-2 {
      width: 100%;
      height: 100%;
      object-fit: cover;
      border-radius: 16px;
    }

    @media (max-width: 900px) {
      .hero-content {
        grid-template-columns: 1fr;
        text-align: center;
      }
    }
  `}</style>
);

function App() {
  return (
    <LanguageProvider>
      <>
        <PageStyles />

        {/* Header */}
        <Header />

        {/* Services */}
        <ServicesSection />

        {/* Hero Section */}
        <main className="hero">
          <div className="hero-content">
            <div className="hero-text">
              <h1>Innovating Agriculture & Fisheries Through Biotechnology</h1>
              <p>
                Kanan Biotech delivers advanced biotechnology solutions for
                agriculture and fisheries, with a strong focus on fish disease
                prevention, health management, and sustainable farming
                practices. Empower your growth with science-driven innovation.
              </p>
              <a href="#booking" className="cta-button">
                Explore Our Solutions
              </a>
            </div>

            <div className="hero-images">
              <div className="image-grid">
                <video
                  src="/Video1.mp4"
                  className="img-large"
                  autoPlay
                  loop
                  muted
                />
                <img
                  src="/Img5.webp"
                  alt="Modern agriculture practices"
                  className="img-small-1"
                />
                <img
                  src="/Photo1.jpeg"
                  alt="Fishery and aquatic health"
                  className="img-small-2"
                />
              </div>
            </div>
          </div>

          {/* ChatBot */}
          <ChatBotWidget />
        </main>

        {/* Footer */}
        <Footer />
      </>
    </LanguageProvider>
  );
}

export default App;
