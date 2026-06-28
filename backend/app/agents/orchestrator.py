from app.agents.quality_agent import analyze_quality
from app.agents.security_agent import analyze_security
from app.agents.bug_agent import analyze_bugs

async def run_review(code: str, filename: str = "code.py"):
    
    quality_result = await analyze_quality(code)
    security_result = await analyze_security(code)
    bug_result = await analyze_bugs(code)

    quality_score = quality_result["score"]
    security_score = security_result["score"]
    readability_score = quality_result["readability_score"]
    overall_score = round((quality_score + security_score + readability_score) / 3, 2)

    all_issues = (
        quality_result["issues"] +
        security_result["issues"] +
        bug_result["issues"]
    )

    all_suggestions = (
        quality_result["suggestions"] +
        security_result["suggestions"] +
        bug_result["suggestions"]
    )

    all_tips = (
        quality_result["learning_tips"] +
        security_result["learning_tips"] +
        bug_result["learning_tips"]
    )

    if overall_score >= 80:
        severity = "Low"
    elif overall_score >= 60:
        severity = "Medium"
    else:
        severity = "Critical"

    return {
        "scores": {
            "quality": quality_score,
            "security": security_score,
            "readability": readability_score,
            "overall": overall_score
        },
        "issues": all_issues,
        "suggestions": all_suggestions,
        "severity": severity,
        "learning_tips": all_tips
    }