import Link from "next/link"
import { Button } from "../components/ui/button"
import { ArrowRight, Phone } from "lucide-react"

export function CTASection() {
  return (
    <section className="py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="hero-gradient rounded-3xl p-8 md:p-16 text-center text-white">
          <h2 className="text-3xl md:text-4xl font-bold mb-4 text-balance">Ready to Transform Your Fish Farm?</h2>
          <p className="text-white/80 max-w-2xl mx-auto mb-8">
            Join thousands of successful fish farmers who trust Kanan Biotech for their aquaculture needs. Get expert
            guidance and premium products.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link href="/signup">
              {/*<Button size="lg" className="bg-white text-primary hover:bg-white/90">
                Get Started Free
                <ArrowRight className="ml-2 w-4 h-4" />
              </Button>*/}
            </Link>
            <Link href="/farmer-connect">
              <Button size="lg" variant="outline" className="border-white text-white hover:bg-white/10 bg-transparent">
                <Phone className="mr-2 w-4 h-4" />
                Contact Sales
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </section>
  )
}
