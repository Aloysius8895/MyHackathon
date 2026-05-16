"use client";

import { useEffect, useState } from "react";
import { ApiService } from "@/services/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";
import { useSession } from "@/contexts/SessionContext";
import { parseADKResponse } from "@/utils/parseADKResponse";
import {
  ArrowLeft,
  LineChart,
  RefreshCcw,
  FileText,
  Brain,
  Loader2,
} from "lucide-react";
import Link from "next/link";
import BackgroundBlur from "@/components/ui/background-blur";
import { motion } from "@/components/ui/motion";

ChartJS.register(BarElement, CategoryScale, LinearScale);

interface Essay {
  topic: string;
  total_score: number;
  date: string;
}

interface PracticeExam {
  area: string;
  score: number;
  date: string;
}

interface Progress {
  essays: Essay[];
  practice_exams: PracticeExam[];
  average_by_area: Record<string, number>;
  recommendations: string[];
}

export default function ProgressTracker() {
  const { userId, sessionId } = useSession();
  const [data, setData] = useState<Progress | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchProgress = async () => {
    setLoading(true);
    try {
      const payload = ApiService.createPayload(
        userId,
        sessionId,
        "Show me my progress report"
      );
      const response = await ApiService.runAgent(payload);
      const parsed = parseADKResponse<Progress>(response.response);
      setData(parsed);
    } catch (e) {
      console.error("Error loading progress", e);
      alert("Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (userId) fetchProgress();
  }, [userId]);

  const chartData = {
    labels: data ? Object.keys(data.average_by_area) : [],
    datasets: [
      {
        label: "Average Score",
        data: data ? Object.values(data.average_by_area) : [],
        backgroundColor: "rgba(99, 102, 241, 0.6)",
        borderRadius: 8,
      },
    ],
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
          <Button
            onClick={fetchProgress}
            disabled={loading}
            className="button-secondary"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Refreshing...
              </>
            ) : (
              <>
                <RefreshCcw className="w-4 h-4 mr-2" />
                Refresh Data
              </>
            )}
          </Button>
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
                <LineChart className="w-4 h-4 mr-2 text-purple-400" />
                <span className="text-sm font-medium text-white/80">
                  Progress Analytics
                </span>
              </div>

              <h1 className="text-4xl md:text-6xl font-bold tracking-tighter mb-6 text-white">
                Your Learning
                <br />
                <span className="gradient-text">Journey</span>
              </h1>

              <p className="text-lg md:text-xl text-white/70 max-w-3xl mx-auto leading-relaxed">
                Track your progress across different subjects and get
                personalized recommendations for improvement.
              </p>
            </div>

            {loading ? (
              <div className="flex justify-center items-center min-h-[400px]">
                <div className="flex flex-col items-center gap-4">
                  <Loader2 className="w-8 h-8 animate-spin text-purple-400" />
                  <p className="text-white/70">Loading your progress data...</p>
                </div>
              </div>
            ) : data ? (
              <div className="space-y-8">
                {/* Average by Area Chart */}
                <Card className="glass-card">
                  <CardHeader>
                    <CardTitle className="text-2xl text-white flex items-center gap-2">
                      <LineChart className="h-6 w-6 text-purple-400" />
                      Performance by Area
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Bar data={chartData} className="max-h-[300px]" />
                  </CardContent>
                </Card>

                {/* Essays Progress */}
                <Card className="glass-card">
                  <CardHeader>
                    <CardTitle className="text-2xl text-white flex items-center gap-2">
                      <FileText className="h-6 w-6 text-purple-400" />
                      Essay History
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    {data.essays.length > 0 ? (
                      <ul className="text-white/80 space-y-3">
                        {data.essays.map((e, i) => (
                          <li
                            key={i}
                            className="p-3 bg-white/5 rounded-lg flex items-center justify-between"
                          >
                            <div>
                              <p className="font-medium text-white">
                                {e.topic}
                              </p>
                              <p className="text-sm text-white/60">{e.date}</p>
                            </div>
                            <div className="flex items-center gap-2">
                              <span className="text-lg font-bold text-purple-400">
                                {e.total_score}
                              </span>
                              <span className="text-sm text-white/60">pts</span>
                            </div>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <div className="text-center py-8 text-white/70">
                        <FileText className="h-12 w-12 mx-auto mb-3 text-white/40" />
                        <p>No essays submitted yet.</p>
                        <Link href="/essay-evaluator">
                          <Button className="button-secondary mt-4">
                            Submit Your First Essay
                          </Button>
                        </Link>
                      </div>
                    )}
                  </CardContent>
                </Card>

                {/* Recommendations */}
                <Card className="glass-card">
                  <CardHeader>
                    <CardTitle className="text-2xl text-white flex items-center gap-2">
                      <Brain className="h-6 w-6 text-purple-400" />
                      Personalized Recommendations
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    {data.recommendations.length > 0 ? (
                      <ul className="grid gap-3">
                        {data.recommendations.map((r, i) => (
                          <li
                            key={i}
                            className="p-4 bg-white/5 rounded-lg text-white/80"
                          >
                            {r}
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <div className="text-center py-8 text-white/70">
                        <Brain className="h-12 w-12 mx-auto mb-3 text-white/40" />
                        <p>
                          Submit more essays to get personalized
                          recommendations.
                        </p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </div>
            ) : (
              <Card className="glass-card text-center py-12">
                <CardContent>
                  <div className="flex flex-col items-center gap-4">
                    <LineChart className="w-12 h-12 text-purple-400" />
                    <h3 className="text-xl font-semibold text-white">
                      No Progress Data
                    </h3>
                    <p className="text-white/70 max-w-md mx-auto">
                      Start your learning journey by submitting essays and
                      taking practice exams.
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
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
}
