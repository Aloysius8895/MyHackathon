from pydantic import BaseModel, Field
from typing import List

class Flashcard(BaseModel):
    question: str = Field(..., description="The question side of the flashcard")
    answer: str = Field(..., description="The answer side of the flashcard")

class VideoSuggestion(BaseModel):
    title: str = Field(..., description="Video title")
    link: str = Field(..., description="YouTube URL to the video")
    description: str = Field(..., description="Short summary of the video's content")

class ContentOutput(BaseModel):
    text_explanation: str = Field(..., description="Clear and accessible explanation about the topic")
    topics_summary: List[str] = Field(..., description="Summary with the main points of the content")
    flashcards: List[Flashcard] = Field(..., description="List of flashcards with question and answer")
    video_suggestions: List[VideoSuggestion] = Field(..., description="List of suggested YouTube videos with metadata")
