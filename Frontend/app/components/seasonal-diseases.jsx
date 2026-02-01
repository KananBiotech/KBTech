"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card"
import { Badge } from "../components/ui/badge"
import { Button } from "../components/ui/button"
import { Snowflake, Sun, AlertTriangle, ArrowRight } from "lucide-react"

const winterDiseases = [
  {
    name: "Saprolegniasis (Winter Fungus)",
    description: "Fungal infection causing cotton-like growth on fish skin and gills.",
    severity: "High",
    symptoms: ["White cotton-like patches", "Lethargy", "Loss of appetite"],
    prevention: "Maintain water quality, avoid overcrowding",
    product: "AquaGuard Anti-Fungal",
  },
  {
    name: "Columnaris Disease",
    description: "Bacterial infection more prevalent in cold water conditions.",
    severity: "Medium",
    symptoms: ["White spots on mouth", "Fin erosion", "Gill damage"],
    prevention: "Regular water changes, proper nutrition",
    product: "BioShield Bacterial Defense",
  },
  {
    name: "Ich (White Spot Disease)",
    description: "Parasitic infection causing white spots during temperature fluctuations.",
    severity: "High",
    symptoms: ["White spots on body", "Scratching against surfaces", "Rapid breathing"],
    prevention: "Stable water temperature, quarantine new fish",
    product: "IchClear Treatment",
  },
]

const summerDiseases = [
  {
    name: "Bacterial Gill Disease",
    description: "Common in warm water with low oxygen levels.",
    severity: "High",
    symptoms: ["Swollen gills", "Gasping at surface", "Reduced feeding"],
    prevention: "Maintain aeration, avoid overfeeding",
    product: "GillCare Plus",
  },
  {
    name: "Epizootic Ulcerative Syndrome",
    description: "Serious fungal disease in warm monsoon conditions.",
    severity: "Critical",
    symptoms: ["Red ulcers on body", "Deep lesions", "Scale loss"],
    prevention: "Good pond hygiene, lime treatment",
    product: "UlcerHeal Advanced",
  },
  {
    name: "Argulosis (Fish Lice)",
    description: "Parasitic infestation common in summer months.",
    severity: "Medium",
    symptoms: ["Visible parasites", "Restlessness", "Bloody spots"],
    prevention: "Regular pond screening, avoid wild fish",
    product: "ParaKill Solution",
  },
]

export function SeasonalDiseases() {
  const [currentSeason, setCurrentSeason] = useState("winter")

  useEffect(() => {
    const month = new Date().getMonth()
    if (month >= 3 && month <= 9) {
      setCurrentSeason("summer")
    } else {
      setCurrentSeason("winter")
    }
  }, [])

  const diseases = currentSeason === "winter" ? winterDiseases : summerDiseases

  return (
    <section className="py-20 bg-muted">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 bg-primary/10 rounded-full px-4 py-2 mb-4">
            {currentSeason === "winter" ? (
              <Snowflake className="w-4 h-4 text-primary" />
            ) : (
              <Sun className="w-4 h-4 text-amber-500" />
            )}
            <span className="text-sm font-medium text-primary">
              {currentSeason === "winter" ? "Winter Season" : "Summer Season"} Alert
            </span>
          </div>
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4 text-balance">Seasonal Fish Diseases</h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Stay informed about common fish diseases during the current season and protect your farm with our
            recommended solutions.
          </p>
        </div>

        <div className="flex justify-center gap-4 mb-8">
          <Button
            variant={currentSeason === "winter" ? "default" : "outline"}
            onClick={() => setCurrentSeason("winter")}
            className="gap-2"
          >
            <Snowflake className="w-4 h-4" />
            Winter Diseases
          </Button>
          <Button
            variant={currentSeason === "summer" ? "default" : "outline"}
            onClick={() => setCurrentSeason("summer")}
            className="gap-2"
          >
            <Sun className="w-4 h-4" />
            Summer Diseases
          </Button>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {diseases.map((disease, index) => (
            <Card key={index} className="card-hover border-0 shadow-lg">
              <CardHeader>
                <div className="flex items-start justify-between gap-4">
                  <CardTitle className="text-lg">{disease.name}</CardTitle>
                  <Badge
                    variant={
                      disease.severity === "Critical"
                        ? "destructive"
                        : disease.severity === "High"
                          ? "default"
                          : "secondary"
                    }
                  >
                    {disease.severity}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <p className="text-sm text-muted-foreground">{disease.description}</p>

                <div>
                  <div className="flex items-center gap-2 text-sm font-medium mb-2">
                    <AlertTriangle className="w-4 h-4 text-amber-500" />
                    Symptoms
                  </div>
                  <ul className="text-sm text-muted-foreground space-y-1">
                    {disease.symptoms.map((symptom, i) => (
                      <li key={i} className="flex items-center gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-primary" />
                        {symptom}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="pt-4 border-t border-border">
                  <div className="text-sm font-medium mb-1">Recommended Product</div>
                  <Link href="/products" className="text-sm text-primary hover:underline flex items-center gap-1">
                    {disease.product}
                    <ArrowRight className="w-3 h-3" />
                  </Link>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="text-center mt-10">
          <Link href="/diseases">
            <Button variant="outline" size="lg">
              View All Diseases Guide
              <ArrowRight className="ml-2 w-4 h-4" />
            </Button>
          </Link>
        </div>
      </div>
    </section>
  )
}
