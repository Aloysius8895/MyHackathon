export type Mentor = {
  id: string;
  name: string;
  role: string;
  initials: string;
  industry: string;
  expertise: string[];
  stageExperience: string[];
  country: string;
  relationshipScore: number;
  activeRelationships: number;
  maxCapacity: number;
  feedbackScore: number;
  graphEvidence: string[];
  riskNote: string;
};

export const mentors: Mentor[] = [
  {
    id: "mentor-maya",
    name: "Maya Tan",
    role: "FinTech fundraising mentor",
    initials: "MT",
    industry: "FinTech",
    expertise: ["Fundraising", "Seed investment", "Investor readiness"],
    stageExperience: ["Pre-seed", "Seed"],
    country: "Malaysia",
    relationshipScore: 94,
    activeRelationships: 2,
    maxCapacity: 5,
    feedbackScore: 4.8,
    graphEvidence: [
      "Mentored 6 fintech startups with positive funding-readiness outcomes.",
      "Strong path: Company needs fundraising <- mentor expert_in fundraising.",
      "High admin feedback on clarity and founder preparedness.",
    ],
    riskNote: "Capacity is healthy, but admin should confirm availability before approval.",
  },
  {
    id: "mentor-arjun",
    name: "Arjun Mehta",
    role: "AI product go-to-market advisor",
    initials: "AM",
    industry: "AI / SaaS",
    expertise: ["Go-to-market", "B2B positioning", "Enterprise pilots"],
    stageExperience: ["Seed", "Growth"],
    country: "Singapore",
    relationshipScore: 89,
    activeRelationships: 3,
    maxCapacity: 4,
    feedbackScore: 4.6,
    graphEvidence: [
      "Previously supported AI startups moving from prototype to pilot.",
      "Semantic match between GTM, enterprise sales, and pilot design needs.",
      "Positive completion outcomes across three B2B relationships.",
    ],
    riskNote: "Near capacity. Assign only if the company needs GTM support urgently.",
  },
  {
    id: "mentor-sofia",
    name: "Sofia Rahman",
    role: "Healthcare ecosystem operator",
    initials: "SR",
    industry: "HealthTech",
    expertise: ["Partnerships", "Regulatory pathways", "Programme readiness"],
    stageExperience: ["Pilot", "Growth"],
    country: "Indonesia",
    relationshipScore: 86,
    activeRelationships: 1,
    maxCapacity: 3,
    feedbackScore: 4.7,
    graphEvidence: [
      "Mentored companies with healthcare partner linkage needs.",
      "Strong relationship path through programme-readiness support.",
      "Admin feedback marks her as high-trust for sensitive regulated sectors.",
    ],
    riskNote: "Best for HealthTech or regulated-sector companies, not general consumer apps.",
  },
  {
    id: "mentor-leon",
    name: "Leon Wong",
    role: "Operations and scaling mentor",
    initials: "LW",
    industry: "Marketplace / Logistics",
    expertise: ["Operations", "Unit economics", "Capacity planning"],
    stageExperience: ["Growth", "Scale-up"],
    country: "Malaysia",
    relationshipScore: 82,
    activeRelationships: 4,
    maxCapacity: 4,
    feedbackScore: 4.4,
    graphEvidence: [
      "Strong history with operationally complex startups.",
      "Useful path for companies needing capacity-aware growth planning.",
      "Feedback quality is strong but current mentor capacity is full.",
    ],
    riskNote: "Over capacity for new assignments unless an active relationship is completed.",
  },
];

export const featuredMentor = mentors[0];
