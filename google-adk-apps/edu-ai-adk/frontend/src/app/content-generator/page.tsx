"use client";

import { useState } from "react";
import Link from "next/link";
import { ApiService } from "@/services/api";
import { parseADKResponse } from "@/utils/parseADKResponse";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import BackgroundBlur from "@/components/ui/background-blur";
import Flashcard from "@/components/ui/flashcard";
import {
  ArrowLeft,
  BookOpen,
  Brain,
  FileText,
  Lightbulb,
  Link as LinkIcon,
  Sparkles,
  Zap,
} from "lucide-react";
import { ContentResponse } from "@/types/ContentResponse";
import { motion } from "@/components/ui/motion";
import { useSession } from "@/contexts/SessionContext";

export default function ContentGeneratorPage() {
  const [topic, setTopic] = useState("");
  const [result, setResult] = useState<ContentResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const { userId, sessionId } = useSession();

  const handleGenerate = async () => {
    setLoading(true);
    setResult(null);
    try {
      const final_text = `The user wants an explanation about: ${topic}.`;
      const payload = ApiService.createPayload(userId, sessionId, final_text);
      const response = await ApiService.runAgent(payload);
      console.log(response);
      const parsed = parseADKResponse<ContentResponse>(response.response);
      setResult(parsed);
    } catch (err) {
      alert("Failed to generate content.");
    } finally {
      setLoading(false);
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

        <div className="max-w-4xl mx-auto">
          {/* Hero section */}
          <div className="text-center mb-12">
            <div className="inline-flex items-center justify-center px-4 py-2 mb-6 border border-white/10 rounded-full bg-white/5 backdrop-blur-sm">
              <Brain className="w-4 h-4 mr-2 text-purple-400" />
              <span className="text-sm font-medium text-white/80">
                Content Generator AI Agent
              </span>
            </div>

            <h1 className="text-4xl md:text-6xl font-bold tracking-tighter mb-6 text-white">
              Educational Content
              <br />
              <span className="gradient-text">Generator</span>
            </h1>

            <p className="text-lg md:text-xl text-white/70 max-w-3xl mx-auto leading-relaxed">
              Generate comprehensive educational content with explanations, key
              points, flashcards, and video suggestions for any topic.
            </p>
          </div>

          {/* Input form */}
          <Card className="glass-card mb-8">
            <CardHeader>
              <CardTitle className="text-2xl text-white flex items-center gap-3">
                <BookOpen className="h-6 w-6 text-purple-400" />
                Enter Your Topic
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex gap-4 items-center">
                <input
                  type="text"
                  placeholder="Enter a topic, e.g. World War II"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  className="flex-1 bg-white/5 border border-white/20 rounded-xl p-4 text-white placeholder-white/50 focus:border-white/40 focus:outline-none transition-colors"
                />
                <Button
                  disabled={loading || !topic.trim()}
                  onClick={handleGenerate}
                  className={`py-4 px-6 text-lg font-medium rounded-xl transition-all duration-300 ${
                    loading || !topic.trim()
                      ? "bg-gray-600 text-gray-300 cursor-not-allowed"
                      : "button-primary hover:scale-[1.02]"
                  }`}
                >
                  {loading ? (
                    <>
                      <Sparkles className="w-5 h-5 mr-2 animate-pulse" />
                      Generating...
                    </>
                  ) : (
                    <>
                      <Zap className="w-5 h-5 mr-2" />
                      Generate
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Results */}
          {result && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-8"
            >
              {/* Explanation */}
              <Card className="glass-card">
                <CardHeader>
                  <CardTitle className="text-xl text-white flex items-center gap-3">
                    <FileText className="h-6 w-6 text-blue-400" />
                    Explanation
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-white/90 whitespace-pre-wrap leading-relaxed">
                    {result.text_explanation}
                  </p>
                </CardContent>
              </Card>

              {/* Key Points */}
              <Card className="glass-card">
                <CardHeader>
                  <CardTitle className="text-xl text-white flex items-center gap-3">
                    <Lightbulb className="h-6 w-6 text-yellow-400" />
                    Key Points
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-3">
                    {result.topics_summary.map((point, i) => (
                      <li
                        key={i}
                        className="flex items-start gap-3 text-white/90 bg-white/5 p-4 rounded-xl border border-white/10"
                      >
                        <span className="flex-shrink-0 w-6 h-6 rounded-full bg-white/10 flex items-center justify-center text-sm">
                          {i + 1}
                        </span>
                        <span className="leading-relaxed">{point}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

              {/* Flashcards */}
              <Card className="glass-card">
                <CardHeader>
                  <CardTitle className="text-xl text-white flex items-center gap-3">
                    <Brain className="h-6 w-6 text-purple-400" />
                    Flashcards
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {result.flashcards.map((fc, i) => (
                      <Flashcard
                        key={i}
                        question={fc.question}
                        answer={fc.answer}
                      />
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Video Suggestions */}
              <Card className="glass-card">
                <CardHeader>
                  <CardTitle className="text-xl text-white flex items-center gap-3">
                    <LinkIcon className="h-6 w-6 text-green-400" />
                    Video Suggestions
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {result.video_suggestions.map((v, i) => (
                      <a
                        key={i}
                        href={v.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="block p-4 rounded-xl border border-white/20 bg-white/5 hover:bg-white/10 transition-colors group"
                      >
                        <h3 className="text-lg font-semibold text-white group-hover:text-purple-400 transition-colors">
                          {v.title}
                        </h3>
                        <p className="text-white/70 mt-2 text-sm">
                          {v.description}
                        </p>
                      </a>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}
