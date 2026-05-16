"use client";

import { useState } from "react";
import { ApiService } from "@/services/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Sparkles, Bot, BookOpenText, Wand2, ArrowLeft } from "lucide-react";
import Link from "next/link";
import { PromptBuilderOutput } from "@/types/PromptBuilderOutput";
import { ADKMessage } from "@/types/ADKMessage";
import { parseADKResponse } from "@/utils/parseADKResponse";
import BackgroundBlur from "@/components/ui/background-blur";
import { motion } from "@/components/ui/motion";
import { useSession } from "@/contexts/SessionContext";

export default function PromptBuilder() {
  const [theme, setTheme] = useState("");
  const [result, setResult] = useState<PromptBuilderOutput | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const { userId, sessionId } = useSession();

  const handleGeneratePrompt = async () => {
    if (!theme.trim()) return;

    setIsLoading(true);
    setResult(null);

    try {
      const final_text = `Generate an essay topic about: ${theme}`;
      const payload = ApiService.createPayload(userId, sessionId, final_text);
      const response = await ApiService.runAgent(payload);
      const parsed = parseADKResponse<PromptBuilderOutput>(response.response);
      setResult(parsed);
    } catch (error) {
      console.error("Error generating theme:", error);
      alert("Error generating theme. Please try again.");
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

        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-8"
          >
            {/* Hero section */}
            <div className="text-center mb-12">
              <div className="inline-flex items-center justify-center px-4 py-2 mb-6 border border-white/10 rounded-full bg-white/5 backdrop-blur-sm">
                <Wand2 className="w-4 h-4 mr-2 text-purple-400" />
                <span className="text-sm font-medium text-white/80">
                  Essay Prompt Builder AI
                </span>
              </div>

              <h1 className="text-4xl md:text-6xl font-bold tracking-tighter mb-6 text-white">
                Generate an
                <br />
                <span className="gradient-text">Essay Theme</span>
              </h1>

              <p className="text-lg md:text-xl text-white/70 max-w-3xl mx-auto leading-relaxed">
                Enter a thematic area (e.g., environment, public health,
                technology) and generate an ENEM-style theme with supporting
                texts and instructions.
              </p>
            </div>

            {/* Input Form */}
            <Card className="glass-card">
              <CardHeader>
                <CardTitle className="text-2xl text-white flex items-center gap-3">
                  <BookOpenText className="h-6 w-6 text-purple-400" />
                  Theme Generator
                </CardTitle>
              </CardHeader>

              <CardContent className="space-y-6">
                <div className="space-y-2">
                  <label className="block text-white font-medium">
                    Thematic Area
                  </label>
                  <input
                    type="text"
                    placeholder="Enter a thematic area..."
                    value={theme}
                    onChange={(e) => setTheme(e.target.value)}
                    className="w-full bg-white/5 border border-white/20 rounded-xl p-4 text-white placeholder-white/50 focus:border-white/40 focus:outline-none transition-colors"
                  />
                </div>

                <Button
                  onClick={handleGeneratePrompt}
                  disabled={isLoading}
                  className={`w-full py-6 text-lg font-medium rounded-xl transition-all duration-300 ${
                    isLoading
                      ? "bg-gray-600 text-gray-300 cursor-not-allowed"
                      : "button-primary hover:scale-[1.02]"
                  }`}
                >
                  {isLoading ? (
                    <>
                      <Sparkles className="w-5 h-5 mr-2 animate-pulse" />
                      Generating Theme...
                    </>
                  ) : (
                    <>
                      <Bot className="w-5 h-5 mr-2" />
                      Generate Theme
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
                <Card className="glass-card">
                  <CardHeader>
                    <CardTitle className="text-2xl text-purple-400">
                      {result.topic}
                    </CardTitle>
                  </CardHeader>

                  <CardContent className="space-y-6">
                    <div className="space-y-4">
                      {result.source_texts.map((text, idx) => (
                        <div
                          key={idx}
                          className="bg-white/5 border border-white/10 rounded-lg p-4"
                        >
                          <p className="text-white/80 leading-relaxed">
                            {text}
                          </p>
                        </div>
                      ))}
                    </div>

                    <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
                      <h3 className="font-semibold text-white mb-2">
                        Instructions:
                      </h3>
                      <p className="text-white/80 leading-relaxed">
                        {result.instructions}
                      </p>
                    </div>
                  </CardContent>
                </Card>

                <div className="flex justify-center">
                  <Button
                    onClick={() => setResult(null)}
                    variant="outline"
                    className="text-white border-white/20 hover:bg-white/10 flex items-center gap-2"
                  >
                    <Wand2 className="w-4 h-4" />
                    Generate Another Theme
                  </Button>
                </div>
              </motion.div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
}
