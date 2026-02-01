"use client"
import React, { useActionState, useEffect, useState } from "react"
import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "../components/ui/card"
import { Button } from "../components/ui/button"
import { Input } from "../components/ui/input"
import { Label } from "../components/ui/label"
import { Checkbox } from "../components/ui/checkbox"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select"
import { Fish, Eye, EyeOff, ArrowLeft, Mail, Lock, User, Phone, MapPin } from "lucide-react"
import { type UserData } from "../types"
import { signup } from "../actions/auth"

export default function SignupPage() {
  const [showPassword, setShowPassword] = useState(false)
  const [formData, setFormData] = useState<UserData>({
    firstName: "",
    lastName: "",
    email: "",
    phone: "",
    state: "",
    password: "",
    confirmPassword: "",
    farmType: "",
  })
  const [acceptTerms, setAcceptTerms] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  const [state, action, pending] = useActionState(signup, undefined)

  useEffect(() => {
    console.log(formData)
  }, [formData])


  const handleChange = (field: keyof UserData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  // const handleSubmit = async (e: React.FormEvent) => {
  //     e.preventDefault()

  //     if (formData.password === formData.confirmPassword) {
  //         const res = await fetch("/api/auth/register", {
  //             method: "POST",
  //             body: JSON.stringify({
  //                 first_name: formData.firstName,
  //                 last_name: formData.lastName,
  //                 email: formData.email,
  //                 phone: formData.phone,
  //                 state: formData.state,
  //                 password: formData.password,
  //                 farm_type: formData.farmType,
  //             })
  //         })

  //         console.log(res)
  //     }
  // }

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

          <h1 className="text-4xl font-bold mb-4 text-balance">Join India's Leading Aquaculture Community</h1>
          <p className="text-white/80 text-lg mb-8">
            Create your free account and get access to tools, resources, and expert guidance to grow your fish farming
            business.
          </p>

          <div className="grid grid-cols-2 gap-6">
            {[
              { number: "10,000+", label: "Active Farmers" },
              { number: "500+", label: "Products Available" },
              { number: "15+", label: "Years Experience" },
              { number: "24/7", label: "Expert Support" },
            ].map((stat, index) => (
              <div key={index} className="bg-white/10 rounded-xl p-4">
                <div className="text-3xl font-bold">{stat.number}</div>
                <div className="text-sm text-white/70">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="flex-1 flex items-center justify-center p-4 sm:p-8 bg-background overflow-y-auto">
        <div className="w-full max-w-md py-8">
          <Link href="/" className="lg:hidden flex items-center gap-2 text-muted-foreground mb-8 hover:text-foreground">
            <ArrowLeft className="w-4 h-4" />
            Back to Home
          </Link>

          <div className="lg:hidden flex items-center gap-2 mb-8">
            <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center">
              <Fish className="w-6 h-6 text-primary-foreground" />
            </div>
            <div>
              <div className="font-bold text-foreground">Kanan Biotech</div>
              <div className="text-xs text-muted-foreground">Pvt. Ltd</div>
            </div>
          </div>

          <Card className="border-0 shadow-lg">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl">Create Account</CardTitle>
              <CardDescription>Start your journey with Kanan Biotech</CardDescription>
            </CardHeader>
            <CardContent>
              <form action={action} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="firstName">First Name</Label>
                    <div className="relative">
                      <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                      <input
                        id="firstName"
                        placeholder="John"
                        name="firstName"
                        // value={formData.firstName}
                        // onChange={(e) => handleChange("firstName", e.target.value)}
                        className="pl-10"
                        required
                      />
                      {state?.errors?.firstName && <p className="text-red-500 text-sm">{state.errors.firstName}</p>}
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="lastName">Last Name</Label>
                    <input
                      id="lastName"
                      placeholder="Doe"
                      name="lastName"
                      // value={formData.lastName}
                      // onChange={(e) => handleChange("lastName", e.target.value)}
                      required
                    />
                    {state?.errors?.lastName && <p className="text-red-500 text-sm">{state.errors.lastName}</p>}
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email">Email Address</Label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                    <input
                      id="email"
                      type="email"
                      placeholder="john@example.com"
                      name="email"
                      // value={formData.email}
                      // onChange={(e) => handleChange("email", e.target.value)}
                      className="pl-10"
                      required
                    />
                    {state?.errors?.email && <p className="text-red-500 text-sm">{state.errors.email}</p>}
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="phone">Phone Number</Label>
                  <div className="relative">
                    <Phone className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                    <input
                      id="phone"
                      type="tel"
                      placeholder="+91 98765 43210"
                      name="phone"
                      // value={formData.phone}
                      // onChange={(e) => handleChange("phone", e.target.value)}
                      className="pl-10"
                      required
                    />
                    {state?.errors?.phone && <p className="text-red-500 text-sm">{state.errors.phone}</p>}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="state">State</Label>

                    <div className="relative">
                      <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />

                      <select
                        id="state"
                        name="state"
                        defaultValue=""
                        required
                        className="w-full h-10 rounded-md border border-input bg-background pl-10 pr-3 text-sm"
                      >
                        <option value="" disabled>
                          Select
                        </option>
                        <option value="ap">Andhra Pradesh</option>
                        <option value="wb">West Bengal</option>
                        <option value="tn">Tamil Nadu</option>
                        <option value="odisha">Odisha</option>
                        <option value="gujarat">Gujarat</option>
                        <option value="karnataka">Karnataka</option>
                        <option value="kerala">Kerala</option>
                        <option value="maharashtra">Maharashtra</option>
                        <option value="other">Other</option>
                      </select>
                    </div>

                    {state?.errors?.state && (
                      <p className="text-red-500 text-sm">{state.errors.state}</p>
                    )}
                  </div>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="farmType">Farm Type</Label>

                  <select
                    id="farmType"
                    name="farmType"
                    required
                    defaultValue={'pond Culture'}
                    className="w-full h-10 rounded-md border border-input bg-background px-3 text-sm"
                  >
                    <option value="" disabled>
                      Select
                    </option>
                    <option value="pond">Pond Culture</option>
                    <option value="cage">Cage Culture</option>
                    <option value="tank">Tank Culture</option>
                    <option value="hatchery">Hatchery</option>
                    <option value="other">Other</option>
                  </select>

                  {state?.errors?.farmType && (
                    <p className="text-red-500 text-sm">{state.errors.farmType}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="password">Password</Label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                    <input
                      id="password"
                      type={showPassword ? "text" : "password"}
                      placeholder="Create a strong password"
                      name="password"
                      // value={formData.password}
                      // onChange={(e) => handleChange("password", e.target.value)}
                      className="pl-10 pr-10"
                      required
                    />
                    {state?.errors?.password && <p className="text-red-500 text-sm">{
                      state.errors.password.map((error) => (
                        <li key={error}>- {error}</li>
                      ))
                    }</p>}
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                    >
                      {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Must be at least 8 characters with a number and special character
                  </p>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="confirmPassword">Confirm Password</Label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                    <Input
                      id="confirmPassword"
                      type="password"
                      placeholder="Confirm your password"
                      name="confirmPassword"
                      // value={formData.confirmPassword}
                      // onChange={(e) => handleChange("confirmPassword", e.target.value)}
                      className="pl-10"
                      required
                    />
                  </div>
                </div>

                <div className="flex items-start space-x-2">
                  <Checkbox
                    id="terms"
                    checked={acceptTerms}
                    onCheckedChange={(checked) => setAcceptTerms(checked === true)}
                    className="mt-0.5"
                  />
                  <Label htmlFor="terms" className="text-sm font-normal text-muted-foreground cursor-pointer">
                    I agree to the{" "}
                    <Link href="#" className="text-primary hover:underline">
                      Terms of Service
                    </Link>{" "}
                    and{" "}
                    <Link href="#" className="text-primary hover:underline">
                      Privacy Policy
                    </Link>
                  </Label>
                </div>

                <Button type="submit" className="w-full" size="lg" disabled={isLoading || !acceptTerms || pending}>
                  {isLoading ? "Creating Account..." : "Create Account"}
                </Button>

                <div className="relative my-6">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t border-border" />
                  </div>
                  <div className="relative flex justify-center text-xs uppercase">
                    <span className="bg-card px-2 text-muted-foreground">Or sign up with</span>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <Button variant="outline" type="button" className="bg-transparent">
                    <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
                      <path
                        fill="currentColor"
                        d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                      />
                      <path
                        fill="currentColor"
                        d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                      />
                      <path
                        fill="currentColor"
                        d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                      />
                      <path
                        fill="currentColor"
                        d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                      />
                    </svg>
                    Google
                  </Button>
                  <Button variant="outline" type="button" className="bg-transparent">
                    <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.604-3.369-1.341-3.369-1.341-.454-1.155-1.11-1.462-1.11-1.462-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.836c.85.004 1.705.114 2.504.336 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.202 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.163 22 16.418 22 12c0-5.523-4.477-10-10-10z" />
                    </svg>
                    GitHub
                  </Button>
                </div>
              </form>

              <p className="text-center text-sm text-muted-foreground mt-6">
                Already have an account?{" "}
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
