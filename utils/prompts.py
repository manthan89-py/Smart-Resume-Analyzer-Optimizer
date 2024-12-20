import json
from utils.data_models import FinalResult, JobComparisionResult, MarkdownResult


def get_markdown_report_prompt(suggestions, resume_content, additional_instructions):
    prompt = f"""
    Objective: Implement a sophisticated, intelligence-driven resume content optimization strategy specifically tailored to meet rigorous Applicant Tracking System (ATS) scanning and parsing requirements.

    ## Intelligent Transformation Methodology
    ### 1. Strategic ATS Optimization Protocols
    #### Core Transformation Principles:
    - Semantic Precision: Surgical linguistic modifications
    - Structural Integrity: Preserve professional narrative essence
    - Keyword Alignment: Maximum ATS compatibility
    - Contextual Intelligence: Deep semantic understanding

    ### 2. Sophisticated Processing Guidelines
    #### Input Processing Ecosystem
    Suggestion Analysis:
    - Deep semantic parsing of improvement vectors
    - Contextual relevance assessment
    - Intelligent modification strategy generation

    Resume Content Evaluation:
    - Granular structural analysis
    - Keyword density optimization
    - Professional terminology standardization

    ### 3. ATS-Centric Transformation Framework
    #### Modification Decision Matrix
    High-Impact Modification Triggers:
    1. Keyword misalignment
    2. Suboptimal semantic structures
    3. Inefficient information presentation
    4. Potential parsing complexity

    #### Non-Modification Safeguards
    Authenticity Preservation Protocols:
    Reject modifications that:
        * Compromise original narrative integrity
        * Introduce semantic ambiguity
        * Potentially reduce comprehension clarity

    ### 4. Intelligent Linguistic Engineering
    #### Transformation Strategies:
    Keyword Optimization:
    - Align with industry-specific terminology
    - Maximize ATS keyword match probability
    - Implement strategic keyword density

    Structural Refinement:
    - Simplify complex linguistic constructions
    - Enhance readability metrics
    - Optimize parsing potential

    Input Specifications:-
    Suggestions: {json.dumps(suggestions, indent=2)}
    Resume Content: {json.dumps(resume_content, indent=2)}
    Additional insturctions provided by user which must be followed: {additional_instructions}

    Final Note: Final content should be in proper markdown content. This content will directly display to UI.

    Below is the pydantic model json schema.
    Don't output all the fields present in the schema. Provide the main fields only.
    {json.dumps(MarkdownResult.model_json_schema(), indent=2)}
    Don't output explanation or any text. Just provide a valid JSON output only.
    """
    return prompt


def get_resume_analyzer_prompt(resume_content):
    prompt = f"""
    Objective: Conduct a meticulous, multi-dimensional analysis of the provided resume to generate a precise Applicant Tracking System (ATS) compatibility score, leveraging
    advanced algorithmic assessment techniques.
    
    Context: You are a high-precision AI resume evaluation specialist tasked with performing a deep, nuanced analysis of professional documentation to determine its optimality for automated recruitment screening systems.

    Holistic Evaluation Methodology:-
    1. Preprocessing Stage
    Structural Decomposition
    - Methodically deconstruct the resume into discrete, granular sections
    - Identify and isolate critical components:
        * Professional header
        * Executive summary/professional narrative
        * Educational credentials
        * Professional experience trajectory
        * Skill matrix
        * Certifications and achievements
        * Additional contextual elements

    2. Deep Analysis Criteria
    Lexical Optimization:
        - Assess keyword density and alignment with industry-specific terminology
        - Evaluate semantic richness and professional vernacular precision
        - Analyze lexical coherence and contextual relevance

    3. Structural Integrity
        - Examine document formatting compliance
        - Validate structural adherence to ATS parsing guidelines
        - Assess visual and textual readability metrics

    4. Content Sophistication
        - Quantify professional achievements' substantiveness
        - Evaluate quantitative and qualitative impact statements
        - Analyze skill-experience congruence

    Scoring Mechanism
        - Implement a comprehensive, multi-dimensional scoring algorithm
        - Generate an ATS compatibility score ranging from 1-100
        - Score derived from:
            * Keyword optimization (35%)
            * Structural formatting (25%)
            * Content quality (20%)
            * Professional narrative coherence (15%)
            * Additional contextual factors (5%)

    Below is the pydantic model json schema.
    Don't output all the fields present in the schema. Provide the main fields only.
    {json.dumps(FinalResult.model_json_schema(), indent=2)}
    Don't output explanation or any text. Just provide a valid JSON output only.

    Resume Content
    {json.dumps(resume_content, indent=2)}
    """
    return prompt


def get_comparision_with_job_description_prompt(resume_content, job_description):
    prompt = f"""
    # Intelligent Resume-Job Description Compatibility Assessment Framework
    ## Comprehensive Evaluation Methodology

    ### 1. Holistic Compatibility Analysis Ecosystem
    #### Primary Objectives:
    - Conduct deep semantic matching between resume and job description
    - Generate precision-driven candidate compatibility assessment
    - Provide actionable, strategic improvement recommendations

    ### 2. Advanced Semantic Matching Protocols
    #### Evaluation Dimensions:
    1. Skill Alignment Matrix
    - Exact skill match percentage
    - Transferable skill identification
    - Domain-specific competency mapping
    2. Experience Relevance Calculation
    - Role-specific experience weight
    - Industry expertise correlation
    - Career trajectory alignment

    ## Intelligent Assessment Architecture
    ### Comprehensive Scoring Methodology
    Scoring Range: 1-100 (Absolute Precision)
    Scoring Dimensions:
    - Technical Skill Match: X%
    - Experience Relevance: Y%
    - Soft Skill Alignment: Z%
    - Professional Narrative Coherence: W%
    
    Input:-
    Resume Content: {json.dumps(resume_content, indent=2)}
    Job Description: {job_description}

    Below is the pydantic model json schema.
    Don't output all the fields present in the schema. Provide the main fields only.
    {json.dumps(JobComparisionResult.model_json_schema(), indent=2)}
    Don't output explanation or any text. Just provide a valid JSON output only.
    
    Do not output any other explanation or text except.
    """
    return prompt
