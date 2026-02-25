"use client"

import Link from "next/link"
import { ArrowLeft, Fish, Mail } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card"
import { Button } from "../components/ui/button"
import { Input } from "../components/ui/input"
import { Label } from "../components/ui/label"

export default function ForgotPasswordPage() {
  return (
    <main className="min-h-screen flex">
      <div className="hidden lg:flex lg:w-1/2 hero-gradient relative">
        <div className="absolute inset-0 flex flex-col justify-center px-12 text-white">
          <Link href="/" className="absolute top-8 left-8 flex items-center gap-2 text-white/80 hover:text-white">
            <ArrowLeft className="w-4 h-4" />
            Back to Home
          </Link>

          <div className="flex items-center gap-3 mb-8">
            <div className="w-14 h-14 rounded-xl bg-white/20 flex items-center justify-center">
              <Fish className="w-8 h-8" />
            </div>
            <div>
              <div className="text-2xl font-bold">Kanan Biotech</div>
              <div className="text-sm text-white/70">Pvt. Ltd</div>
            </div>
          </div>

          <h1 className="text-4xl font-bold mb-4 text-balance">Reset Your Password</h1>
          <p className="text-white/80 text-lg">
            Enter your registered email and we will help you recover your account.
          </p>
        </div>
      </div>

      <div className="flex-1 flex items-center justify-center p-4 sm:p-8 bg-background">
        <div className="w-full max-w-md">
          <Link href="/login" className="lg:hidden flex items-center gap-2 text-muted-foreground mb-8 hover:text-foreground">
            <ArrowLeft className="w-4 h-4" />
            Back to Login
          </Link>

          <Card className="border-0 shadow-lg">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl">Forgot Password</CardTitle>
              <CardDescription>We will send a reset link to your email</CardDescription>
            </CardHeader>
            <CardContent>
              <form className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="email">Email Address</Label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                    <Input id="email" type="email" name="email" className="pl-10" placeholder="john@example.com" required />
                  </div>
                </div>
                <Button type="submit" className="w-full" size="lg" disabled>
                  Reset Link (Coming Soon)
                </Button>
              </form>

              <p className="text-center text-sm text-muted-foreground mt-6">
                Remembered your password?{" "}
                <Link href="/login" className="text-primary font-medium hover:underline">
                  Sign in
                </Link>
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </main>
  )
}
