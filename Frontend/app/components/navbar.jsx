"use client"

import { useState } from "react"
import Link from "next/link"
import { Menu, X, Fish, ChevronDown } from "lucide-react"
import { Button } from "../components/ui/button"


export function Navbar() {
  const [isOpen, setIsOpen] = useState(false)
  const [showProducts, setShowProducts] = useState(false)

  const navLinks = [
    { name: "Home", href: "/" },
    { name: "Products", href: "/products", hasDropdown: true },
    { name: "Diseases", href: "/diseases" },
    { name: "Feed Calculator", href: "/feed-calculator" },
    { name: "Weather", href: "/weather" },
    { name: "Farmer Connect", href: "/farmer-connect" },
  ]

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/95 backdrop-blur-md border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center">
              <Fish className="w-6 h-6 text-primary-foreground" />
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-foreground text-lg leading-tight">Kanan Biotech</span>
              <span className="text-xs text-muted-foreground">Pvt. Ltd</span>
            </div>
          </Link>

          <div className="hidden lg:flex items-center gap-1">
            {navLinks.map((link) => (
              <div key={link.name} className="relative">
                {link.hasDropdown ? (
                  <button
                    onMouseEnter={() => setShowProducts(true)}
                    onMouseLeave={() => setShowProducts(false)}
                    className="flex items-center gap-1 px-4 py-2 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {link.name}
                    <ChevronDown className="w-4 h-4" />
                  </button>
                ) : (
                  <Link
                    href={link.href}
                    className="px-4 py-2 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {link.name}
                  </Link>
                )}
                {link.hasDropdown && showProducts && (
                  <div
                    onMouseEnter={() => setShowProducts(true)}
                    onMouseLeave={() => setShowProducts(false)}
                    className="absolute top-full left-0 w-48 bg-background border border-border rounded-lg shadow-lg py-2"
                  >
                    <Link href="/products" className="block px-4 py-2 text-sm hover:bg-muted">
                      All Products
                    </Link>
                    <Link href="/products#feed" className="block px-4 py-2 text-sm hover:bg-muted">
                      Fish Feed
                    </Link>
                    <Link href="/products#medicine" className="block px-4 py-2 text-sm hover:bg-muted">
                      Medicines
                    </Link>
                    <Link href="/products#supplements" className="block px-4 py-2 text-sm hover:bg-muted">
                      Supplements
                    </Link>
                  </div>
                )}
              </div>
            ))}
          </div>

          <div className="hidden lg:flex items-center gap-3">
            <Link href="/login">
              <Button variant="ghost">Login</Button>
            </Link>
            <Link href="/signup">
              <Button>Sign Up</Button>
            </Link>
          </div>

          <button className="lg:hidden p-2" onClick={() => setIsOpen(!isOpen)}>
            {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {isOpen && (
        <div className="lg:hidden bg-background border-t border-border">
          <div className="px-4 py-4 space-y-2">
            {navLinks.map((link) => (
              <Link
                key={link.name}
                href={link.href}
                className="block px-4 py-2 text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-muted rounded-lg"
                onClick={() => setIsOpen(false)}
              >
                {link.name}
              </Link>
            ))}
            <div className="pt-4 flex flex-col gap-2">
              <Link href="/login">
                <Button variant="outline" className="w-full bg-transparent">
                  Login
                </Button>
              </Link>
              <Link href="/signup">
                <Button className="w-full">Sign Up</Button>
              </Link>
            </div>
          </div>
        </div>
      )}
    </nav>
  )
}
