from pydantic import BaseModel, Field

class RephrasingSuggestion(BaseModel):
    original: str = Field(..., description="Original text submitted by the student")
    rewritten: str = Field(..., description="Improved rewrite suggestion")
    explanation: str = Field(..., description="Clear explanation of the improvements made")
