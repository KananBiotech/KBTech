"use client"

import { Navbar } from "@/components/navbar"
import { Footer } from "@/components/footer"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { User, Mail, Phone, MapPin } from "lucide-react"

export default function AccountPage() {
  return (
    <main className="min-h-screen bg-background">
      <Navbar />

      <div className="pt-24 pb-12 hero-gradient text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3 mb-4">
            <User className="w-8 h-8" />
            <h1 className="text-4xl md:text-5xl font-bold">My Account</h1>
          </div>
          <p className="text-white/80 max-w-2xl">
            View your profile and account details.
          </p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Card className="border-0 shadow-lg">
          <CardHeader>
            <CardTitle>Profile Details</CardTitle>
            <CardDescription>Account information linked to your login.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                <User className="w-5 h-5 text-primary" />
              </div>
              <div>
                <p className="font-medium">Kanan Biotech User</p>
                <Badge variant="secondary">Member</Badge>
              </div>
            </div>

            <div className="grid sm:grid-cols-2 gap-4">
              <div className="rounded-lg border p-4">
                <p className="text-sm text-muted-foreground flex items-center gap-2">
                  <Mail className="w-4 h-4" /> Email
                </p>
                <p className="mt-1 font-medium">Available after profile sync</p>
              </div>
              <div className="rounded-lg border p-4">
                <p className="text-sm text-muted-foreground flex items-center gap-2">
                  <Phone className="w-4 h-4" /> Phone
                </p>
                <p className="mt-1 font-medium">Available after profile sync</p>
              </div>
              <div className="rounded-lg border p-4 sm:col-span-2">
                <p className="text-sm text-muted-foreground flex items-center gap-2">
                  <MapPin className="w-4 h-4" /> State
                </p>
                <p className="mt-1 font-medium">Available after profile sync</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Footer />
    </main>
  )
}
