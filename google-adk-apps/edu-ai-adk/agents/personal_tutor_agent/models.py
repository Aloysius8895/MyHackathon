from pydantic import BaseModel, Field
from typing import List

class TutorRecommendation(BaseModel):
    priorities: List[str] = Field(..., description="Topics or skills the student needs to review")
    recommendation: str = Field(..., description="General educational guidance for the student")
    trigger_agents: List[str] = Field(..., description="List of agents to be triggered to generate content or practice exams")
