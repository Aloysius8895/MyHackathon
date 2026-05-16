"use client";

import { useState } from "react";
import { ApiService } from "@/services/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Bot, Brain, ArrowLeft } from "lucide-react";
import Link from "next/link";
import { parseADKResponse } from "@/utils/parseADKResponse";
import { useSession } from "@/contexts/SessionContext";
import { TutorRecommendation } from "@/types/TutorRecommendation";
import BackgroundBlur from "@/components/ui/background-blur";
import { motion } from "@/components/ui/motion";

export default function PersonalTutor() {
  const { userId, sessionId } = useSession();
  const [result, setResult] = useState<TutorRecommendation | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const mockSummary = `
Student performance:
- Human Sciences: 480
- Natural Sciences: 620
- Math: 570
- Writing:
  comp1: 160
  comp2: 120
  comp3: 140
  comp4: 150
  comp5: 110
Common mistakes: textual cohesion, interpretation of graphs, organic chemistry
`;

  const handleGenerateRecommendation = async () => {
    setIsLoading(true);
    setResult(null);

    try {
      const payload = ApiService.createPayload(userId, sessionId, mockSummary);
      const response = await ApiService.runAgent(payload);
      const parsed = parseADKResponse<TutorRecommendation>(response.response);
      setResult(parsed);
    } catch (error) {
      console.error("Error generating tutor recommendation:", error);
      alert("Something went wrong. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      <div className="mx-auto px-4 py-8 relative z-10">
        <BackgroundBlur />

        {/* Navigation */}
        <div className="flex items-center justify-between mb-8">
          <Link href="/dashboard">
            <Button className="button-secondary flex items-center gap-2">
              <ArrowLeft className="h-4 w-4" />
              Back to Home
            </Button>
          </Link>
        </div>

        {/* Main Content */}
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-8"
          >
            {/* Hero */}
            <div className="text-center mb-12">
              <div className="inline-flex items-center justify-center px-4 py-2 mb-6 border border-white/10 rounded-full bg-white/5 backdrop-blur-sm">
                <Brain className="w-4 h-4 mr-2 text-green-400" />
                <span className="text-sm font-medium text-white/80">
                  Personalized AI Tutor
                </span>
              </div>

              <h1 className="text-4xl md:text-6xl font-bold tracking-tighter mb-6 text-white">
                Get Your
                <br />
                <span className="gradient-text">Study Plan</span>
              </h1>

              <p className="text-lg md:text-xl text-white/70 max-w-3xl mx-auto leading-relaxed">
                Based on your recent performance, we'll recommend what to review
                next.
              </p>

              <Button
                onClick={handleGenerateRecommendation}
                disabled={isLoading}
                className={`mt-8 px-6 py-4 rounded-xl text-lg font-semibold transition-all ${
                  isLoading
                    ? "bg-gray-600 text-gray-300 cursor-not-allowed"
                    : "button-primary hover:scale-[1.02]"
                }`}
              >
                {isLoading ? (
                  <>
                    <Bot className="w-5 h-5 mr-2 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Bot className="w-5 h-5 mr-2" />
                    Generate Personalized Plan
                  </>
                )}
              </Button>
            </div>

            {/* Result */}
            {result && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-8"
              >
                <Card className="glass-card">
                  <CardHeader>
                    <CardTitle className="text-2xl text-purple-400">
                      🎯 Study Recommendation
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <p className="text-white/80 leading-relaxed">
                      {result.recommendation}
                    </p>

                    <div>
                      <h3 className="text-white font-semibold mb-2">
                        🧠 Priorities:
                      </h3>
                      <ul className="text-white/80 list-disc pl-6 space-y-1">
                        {result.priorities.map((item, i) => (
                          <li key={i}>{item}</li>
                        ))}
                      </ul>
                    </div>

                    <p className="text-sm text-white/50 italic">
                      Suggested agents: {result.trigger_agents.join(", ")}
                    </p>
                  </CardContent>
                </Card>
              </motion.div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
}
