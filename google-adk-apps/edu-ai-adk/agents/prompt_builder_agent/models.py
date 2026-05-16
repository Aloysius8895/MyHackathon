from pydantic import BaseModel, Field
from typing import List

class PromptOutput(BaseModel):
    topic: str = Field(..., description="Essay topic in the ENEM style")
    source_texts: List[str] = Field(..., description="Motivating texts based on the topic, with data, quotes, or social/historical context")
    instructions: str = Field(..., description="Instructions for the student to develop the argumentative essay")
