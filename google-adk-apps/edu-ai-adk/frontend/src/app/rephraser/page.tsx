"use client";

import { useState } from "react";
import Link from "next/link";
import { ApiService } from "@/services/api";
import { parseADKResponse } from "@/utils/parseADKResponse";
import { RephrasingSuggestion } from "@/types/RephrasingSuggestion";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import BackgroundBlur from "@/components/ui/background-blur";
import { motion } from "@/components/ui/motion";
import {
  ArrowLeft,
  PenTool,
  Sparkles,
  Zap,
  FileText,
  CheckCircle,
  Lightbulb,
} from "lucide-react";
import { useSession } from "@/contexts/SessionContext";

export default function RephraserPage() {
  const [inputText, setInputText] = useState("");
  const [result, setResult] = useState<RephrasingSuggestion | null>(null);
  const [loading, setLoading] = useState(false);
  const { userId, sessionId } = useSession();

  const handleRephrase = async () => {
    setLoading(true);
    setResult(null);
    try {
      const final_text = `The user wants to rephrase and improve the following text: ${inputText}.`;
      const payload = ApiService.createPayload(userId, sessionId, final_text);
      const response = await ApiService.runAgent(payload);
      const parsed = parseADKResponse<RephrasingSuggestion>(response);
      if (parsed) setResult(parsed);
    } catch (err) {
      alert("Error while rephrasing. Please try again.");
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
              <PenTool className="w-4 h-4 mr-2 text-purple-400" />
              <span className="text-sm font-medium text-white/80">
                Text Rephraser AI Agent
              </span>
            </div>

            <h1 className="text-4xl md:text-6xl font-bold tracking-tighter mb-6 text-white">
              Enhance Your
              <br />
              <span className="gradient-text">Writing Style</span>
            </h1>

            <p className="text-lg md:text-xl text-white/70 max-w-3xl mx-auto leading-relaxed">
              Transform your text into more polished and professional writing
              with our AI-powered rephrasing tool.
            </p>
          </div>

          {/* Input form */}
          <Card className="glass-card mb-8">
            <CardHeader>
              <CardTitle className="text-2xl text-white flex items-center gap-3">
                <FileText className="h-6 w-6 text-purple-400" />
                Enter Your Text
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Paste your text here to improve its clarity, flow, and professionalism..."
                className="w-full bg-white/5 border border-white/20 rounded-xl p-4 text-white placeholder-white/50 focus:border-white/40 focus:outline-none transition-colors min-h-[200px] resize-none"
              />

              <Button
                onClick={handleRephrase}
                disabled={loading || !inputText.trim()}
                className={`w-full py-6 text-lg font-medium rounded-xl transition-all duration-300 ${
                  loading || !inputText.trim()
                    ? "bg-gray-600 text-gray-300 cursor-not-allowed"
                    : "button-primary hover:scale-[1.02]"
                }`}
              >
                {loading ? (
                  <>
                    <Sparkles className="w-5 h-5 mr-2 animate-pulse" />
                    Enhancing your text...
                  </>
                ) : (
                  <>
                    <Zap className="w-5 h-5 mr-2" />
                    Enhance Writing
                  </>
                )}
              </Button>
            </CardContent>
          </Card>

          {/* Results */}
          {result && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-8"
            >
              {/* Original Text */}
              <Card className="glass-card">
                <CardHeader>
                  <CardTitle className="text-xl text-white flex items-center gap-3">
                    <FileText className="h-6 w-6 text-blue-400" />
                    Original Text
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-white/80 whitespace-pre-wrap leading-relaxed bg-white/5 p-4 rounded-xl border border-white/10">
                    {result.original}
                  </p>
                </CardContent>
              </Card>

              {/* Improved Text */}
              <Card className="glass-card">
                <CardHeader>
                  <CardTitle className="text-xl text-white flex items-center gap-3">
                    <CheckCircle className="h-6 w-6 text-green-400" />
                    Enhanced Version
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-green-400 whitespace-pre-wrap leading-relaxed bg-white/5 p-4 rounded-xl border border-green-500/20">
                    {result.rewritten}
                  </p>
                </CardContent>
              </Card>

              {/* Explanation */}
              <Card className="glass-card">
                <CardHeader>
                  <CardTitle className="text-xl text-white flex items-center gap-3">
                    <Lightbulb className="h-6 w-6 text-yellow-400" />
                    Improvements Explained
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="bg-white/5 border border-white/10 rounded-xl p-4">
                    <p className="text-white/90 leading-relaxed">
                      {result.explanation}
                    </p>
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
