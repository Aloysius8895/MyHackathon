"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { ApiService } from "@/services/api";
import { SimulatedExamResult } from "@/types/SimulatedExamResult";
import { parseADKResponse } from "@/utils/parseADKResponse";
import { ADKMessage } from "@/types/ADKMessage";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { motion } from "@/components/ui/motion";
import GradientText from "@/components/ui/gradient-text";
import BackgroundBlur from "@/components/ui/background-blur";
import {
  Clock,
  BookOpen,
  Brain,
  CheckCircle,
  XCircle,
  Trophy,
  ArrowRight,
  RotateCcw,
  Timer,
  Target,
  Zap,
  StopCircle,
  AlertTriangle,
  Home,
  ArrowLeft,
} from "lucide-react";
import { useSession } from "@/contexts/SessionContext";

type QuizState = "form" | "loading" | "quiz" | "results";

interface QuizAnswer {
  questionIndex: number;
  selectedOption: string;
  isCorrect: boolean;
}

export default function SimulatedExam() {
  // Form state
  const [form, setForm] = useState({
    topic: "",
    subject: "Natural Sciences",
    difficulty: "Medium",
    time: 30,
  });

  // Quiz state
  const [quizState, setQuizState] = useState<QuizState>("form");
  const [questions, setQuestions] = useState<SimulatedExamResult>();
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<QuizAnswer[]>([]);
  const [selectedOption, setSelectedOption] = useState<string>("");

  // Timer state
  const [timeLeft, setTimeLeft] = useState(0);
  const [timerActive, setTimerActive] = useState(false);

  // Loading state
  const [loading, setLoading] = useState(false);

  // Stop confirmation state
  const [showStopConfirmation, setShowStopConfirmation] = useState(false);

  const { userId, sessionId } = useSession();

  // Timer effect
  useEffect(() => {
    let interval: NodeJS.Timeout;

    if (timerActive && timeLeft > 0) {
      interval = setInterval(() => {
        setTimeLeft((prev) => {
          if (prev <= 1) {
            setTimerActive(false);
            finishQuiz();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }

    return () => clearInterval(interval);
  }, [timerActive, timeLeft]);

  const formatTime = (seconds: number): string => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, "0")}:${remainingSeconds
      .toString()
      .padStart(2, "0")}`;
  };

  const handleFormChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.topic.trim()) return;

    setLoading(true);
    setQuizState("loading");

    try {
      const final_text = `The user wants a simulated exam about the topic "${form.topic}" in the area of "${form.subject}" with difficulty "${form.difficulty}" and time of ${form.time} minutes.`;
      const payload = ApiService.createPayload(userId, sessionId, final_text);

      const data = await ApiService.runAgent(payload);
      const parsed = parseADKResponse<SimulatedExamResult>(data.response);

      if (parsed && parsed.questions?.length > 0) {
        setQuestions(parsed);
        setTimeLeft(form.time * 60); // Convert minutes to seconds
        setQuizState("quiz");
        setTimerActive(true);
        setCurrentQuestionIndex(0);
        setAnswers([]);
        setSelectedOption("");
      } else {
        throw new Error("Could not generate the exam");
      }
    } catch (err) {
      alert("Error generating exam. Please try again.");
      setQuizState("form");
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerSelect = (option: string) => {
    setSelectedOption(option);
  };

  const handleNextQuestion = () => {
    if (!selectedOption || !questions) return;

    const currentQuestion = questions.questions[currentQuestionIndex];
    const isCorrect = selectedOption === currentQuestion.correct_answer;

    const newAnswer: QuizAnswer = {
      questionIndex: currentQuestionIndex,
      selectedOption,
      isCorrect,
    };

    setAnswers((prev) => [...prev, newAnswer]);
    setSelectedOption("");

    if (currentQuestionIndex + 1 < questions.questions.length) {
      setCurrentQuestionIndex((prev) => prev + 1);
    } else {
      finishQuiz();
    }
  };

  const finishQuiz = () => {
    setTimerActive(false);
    setQuizState("results");
  };

  const handleStopQuiz = () => {
    setShowStopConfirmation(true);
  };

  const confirmStopQuiz = () => {
    setTimerActive(false);
    setQuizState("results");
    setShowStopConfirmation(false);
  };

  const cancelStopQuiz = () => {
    setShowStopConfirmation(false);
  };

  const resetQuiz = () => {
    setQuizState("form");
    setQuestions(undefined);
    setCurrentQuestionIndex(0);
    setAnswers([]);
    setSelectedOption("");
    setTimeLeft(0);
    setTimerActive(false);
    setForm({
      topic: "",
      subject: "Natural Sciences",
      difficulty: "Medium",
      time: 30,
    });
    setShowStopConfirmation(false);
  };

  const calculateScore = () => {
    const correctAnswers = answers.filter((answer) => answer.isCorrect).length;
    const totalQuestions = questions?.questions.length || 0;
    return { correct: correctAnswers, total: totalQuestions };
  };

  if (quizState === "loading") {
    return (
      <div className="min-h-screen bg-background relative overflow-hidden">
        <div className="mx-auto px-4 py-8 relative z-10">
          <BackgroundBlur />
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            className="text-center space-y-8 max-w-lg mx-auto px-4 flex items-center flex-col mt-24"
          >
            <div className="relative">
              <div className="w-20 h-20 border-4 border-primary/30 rounded-full animate-spin border-t-primary mx-auto"></div>
              <Brain className="w-10 h-10 text-primary absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
            </div>
            <div className="space-y-6 flex flex-col items-center">
              <div className="space-y-3">
                <h2 className="text-3xl font-bold text-white">
                  Generating your exam...
                </h2>
                <p className="text-lg text-white/70">
                  Our AI is creating personalized questions for you
                </p>
              </div>
              <Link href="/dashboard">
                <Button
                  variant="outline"
                  className="button-secondary flex items-center gap-2"
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
                    ENEM Simulated Exam
                  </span>
                </div>

                <h1 className="text-4xl md:text-6xl font-bold tracking-tighter mb-6 text-white">
                  Test Your
                  <br />
                  <span className="gradient-text">Knowledge</span>
                </h1>

                <p className="text-lg md:text-xl text-white/70 max-w-3xl mx-auto leading-relaxed">
                  Challenge yourself with personalized questions based on your
                  chosen subject and difficulty level.
                </p>
              </div>

              {/* Form */}
              <Card className="glass-card">
                <CardHeader>
                  <CardTitle className="text-2xl text-white flex items-center gap-3">
                    <BookOpen className="h-6 w-6 text-purple-400" />
                    Exam Configuration
                  </CardTitle>
                </CardHeader>

                <CardContent>
                  <form onSubmit={handleFormSubmit} className="space-y-6">
                    <div className="space-y-2">
                      <label className="block text-white font-medium">
                        Topic
                      </label>
                      <input
                        type="text"
                        name="topic"
                        placeholder="E.g., Urban Ecology, Industrial Revolution..."
                        value={form.topic}
                        onChange={handleFormChange}
                        className="w-full bg-white/5 border border-white/20 rounded-xl p-4 text-white placeholder-white/50 focus:border-white/40 focus:outline-none transition-colors"
                        required
                      />
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="space-y-2">
                        <label className="block text-white font-medium">
                          Subject Area
                        </label>
                        <select
                          name="subject"
                          value={form.subject}
                          onChange={handleFormChange}
                          className="w-full bg-white/5 border border-white/20 rounded-xl p-4 text-white focus:border-white/40 focus:outline-none transition-colors"
                        >
                          <option value="Natural Sciences">
                            Natural Sciences
                          </option>
                          <option value="Human Sciences">Human Sciences</option>
                          <option value="Languages">Languages</option>
                          <option value="Mathematics">Mathematics</option>
                        </select>
                      </div>

                      <div className="space-y-2">
                        <label className="block text-white font-medium">
                          Difficulty
                        </label>
                        <select
                          name="difficulty"
                          value={form.difficulty}
                          onChange={handleFormChange}
                          className="w-full bg-white/5 border border-white/20 rounded-xl p-4 text-white focus:border-white/40 focus:outline-none transition-colors"
                        >
                          <option value="Easy">Easy</option>
                          <option value="Medium">Medium</option>
                          <option value="Hard">Hard</option>
                        </select>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <label className="text-white font-medium flex items-center gap-2">
                        <Timer className="w-4 h-4" />
                        Time (minutes)
                      </label>
                      <input
                        type="number"
                        name="time"
                        min="5"
                        max="120"
                        value={form.time}
                        onChange={handleFormChange}
                        className="w-full bg-white/5 border border-white/20 rounded-xl p-4 text-white focus:border-white/40 focus:outline-none transition-colors"
                        required
                      />
                    </div>

                    <Button
                      type="submit"
                      disabled={loading || !form.topic.trim()}
                      className={`w-full py-6 text-lg font-medium rounded-xl transition-all duration-300 ${
                        loading
                          ? "bg-gray-600 text-gray-300 cursor-not-allowed"
                          : "button-primary hover:scale-[1.02]"
                      }`}
                    >
                      {loading ? (
                        <>
                          <Brain className="w-5 h-5 mr-2 animate-pulse" />
                          Generating Exam...
                        </>
                      ) : (
                        <>
                          <Zap className="w-5 h-5 mr-2" />
                          Start Exam
                        </>
                      )}
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </motion.div>
          </div>
        </div>
      </div>
    );
  }

  if (quizState === "quiz" && questions) {
    const currentQuestion = questions.questions[currentQuestionIndex];
    const progress =
      ((currentQuestionIndex + 1) / questions.questions.length) * 100;

    return (
      <div className="min-h-screen bg-background relative overflow-hidden flex flex-col">
        <div className="w-full relative z-10 flex-1 flex flex-col">
          <BackgroundBlur />
          {/* Timer and Progress Header */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex items-center justify-between p-4 glass-card border-white/10 rounded-lg max-w-4xl mx-auto w-full mt-8 px-4"
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
              <div className="flex items-center gap-2 text-white">
                <Clock className="w-5 h-5 text-primary" />
                <span className="font-mono text-lg font-semibold">
                  {formatTime(timeLeft)}
                </span>
              </div>
              <div className="text-white/70">
                Question {currentQuestionIndex + 1} of{" "}
                {questions.questions.length}
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex-1 max-w-xs">
                <div className="w-full bg-white/10 rounded-full h-2">
                  <div
                    className="bg-primary h-2 rounded-full transition-all duration-500 ease-out"
                    style={{ width: `${progress}%` }}
                  />
                </div>
              </div>
              <Button
                onClick={handleStopQuiz}
                variant="outline"
                size="sm"
                className="text-red-400 border-red-400/30 hover:bg-red-400/10 hover:border-red-400 transition-colors"
              >
                <StopCircle className="w-4 h-4 mr-2" />
                Stop
              </Button>
            </div>
          </motion.div>

          {/* Question Card */}
          <motion.div
            key={currentQuestionIndex}
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -50 }}
            transition={{ duration: 0.3 }}
            className="flex-1 flex items-center max-w-4xl mx-auto w-full px-4 py-8"
          >
            <Card className="glass-card border-white/10 w-full">
              <CardHeader>
                <CardTitle className="text-xl text-white leading-relaxed">
                  {currentQuestion.question}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {Object.entries(currentQuestion.alternatives).map(
                  ([letra, texto]) => (
                    <button
                      key={letra}
                      onClick={() => handleAnswerSelect(letra)}
                      className={`w-full p-4 rounded-xl text-left transition-all duration-200 hover:scale-[1.02] active:scale-[0.98] ${
                        selectedOption === letra
                          ? "bg-primary/20 border-primary border-2"
                          : "bg-white/5 border border-white/20 hover:bg-white/10"
                      }`}
                    >
                      <div className="flex items-start gap-3">
                        <span className="font-semibold text-primary bg-primary/20 w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0">
                          {letra}
                        </span>
                        <span className="text-white">{texto as string}</span>
                      </div>
                    </button>
                  )
                )}

                <div className="pt-6 border-t border-white/10">
                  <Button
                    onClick={handleNextQuestion}
                    disabled={!selectedOption}
                    className="w-full button-primary py-6 text-lg font-medium rounded-xl transition-all duration-300 hover:scale-[1.02] flex items-center justify-center gap-2"
                  >
                    {currentQuestionIndex + 1 === questions.questions.length ? (
                      <>
                        <Trophy className="w-5 h-5" />
                        Finish Exam
                      </>
                    ) : (
                      <>
                        Next Question
                        <ArrowRight className="w-5 h-5 transition-transform duration-200 group-hover:translate-x-1" />
                      </>
                    )}
                  </Button>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Stop Confirmation Modal */}
          {showStopConfirmation && (
            <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="glass-card border-white/10 rounded-xl p-8 max-w-md mx-4 text-center space-y-6"
              >
                <div className="w-16 h-16 bg-red-500/20 border border-red-500/30 rounded-full flex items-center justify-center mx-auto">
                  <AlertTriangle className="w-8 h-8 text-red-400" />
                </div>
                <h3 className="text-xl font-semibold text-white">Stop Exam?</h3>
                <p className="text-white/70">
                  Are you sure you want to stop the exam? You can view the
                  results of answered questions or return to the home page.
                </p>
                <div className="flex flex-col sm:flex-row gap-3 justify-center">
                  <Button
                    onClick={cancelStopQuiz}
                    variant="outline"
                    className="text-white border-white/20 hover:bg-white/10"
                  >
                    Continue
                  </Button>
                  <Button
                    onClick={confirmStopQuiz}
                    className="bg-red-500 hover:bg-red-600 text-white"
                  >
                    <StopCircle className="w-4 h-4 mr-2" />
                    View Results
                  </Button>
                  <Link href="/dashboard">
                    <Button
                      variant="outline"
                      className="text-white border-white/20 hover:bg-white/10 flex items-center gap-2 w-full sm:w-auto"
                    >
                      <Home className="w-4 h-4" />
                      Home Page
                    </Button>
                  </Link>
                </div>
              </motion.div>
            </div>
          )}
        </div>
      </div>
    );
  }

  if (quizState === "results" && questions) {
    const score = calculateScore();
    const percentage = Math.round((score.correct / score.total) * 100);

    return (
      <div className="min-h-screen bg-background relative overflow-hidden">
        <div className="mx-auto px-4 py-8 relative z-10">
          <BackgroundBlur />
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-8 max-w-4xl mx-auto"
          >
            {/* Results Header */}
            <div className="text-center space-y-6">
              <div className="inline-flex items-center justify-center px-4 py-2 mb-6 border border-white/10 rounded-full bg-white/5 backdrop-blur-sm">
                <Trophy className="w-4 h-4 mr-2 text-yellow-400" />
                <span className="text-sm font-medium text-white/80">
                  {answers.length === questions.questions.length
                    ? "Exam Completed"
                    : "Exam Interrupted"}
                </span>
              </div>

              <div className="inline-flex items-center justify-center w-20 h-20 bg-primary/20 rounded-full border border-primary/30">
                <Trophy className="w-10 h-10 text-primary" />
              </div>

              <div>
                <h1 className="text-4xl md:text-6xl font-bold tracking-tighter mb-6 text-white">
                  Your
                  <br />
                  <span className="gradient-text">Results</span>
                </h1>
                <div className="text-6xl md:text-7xl font-bold text-white mb-2">
                  {percentage}
                  <span className="text-3xl text-white/60 ml-2">%</span>
                </div>
              </div>

              <p className="text-white/70 text-lg">
                You got {score.correct} out of {answers.length} questions
                correct
                {answers.length < questions.questions.length && (
                  <span className="block text-sm mt-1 text-yellow-400">
                    ({questions.questions.length - answers.length} unanswered
                    questions)
                  </span>
                )}
              </p>
            </div>

            {/* Detailed Results */}
            <div className="space-y-6">
              <h2 className="text-2xl font-semibold text-white">
                Question Review
              </h2>
              {questions.questions.map((question, index) => {
                const userAnswer = answers.find(
                  (a) => a.questionIndex === index
                );
                const isCorrect = userAnswer?.isCorrect || false;
                const wasAnswered = !!userAnswer;

                return (
                  <Card
                    key={index}
                    className={`glass-card border-white/10 ${
                      !wasAnswered ? "opacity-60" : ""
                    }`}
                  >
                    <CardContent className="p-6">
                      <div className="flex items-start gap-4">
                        <div className="flex-shrink-0">
                          {!wasAnswered ? (
                            <div className="w-8 h-8 bg-gray-500/20 border border-gray-500 rounded-full flex items-center justify-center">
                              <Clock className="w-5 h-5 text-gray-400" />
                            </div>
                          ) : isCorrect ? (
                            <div className="w-8 h-8 bg-green-500/20 border border-green-500 rounded-full flex items-center justify-center">
                              <CheckCircle className="w-5 h-5 text-green-400" />
                            </div>
                          ) : (
                            <div className="w-8 h-8 bg-red-500/20 border border-red-500 rounded-full flex items-center justify-center">
                              <XCircle className="w-5 h-5 text-red-400" />
                            </div>
                          )}
                        </div>
                        <div className="flex-1 space-y-3">
                          <h3 className="text-white font-medium">
                            {index + 1}. {question.question}
                            {!wasAnswered && (
                              <span className="ml-2 text-xs bg-gray-500/20 text-gray-400 px-2 py-1 rounded">
                                Not answered
                              </span>
                            )}
                          </h3>
                          <div className="grid grid-cols-1 gap-2">
                            {Object.entries(question.alternatives).map(
                              ([letra, texto]) => {
                                const isUserAnswer =
                                  userAnswer?.selectedOption === letra;
                                const isCorrectAnswer =
                                  question.correct_answer === letra;

                                return (
                                  <div
                                    key={letra}
                                    className={`p-3 rounded-lg text-sm ${
                                      !wasAnswered
                                        ? isCorrectAnswer
                                          ? "bg-green-500/20 border border-green-500/50 text-green-200"
                                          : "text-white/40"
                                        : isCorrectAnswer
                                        ? "bg-green-500/20 border border-green-500/50 text-green-200"
                                        : isUserAnswer
                                        ? "bg-red-500/20 border border-red-500/50 text-red-200"
                                        : "text-white/60"
                                    }`}
                                  >
                                    <strong>{letra})</strong> {texto as string}
                                    {!wasAnswered && isCorrectAnswer && (
                                      <span className="ml-2 text-xs text-green-400">
                                        (Correct answer)
                                      </span>
                                    )}
                                  </div>
                                );
                              }
                            )}
                          </div>
                          <div className="bg-blue-500/10 border border-blue-500/30 p-4 rounded-lg text-blue-200 text-sm">
                            <strong>Explanation:</strong> {question.explanation}
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center pt-6">
              <Link href="/dashboard">
                <Button
                  variant="outline"
                  className="text-white border-white/20 hover:bg-white/10 flex items-center gap-2 w-full sm:w-auto"
                >
                  <Home className="w-5 h-5" />
                  Return Home
                </Button>
              </Link>
              <Button
                onClick={resetQuiz}
                className="button-primary flex items-center gap-2 w-full sm:w-auto"
              >
                <RotateCcw className="w-5 h-5" />
                New Exam
              </Button>
            </div>
          </motion.div>
        </div>
      </div>
    );
  }

  return null;
}
