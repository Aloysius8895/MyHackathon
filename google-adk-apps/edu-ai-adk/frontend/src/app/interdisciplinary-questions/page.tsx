"use client";

import { useState } from "react";
import Link from "next/link";
import { ApiService } from "@/services/api";
import { InterdisciplinaryQuestion } from "@/types/InterdisciplinaryQuestion";
import { ADKMessage } from "@/types/ADKMessage";
import { parseADKResponse } from "@/utils/parseADKResponse";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { motion } from "@/components/ui/motion";
import GradientText from "@/components/ui/gradient-text";
import BackgroundBlur from "@/components/ui/background-blur";
import {
  BookOpen,
  Brain,
  CheckCircle,
  XCircle,
  ArrowRight,
  RotateCcw,
  Target,
  Zap,
  Home,
  Lightbulb,
  RefreshCw,
  ArrowLeft,
} from "lucide-react";
import { useSession } from "@/contexts/SessionContext";

type QuizState = "form" | "loading" | "question" | "answered";

export default function InterdisciplinaryPage() {
  // Form state
  const [form, setForm] = useState({
    area1: "History",
    area2: "Physics",
  });

  // Quiz state
  const [quizState, setQuizState] = useState<QuizState>("form");
  const [question, setQuestion] = useState<InterdisciplinaryQuestion | null>(
    null
  );
  const [selectedOption, setSelectedOption] = useState<string>("");
  const [isCorrect, setIsCorrect] = useState<boolean>(false);

  // Loading state
  const [loading, setLoading] = useState(false);

  const { userId, sessionId } = useSession();

  const handleFormChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    setLoading(true);
    setQuizState("loading");

    try {
      const final_text = `Generate an interdisciplinary question about: ${form.area1} and ${form.area2}.`;
      const payload = ApiService.createPayload(userId, sessionId, final_text);

      const data = await ApiService.runAgent(payload);
      const parsed = parseADKResponse<InterdisciplinaryQuestion>(data);

      if (parsed) {
        setQuestion(parsed);
        setQuizState("question");
        setSelectedOption("");
        setIsCorrect(false);
      } else {
        throw new Error("Could not generate the question");
      }
    } catch (err) {
      alert("Error generating question. Please try again.");
      setQuizState("form");
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerSelect = (option: string) => {
    if (selectedOption) return; // Already answered

    setSelectedOption(option);
    const correct = option === question?.correct_answer;
    setIsCorrect(correct);
    setQuizState("answered");
  };

  const resetQuiz = () => {
    setQuizState("form");
    setQuestion(null);
    setSelectedOption("");
    setIsCorrect(false);
  };

  const generateNewQuestion = () => {
    setQuizState("loading");
    setSelectedOption("");
    setIsCorrect(false);
    setLoading(true);

    // Use the same parameters to generate a new question
    handleFormSubmit({ preventDefault: () => {} } as React.FormEvent);
  };

  if (quizState === "loading") {
    return (
      <div className="min-h-screen bg-background relative overflow-hidden">
        <div className="mx-auto px-4 py-8 relative z-10">
          <BackgroundBlur />
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            className="text-center space-y-6"
          >
            <div className="relative">
              <div className="w-16 h-16 border-4 border-primary/30 rounded-full animate-spin border-t-primary mx-auto"></div>
              <Brain className="w-8 h-8 text-primary absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
            </div>
            <div className="space-y-4 flex flex-col items-center">
              <div className="space-y-2">
                <h2 className="text-2xl font-semibold text-white">
                  Generating interdisciplinary question...
                </h2>
                <p className="text-white/70">
                  Connecting {form.area1} and {form.area2} in a unique question
                </p>
              </div>
              <Link href="/dashboard">
                <Button
                  variant="outline"
                  className="text-white border-white/20 hover:bg-white/10 flex items-center gap-2"
                >
                  <Home className="w-4 h-4" />
                  Cancel and Return
                </Button>
              </Link>
            </div>
          </motion.div>
        </div>
      </div>
    );
  }

  if (quizState === "form") {
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
                  <Target className="w-4 h-4 mr-2 text-purple-400" />
                  <span className="text-sm font-medium text-white/80">
                    Interdisciplinary Questions
                  </span>
                </div>

                <h1 className="text-4xl md:text-6xl font-bold tracking-tighter mb-6 text-white">
                  Connect Different
                  <br />
                  <span className="gradient-text">Knowledge Areas</span>
                </h1>

                <p className="text-lg md:text-xl text-white/70 max-w-3xl mx-auto leading-relaxed">
                  Challenge yourself with questions that bridge multiple
                  subjects, enhancing your interdisciplinary understanding.
                </p>
              </div>

              {/* Form */}
              <Card className="glass-card">
                <CardHeader>
                  <CardTitle className="text-2xl text-white flex items-center gap-3">
                    <BookOpen className="h-6 w-6 text-purple-400" />
                    Select Knowledge Areas
                  </CardTitle>
                </CardHeader>

                <CardContent>
                  <form onSubmit={handleFormSubmit} className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="space-y-2">
                        <label className="block text-white font-medium">
                          First Area
                        </label>
                        <select
                          name="area1"
                          value={form.area1}
                          onChange={handleFormChange}
                          className="w-full bg-white/5 border border-white/20 rounded-xl p-4 text-white focus:border-white/40 focus:outline-none transition-colors"
                        >
                          <option value="History">History</option>
                          <option value="Physics">Physics</option>
                          <option value="Biology">Biology</option>
                          <option value="Mathematics">Mathematics</option>
                          <option value="Geography">Geography</option>
                          <option value="Chemistry">Chemistry</option>
                          <option value="Languages">Languages</option>
                        </select>
                      </div>

                      <div className="space-y-2">
                        <label className="block text-white font-medium">
                          Second Area
                        </label>
                        <select
                          name="area2"
                          value={form.area2}
                          onChange={handleFormChange}
                          className="w-full bg-white/5 border border-white/20 rounded-xl p-4 text-white focus:border-white/40 focus:outline-none transition-colors"
                        >
                          <option value="History">History</option>
                          <option value="Physics">Physics</option>
                          <option value="Biology">Biology</option>
                          <option value="Mathematics">Mathematics</option>
                          <option value="Geography">Geography</option>
                          <option value="Chemistry">Chemistry</option>
                          <option value="Languages">Languages</option>
                        </select>
                      </div>
                    </div>

                    <Button
                      type="submit"
                      disabled={loading || form.area1 === form.area2}
                      className={`w-full py-6 text-lg font-medium rounded-xl transition-all duration-300 ${
                        loading || form.area1 === form.area2
                          ? "bg-gray-600 text-gray-300 cursor-not-allowed"
                          : "button-primary hover:scale-[1.02]"
                      }`}
                    >
                      {loading ? (
                        <>
                          <Brain className="w-5 h-5 mr-2 animate-pulse" />
                          Generating Question...
                        </>
                      ) : (
                        <>
                          <Zap className="w-5 h-5 mr-2" />
                          Generate Question
                        </>
                      )}
                    </Button>

                    {form.area1 === form.area2 && (
                      <p className="text-yellow-400 text-sm text-center">
                        Please select two different areas to create an
                        interdisciplinary question
                      </p>
                    )}
                  </form>
                </CardContent>
              </Card>
            </motion.div>
          </div>
        </div>
      </div>
    );
  }

  if ((quizState === "question" || quizState === "answered") && question) {
    return (
      <div className="min-h-screen bg-background relative overflow-hidden">
        <div className="mx-auto px-4 py-8 relative z-10">
          <BackgroundBlur />
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex items-center justify-between mb-8 p-4 glass-card border-white/10 rounded-lg max-w-4xl mx-auto"
          >
            <div className="flex items-center gap-4">
              <Link href="/dashboard">
                <Button
                  variant="outline"
                  size="sm"
                  className="text-white border-white/20 hover:bg-white/10 flex items-center gap-2"
                >
                  <Home className="w-4 h-4" />
                  Home
                </Button>
              </Link>
              <div className="text-white">
                <span className="font-semibold">{form.area1}</span>
                <span className="mx-2 text-white/50">×</span>
                <span className="font-semibold">{form.area2}</span>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <Button
                onClick={generateNewQuestion}
                variant="outline"
                size="sm"
                className="text-white border-white/20 hover:bg-white/10 flex items-center gap-2"
                disabled={loading}
              >
                <RefreshCw className="w-4 h-4" />
                New Question
              </Button>
            </div>
          </motion.div>

          {/* Question Card */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3 }}
            className="max-w-4xl mx-auto"
          >
            <Card className="glass-card">
              <CardHeader>
                <CardTitle className="text-xl text-white leading-relaxed">
                  {question.question}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {Object.entries(question.alternatives).map(([letra, texto]) => {
                  const isSelected = selectedOption === letra;
                  const isCorrectAnswer = question.correct_answer === letra;
                  const showResult = quizState === "answered";

                  return (
                    <button
                      key={letra}
                      onClick={() => handleAnswerSelect(letra)}
                      disabled={showResult}
                      className={`w-full p-4 rounded-xl text-left transition-all duration-200 ${
                        showResult
                          ? isCorrectAnswer
                            ? "bg-green-500/20 border-green-500 border-2"
                            : isSelected
                            ? "bg-red-500/20 border-red-500 border-2"
                            : "bg-white/5 border border-white/20"
                          : isSelected
                          ? "bg-primary/20 border-primary border-2"
                          : "bg-white/5 border border-white/20 hover:bg-white/10 hover:scale-[1.02] active:scale-[0.98]"
                      }`}
                    >
                      <div className="flex items-start gap-3">
                        <div className="flex items-center gap-2">
                          <span
                            className={`font-semibold w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                              showResult
                                ? isCorrectAnswer
                                  ? "text-green-400 bg-green-500/20"
                                  : isSelected
                                  ? "text-red-400 bg-red-500/20"
                                  : "text-primary bg-primary/20"
                                : "text-primary bg-primary/20"
                            }`}
                          >
                            {letra}
                          </span>
                          {showResult && isCorrectAnswer && (
                            <CheckCircle className="w-5 h-5 text-green-400" />
                          )}
                          {showResult && isSelected && !isCorrectAnswer && (
                            <XCircle className="w-5 h-5 text-red-400" />
                          )}
                        </div>
                        <span className="text-white">{texto}</span>
                      </div>
                    </button>
                  );
                })}

                {quizState === "answered" && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-6 p-6 rounded-lg bg-blue-500/10 border border-blue-500/30"
                  >
                    <div className="flex items-start gap-3">
                      <Lightbulb className="w-6 h-6 text-blue-400 flex-shrink-0 mt-0.5" />
                      <div className="space-y-2">
                        <h3 className="text-blue-200 font-semibold">
                          {isCorrect
                            ? "Congratulations! Correct answer!"
                            : "Incorrect answer"}
                        </h3>
                        <p className="text-blue-200 text-sm leading-relaxed">
                          <strong>Explanation:</strong> {question.explanation}
                        </p>
                      </div>
                    </div>
                  </motion.div>
                )}
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    );
  }

  return null;
}
