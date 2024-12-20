def load_markdown_content(filename):
    try:
        with open(filename) as file:
            content = file.read()
        return content
    except Exception:
        return "### Updated Resume has not been found."


def format_ats_score(score_data: dict):
    if not score_data:
        return ""

    html = "<div style='padding: 20px; background: #2d2d2d; border-radius: 10px; color: #e0e0e0;'>"

    # Overall Score
    overall_score = score_data.get("overall_score", 0)
    if not isinstance(overall_score, (int, float)):
        overall_score = 0

    html += f"""
        <div style='text-align: center; padding: 20px; background: #383838; color: #ffffff; border-radius: 8px; margin-bottom: 20px;'>
            <h2 style='margin: 0; font-size: 2.5em;'>{overall_score}/100</h2>
            <p style='margin: 5px 0 0 0;'>Overall ATS Score</p>
        </div>
    """

    # Category Breakdowns
    html += "<div style='margin-top: 20px;'>"
    html += "<h3 style='color: #ffffff; margin-bottom: 15px;'>Category Breakdown</h3>"

    category_breakdowns = score_data.get("category_breakdowns", {})
    if isinstance(category_breakdowns, dict):
        for category, score in category_breakdowns.items():
            if not isinstance(score, (int, float)):
                score = 0
            category_name = category.replace("_", " ").title()
            percentage = (score / 100) * 100  # Assuming max score is 100

            html += f"""
                <div style='margin: 12px 0;'>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>
                        <span style='font-weight: 500; color: #e0e0e0;'>{category_name}</span>
                        <span style='color: #e0e0e0;'>{score} points</span>
                    </div>
                    <div style='background: #404040; border-radius: 4px; height: 8px;'>
                        <div style='background: #3b82f6; width: {percentage}%; height: 100%; border-radius: 4px;'></div>
                    </div>
                </div>
            """

    html += "</div></div>"
    return html


def format_recommendations(recommendations: list):
    if not recommendations:
        return ""

    html = "<div style='padding: 20px; background: #2d2d2d; border-radius: 10px; margin-top: 20px; color: #e0e0e0;'>"
    html += (
        "<h3 style='color: #ffffff; margin-bottom: 15px;'>Detailed Recommendations</h3>"
    )
    html += "<ul style='list-style-type: disc; margin-left: 20px;'>"
    for rec in recommendations:
        html += f"<li style='margin: 10px 0;'>{rec}</li>"
    html += "</ul></div>"
    return html


def format_strategies(strategies: list):
    if not strategies:
        return ""

    html = "<div style='padding: 20px; background: #2d2d2d; border-radius: 10px; margin-top: 20px; color: #e0e0e0;'>"
    html += (
        "<h3 style='color: #ffffff; margin-bottom: 15px;'>Improvement Strategies</h3>"
    )
    html += "<ul style='list-style-type: disc; margin-left: 20px;'>"
    for strategy in strategies:
        html += f"<li style='margin: 10px 0;'>{strategy}</li>"
    html += "</ul></div>"
    return html


def format_detailed_report(report_data: dict):
    if not report_data:
        return ""

    html = "<div style='padding: 20px; background: #2d2d2d; border-radius: 10px; color: #e0e0e0; margin-top: 20px;'>"

    # Content Section
    html += """
        <div style='margin-bottom: 20px;'>
            <h3 style='color: #ffffff; margin-bottom: 10px;'>📄 Improved Resume Content</h3>
            <div style='background: #383838; padding: 15px; border-radius: 8px; border-left: 4px solid #3b82f6;'>
    """
    content = report_data.get("content", "")
    if isinstance(content, str):
        html += content.replace("\n", "<br>")
    html += "</div></div>"

    # Changes Section
    html += """
        <div style='margin-bottom: 20px;'>
            <h3 style='color: #ffffff; margin-bottom: 10px;'>📝 Changes Made</h3>
            <div style='background: #383838; padding: 15px; border-radius: 8px; border-left: 4px solid #60a5fa;'>
    """
    changes = report_data.get("changes", [])
    if isinstance(changes, list):
        html += "<ul style='list-style-type: disc; margin-left: 20px;'>"
        for change in changes:
            html += f"<li style='margin: 10px 0;'>{change}</li>"
        html += "</ul>"
    html += "</div></div>"

    # Additional Instructions Response
    if report_data.get("additional"):
        html += """
            <div>
                <h3 style='color: #ffffff; margin-bottom: 10px;'>💡 Additional Instructions Response</h3>
                <div style='background: #383838; padding: 15px; border-radius: 8px; border-left: 4px solid #22c55e;'>
        """
        additional = report_data.get("additional", "")
        if isinstance(additional, str):
            html += additional.replace("\n", "<br>")
        html += "</div></div>"

    html += "</div>"
    return html


def format_job_comparison(comparison_data: dict):
    if not comparison_data:
        return ""

    html = "<h2 style='color: #ffffff; margin-bottom: 10px;'>Analysis Job Description with Resume</h2><div style='padding: 20px; background: #2d2d2d; border-radius: 10px; color: #e0e0e0;'>"

    # Selection Chance
    selection_chance = comparison_data.get("percentage_of_chances", 0)
    html += f"""
        <div style='text-align: center; padding: 20px; background: #383838; color: #ffffff; border-radius: 8px; margin-bottom: 20px;'>
            <h2 style='margin: 0; font-size: 2.5em;'>{selection_chance}%</h2>
            <p style='margin: 5px 0 0 0;'>Chance of Selection</p>
        </div>
    """

    # Analysis
    html += """
        <div style='margin-bottom: 20px;'>
            <h3 style='color: #ffffff; margin-bottom: 10px;'>📊 Analysis</h3>
            <div style='background: #383838; padding: 15px; border-radius: 8px; border-left: 4px solid #3b82f6;'>
    """
    analysis = comparison_data.get("analysis", "")
    if isinstance(analysis, str):
        html += analysis.replace(".", ".<br>")
    html += "</div></div>"

    # Suggestions
    html += """
        <div>
            <h3 style='color: #ffffff; margin-bottom: 10px;'>💡 Improvement Suggestions</h3>
            <div style='background: #383838; padding: 15px; border-radius: 8px; border-left: 4px solid #22c55e;'>
    """
    suggestions = comparison_data.get("suggestions", "")
    if isinstance(suggestions, str):
        html += suggestions.replace(".", ".<br>")
    html += "</div></div></div>"

    return html
