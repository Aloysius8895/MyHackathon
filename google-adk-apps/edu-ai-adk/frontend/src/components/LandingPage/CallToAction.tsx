import React from "react";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import {
  ArrowRight,
  FileText,
  BarChart,
  Users,
  Award,
  Star,
  Bot,
  Zap,
  Globe,
  Brain,
  Target,
  BookOpen,
  Sparkles,
  TrendingUp,
} from "lucide-react";

const CallToAction = () => {
  return (
    <section className="w-full py-16 md:py-24 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-r from-purple-900/20 to-pink-900/20"></div>
      <div className="absolute -top-24 -right-24 w-96 h-96 bg-gradient-to-r from-blue-600/10 to-purple-600/10 rounded-full blur-3xl"></div>
      <div className="absolute -bottom-24 -left-24 w-96 h-96 bg-gradient-to-r from-purple-600/10 to-pink-600/10 rounded-full blur-3xl"></div>

      <div className="px-4 md:px-6 relative">
        <div className="glass-card max-w-7xl mx-auto p-8 md:p-12">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Text content */}
            <div className="text-center lg:text-left">
              <div className="inline-flex items-center justify-center lg:justify-start px-4 py-2 mb-6 border border-white/10 rounded-full bg-white/5 backdrop-blur-sm">
                <Globe className="w-4 h-4 mr-2 text-blue-400" />
                <span className="text-sm font-medium text-white/80">
                  Democratizing Education with Google ADK
                </span>
              </div>

              <h2 className="text-3xl md:text-5xl font-bold tracking-tighter mb-6 text-white">
                Ready to Transform
                <br />
                <span className="gradient-text">Brazil's Education</span>?
              </h2>

              <p className="text-lg md:text-xl text-white/70 mb-8 leading-relaxed">
                Join our mission to democratize quality ENEM preparation.
                Experience the power of AI agents working together to provide
                personalized education that was once only available to the
                privileged few.
              </p>

              {/* Impact metrics */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                <div className="text-center">
                  <div className="text-2xl font-bold text-white mb-1">5M+</div>
                  <div className="text-white/60 text-sm">ENEM Students</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-white mb-1">8</div>
                  <div className="text-white/60 text-sm">AI Agents</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-white mb-1">Free</div>
                  <div className="text-white/60 text-sm">Access</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-white mb-1">24/7</div>
                  <div className="text-white/60 text-sm">Available</div>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row justify-center lg:justify-start gap-4">
                <Link href="/dashboard">
                  <Button className="button-primary text-lg px-8 py-4 group">
                    <Bot className="mr-2 h-5 w-5" />
                    Experience AI Agents
                    <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
                  </Button>
                </Link>
              </div>
            </div>

            {/* Agent showcase cards */}
            <div className="grid grid-cols-2 gap-4">
              {/* Agent card 1 */}
              <div className="bg-black/40 backdrop-blur-md border border-white/10 p-6 rounded-2xl relative overflow-hidden group hover:border-white/20 transition-all hover:transform hover:scale-105">
                <div className="absolute -inset-1 bg-gradient-to-r from-purple-600/20 to-pink-600/20 rounded-2xl opacity-0 group-hover:opacity-100 transition-all blur-xl"></div>
                <div className="relative z-10 text-center">
                  <div className="w-14 h-14 rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 flex items-center justify-center mb-4 mx-auto">
                    <FileText className="h-7 w-7 text-white" />
                  </div>
                  <h3 className="text-lg font-semibold text-white mb-2">
                    Essay Evaluator
                  </h3>
                  <p className="text-sm text-white/70 mb-3">
                    AI agent that provides detailed ENEM essay feedback
                  </p>
                  <Link href="/dashboard">
                    <Button
                      variant="outline"
                      size="sm"
                      className="w-full bg-white/10 border-white/20 text-white hover:bg-white/20"
                    >
                      <Zap className="w-4 h-4 mr-1" />
                      Try Now
                    </Button>
                  </Link>
                </div>
              </div>

              {/* Agent card 2 */}
              <div className="bg-black/40 backdrop-blur-md border border-white/10 p-6 rounded-2xl relative overflow-hidden group hover:border-white/20 transition-all hover:transform hover:scale-105">
                <div className="absolute -inset-1 bg-gradient-to-r from-blue-600/20 to-cyan-600/20 rounded-2xl opacity-0 group-hover:opacity-100 transition-all blur-xl"></div>
                <div className="relative z-10 text-center">
                  <div className="w-14 h-14 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-600 flex items-center justify-center mb-4 mx-auto">
                    <Brain className="h-7 w-7 text-white" />
                  </div>
                  <h3 className="text-lg font-semibold text-white mb-2">
                    Personal Tutor
                  </h3>
                  <p className="text-sm text-white/70 mb-3">
                    Adaptive learning agent for personalized study paths
                  </p>
                  <Link href="/dashboard">
                    <Button
                      variant="outline"
                      size="sm"
                      className="w-full bg-white/10 border-white/20 text-white hover:bg-white/20"
                    >
                      <Zap className="w-4 h-4 mr-1" />
                      Try Now
                    </Button>
                  </Link>
                </div>
              </div>

              {/* Agent card 3 */}
              <div className="bg-black/40 backdrop-blur-md border border-white/10 p-6 rounded-2xl relative overflow-hidden group hover:border-white/20 transition-all hover:transform hover:scale-105">
                <div className="absolute -inset-1 bg-gradient-to-r from-green-600/20 to-emerald-600/20 rounded-2xl opacity-0 group-hover:opacity-100 transition-all blur-xl"></div>
                <div className="relative z-10 text-center">
                  <div className="w-14 h-14 rounded-xl bg-gradient-to-r from-green-600 to-emerald-600 flex items-center justify-center mb-4 mx-auto">
                    <BookOpen className="h-7 w-7 text-white" />
                  </div>
                  <h3 className="text-lg font-semibold text-white mb-2">
                    Exam Generator
                  </h3>
                  <p className="text-sm text-white/70 mb-3">
                    Creates personalized practice exams for all subjects
                  </p>
                  <Link href="/dashboard">
                    <Button
                      variant="outline"
                      size="sm"
                      className="w-full bg-white/10 border-white/20 text-white hover:bg-white/20"
                    >
                      <Zap className="w-4 h-4 mr-1" />
                      Try Now
                    </Button>
                  </Link>
                </div>
              </div>

              {/* Agent card 4 */}
              <div className="bg-black/40 backdrop-blur-md border border-white/10 p-6 rounded-2xl relative overflow-hidden group hover:border-white/20 transition-all hover:transform hover:scale-105">
                <div className="absolute -inset-1 bg-gradient-to-r from-amber-600/20 to-orange-600/20 rounded-2xl opacity-0 group-hover:opacity-100 transition-all blur-xl"></div>
                <div className="relative z-10 text-center">
                  <div className="w-14 h-14 rounded-xl bg-gradient-to-r from-amber-600 to-orange-600 flex items-center justify-center mb-4 mx-auto">
                    <TrendingUp className="h-7 w-7 text-white" />
                  </div>
                  <h3 className="text-lg font-semibold text-white mb-2">
                    Progress Tracker
                  </h3>
                  <p className="text-sm text-white/70 mb-3">
                    Intelligent analytics and performance monitoring
                  </p>
                  <Link href="/dashboard">
                    <Button
                      variant="outline"
                      size="sm"
                      className="w-full bg-white/10 border-white/20 text-white hover:bg-white/20"
                    >
                      <Zap className="w-4 h-4 mr-1" />
                      Try Now
                    </Button>
                  </Link>
                </div>
              </div>
            </div>
          </div>

          {/* Bottom CTA section */}
          <div className="border-t border-white/10 mt-12 pt-8">
            <div className="text-center max-w-4xl mx-auto">
              <h3 className="text-2xl md:text-3xl font-bold text-white mb-4">
                🌟 Built for Google Cloud & ADK Hackathon
              </h3>
              <p className="text-white/70 text-lg mb-6 leading-relaxed">
                This project showcases the power of Google's Agent Development
                Kit (ADK) in solving real-world challenges, along with Google
                Cloud. We have a mission to democratize access to quality
                education for millions of Brazilian students.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CallToAction;
