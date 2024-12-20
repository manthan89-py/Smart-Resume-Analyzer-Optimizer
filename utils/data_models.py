from pydantic import BaseModel, Field
from typing import List


class CategoryBreakdowns(BaseModel):
    keyword_optimization: int
    structural_formatting: int
    content_quality: int
    professional_narrative: int
    additional_factors: int


class ATSScore(BaseModel):
    overall_score: int
    category_breakdowns: CategoryBreakdowns


class FinalResult(BaseModel):
    ats_score: ATSScore
    detailed_recommendations: List[str]
    improvement_strategies: List[str]


class MarkdownResult(BaseModel):
    content: str = Field(description="Fully transformed Markdown resume document.")
    changes: List[str] = Field(
        description="Track changes you made in resume content. Provide the exact words or section you have added or modified in the resume."
    )
    additional: str = Field(
        description="Additional answer to the user additional instructions. If no additional instructions provided then make this empty. Make sure output is normal text and not a markdown text."
    )

class JobComparisionResult(BaseModel):
    analysis: str = Field(description="Analysis of job description and resume")
    percentage_of_chances: int = Field(
        description="percentage for candidate to get selected for given job descriptions. This should be approximately percentage based on the resume and job description candidate can get selected."
    )
    suggestions: str = Field(
        description="To get selected for job description what candidate needs to do provide some suggestions"
    )
