"use client"

import { Navbar } from "@/components/navbar"
import { Footer } from "@/components/footer"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Clock, Activity } from "lucide-react"

const recentActivity = [
  { id: 1, label: "Signed in", time: "Just now", status: "success" },
  { id: 2, label: "Visited dashboard", time: "Today", status: "info" },
  { id: 3, label: "Opened feed calculator", time: "Today", status: "info" },
]

export default function HistoryPage() {
  return (
    <main className="min-h-screen bg-background">
      <Navbar />

      <div className="pt-24 pb-12 hero-gradient text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3 mb-4">
            <Clock className="w-8 h-8" />
            <h1 className="text-4xl md:text-5xl font-bold">History</h1>
          </div>
          <p className="text-white/80 max-w-2xl">
            See your recent account activity.
          </p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Card className="border-0 shadow-lg">
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
            <CardDescription>Your latest actions in the platform.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {recentActivity.map((item) => (
              <div key={item.id} className="rounded-lg border p-4 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-full bg-primary/10 flex items-center justify-center">
                    <Activity className="w-4 h-4 text-primary" />
                  </div>
                  <div>
                    <p className="font-medium">{item.label}</p>
                    <p className="text-sm text-muted-foreground">{item.time}</p>
                  </div>
                </div>
                <Badge variant={item.status === "success" ? "default" : "secondary"}>
                  {item.status}
                </Badge>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      <Footer />
    </main>
  )
}
