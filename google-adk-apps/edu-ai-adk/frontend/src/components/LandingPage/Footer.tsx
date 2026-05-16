import React from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  Bot,
  ArrowRight,
  Globe,
  Brain,
  FileText,
  BookOpen,
  BarChart3,
  Users,
  Sparkles,
} from "lucide-react";

const Footer = () => {
  return (
    <footer className="w-full py-16 bg-black/20 border-t border-white/10">
      <div className="container px-4 md:px-6">
        {/* Top section with branding and CTA */}
        <div className="text-center mb-12 max-w-4xl mx-auto">
          <h3 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Democratizing ENEM Education with{" "}
            <span className="gradient-text">AI Agents</span>
          </h3>
          <p className="text-white/70 text-lg mb-6 leading-relaxed">
            Built with Google's Agent Development Kit to break educational
            barriers and provide every Brazilian student with access to quality
            ENEM preparation.
          </p>
          <Link href="/dashboard">
            <Button className="button-primary px-8 py-4 text-lg flex items-center gap-3 mx-auto group">
              <Bot className="w-5 h-5" />
              Start Learning with AI Agents
              <ArrowRight className="w-5 h-5 transition-transform group-hover:translate-x-1" />
            </Button>
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
          <div className="space-y-4">
            <h3 className="text-2xl font-bold gradient-text">Edu.AI</h3>
            <p className="text-white/70 text-sm leading-relaxed">
              Transforming ENEM preparation through intelligent AI agents
              powered by Google's ADK. Making quality education accessible to
              all Brazilian students.
            </p>
            <div className="text-xs text-white/50">
              🚀 Built for Google Cloud Hackathon
            </div>
          </div>

          <div className="space-y-4">
            <h4 className="font-semibold text-white">AI Agents</h4>
            <ul className="space-y-2">
              <li>
                <Link
                  href="/dashboard"
                  className="text-white/70 hover:text-white text-sm flex items-center gap-2 group transition-colors"
                >
                  <FileText className="w-4 h-4 group-hover:text-purple-400" />
                  Essay Evaluator Agent
                </Link>
              </li>
              <li>
                <Link
                  href="/dashboard"
                  className="text-white/70 hover:text-white text-sm flex items-center gap-2 group transition-colors"
                >
                  <Brain className="w-4 h-4 group-hover:text-blue-400" />
                  Personal Tutor Agent
                </Link>
              </li>
              <li>
                <Link
                  href="/dashboard"
                  className="text-white/70 hover:text-white text-sm flex items-center gap-2 group transition-colors"
                >
                  <BookOpen className="w-4 h-4 group-hover:text-green-400" />
                  Exam Generator Agent
                </Link>
              </li>
              <li>
                <Link
                  href="/dashboard"
                  className="text-white/70 hover:text-white text-sm flex items-center gap-2 group transition-colors"
                >
                  <BarChart3 className="w-4 h-4 group-hover:text-orange-400" />
                  Progress Tracker Agent
                </Link>
              </li>
            </ul>
          </div>

          <div className="space-y-4">
            <h4 className="font-semibold text-white">Impact</h4>
            <ul className="space-y-2">
              <li className="text-white/70 text-sm flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-blue-400"></div>
                5M+ ENEM Students Annually
              </li>
              <li className="text-white/70 text-sm flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-purple-400"></div>8
                Specialized AI Agents
              </li>
              <li className="text-white/70 text-sm flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-green-400"></div>
                Free Quality Education
              </li>
              <li className="text-white/70 text-sm flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-orange-400"></div>
                24/7 AI Tutoring
              </li>
            </ul>
          </div>

          <div className="space-y-4">
            <h4 className="font-semibold text-white">Technology</h4>
            <ul className="space-y-2">
              <li className="text-white/70 text-sm">
                Google Agent Development Kit
              </li>
              <li className="text-white/70 text-sm">Google Cloud Platform</li>
              <li className="text-white/70 text-sm">Vertex AI & BigQuery</li>
              <li className="text-white/70 text-sm">
                Multi-Agent Orchestration
              </li>
            </ul>
          </div>
        </div>

        {/* Mission statement */}
        <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
            <div>
              <h4 className="text-xl font-bold text-white mb-3 flex items-center gap-2">
                <Globe className="w-5 h-5 text-blue-400" />
                Our Mission
              </h4>
              <p className="text-white/70 text-sm leading-relaxed">
                In Brazil, quality ENEM preparation often costs thousands of
                reais, creating educational inequality. Our AI agents
                democratize access to personalized, high-quality education for
                every student, regardless of their economic background or
                location.
              </p>
            </div>
            <div className="text-center md:text-right">
              <div className="inline-flex items-center gap-2 text-2xl font-bold text-white mb-2">
                <Sparkles className="w-6 h-6 text-yellow-400" />
                Breaking Barriers
              </div>
              <p className="text-white/60 text-sm">
                Through AI-Powered Education
              </p>
            </div>
          </div>
        </div>

        <div className="border-t border-white/10 pt-8 flex flex-col md:flex-row justify-between items-center">
          <div className="flex flex-col md:flex-row items-center gap-4 mb-4 md:mb-0">
            <p className="text-sm text-white/60">
              © 2025 Edu.AI - Democratizing Education through AI
            </p>
            <div className="flex items-center gap-2 text-xs text-white/40">
              <Bot className="w-3 h-3" />
              Powered by Google's Agent Development Kit
            </div>
          </div>

          <div className="flex items-center gap-4">
            <Link href="/dashboard">
              <Button variant="outline" className="button-secondary">
                <Users className="w-4 h-4 mr-2" />
                Try All Agents
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
