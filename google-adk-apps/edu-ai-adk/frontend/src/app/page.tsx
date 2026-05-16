"use client";

import Hero from "@/components/LandingPage/Hero";
import CallToAction from "@/components/LandingPage/CallToAction";
import Features from "@/components/LandingPage/Features";
import HowItWorks from "@/components/LandingPage/HowItWorks";

export default function Home() {
  return (
    <>
      <Hero />
      <Features />
      <HowItWorks />
      <CallToAction />
    </>
  );
}
