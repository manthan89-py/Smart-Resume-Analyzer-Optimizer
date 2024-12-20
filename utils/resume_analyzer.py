import PyPDF2
from typing import Dict, Any
from .prompts import (
    get_resume_analyzer_prompt,
    get_markdown_report_prompt,
    get_comparision_with_job_description_prompt,
)

from .llm_models import get_response_from_llm_model, SUPPORTED_MODELS


class ResumeAnalyzer:
    def __init__(self):
        self.supported_models = SUPPORTED_MODELS

    def extract_pdf_content(self, pdf_file) -> Dict[str, str]:
        """
        Extract text content from PDF and segment into sections
        """
        with open(pdf_file, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            full_text = ""

            # Extract full text
            for page in pdf_reader.pages:
                full_text += page.extract_text()

            sections = {"content": full_text}
            return sections

    def _extract_section(
        self, text: str, start_keyword: str, end_keyword: str = None
    ) -> str:
        """
        Extract a specific section from text
        """
        text = text.lower()
        start_idx = text.find(start_keyword)
        if start_idx == -1:
            return ""

        if end_keyword:
            end_idx = text.find(end_keyword, start_idx)
            return text[start_idx:end_idx] if end_idx != -1 else text[start_idx:]

        return text[start_idx:]

    def analyze_resume(
        self, sections: Dict[str, str], model: str, api_key: str
    ) -> Dict[str, Any]:
        """
        Analyze resume using selected LLM
        """
        prompt = get_resume_analyzer_prompt(resume_content=sections)
        response = get_response_from_llm_model(model, api_key, prompt)
        return response

    def markdown_report(
        self,
        model,
        api_key,
        suggestions,
        additional_insturctions,
        resume_content,
        filename,
    ):
        prompt = get_markdown_report_prompt(
            suggestions, resume_content, additional_insturctions
        )
        filename = filename.split("/")[-1]
        filename = filename.split(".")[0]
        response = get_response_from_llm_model(model, api_key, prompt)
        with open(f"Resumes/{filename}_updated_resume.md", "w") as f:
            f.write(response.get("content", ""))
        response["content"] = (
            f"Your updated resume has been successfully saved as 'Resumes/{filename}_updated_resume.md' on your local device. For a summary of the modifications made, please refer to the below section. You can also view the updated version of your resume in the 'Updated Resume' section. If you’d like to make further changes, feel free to provide additional instructions in the 'Resume Analysis' section."
        )
        return response

    def compare_with_job_descriptions(
        self, model, api_key, resume_content, job_descriptions
    ):
        job_descriptions = job_descriptions.strip()
        if len(job_descriptions):
            prompt = get_comparision_with_job_description_prompt(
                resume_content, job_descriptions
            )
            response = get_response_from_llm_model(model, api_key, prompt)
            return response
        else:
            {
                "analysis": "No job description provided.",
                "percentage_of_chances": "N/A",
                "suggestions": "N/A",
            }
