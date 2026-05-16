from pydantic import BaseModel, Field

class EssayEvaluationResult(BaseModel):
    extracted_essay: str = Field(..., description="Extracted text from the student's essay")
    comp1_score: int = Field(..., ge=0, le=200, description="Score for Competency 1: formal written language")
    comp1_feedback: str = Field(..., description="Feedback for Competency 1")
    comp2_score: int = Field(..., ge=0, le=200, description="Score for Competency 2: understanding and developing the topic")
    comp2_feedback: str = Field(..., description="Feedback for Competency 2")
    comp3_score: int = Field(..., ge=0, le=200, description="Score for Competency 3: argumentation and critical thinking")
    comp3_feedback: str = Field(..., description="Feedback for Competency 3")
    comp4_score: int = Field(..., ge=0, le=200, description="Score for Competency 4: coherence and cohesion")
    comp4_feedback: str = Field(..., description="Feedback for Competency 4")
    comp5_score: int = Field(..., ge=0, le=200, description="Score for Competency 5: proposal of intervention")
    comp5_feedback: str = Field(..., description="Feedback for Competency 5")
    total_score: int = Field(..., ge=0, le=1000, description="Total score for the essay (sum of all competencies)")
    overall_feedback: str = Field(..., description="General feedback summarizing the essay's performance")
