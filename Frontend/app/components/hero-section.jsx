import Link from "next/link"
import { Button } from "../components/ui/button"
import { ArrowRight, Play } from "lucide-react"

export function HeroSection() {
  return (
    <section className="hero-gradient min-h-screen flex items-center pt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="text-white">
            <div className="inline-flex items-center gap-2 bg-white/10 rounded-full px-4 py-2 mb-6">
              <span className="w-2 h-2 bg-secondary rounded-full animate-pulse" />
              <span className="text-sm font-medium">Trusted by 10,000+ Fish Farmers</span>
            </div>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight text-balance mb-6">
              Empowering Aquaculture with Science
            </h1>
            <p className="text-lg text-white/80 leading-relaxed mb-8 max-w-xl">
              Premium fish health solutions, advanced feed management, and expert guidance to maximize your farm's
              productivity and profitability.
            </p>
            <div className="flex flex-wrap gap-4">
              <Link href="/products">
                <Button size="lg" className="bg-white text-primary hover:bg-white/90">
                  Explore Products
                  <ArrowRight className="ml-2 w-4 h-4" />
                </Button>
              </Link>
              <Link href="/feed-calculator">
                <Button
                  size="lg"
                  variant="outline"
                  className="border-white text-white hover:bg-white/10 bg-transparent"
                >
                  <Play className="mr-2 w-4 h-4" />
                  Try Feed Calculator
                </Button>
              </Link>
            </div>

            <div className="grid grid-cols-3 gap-8 mt-12 pt-8 border-t border-white/20">
              <div>
                <div className="text-3xl font-bold">500+</div>
                <div className="text-sm text-white/70">Products</div>
              </div>
              <div>
                <div className="text-3xl font-bold">15+</div>
                <div className="text-sm text-white/70">Years Experience</div>
              </div>
              <div>
                <div className="text-3xl font-bold">24/7</div>
                <div className="text-sm text-white/70">Support</div>
              </div>
            </div>
          </div>

          <div className="relative">
            <div className="relative rounded-2xl overflow-hidden shadow-2xl">
              <img src="/fish-farm-aquaculture-pond-aerial-view-professiona.jpg" alt="Fish farm aerial view" className="w-full h-auto" />
              <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />
              <div className="absolute bottom-6 left-6 right-6 bg-white/95 backdrop-blur rounded-xl p-4">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-full bg-secondary/20 flex items-center justify-center">
                    <span className="text-2xl">🐟</span>
                  </div>
                  <div>
                    <div className="font-semibold text-foreground">Seasonal Disease Alert</div>
                    <div className="text-sm text-muted-foreground">Winter diseases prevention guide available</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
