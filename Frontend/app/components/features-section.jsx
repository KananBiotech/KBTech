import Link from "next/link"
import { Card, CardContent } from "../components/ui/card"
import { Calculator, Cloud, Users, Package, Pill, BarChart3 } from "lucide-react"

const features = [
  {
    icon: Calculator,
    title: "Feed Calculator",
    description: "Calculate optimal feed quantities based on fish species, weight, and pond conditions.",
    href: "/feed-calculator",
    color: "bg-primary/10 text-primary",
  },
  {
    icon: Cloud,
    title: "Weather Report",
    description: "Real-time weather updates with temperature, humidity, and farming recommendations.",
    href: "/weather",
    color: "bg-secondary/10 text-secondary",
  },
  {
    icon: Users,
    title: "Farmer Connect",
    description: "Connect with buyers and sellers for fish selling and farming consultation.",
    href: "/farmer-connect",
    color: "bg-amber-100 text-amber-600",
  },
  {
    icon: Package,
    title: "Product Catalog",
    description: "Browse our complete range of fish feed, medicines, and aquaculture supplies.",
    href: "/products",
    color: "bg-emerald-100 text-emerald-600",
  },
  {
    icon: Pill,
    title: "Disease Guide",
    description: "Comprehensive guide to fish diseases with prevention and treatment information.",
    href: "/diseases",
    color: "bg-rose-100 text-rose-600",
  },
  {
    icon: BarChart3,
    title: "Feed Management",
    description: "Track and optimize your feeding schedules for maximum growth efficiency.",
    href: "/feed-calculator",
    color: "bg-indigo-100 text-indigo-600",
  },
]

export function FeaturesSection() {
  return (
    <section className="py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4 text-balance">
            Everything You Need for Successful Aquaculture
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Comprehensive tools and resources to help you manage your fish farm efficiently and profitably.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <Link key={index} href={feature.href}>
              <Card className="card-hover h-full border-0 shadow-md hover:shadow-xl cursor-pointer">
                <CardContent className="p-6">
                  <div className={`w-12 h-12 rounded-xl ${feature.color} flex items-center justify-center mb-4`}>
                    <feature.icon className="w-6 h-6" />
                  </div>
                  <h3 className="text-lg font-semibold text-foreground mb-2">{feature.title}</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">{feature.description}</p>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      </div>
    </section>
  )
}
