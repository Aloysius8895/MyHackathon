from typing import List, Dict
from pydantic import BaseModel, Field

class Essay(BaseModel):
    topic: str
    total_score: int
    date: str

class PracticeExam(BaseModel):
    area: str
    score: int
    date: str

class Progress(BaseModel):
    essays: List[Essay]
    practice_exams: List[PracticeExam]
    average_by_area: Dict[str, float]
    recommendations: List[str]
