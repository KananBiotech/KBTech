"use client"

import { useState } from "react"
import { Navbar } from "@/components/navbar"
import { Footer } from "@/components/footer"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Search,
  AlertTriangle,
  Snowflake,
  Sun,
  Thermometer,
  Shield,
  Pill,
  ChevronDown,
  ChevronUp,
  ArrowRight,
} from "lucide-react"
import Link from "next/link"

const diseases = {
  winter: [
    {
      id: 1,
      name: "Saprolegniasis (Winter Fungus)",
      description:
        "A fungal infection that causes cotton-like growth on fish skin, fins, and gills. Most common during cold weather when fish immunity is compromised.",
      severity: "High",
      causes: ["Low water temperature", "Physical injuries", "Poor water quality", "Stress from handling"],
      symptoms: [
        "White cotton-like patches on body",
        "Gray/brown fuzzy growth on fins",
        "Lethargy and loss of appetite",
        "Difficulty swimming",
        "Gill damage in severe cases",
      ],
      prevention: [
        "Maintain water quality parameters",
        "Avoid overcrowding",
        "Handle fish carefully to prevent injuries",
        "Maintain stable water temperature",
        "Regular health monitoring",
      ],
      treatment: [
        "Salt bath treatment (2-3% solution)",
        "Anti-fungal medication",
        "Remove affected fish for treatment",
        "Improve water quality",
      ],
      recommendedProducts: ["FungoCure Anti-Fungal", "BioShield Immunity Booster"],
    },
    {
      id: 2,
      name: "Columnaris Disease",
      description:
        "Bacterial infection caused by Flavobacterium columnare. More prevalent during temperature fluctuations in winter months.",
      severity: "Medium",
      causes: ["Temperature stress", "Poor nutrition", "High organic load", "Crowded conditions"],
      symptoms: [
        "White patches on mouth (cotton mouth)",
        "Fin erosion and fraying",
        "Saddle-shaped lesions on back",
        "Gill necrosis",
        "Rapid breathing",
      ],
      prevention: [
        "Maintain stable water temperature",
        "Proper nutrition with vitamins",
        "Regular water changes",
        "Quarantine new fish",
      ],
      treatment: [
        "Antibiotic treatment",
        "Salt treatment for mild cases",
        "Improve water quality",
        "Reduce stocking density",
      ],
      recommendedProducts: ["GillCare Treatment", "ProBiotic Plus"],
    },
    {
      id: 3,
      name: "Ich (White Spot Disease)",
      description:
        "Caused by the parasite Ichthyophthirius multifiliis. Common during temperature fluctuations in winter.",
      severity: "High",
      causes: ["Sudden temperature changes", "Stressed fish", "Introduction of infected fish", "Poor water quality"],
      symptoms: [
        "Small white spots on body and fins",
        "Scratching against objects",
        "Clamped fins",
        "Rapid gill movement",
        "Lethargy",
      ],
      prevention: [
        "Quarantine new fish for 2 weeks",
        "Maintain stable temperature",
        "Keep fish stress-free",
        "Regular water testing",
      ],
      treatment: [
        "Raise water temperature gradually",
        "Salt treatment",
        "Commercial ich medication",
        "Treat entire pond",
      ],
      recommendedProducts: ["BioShield Immunity Booster", "PondClear Water Treatment"],
    },
    {
      id: 4,
      name: "Dropsy",
      description:
        "Internal bacterial infection causing fluid buildup and scale protrusion. More common during cold stress.",
      severity: "Critical",
      causes: [
        "Bacterial infection (Aeromonas)",
        "Compromised immune system",
        "Poor water quality",
        "Internal organ damage",
      ],
      symptoms: [
        "Swollen belly",
        "Scales standing out (pine cone appearance)",
        "Lethargy",
        "Loss of appetite",
        "Pale gills",
      ],
      prevention: [
        "Maintain excellent water quality",
        "Balanced nutrition",
        "Reduce stress factors",
        "Regular health checks",
      ],
      treatment: ["Isolate affected fish", "Antibiotic treatment", "Epsom salt bath", "Often difficult to treat"],
      recommendedProducts: ["GillCare Treatment", "BioShield Immunity Booster"],
    },
  ],
  summer: [
    {
      id: 5,
      name: "Bacterial Gill Disease",
      description: "Common in warm water with low oxygen levels. Affects the gill tissue causing respiratory distress.",
      severity: "High",
      causes: ["High water temperature", "Low dissolved oxygen", "High ammonia levels", "Overcrowding"],
      symptoms: [
        "Swollen, discolored gills",
        "Gasping at water surface",
        "Reduced feeding",
        "Lethargy",
        "Excess mucus production",
      ],
      prevention: [
        "Maintain proper aeration",
        "Avoid overfeeding",
        "Regular water quality monitoring",
        "Proper stocking density",
      ],
      treatment: [
        "Improve oxygen levels immediately",
        "Reduce feeding",
        "Antibiotic treatment",
        "Water quality correction",
      ],
      recommendedProducts: ["GillCare Treatment", "OxyBoost Aerator Tablets"],
    },
    {
      id: 6,
      name: "Epizootic Ulcerative Syndrome (EUS)",
      description: "Serious fungal disease common during warm monsoon conditions. Causes deep ulcerative lesions.",
      severity: "Critical",
      causes: ["Aphanomyces fungus", "Monsoon flooding", "Contaminated water sources", "Wounds from parasites"],
      symptoms: ["Red ulcers on body", "Deep necrotic lesions", "Scale loss", "Hemorrhaging", "Secondary infections"],
      prevention: [
        "Good pond hygiene",
        "Lime treatment of ponds",
        "Avoid wild fish introduction",
        "Proper water source management",
      ],
      treatment: [
        "Lime application to pond",
        "Potassium permanganate treatment",
        "Remove severely affected fish",
        "Disinfect equipment",
      ],
      recommendedProducts: ["FungoCure Anti-Fungal", "PondClear Water Treatment"],
    },
    {
      id: 7,
      name: "Argulosis (Fish Lice)",
      description: "Parasitic infestation by Argulus species. Common in summer months in outdoor ponds.",
      severity: "Medium",
      causes: [
        "Introduction of wild fish",
        "Contaminated water",
        "Poor pond management",
        "Warm temperatures favor reproduction",
      ],
      symptoms: [
        "Visible flat parasites on body",
        "Restlessness and jumping",
        "Bloody spots at attachment sites",
        "Rubbing against objects",
        "Secondary infections",
      ],
      prevention: [
        "Screen incoming water",
        "Quarantine new fish",
        "Regular visual inspection",
        "Pond drying between cycles",
      ],
      treatment: ["Manual removal of parasites", "Organophosphate treatment", "Lime treatment", "Treat entire pond"],
      recommendedProducts: ["BioShield Immunity Booster", "PondClear Water Treatment"],
    },
    {
      id: 8,
      name: "Vibriosis",
      description: "Bacterial disease caused by Vibrio species. More common in brackish water during summer.",
      severity: "High",
      causes: ["High salinity fluctuations", "Warm water temperatures", "Stress from handling", "Poor water quality"],
      symptoms: [
        "Hemorrhaging on body",
        "Skin ulcers",
        "Swollen intestines",
        "Dark coloration",
        "Lethargy and anorexia",
      ],
      prevention: [
        "Stable salinity levels",
        "Proper water management",
        "Reduce handling stress",
        "Vaccination programs",
      ],
      treatment: ["Antibiotic therapy", "Improve water quality", "Reduce stocking density", "Supportive nutrition"],
      recommendedProducts: ["GillCare Treatment", "ProBiotic Plus"],
    },
  ],
  yearRound: [
    {
      id: 9,
      name: "Ammonia Poisoning",
      description: "Not a disease but a common water quality issue that affects fish health year-round.",
      severity: "High",
      causes: ["Overfeeding", "Overstocking", "Poor filtration", "Decomposing organic matter"],
      symptoms: [
        "Gasping at surface",
        "Red or inflamed gills",
        "Lethargy",
        "Loss of appetite",
        "Death in severe cases",
      ],
      prevention: ["Regular water testing", "Proper feeding amounts", "Adequate filtration", "Regular water changes"],
      treatment: ["Immediate water change", "Stop feeding", "Add beneficial bacteria", "Improve aeration"],
      recommendedProducts: ["PondClear Water Treatment", "OxyBoost Aerator Tablets"],
    },
    {
      id: 10,
      name: "Nutritional Deficiencies",
      description: "Various health issues caused by improper or inadequate nutrition affecting growth and immunity.",
      severity: "Medium",
      causes: ["Poor quality feed", "Imbalanced diet", "Inadequate feeding", "Storage damaged feed"],
      symptoms: [
        "Poor growth rate",
        "Deformities",
        "Pale coloration",
        "Weak immunity",
        "Increased disease susceptibility",
      ],
      prevention: [
        "Use quality commercial feed",
        "Proper storage of feed",
        "Balanced nutrition program",
        "Regular supplementation",
      ],
      treatment: ["Upgrade feed quality", "Add vitamin supplements", "Adjust feeding schedule", "Monitor growth rates"],
      recommendedProducts: ["AquaGrow Premium Feed", "BioShield Immunity Booster"],
    },
  ],
}

const speciesGuides = [
  {
    id: 101,
    fishName: "Shrimp",
    scientificName: "Penaeus vannamei / Penaeus monodon",
    commonDisease: "White Spot Syndrome (WSSV)",
    symptoms: ["White spots on shell", "Reduced feeding", "Weak movement", "Sudden heavy mortality"],
    causes: ["Infected seed", "Poor biosecurity", "Stress from salinity/temperature fluctuation"],
    solve: [
      "Immediately isolate affected pond and stop water exchange with other ponds",
      "Disinfect equipment and entry points with approved sanitizers",
      "Improve aeration and stabilize water quality (pH, salinity, ammonia)",
      "Use SPF seed and strict biosecurity for next cycle",
    ],
    prevention: ["Stock disease-free seed", "Quarantine new seed", "Regular PCR screening", "Maintain pond hygiene"],
  },
  {
    id: 102,
    fishName: "Scampi",
    scientificName: "Macrobrachium rosenbergii",
    commonDisease: "Shell Disease / Bacterial Lesions",
    symptoms: ["Brown-black spots on shell", "Slow growth", "Weakness", "Poor molting"],
    causes: ["Organic waste buildup", "High stocking density", "Poor water quality"],
    solve: [
      "Reduce organic load through siphoning and water management",
      "Apply pond probiotics as per recommendation",
      "Reduce stocking stress and maintain dissolved oxygen",
      "Provide balanced mineral and vitamin support for molting",
    ],
    prevention: ["Regular bottom cleaning", "Proper feed management", "Avoid overstocking", "Routine water testing"],
  },
  {
    id: 103,
    fishName: "Pangasius (Pangasias)",
    scientificName: "Pangasianodon hypophthalmus",
    commonDisease: "Motile Aeromonas Septicemia",
    symptoms: ["Red patches on body", "Ulcers", "Abdominal swelling", "Erratic swimming"],
    causes: ["Aeromonas infection", "Poor water quality", "Handling stress"],
    solve: [
      "Separate severely affected fish",
      "Correct ammonia/nitrite and increase aeration",
      "Use veterinarian-guided antibacterial treatment",
      "Support recovery with high-quality feed and immunostimulants",
    ],
    prevention: ["Maintain clean water", "Minimize netting stress", "Use quality seed", "Periodic health checks"],
  },
  {
    id: 104,
    fishName: "Rohu (Rahu Fish)",
    scientificName: "Labeo rohita",
    commonDisease: "Argulosis (Fish Lice)",
    symptoms: ["Rubbing against pond wall", "Visible parasites on skin", "Red wounds", "Reduced feeding"],
    causes: ["Parasitic infestation", "Entry of wild carrier fish", "Poor pond hygiene"],
    solve: [
      "Treat whole pond under expert supervision for ectoparasites",
      "Improve pond sanitation and remove debris",
      "Apply lime where recommended and maintain pH balance",
      "Monitor fish for secondary bacterial infection",
    ],
    prevention: ["Screen inlet water", "Quarantine new stock", "Regular parasite monitoring", "Dry pond between cycles"],
  },
  {
    id: 105,
    fishName: "Catla (Katla Fish)",
    scientificName: "Catla catla",
    commonDisease: "Gill Rot",
    symptoms: ["Rapid breathing", "Gasping at surface", "Pale/eroded gills", "Lethargy"],
    causes: ["High organic load", "Low dissolved oxygen", "Bacterial/fungal gill infection"],
    solve: [
      "Increase aeration immediately",
      "Reduce feeding and remove excess waste",
      "Apply suitable gill-care treatment as advised",
      "Maintain optimum water exchange and plankton balance",
    ],
    prevention: ["Avoid overfeeding", "Keep DO at safe level", "Regular gill checks", "Pond bottom management"],
  },
  {
    id: 106,
    fishName: "Mrigal Fish",
    scientificName: "Cirrhinus mrigala",
    commonDisease: "EUS (Epizootic Ulcerative Syndrome)",
    symptoms: ["Red ulcers", "Deep wounds", "Scale loss", "Weak swimming"],
    causes: ["Fungal invasion", "Monsoon stress", "Contaminated water"],
    solve: [
      "Isolate severely affected fish",
      "Improve pond sanitation and apply liming program",
      "Use antifungal support and secondary infection control as advised",
      "Strengthen fish immunity with quality nutrition",
    ],
    prevention: ["Pond preparation before stocking", "Disinfect equipment", "Prevent sudden water quality swings"],
  },
  {
    id: 107,
    fishName: "Grass Carp (Grash carp)",
    scientificName: "Ctenopharyngodon idella",
    commonDisease: "Ich (White Spot Disease)",
    symptoms: ["White pinhead spots", "Flashing/rubbing", "Fin clamping", "Loss of appetite"],
    causes: ["Protozoan parasite", "Stress and temperature fluctuation"],
    solve: [
      "Treat pond for protozoan infestation in full cycle",
      "Stabilize water temperature where possible",
      "Improve water hygiene and reduce crowding",
      "Continue observation after treatment to prevent relapse",
    ],
    prevention: ["Quarantine new fish", "Stable pond conditions", "Regular health inspection"],
  },
  {
    id: 108,
    fishName: "Amur Carp",
    scientificName: "Cyprinus rubrofuscus (Amur strain)",
    commonDisease: "Koi Herpes-like Viral Outbreak",
    symptoms: ["Gill necrosis", "Sunken eyes", "Skin lesions", "Sudden deaths"],
    causes: ["Viral transmission", "Carrier fish introduction", "Temperature stress"],
    solve: [
      "Strictly isolate affected stock and restrict movement",
      "Disinfect nets, tanks, and transport units",
      "Maintain optimal water quality to reduce stress load",
      "Use certified healthy seed and avoid mixed-source stocking",
    ],
    prevention: ["Buy certified seed", "Quarantine new batches", "Separate tools per pond", "Routine surveillance"],
  },
  {
    id: 109,
    fishName: "Silver Carp",
    scientificName: "Hypophthalmichthys molitrix",
    commonDisease: "Bacterial Hemorrhagic Septicemia",
    symptoms: ["Red hemorrhagic patches", "Fin base bleeding", "Lethargy", "Poor feeding"],
    causes: ["Bacterial load in poor water", "High stress", "Abrupt environmental change"],
    solve: [
      "Improve water quality and increase dissolved oxygen",
      "Remove dead/weak fish quickly",
      "Apply expert-guided antibacterial treatment protocol",
      "Support fish with high digestibility feed and vitamins",
    ],
    prevention: ["Routine pond water checks", "Balanced stocking", "Stress-free handling"],
  },
  {
    id: 110,
    fishName: "Mixed Carp Ponds (Rohu, Catla, Mrigal, Grass, Silver)",
    scientificName: "Polyculture System",
    commonDisease: "Ammonia Toxicity and Secondary Infections",
    symptoms: ["Surface gasping", "Gill irritation", "Slow growth", "Frequent opportunistic diseases"],
    causes: ["Overfeeding", "High stocking density", "Poor sludge management"],
    solve: [
      "Partial water exchange and strong aeration",
      "Cut feed temporarily and restart with corrected ration",
      "Apply probiotics and improve bottom management",
      "Monitor ammonia, nitrite, pH daily until stable",
    ],
    prevention: ["Feed budgeting", "Regular siphoning/desludging", "Water quality logs", "Periodic health audit"],
  },
]

export default function DiseasesPage() {
  const [searchQuery, setSearchQuery] = useState("")
  const [expandedDisease, setExpandedDisease] = useState(null)
  const [activeTab, setActiveTab] = useState("winter")

  const currentMonth = new Date().getMonth()
  const isWinterSeason = currentMonth < 3 || currentMonth > 9

  const filterDiseases = (diseaseList) => {
    if (!searchQuery) return diseaseList
    return diseaseList.filter(
      (disease) =>
        disease.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        disease.description.toLowerCase().includes(searchQuery.toLowerCase()),
    )
  }

  const filteredSpeciesGuides = speciesGuides.filter((guide) => {
    if (!searchQuery) return true
    const q = searchQuery.toLowerCase()
    return (
      guide.fishName.toLowerCase().includes(q) ||
      guide.commonDisease.toLowerCase().includes(q) ||
      guide.description?.toLowerCase?.().includes?.(q)
    )
  })

  const DiseaseCard = ({ disease }) => {
    const isExpanded = expandedDisease === disease.id

    return (
      <Card className="border-0 shadow-md overflow-hidden">
        <CardHeader
          className="cursor-pointer hover:bg-muted/50 transition-colors"
          onClick={() => setExpandedDisease(isExpanded ? null : disease.id)}
        >
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
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
              <p className="text-sm text-muted-foreground">{disease.description}</p>
            </div>
            {isExpanded ? (
              <ChevronUp className="w-5 h-5 text-muted-foreground" />
            ) : (
              <ChevronDown className="w-5 h-5 text-muted-foreground" />
            )}
          </div>
        </CardHeader>

        {isExpanded && (
          <CardContent className="border-t border-border pt-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <div className="mb-4">
                  <h4 className="font-semibold text-foreground mb-2 flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4 text-amber-500" />
                    Causes
                  </h4>
                  <ul className="space-y-1">
                    {disease.causes.map((cause, i) => (
                      <li key={i} className="text-sm text-muted-foreground flex items-center gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-amber-500" />
                        {cause}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="mb-4">
                  <h4 className="font-semibold text-foreground mb-2 flex items-center gap-2">
                    <Thermometer className="w-4 h-4 text-rose-500" />
                    Symptoms
                  </h4>
                  <ul className="space-y-1">
                    {disease.symptoms.map((symptom, i) => (
                      <li key={i} className="text-sm text-muted-foreground flex items-center gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-rose-500" />
                        {symptom}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <div>
                <div className="mb-4">
                  <h4 className="font-semibold text-foreground mb-2 flex items-center gap-2">
                    <Shield className="w-4 h-4 text-secondary" />
                    Prevention
                  </h4>
                  <ul className="space-y-1">
                    {disease.prevention.map((item, i) => (
                      <li key={i} className="text-sm text-muted-foreground flex items-center gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-secondary" />
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="mb-4">
                  <h4 className="font-semibold text-foreground mb-2 flex items-center gap-2">
                    <Pill className="w-4 h-4 text-primary" />
                    Treatment
                  </h4>
                  <ul className="space-y-1">
                    {disease.treatment.map((item, i) => (
                      <li key={i} className="text-sm text-muted-foreground flex items-center gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-primary" />
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            <div className="mt-4 pt-4 border-t border-border">
              <h4 className="font-semibold text-foreground mb-3">Recommended Products</h4>
              <div className="flex flex-wrap gap-2">
                {disease.recommendedProducts.map((product, i) => (
                  <Link key={i} href="/products">
                    <Badge variant="outline" className="cursor-pointer hover:bg-primary hover:text-primary-foreground">
                      {product}
                      <ArrowRight className="ml-1 w-3 h-3" />
                    </Badge>
                  </Link>
                ))}
              </div>
            </div>
          </CardContent>
        )}
      </Card>
    )
  }

  const SpeciesCard = ({ guide }) => {
    return (
      <Card className="border-0 shadow-md overflow-hidden">
        <CardHeader className="bg-muted/30">
          <div className="flex items-center justify-between gap-3">
            <div>
              <CardTitle className="text-lg">{guide.fishName}</CardTitle>
              <p className="text-sm text-muted-foreground">{guide.scientificName}</p>
            </div>
            <Badge variant="secondary">Species Guide</Badge>
          </div>
          <p className="text-sm mt-3">
            <span className="font-semibold">Common Disease: </span>
            {guide.commonDisease}
          </p>
        </CardHeader>
        <CardContent className="pt-6">
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-semibold text-foreground mb-2 flex items-center gap-2">
                <Thermometer className="w-4 h-4 text-rose-500" />
                Symptoms
              </h4>
              <ul className="space-y-1 mb-5">
                {guide.symptoms.map((item, i) => (
                  <li key={i} className="text-sm text-muted-foreground flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-rose-500" />
                    {item}
                  </li>
                ))}
              </ul>

              <h4 className="font-semibold text-foreground mb-2 flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-amber-500" />
                Causes
              </h4>
              <ul className="space-y-1">
                {guide.causes.map((item, i) => (
                  <li key={i} className="text-sm text-muted-foreground flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-amber-500" />
                    {item}
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h4 className="font-semibold text-foreground mb-2 flex items-center gap-2">
                <Pill className="w-4 h-4 text-primary" />
                How To Solve
              </h4>
              <ul className="space-y-1 mb-5">
                {guide.solve.map((item, i) => (
                  <li key={i} className="text-sm text-muted-foreground flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-primary" />
                    {item}
                  </li>
                ))}
              </ul>

              <h4 className="font-semibold text-foreground mb-2 flex items-center gap-2">
                <Shield className="w-4 h-4 text-secondary" />
                Prevention
              </h4>
              <ul className="space-y-1">
                {guide.prevention.map((item, i) => (
                  <li key={i} className="text-sm text-muted-foreground flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-secondary" />
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <main className="min-h-screen bg-background">
      <Navbar />

      <div className="pt-24 pb-12 hero-gradient text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-2 mb-4">
            {isWinterSeason ? <Snowflake className="w-6 h-6" /> : <Sun className="w-6 h-6" />}
            <Badge variant="secondary" className="bg-white/20 text-white">
              {isWinterSeason ? "Winter Season" : "Summer Season"} Guide
            </Badge>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Fish Disease Guide</h1>
          <p className="text-white/80 max-w-2xl">
            Comprehensive guide to identifying, preventing, and treating common fish diseases. Stay informed and protect
            your farm.
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="relative mb-8">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
          <Input
            placeholder="Search diseases..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 max-w-md"
          />
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="mb-6">
            <TabsTrigger value="winter" className="gap-2">
              <Snowflake className="w-4 h-4" />
              Winter Diseases
            </TabsTrigger>
            <TabsTrigger value="summer" className="gap-2">
              <Sun className="w-4 h-4" />
              Summer Diseases
            </TabsTrigger>
            <TabsTrigger value="yearRound" className="gap-2">
              Year-Round Issues
            </TabsTrigger>
            <TabsTrigger value="species" className="gap-2">
              Species-Wise Guide
            </TabsTrigger>
          </TabsList>

          <TabsContent value="winter" className="space-y-4">
            {filterDiseases(diseases.winter).map((disease) => (
              <DiseaseCard key={disease.id} disease={disease} />
            ))}
          </TabsContent>

          <TabsContent value="summer" className="space-y-4">
            {filterDiseases(diseases.summer).map((disease) => (
              <DiseaseCard key={disease.id} disease={disease} />
            ))}
          </TabsContent>

          <TabsContent value="yearRound" className="space-y-4">
            {filterDiseases(diseases.yearRound).map((disease) => (
              <DiseaseCard key={disease.id} disease={disease} />
            ))}
          </TabsContent>

          <TabsContent value="species" className="space-y-4">
            {filteredSpeciesGuides.map((guide) => (
              <SpeciesCard key={guide.id} guide={guide} />
            ))}
          </TabsContent>
        </Tabs>
      </div>

      <Footer />
    </main>
  )
}
