import { EssayEvaluationResult } from "@/types/EssayEvaluationResult";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  CheckCircle,
  TrendingUp,
  FileText,
  Star,
  Award,
  BarChart3,
  Brain,
  PenTool,
  Target,
  Lightbulb,
} from "lucide-react";

export default function FeedbackBox({ data }: { data: EssayEvaluationResult }) {
  const competencies = [
    {
      number: 1,
      title: "Standard Language Usage",
      score: data.comp1_score,
      feedback: data.comp1_feedback,
      icon: <PenTool className="h-6 w-6 text-white" />,
      color: "from-violet-600 to-purple-600",
    },
    {
      number: 2,
      title: "Topic Understanding",
      score: data.comp2_score,
      feedback: data.comp2_feedback,
      icon: <Brain className="h-6 w-6 text-white" />,
      color: "from-blue-600 to-indigo-600",
    },
    {
      number: 3,
      title: "Argumentation",
      score: data.comp3_score,
      feedback: data.comp3_feedback,
      icon: <Target className="h-6 w-6 text-white" />,
      color: "from-green-600 to-emerald-600",
    },
    {
      number: 4,
      title: "Cohesion and Coherence",
      score: data.comp4_score,
      feedback: data.comp4_feedback,
      icon: <BarChart3 className="h-6 w-6 text-white" />,
      color: "from-orange-600 to-red-600",
    },
    {
      number: 5,
      title: "Solution Proposal",
      score: data.comp5_score,
      feedback: data.comp5_feedback,
      icon: <Lightbulb className="h-6 w-6 text-white" />,
      color: "from-pink-600 to-purple-700",
    },
  ];

  const getScoreColor = (score: number) => {
    if (score >= 160) return "text-green-400";
    if (score >= 120) return "text-yellow-400";
    if (score >= 80) return "text-orange-400";
    return "text-red-400";
  };

  const getScoreLabel = (score: number) => {
    if (score >= 160) return "Excellent";
    if (score >= 120) return "Good";
    if (score >= 80) return "Fair";
    return "Needs Improvement";
  };

  return (
    <div className="space-y-8">
      {/* Header with total score */}
      <div className="glass-card p-8 text-center">
        <div className="flex items-center justify-center mb-4">
          <Award className="h-8 w-8 text-yellow-400 mr-3" />
          <h2 className="text-3xl md:text-4xl font-bold text-white">
            Evaluation <span className="gradient-text">Results</span>
          </h2>
        </div>

        <div className="mb-6">
          <div className="text-6xl md:text-7xl font-bold text-white mb-2">
            {data.total_score}
            <span className="text-3xl text-white/60 ml-2">/ 1000</span>
          </div>
          <div
            className={`text-xl font-semibold ${getScoreColor(
              data.total_score
            )}`}
          >
            {getScoreLabel(data.total_score)}
          </div>
        </div>

        <div className="bg-white/5 rounded-full h-4 max-w-md mx-auto mb-4">
          <div
            className="bg-gradient-to-r from-blue-500 to-purple-500 h-4 rounded-full transition-all duration-1000"
            style={{ width: `${(data.total_score / 1000) * 100}%` }}
          ></div>
        </div>

        <p className="text-white/70 text-lg">
          Your essay was evaluated based on ENEM's 5 competencies
        </p>
      </div>

      {/* Competencies grid - 3 + 2 layout */}
      <div className="space-y-6">
        {/* First row - 3 competencies */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {competencies.slice(0, 3).map((comp, index) => (
            <div key={index} className="group relative">
              <div
                className={`absolute -inset-0.5 bg-gradient-to-r ${comp.color} opacity-20 group-hover:opacity-40 transition-opacity duration-300 rounded-2xl blur-sm`}
              ></div>

              <Card className="relative h-full bg-black/40 border-white/10 hover:border-white/20 transition-all duration-300 backdrop-blur-sm">
                <CardHeader className="pb-4">
                  <div className="flex items-center justify-between mb-4">
                    <div
                      className={`w-14 h-14 rounded-xl bg-gradient-to-r ${comp.color} flex items-center justify-center shadow-lg`}
                    >
                      {comp.icon}
                    </div>
                    <span className="text-xs px-2 py-1 bg-white/10 text-white/70 rounded-full">
                      Comp. {comp.number}
                    </span>
                  </div>

                  <CardTitle className="text-xl text-white font-semibold leading-tight">
                    {comp.title}
                  </CardTitle>
                </CardHeader>

                <CardContent className="space-y-4">
                  <div className="text-center">
                    <div className="flex items-center justify-center gap-2 mb-3">
                      <span
                        className={`text-4xl font-bold ${getScoreColor(
                          comp.score
                        )}`}
                      >
                        {comp.score}
                      </span>
                      <span className="text-white/60 text-lg">/ 200</span>
                    </div>

                    <div className="bg-white/5 rounded-full h-3 mb-3">
                      <div
                        className={`bg-gradient-to-r ${comp.color} h-3 rounded-full transition-all duration-1000`}
                        style={{ width: `${(comp.score / 200) * 100}%` }}
                      ></div>
                    </div>

                    <span
                      className={`text-sm font-medium ${getScoreColor(
                        comp.score
                      )}`}
                    >
                      {getScoreLabel(comp.score)}
                    </span>
                  </div>

                  <CardDescription className="text-white/70 text-base leading-relaxed">
                    {comp.feedback}
                  </CardDescription>
                </CardContent>
              </Card>
            </div>
          ))}
        </div>

        {/* Second row - 2 competencies centered */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
          {competencies.slice(3, 5).map((comp, index) => (
            <div key={index + 3} className="group relative">
              <div
                className={`absolute -inset-0.5 bg-gradient-to-r ${comp.color} opacity-20 group-hover:opacity-40 transition-opacity duration-300 rounded-2xl blur-sm`}
              ></div>

              <Card className="relative h-full bg-black/40 border-white/10 hover:border-white/20 transition-all duration-300 backdrop-blur-sm">
                <CardHeader className="pb-4">
                  <div className="flex items-center justify-between mb-4">
                    <div
                      className={`w-14 h-14 rounded-xl bg-gradient-to-r ${comp.color} flex items-center justify-center shadow-lg`}
                    >
                      {comp.icon}
                    </div>
                    <span className="text-xs px-2 py-1 bg-white/10 text-white/70 rounded-full">
                      Comp. {comp.number}
                    </span>
                  </div>

                  <CardTitle className="text-xl text-white font-semibold leading-tight">
                    {comp.title}
                  </CardTitle>
                </CardHeader>

                <CardContent className="space-y-4">
                  <div className="text-center">
                    <div className="flex items-center justify-center gap-2 mb-3">
                      <span
                        className={`text-4xl font-bold ${getScoreColor(
                          comp.score
                        )}`}
                      >
                        {comp.score}
                      </span>
                      <span className="text-white/60 text-lg">/ 200</span>
                    </div>

                    <div className="bg-white/5 rounded-full h-3 mb-3">
                      <div
                        className={`bg-gradient-to-r ${comp.color} h-3 rounded-full transition-all duration-1000`}
                        style={{ width: `${(comp.score / 200) * 100}%` }}
                      ></div>
                    </div>

                    <span
                      className={`text-sm font-medium ${getScoreColor(
                        comp.score
                      )}`}
                    >
                      {getScoreLabel(comp.score)}
                    </span>
                  </div>

                  <CardDescription className="text-white/70 text-base leading-relaxed">
                    {comp.feedback}
                  </CardDescription>
                </CardContent>
              </Card>
            </div>
          ))}
        </div>
      </div>

      {/* Overall feedback */}
      {data.overall_feedback && (
        <div className="glass-card p-8">
          <div className="flex items-center mb-6">
            <FileText className="h-6 w-6 text-blue-400 mr-3" />
            <h3 className="text-2xl font-bold text-white">
              Overall <span className="gradient-text">Feedback</span>
            </h3>
          </div>

          <div className="bg-white/5 rounded-xl p-6 border border-white/10">
            <p className="text-white/80 text-base leading-relaxed whitespace-pre-wrap">
              {data.overall_feedback}
            </p>
          </div>
        </div>
      )}

      {/* Action suggestions */}
      <div className="glass-card p-8">
        <div className="flex items-center mb-6">
          <TrendingUp className="h-6 w-6 text-green-400 mr-3" />
          <h3 className="text-2xl font-bold text-white">
            Next <span className="gradient-text">Steps</span>
          </h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white/5 rounded-xl p-4 border border-white/10">
            <div className="flex items-center mb-2">
              <CheckCircle className="h-5 w-5 text-green-400 mr-2" />
              <span className="text-white font-medium">Keep Practicing</span>
            </div>
            <p className="text-white/70 text-sm">
              Continue practicing with new topics to improve your competencies
            </p>
          </div>

          <div className="bg-white/5 rounded-xl p-4 border border-white/10">
            <div className="flex items-center mb-2">
              <Star className="h-5 w-5 text-yellow-400 mr-2" />
              <span className="text-white font-medium">
                Focus on Weak Points
              </span>
            </div>
            <p className="text-white/70 text-sm">
              Focus on competencies with lower scores to balance your
              performance
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
