from pydantic import BaseModel, Field

class Alternatives(BaseModel):
    A: str
    B: str
    C: str
    D: str
    E: str

class InterdisciplinaryQuestion(BaseModel):
    question: str = Field(..., description="The question prompt")
    alternatives: Alternatives = Field(..., description="Answer choices A–E")
    correct_answer: str = Field(..., pattern="^[A-E]$", description="Letter of the correct answer")
    explanation: str = Field(..., description="Explanation for the correct answer, highlighting the interdisciplinary reasoning")
