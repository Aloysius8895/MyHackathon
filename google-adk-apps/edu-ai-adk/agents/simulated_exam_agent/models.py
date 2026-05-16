from pydantic import BaseModel, Field
from typing import List

class Alternatives(BaseModel):
    A: str
    B: str
    C: str
    D: str
    E: str

class SimulatedQuestion(BaseModel):
    question: str = Field(..., description="ENEM-style question prompt")
    alternatives: Alternatives = Field(..., description="Answer choices A to E")
    correct_answer: str = Field(..., pattern="^[A-E]$", description="Correct answer letter")
    explanation: str = Field(..., description="Justification for the correct answer")

class SimulatedExamOutput(BaseModel):
    questions: List[SimulatedQuestion] = Field(..., description="List of generated ENEM-style questions")
