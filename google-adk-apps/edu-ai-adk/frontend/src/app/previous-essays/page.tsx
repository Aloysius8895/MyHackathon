"use client";

import { useEffect, useState } from "react";
import { ApiService } from "@/services/api";
import { useSession } from "@/contexts/SessionContext";
import { EssayEvaluationResult } from "@/types/EssayEvaluationResult";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  ArrowLeft,
  FileText,
  Loader2,
  BookOpen,
  Star,
  Target,
} from "lucide-react";
import { parseADKResponse } from "@/utils/parseADKResponse";
import BackgroundBlur from "@/components/ui/background-blur";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import FeedbackBox from "@/components/Essays/FeedbackBox";

export default function PreviousEssays() {
  const [essays, setEssays] = useState<EssayEvaluationResult[] | null>([]);
  const { userId, sessionId } = useSession();
  const [isLoading, setIsLoading] = useState(false);
  const [selectedEssay, setSelectedEssay] =
    useState<EssayEvaluationResult | null>(null);

  const getPreviousEssays = async () => {
    const final_text = "Show me all my previous essays";
    const payload = ApiService.createPayload(userId, sessionId, final_text);
    const response = await ApiService.runAgent(payload);
    const parsed = parseADKResponse<{ essays: EssayEvaluationResult[] }>(
      response.response
    );
    setEssays(parsed?.essays ?? []);
    setIsLoading(false);
  };

  useEffect(() => {
    setIsLoading(true);
    if (!userId) return;
    console.log("🔄 Loading essays for user:", userId);

    getPreviousEssays();
  }, [userId]);

  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      <div className="mx-auto px-4 py-8 relative z-10">
        <BackgroundBlur />

        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <Link href="/dashboard">
            <Button className="button-secondary flex items-center gap-2">
              <ArrowLeft className="h-4 w-4" />
              Back to Home
            </Button>
          </Link>
        </div>

        {/* Main content */}
        <div className="max-w-6xl mx-auto">
          {/* Hero section */}
          <div className="text-center mb-12">
            <div className="inline-flex items-center justify-center px-4 py-2 mb-6 border border-white/10 rounded-full bg-white/5 backdrop-blur-sm">
              <BookOpen className="w-4 h-4 mr-2 text-purple-400" />
              <span className="text-sm font-medium text-white/80">
                Previous Essays Archive
              </span>
            </div>

            <h1 className="text-4xl md:text-6xl font-bold tracking-tighter mb-6 text-white">
              Your Essay
              <br />
              <span className="gradient-text">History</span>
            </h1>

            <p className="text-lg md:text-xl text-white/70 max-w-3xl mx-auto leading-relaxed">
              Review your past essays, track your progress, and learn from
              detailed feedback across all competencies.
            </p>

            <Link href="/essay-evaluator">
              <Button className="button-secondary mt-4">
                <FileText className="w-4 h-4 mr-2" />
                Evaluate New Essay
              </Button>
            </Link>
          </div>

          {/* Loading State */}
          {isLoading ? (
            <div className="flex justify-center items-center min-h-[400px]">
              <div className="flex flex-col items-center gap-4">
                <Loader2 className="w-8 h-8 animate-spin text-purple-400" />
                <p className="text-white/70">Loading your essays...</p>
              </div>
            </div>
          ) : essays?.length === 0 ? (
            /* Empty State */
            <Card className="glass-card text-center py-12">
              <CardContent>
                <div className="flex flex-col items-center gap-4">
                  <FileText className="w-12 h-12 text-purple-400" />
                  <h3 className="text-xl font-semibold text-white">
                    No Essays Yet
                  </h3>
                  <p className="text-white/70 max-w-md mx-auto">
                    You haven't submitted any essays for evaluation. Start by
                    submitting your first essay to get detailed feedback.
                  </p>
                  <Link href="/essay-evaluator">
                    <Button className="button-primary mt-4">
                      <FileText className="w-4 h-4 mr-2" />
                      Submit Your First Essay
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          ) : (
            /* Essays List */
            <div className="space-y-6">
              {selectedEssay ? (
                /* Detailed Essay View */
                <div className="space-y-6">
                  <Button
                    onClick={() => setSelectedEssay(null)}
                    className="button-secondary"
                  >
                    <ArrowLeft className="w-4 h-4 mr-2" />
                    Back to Essays
                  </Button>
                  <FeedbackBox data={selectedEssay} />
                </div>
              ) : (
                /* Essays Grid */
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {essays?.map((essay, index) => (
                    <Card
                      key={index}
                      className="glass-card hover:border-purple-400/50 transition-all cursor-pointer"
                      onClick={() => setSelectedEssay(essay)}
                    >
                      <CardHeader>
                        <div className="flex items-center justify-between">
                          <div className="inline-flex items-center px-3 py-1 rounded-full bg-purple-400/10 border border-purple-400/20">
                            <Target className="w-4 h-4 mr-2 text-purple-400" />
                            <span className="text-sm font-medium text-white">
                              Essay #{index + 1}
                            </span>
                          </div>
                          <div className="flex items-center gap-2">
                            <Star className="w-4 h-4 text-yellow-400" />
                            <span className="text-lg font-bold text-white">
                              {essay.total_score}
                            </span>
                          </div>
                        </div>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-4">
                          {/* Competency Scores */}
                          <div className="grid grid-cols-5 gap-2">
                            {[1, 2, 3, 4, 5].map((comp) => (
                              <div
                                key={comp}
                                className="flex flex-col items-center p-2 rounded-lg bg-white/5"
                              >
                                <span className="text-xs text-white/60">
                                  C{comp}
                                </span>
                                <span className="text-sm font-bold text-white">
                                  {
                                    essay[
                                      `competency_${comp}_score` as keyof EssayEvaluationResult
                                    ]
                                  }
                                </span>
                              </div>
                            ))}
                          </div>

                          {/* Essay Preview */}
                          <div>
                            <p className="text-white/70 text-sm line-clamp-3">
                              {essay.extracted_essay.slice(0, 180)}...
                            </p>
                          </div>

                          {/* View Details Button */}
                          <Button className="w-full button-secondary">
                            View Detailed Feedback
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
