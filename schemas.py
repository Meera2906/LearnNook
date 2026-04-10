from pydantic import BaseModel, Field
from typing import List, Optional

class SessionStartRequest(BaseModel):
    class_grade: str = Field(..., example="8th")
    subject: str = Field(..., example="Math")
    topic: str = Field(..., example="Fractions")

class EvaluateRequest(BaseModel):
    session_id: str
    answers: List[int] # List of indices for MCQs

class MCQQuestion(BaseModel):
    question: str
    options: List[str]
    correct_index: int
    explanation: str # Why the correct answer is correct
    hint: str # Brief one-line educational hint

class PerQuestionFeedback(BaseModel):
    correct: bool
    partial: Optional[bool] = False
    comment: str
    explanation: str

class SessionStartResponse(BaseModel):
    session_id: str
    explanation: str
    image_url: Optional[str] = None
    questions: List[MCQQuestion]
    cached: bool = False

class EvaluateResponse(BaseModel):
    score: str
    feedback: str
    per_question: List[PerQuestionFeedback]
