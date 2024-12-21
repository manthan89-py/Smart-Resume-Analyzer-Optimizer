# Smart Resume Analyzer & Optimizer 🚀

Transform your resume with AI-powered analysis and optimization. Get instant feedback leveraging multiple state-of-the-art language models.

## ✨ Key Features

- **ATS Compatibility Score**: Comprehensive analysis of your resume's compatibility with Applicant Tracking Systems
- **Detailed Content Analysis**: In-depth evaluation of structure, keywords, and content quality
- **Tailored Recommendations**: Specific suggestions to improve your resume's effectiveness
- **Job Description Matching**: Compare your resume against job requirements with precision scoring
- **Interactive Resume Chat**: Ask questions about your resume and get instant answers
- **Multi-Model Support**: Access to leading AI models including:
  - OpenAI (From GPT-3.5-turbo to GPT-4o-mini)
  - Mistral (medium and large)
  - Claude (3.5-sonnet, 3.5-haiku, 3 opus)
  - HuggingFace Inference API
  - Groq Models
  - Ollama Models

## 🛠️ Installation & Setup

### Using Docker (Recommended)

Pull and run the pre-built image:
```bash
docker pull manthan07/resume_analyzer:main-latest
docker run -p 7860:7860 manthan07/resume_analyzer:main-latest
```

### Alternative Docker Build
```bash
git clone https://github.com/manthan89-py/Smart-Resume-Analyzer-Optimizer
cd Smart-Resume-Analyzer-Optimizer
docker build -t localmachine/resume_analyzer:main-latest .
docker run -p 7860:7860 localmachine/resume_analyzer:main-latest
```

### Local Installation
```bash
git clone https://github.com/manthan89-py/Smart-Resume-Analyzer-Optimizer
cd Smart-Resume-Analyzer-Optimizer
sh start.sh  # Requires Python 3.12+
```

## 🎯 Usage Guide

1. Access the application at `https://localhost:7860`
2. Upload your resume in PDF format
3. Select your preferred LLM Model
4. Provide API Key/Model Token if required
5. (Optional) Add specific questions or instructions
6. (Optional) Include a job description for comparison analysis

## 💡 Example Queries

- "What are the strengths and weaknesses of my resume?"
- "What interview questions might be asked for [JOB ROLE]?"
- "Highlight my main technical skills"
- "Provide a professional summary for my resume"

## ⚙️ Technical Details

### Analysis Components

1. **ATS Score Calculation**
   - Keyword optimization (35%)
   - Structural formatting (25%)
   - Content quality (20%)
   - Professional narrative coherence (15%)
   - Additional contextual factors (5%)

2. **Job Description Matching**
   - Technical skill match
   - Experience relevance
   - Soft skill alignment
   - Professional narrative coherence

### Preprocessing and Analysis
- Structural decomposition of resume sections
- Lexical optimization and keyword analysis
- Content sophistication evaluation
- Intelligent transformation methodology

## ⚠️ Current Limitations & Workarounds

- **Model Parsing Issues**: Implemented retry mechanism for LLM calls. Consider using Groq (limited usage) or Mistral models (currently free) as alternatives
- **Markdown Formatting**: Some inconsistencies in output formatting. Currently optimized for content analysis over formatting
- **Processing Time**: Check container/server logs for performance issues. Multiple model options available as alternatives

## 🚀 Future Enhancements

- Additional model support including Local Models API (LLMStudio)
- Enhanced ATS Score breakdown
- Advanced resume analysis features
- LinkedIn Profile integration and comparison
- Improved markdown formatting
- Direct update capability for source documents (Docx, PDF)
- Resume-LinkedIn profile comparison analysis

## 📝 Note on Ollama Models
For Ollama models, ensure the Ollama service is running. Check status with:
```bash
ollama ps
```

## 🔒 Prerequisites
- Python 3.12 or higher (for local installation)
- Docker (for containerized deployment)
- Relevant API keys for chosen language models

## 🤝 Contributing

Thanks for your interest in improving Smart Resume Analyzer & Optimizer! Here's how you can help:

### Quick Start

1. Fork the repo and create your branch from `main`
2. Make your changes
3. Test your changes
4. Submit a pull request

### Guidelines

- **Bug Reports**: Use GitHub's [issue tracker](https://github.com/manthan89-py/Smart-Resume-Analyzer-Optimizer/issues)
  - Include steps to reproduce
  - Provide example code when possible
  - Describe expected vs actual behavior

- **Code Style**:
  - Follow PEP 8
  - Use black formatter

- **Pull Requests**:
  - Update readme if needed
  - Update requirements.txt for new dependencies
  - Get approval from at least one maintainer
