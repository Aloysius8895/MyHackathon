"use client";

import { useState } from "react";

interface FlashcardProps {
  question: string;
  answer: string;
}

export default function Flashcard({ question, answer }: FlashcardProps) {
  const [isFlipped, setIsFlipped] = useState(false);

  return (
    <div
      className="relative h-48 cursor-pointer"
      onClick={() => setIsFlipped(!isFlipped)}
      style={{ perspective: "1000px" }}
    >
      <div
        className={`relative w-full h-full transition-transform duration-700 transform-style-3d ${
          isFlipped ? "rotate-y-180" : ""
        }`}
      >
        {/* Front side (Question) */}
        <div className="absolute w-full h-full rounded-xl border border-white/20 bg-white/5 p-6 flex flex-col justify-between backface-hidden">
          <div className="flex-1 flex items-center justify-center text-center">
            <p className="text-white text-lg">{question}</p>
          </div>
          <p className="text-white/50 text-sm text-center">
            Click to reveal answer
          </p>
        </div>

        {/* Back side (Answer) */}
        <div className="absolute w-full h-full rounded-xl border border-white/20 bg-white/5 p-6 flex flex-col justify-between backface-hidden rotate-y-180">
          <div className="flex-1 flex items-center justify-center text-center">
            <p className="text-white text-lg">{answer}</p>
          </div>
          <p className="text-white/50 text-sm text-center">
            Click to see question
          </p>
        </div>
      </div>
    </div>
  );
}
