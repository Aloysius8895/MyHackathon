export type SimulatedQuestion = {
  question: string;
  alternatives: {
    A: string;
    B: string;
    C: string;
    D: string;
    E: string;
  };
  correct_answer: "A" | "B" | "C" | "D" | "E";
  explanation: string;
};

export type SimulatedExamResult = {
  questions: SimulatedQuestion[];
};
