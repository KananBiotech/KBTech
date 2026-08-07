"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card"
import { Badge } from "../components/ui/badge"
import { Button } from "../components/ui/button"
import { Snowflake, Sun, CloudRain, AlertTriangle, ArrowRight, Loader2, Sparkles } from "lucide-react"

export function SeasonalDiseases() {
  const [currentSeason, setCurrentSeason] = useState("")
  const [diseases, setDiseases] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchAdvice = async () => {
    setLoading(true)
    setError(null)
    try {
      const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${baseUrl}/api/ai/seasonal-advice/`);
      if (!response.ok) throw new Error("Failed to fetch seasonal advice");

      const data = await response.json();
      if (data.diseases) {
        setDiseases(data.diseases);
        setCurrentSeason(data.season.toLowerCase());
      } else {
        throw new Error("Invalid data format from AI");
      }
    } catch (err) {
      console.error("Error fetching seasonal advice:", err);
      setError("Unable to load real-time AI suggestions. Showing general info.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchAdvice()
  }, [])

  const getSeasonIcon = (season) => {
    switch(season) {
      case 'winter': return <Snowflake className="w-4 h-4 text-primary" />;
      case 'summer': return <Sun className="w-4 h-4 text-amber-500" />;
      case 'monsoon': return <CloudRain className="w-4 h-4 text-blue-500" />;
      default: return <Sparkles className="w-4 h-4 text-primary" />;
    }
  }

  return (
    <section className="py-20 bg-muted/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 bg-primary/10 rounded-full px-4 py-2 mb-4">
            {getSeasonIcon(currentSeason)}
            <span className="text-sm font-medium text-primary uppercase tracking-wider">
              {currentSeason || "Current"} Season AI Insight
            </span>
          </div>
          {/* Requested Title */}
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4 text-balance">
            Seasonal Fish Diseases
          </h2>
          {/* Requested Subtitle */}
          <p className="text-muted-foreground max-w-2xl mx-auto text-lg">
            Stay informed about common fish diseases during the current season and protect your farm with our recommended solutions.
          </p>
        </div>

        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 bg-background/50 rounded-2xl border border-dashed border-border">
            <Loader2 className="w-10 h-10 animate-spin text-primary mb-4" />
            <p className="text-muted-foreground font-medium">Consulting KBTech RAG AI for today's advice...</p>
          </div>
        ) : error ? (
           <div className="text-center py-10 text-destructive bg-destructive/5 rounded-2xl border border-destructive/20">
             {error}
           </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {diseases.map((disease, index) => (
              <Card key={index} className="card-hover border-border/50 shadow-lg bg-card">
                <CardHeader>
                  <div className="flex items-start justify-between gap-4">
                    <CardTitle className="text-lg font-bold">{disease.name}</CardTitle>
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
                  <p className="text-sm text-muted-foreground italic border-l-2 border-primary/20 pl-3">
                    {disease.description}
                  </p>

                  <div className="bg-muted/30 p-3 rounded-lg">
                    <div className="flex items-center gap-2 text-sm font-semibold mb-2">
                      <AlertTriangle className="w-4 h-4 text-amber-500" />
                      Symptoms
                    </div>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      {disease.symptoms.map((symptom, i) => (
                        <li key={i} className="flex items-start gap-2">
                          <span className="w-1.5 h-1.5 rounded-full bg-primary mt-1.5 shrink-0" />
                          <span>{symptom}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="pt-4 border-t border-border">
                    <div className="text-sm font-bold text-foreground mb-1">Recommended Solution</div>
                    <div className="text-sm text-muted-foreground mb-3">{disease.prevention}</div>
                    <Link href="/products" className="text-sm text-primary hover:underline flex items-center gap-1 font-bold">
                      Order {disease.product || "KBTech Product"}
                      <ArrowRight className="w-3 h-3" />
                    </Link>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        <div className="text-center mt-12 flex items-center justify-center gap-4">
          <Button variant="outline" size="lg" onClick={fetchAdvice} disabled={loading} className="rounded-full">
            Refresh AI Advice
          </Button>
          <Link href="/diseases">
            <Button variant="default" size="lg" className="rounded-full">
              Full Disease Guide
              <ArrowRight className="ml-2 w-4 h-4" />
            </Button>
          </Link>
        </div>
      </div>
    </section>
  )
}
