import Link from "next/link"
import { Fish, Phone, Mail, MapPin, Facebook, Twitter, Linkedin, Youtube } from "lucide-react"

export function Footer() {
  return (
    <footer className="bg-foreground text-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12">
          <div>
            <div className="flex items-center gap-2 mb-6">
              <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center">
                <Fish className="w-6 h-6 text-primary-foreground" />
              </div>
              <div className="flex flex-col">
                <span className="font-bold text-lg leading-tight">Kanan Biotech</span>
                <span className="text-xs text-muted-foreground">Pvt. Ltd</span>
              </div>
            </div>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Leading provider of aquaculture solutions, helping fish farmers achieve optimal productivity and fish
              health.
            </p>
          </div>

          <div>
            <h4 className="font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-3">
              <li>
                {/*<Link
                  href="/products"
                  className="text-sm text-muted-foreground hover:text-background transition-colors"
                >
                  Products
                </Link> */}
              </li>
              <li>
                <Link
                  href="/diseases"
                  className="text-sm text-muted-foreground hover:text-background transition-colors"
                >
                  Fish Diseases
                </Link>
              </li>
              <li>
                <Link
                  href="/feed-calculator"
                  className="text-sm text-muted-foreground hover:text-background transition-colors"
                >
                  Feed Calculator
                </Link>
              </li>
              <li>
                {/*
                <Link href="/weather" className="text-sm text-muted-foreground hover:text-background transition-colors">
                  Weather Report
                </Link> */}
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold mb-4">Services</h4>
            <ul className="space-y-3">
              <li>
                <Link
                  href="/farmer-connect"
                  className="text-sm text-muted-foreground hover:text-background transition-colors"
                >
                  Farmer Connect
                </Link>
              </li>
              <li>
                <Link
                  href="/feed-calculator"
                  className="text-sm text-muted-foreground hover:text-background transition-colors"
                >
                  Feed Management
                </Link>
              </li>
              <li>
                <Link
                  href="/diseases"
                  className="text-sm text-muted-foreground hover:text-background transition-colors"
                >
                  Disease Guide
                </Link>
              </li>
              <li>
                {/*<Link
                  href="/products"
                  className="text-sm text-muted-foreground hover:text-background transition-colors"
                >
                  Product Catalog
                </Link> */}
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold mb-4">Contact Us</h4>
            <ul className="space-y-3">
              <li className="flex items-center gap-2 text-sm text-muted-foreground">
                <Phone className="w-4 h-4" />
                +91 98765 43210
              </li>
              <li className="flex items-center gap-2 text-sm text-muted-foreground">
                <Mail className="w-4 h-4" />
                kananbiotech@gmail.com
              </li>
              <li className="flex items-start gap-2 text-sm text-muted-foreground">
                <MapPin className="w-4 h-4 mt-0.5" />
                <span>
                  Debra, Kharagpur, Paschim Midnapore
                  <br />
                  West Bengal, Pin-721126
                </span>
              </li>
            </ul>
            <div className="flex gap-4 mt-6">
              <a href="https://www.facebook.com/profile.php?id=61580163557719" className="text-muted-foreground hover:text-background transition-colors">
                <Facebook className="w-5 h-5" />
              </a>
              <a href="https://x.com/infokbtech" className="text-muted-foreground hover:text-background transition-colors">
                <Twitter className="w-5 h-5" />
              </a>
              <a href="https://www.linkedin.com/in/kanan-biotech-951a9b3a9/" className="text-muted-foreground hover:text-background transition-colors">
                <Linkedin className="w-5 h-5" />
              </a>
              {/*<a href="#" className="text-muted-foreground hover:text-background transition-colors">
                <Youtube className="w-5 h-5" />
              </a>*/}
            </div>
          </div>
        </div>

        <div className="border-t border-muted-foreground/20 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-sm text-muted-foreground">© 2026 Kanan Biotech Pvt. Ltd. All rights reserved.</p>
          <div className="flex gap-6">
            <Link href="#" className="text-sm text-muted-foreground hover:text-background transition-colors">
              Privacy Policy
            </Link>
            <Link href="#" className="text-sm text-muted-foreground hover:text-background transition-colors">
              Terms of Service
            </Link>
          </div>
        </div>
      </div>
    </footer>
  )
}
