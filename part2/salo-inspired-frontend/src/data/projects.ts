import orbitDesktop from "../assets/projects/orbit-desktop.svg?url";
import orbitMobile from "../assets/projects/orbit-mobile.svg?url";
import auroraDesktop from "../assets/projects/aurora-desktop.svg?url";
import auroraMobile from "../assets/projects/aurora-mobile.svg?url";
import northstarDesktop from "../assets/projects/northstar-desktop.svg?url";
import northstarMobile from "../assets/projects/northstar-mobile.svg?url";
import tideDesktop from "../assets/projects/tide-desktop.svg?url";
import tideMobile from "../assets/projects/tide-mobile.svg?url";

export type Project = {
  slug: string;
  client: string;
  logoText: string;
  category: string;
  categoryColor: string;
  title: string;
  description: string;
  desktopImage: string;
  mobileImage: string;
};

export const projects: Project[] = [
  {
    slug: "profile-extraction",
    client: "Profile Intelligence",
    logoText: "PI",
    category: "Step 1",
    categoryColor: "var(--color-purple)",
    title: "Turning messy ecosystem profiles into structured matching data",
    description:
      "Gemini extracts industry, stage, needs, expertise, country, availability, capacity, and missing fields before any match is suggested.",
    desktopImage: orbitDesktop,
    mobileImage: orbitMobile,
  },
  {
    slug: "hybrid-matching",
    client: "Hybrid Matching",
    logoText: "HM",
    category: "Steps 2-4",
    categoryColor: "var(--color-green)",
    title: "Filtering, retrieving, and scoring mentors with transparent logic",
    description:
      "Hard eligibility rules remove invalid pairs, hybrid retrieval finds relevant mentors, and weighted scoring explains the rank.",
    desktopImage: auroraDesktop,
    mobileImage: auroraMobile,
  },
  {
    slug: "relationship-graph",
    client: "Relationship Graph",
    logoText: "RG",
    category: "Step 5",
    categoryColor: "var(--color-cyan)",
    title: "Reusing relationship evidence instead of one-off assignments",
    description:
      "Graph-lite edges connect companies, needs, mentors, expertise, outcomes, countries, and programmes to improve future matches.",
    desktopImage: northstarDesktop,
    mobileImage: northstarMobile,
  },
  {
    slug: "feedback-learning",
    client: "Feedback Learning",
    logoText: "FL",
    category: "Steps 6-10",
    categoryColor: "var(--color-yellow)",
    title: "Approving, creating, and improving ecosystem relationships",
    description:
      "Capacity-aware assignment, admin approval, relationship entities, and Bayesian feedback turn each match into reusable intelligence.",
    desktopImage: tideDesktop,
    mobileImage: tideMobile,
  },
];
