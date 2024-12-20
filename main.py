import gradio as gr
from utils.resume_analyzer import ResumeAnalyzer
from utils.ui_components import (
    load_markdown_content,
    format_ats_score,
    format_detailed_report,
    format_job_comparison,
    format_recommendations,
    format_strategies,
)
from typing import Dict, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the ResumeAnalyzer instance
analyzer = ResumeAnalyzer()


def process_resume(
    pdf_file: str,
    model: str,
    huggingface_model_name: str,
    ollama_model_name: str,
    groq_model_name: str,
    api_key: str,
    additional_instructions: str,
    job_descriptions: str,
) -> Tuple[str, str, str, str]:
    """Process the resume and generate analysis reports."""
    try:
        # Validate inputs
        if not pdf_file:
            raise ValueError("Please upload a PDF file")

        # Extract content
        sections = analyzer.extract_pdf_content(pdf_file)

        # Prepare model configuration
        model_config = prepare_model_config(
            model, huggingface_model_name, ollama_model_name, groq_model_name
        )

        # Analyze resume
        result = analyzer.analyze_resume(sections, model_config, api_key)

        # Generate suggestions
        suggestions = {
            "detailed_recommendations": result.get("detailed_recommendations", []),
            "improvement_strategies": result.get("improvement_strategies", []),
        }

        # Generate reports
        report = analyzer.markdown_report(
            model_config,
            api_key,
            suggestions,
            additional_instructions or "",
            sections,
            pdf_file,
        )

        # Compare with job descriptions if provided
        comparison_of_jd = analyzer.compare_with_job_descriptions(
            model_config, api_key, sections, job_descriptions
        )

        # Load markdown content
        markdown_content = load_markdown_content_from_file(pdf_file)

        # Format outputs
        return format_outputs(result, report, comparison_of_jd, markdown_content)

    except Exception as e:
        logger.error(f"Error processing resume: {str(e)}", exc_info=True)
        return create_error_message(e), "", "", ""


def create_interface() -> gr.Blocks:
    """Create and return the Gradio interface."""
    with gr.Blocks(
        title="Smart Resume Analyzer & Optimizer",
        css="footer {visibility: hidden} .container { max-width: 1200px; margin: 0 auto; }",
    ) as demo:
        create_header()

        with gr.Tabs():
            with gr.TabItem("📝 Resume Analysis", id=1):
                input_components = create_input_section()
                analysis_output = gr.HTML(label="Analysis Results")

            with gr.TabItem("📊 Detailed Reports", id=2):
                report_output = gr.HTML(label="Enhanced Content Report")
                comparison_output = gr.HTML(label="Job Match Analysis")

            with gr.TabItem("📄 Optimized Resume", id=3):
                markdown_output = gr.Markdown()

        setup_event_handlers(
            input_components,
            [analysis_output, report_output, comparison_output, markdown_output],
        )

    return demo


def setup_event_handlers(inputs: Dict, outputs: list):
    """Setup event handlers for the interface."""
    # Model selection handlers
    inputs["model_dropdown"].change(
        fn=lambda x: (
            gr.update(
                visible=x == "HuggingFace Inference API",
                value="" if x != "HuggingFace Inference API" else None,
            ),
            gr.update(
                visible=x == "Ollama Model", value="" if x != "Ollama Model" else None
            ),
            gr.update(
                visible=x == "Groq Model", value="" if x != "Groq Model" else None
            ),
            gr.update(visible=x != "Ollama Model"),
        ),
        inputs=[inputs["model_dropdown"]],
        outputs=[
            inputs["hf_model_input"],
            inputs["ollama_model_input"],
            inputs["groq_model_input"],
            inputs["api_key_input"],
        ],
    )

    # Submit button handler remains the same
    inputs["submit_btn"].click(
        fn=process_resume,
        inputs=[
            inputs["pdf_input"],
            inputs["model_dropdown"],
            inputs["hf_model_input"],
            inputs["ollama_model_input"],
            inputs["groq_model_input"],
            inputs["api_key_input"],
            inputs["additional_instructions"],
            inputs["job_descriptions"],
        ],
        outputs=outputs,
    )


def create_header():
    """Create the application header."""
    gr.Markdown(
        """
        # 🚀 Smart Resume Analyzer & Optimizer
        
        Transform your resume with AI-powered analysis and optimization. Get instant feedback on:
        - ✨ ATS Compatibility Score
        - 📈 Detailed Content Analysis
        - 💡 Tailored Improvement Recommendations
        - 🎯 Job Description Matching
        """
    )


def create_input_section() -> Dict:
    """Create and return input components."""
    with gr.Column(scale=1):
        pdf_input = gr.File(
            label="📎 Upload Your Resume (PDF)",
            type="filepath",
        )

        with gr.Row():
            model_dropdown = gr.Dropdown(
                choices=list(analyzer.supported_models.keys()),
                label="🤖 Select AI Model",
                value="Mistral Medium",
            )
            api_key_input = gr.Textbox(
                label="🔑 API Key",
                type="password",
                placeholder="Enter your API key here",
            )

        hf_model_input = gr.Textbox(
            label="🤗 HuggingFace Model Name",
            placeholder="Enter model name (e.g., gpt2, facebook/opt-1.3b)",
            visible=False,
        )
        ollama_model_input = gr.Textbox(
            label="🦙 Ollama Model Name",
            placeholder="Enter model name (e.g., llama3.3, qwq, gemma)",
            visible=False,
        )
        groq_model_input = gr.Textbox(
            label="⚡ Groq Model Name",
            placeholder="Enter model name (e.g., llama3.3, qwq, gemma)",
            visible=False,
        )

        additional_instructions = gr.Textbox(
            label="✍️ Additional Instructions",
            placeholder="Add any specific requirements or focus areas for the analysis",
            lines=3,
        )

        job_descriptions = gr.Textbox(
            label="💼 Job Descriptions",
            placeholder="Paste job descriptions to match your resume against them",
            lines=5,
        )

        submit_btn = gr.Button("🔍 Analyze Resume", variant="primary", scale=1)

    return {
        "pdf_input": pdf_input,
        "model_dropdown": model_dropdown,
        "api_key_input": api_key_input,
        "hf_model_input": hf_model_input,
        "ollama_model_input": ollama_model_input,
        "groq_model_input": groq_model_input,
        "additional_instructions": additional_instructions,
        "job_descriptions": job_descriptions,
        "submit_btn": submit_btn,
    }


def prepare_model_config(
    model: str,
    huggingface_model_name: str,
    ollama_model_name: str,
    groq_model_name: str,
) -> Dict:
    """Prepare model configuration based on selection."""
    if model == "HuggingFace Inference API" and huggingface_model_name.strip():
        return {model: huggingface_model_name}
    elif model == "Ollama Model" and ollama_model_name.strip():
        return {model: ollama_model_name}
    elif model == "Groq Model" and groq_model_name.strip():
        return {model: groq_model_name}
    return model


def load_markdown_content_from_file(pdf_file: str) -> str:
    """Load markdown content from file."""
    if not pdf_file:
        return "### No content provided"

    filename = f"{pdf_file.split('/')[-1].split('.')[0]}_updated_resume.md"
    return load_markdown_content(f"Resumes/{filename}")


def format_outputs(
    result: Dict, report: str, comparison_of_jd: str, markdown_content: str
) -> Tuple[str, str, str, str]:
    """Format all outputs for display."""
    ats_score_html = format_ats_score(result.get("ats_score", {}))
    recommendations_html = format_recommendations(
        result.get("detailed_recommendations", [])
    )
    strategies_html = format_strategies(result.get("improvement_strategies", []))
    report_html = format_detailed_report(report)
    comparison_html = format_job_comparison(comparison_of_jd)

    return (
        ats_score_html,
        recommendations_html + strategies_html + report_html,
        comparison_html,
        markdown_content,
    )


def create_error_message(error: Exception) -> str:
    """Create formatted error message."""
    return f"""
        <div style='padding: 20px; background: #fee2e2; border-radius: 10px; color: #dc2626;'>
            <h3>⚠️ Error Processing Resume</h3>
            <p>{str(error)}</p>
            <p>Please check your inputs and try again. If the problem persists, contact support.</p>
        </div>
    """
