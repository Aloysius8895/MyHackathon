import React from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  ArrowRight,
  Upload,
  Bot,
  BarChart3,
  Target,
  Zap,
  Users,
  BookOpen,
  FileText,
  Brain,
} from "lucide-react";

const HowItWorks = () => {
  const steps = [
    {
      number: "01",
      title: "Upload Your Content",
      description:
        "Submit essays, take practice exams, or ask questions. Our multi-modal agents can process text, images, and voice inputs for maximum accessibility.",
      icon: <Upload className="w-6 h-6 text-white" />,
      agents: ["Essay Evaluator", "Image Processing"],
      color: "from-blue-600 to-indigo-600",
    },
    {
      number: "02",
      title: "AI Agents Collaborate",
      description:
        "Multiple specialized agents work together using Google's ADK - analyzing, generating content, and creating personalized learning paths tailored to your needs.",
      icon: <Bot className="w-6 h-6 text-white" />,
      agents: ["Personal Tutor", "Content Generator", "Analyzer"],
      color: "from-purple-600 to-pink-600",
    },
    {
      number: "03",
      title: "Get Instant Feedback",
      description:
        "Receive detailed ENEM-aligned feedback, practice materials, and improvement suggestions. All powered by AI that understands Brazilian education standards.",
      icon: <FileText className="w-6 h-6 text-white" />,
      agents: ["Essay Evaluator", "Rephraser", "Prompt Builder"],
      color: "from-green-600 to-emerald-600",
    },
    {
      number: "04",
      title: "Track Your Progress",
      description:
        "Monitor your improvement across all ENEM competencies with intelligent analytics. The Progress Tracker Agent provides insights that adapt your learning journey.",
      icon: <BarChart3 className="w-6 h-6 text-white" />,
      agents: ["Progress Tracker", "Personal Tutor"],
      color: "from-orange-600 to-red-600",
    },
  ];

  return (
    <section id="how-it-works" className="w-full py-16 md:py-24 bg-black/5">
      <div className="px-4 md:px-6">
        <div className="text-center mb-16 max-w-4xl mx-auto">
          <div className="inline-flex items-center justify-center px-4 py-2 mb-6 border border-white/10 rounded-full bg-white/5 backdrop-blur-sm">
            <Brain className="w-4 h-4 mr-2 text-purple-400" />
            <span className="text-sm font-medium text-white/80">
              Intelligent Agent Orchestration
            </span>
          </div>

          <h2 className="text-3xl md:text-5xl font-bold tracking-tighter mb-6">
            How Our <span className="gradient-text">AI Agents</span>
            <br />
            Transform ENEM Learning
          </h2>
          <p className="text-lg md:text-xl text-white/70 max-w-3xl mx-auto leading-relaxed">
            Experience the power of Google's Agent Development Kit as our
            specialized AI agents work together to democratize quality education
            for every Brazilian student.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 max-w-6xl mx-auto mb-16">
          {steps.map((step, index) => (
            <div key={index} className="group relative">
              <div
                className={`absolute -inset-0.5 bg-gradient-to-r ${step.color} opacity-20 group-hover:opacity-40 transition-opacity duration-300 rounded-2xl blur-sm`}
              ></div>

              <div className="relative bg-black/40 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:border-white/20 transition-all duration-300 group-hover:transform group-hover:scale-[1.02] min-h-72">
                <div className="flex items-start gap-6">
                  <div
                    className={`w-16 h-16 rounded-xl bg-gradient-to-r ${step.color} flex items-center justify-center shadow-lg`}
                  >
                    {step.icon}
                  </div>

                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-3">
                      <span className="text-2xl font-bold text-white/40">
                        {step.number}
                      </span>
                      <h3 className="text-xl md:text-2xl font-semibold text-white">
                        {step.title}
                      </h3>
                    </div>

                    <p className="text-white/70 text-base leading-relaxed mb-4">
                      {step.description}
                    </p>

                    <div className="space-y-2">
                      <p className="text-white font-medium text-sm">
                        Active Agents:
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {step.agents.map((agent, idx) => (
                          <span
                            key={idx}
                            className="px-3 py-1 bg-white/10 border border-white/20 rounded-full text-xs text-white/80"
                          >
                            {agent}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="max-w-5xl mx-auto">
          <div className="bg-gradient-to-r from-purple-600/10 to-pink-600/10 backdrop-blur-sm border border-white/10 rounded-3xl p-8 md:p-12 text-center">
            <h3 className="text-2xl md:text-3xl font-bold text-white mb-4">
              🌍 Breaking Educational Barriers in Brazil
            </h3>
            <p className="text-white/70 text-lg leading-relaxed mb-8 max-w-3xl mx-auto">
              In a country where quality ENEM preparation can cost thousands of
              reais, our AI agents provide the same level of personalized
              education for free. We're not just building technology - we're
              democratizing access to higher education for 5+ million Brazilian
              students.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="text-center">
                <div className="text-3xl font-bold text-white mb-2">Free</div>
                <div className="text-white/60">High-Quality Education</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-white mb-2">24/7</div>
                <div className="text-white/60">AI Tutoring Available</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-white mb-2">8</div>
                <div className="text-white/60">Specialized Agents</div>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/dashboard">
                <Button className="button-primary px-8 py-4 text-lg flex items-center gap-3">
                  <Target className="w-5 h-5" />
                  Start Your ENEM Journey
                  <ArrowRight className="w-5 h-5" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
