"use client";

import { Navbar } from "./components/navbar";
import { HeroSection } from "./components/hero-section";
import { FeaturesSection } from "./components/features-section";
import { SeasonalDiseases } from "./components/seasonal-diseases";
import { ProductsPreview } from "./components/products-preview";
import { CTASection } from "./components/cta-section";
import { Footer } from "./components/footer";

export default function HomePage() {
  return (
    <main>
      <Navbar />
      <HeroSection />
      <FeaturesSection />
      <SeasonalDiseases />
      <ProductsPreview />
      <CTASection />
      <Footer />
    </main>
  );
}
