import ast
import google.generativeai as genai
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def check_ast(code: str):
    issues = []
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not ast.get_docstring(node):
                    issues.append(f"Function '{node.name}' is missing a docstring")
            if isinstance(node, ast.For):
                if isinstance(node.iter, ast.Call):
                    if isinstance(node.iter.func, ast.Name):
                        if node.iter.func.id == "range":
                            pass
    except SyntaxError as e:
        issues.append(f"Syntax error: {str(e)}")
    return issues

async def analyze_quality(code: str):
    ast_issues = check_ast(code)

    prompt = f"""You are a Python code quality expert.
Analyze this code for PEP8 violations, readability, and optimization issues.

Code:
{code}

Respond in this exact format:
QUALITY_SCORE: (number 0-100)
READABILITY_SCORE: (number 0-100)
ISSUES: (list each issue on new line starting with -)
SUGGESTIONS: (list each suggestion on new line starting with -)
LEARNING_TIPS: (list each tip on new line starting with -)"""

    response = model.generate_content(prompt)
    content = response.text

    quality_score = 70
    readability_score = 70
    issues = ast_issues.copy()
    suggestions = []
    learning_tips = []

    lines = content.split("\n")
    current_section = None

    for line in lines:
        line = line.strip()
        if line.startswith("QUALITY_SCORE:"):
            try:
                quality_score = float(line.split(":")[1].strip())
            except:
                pass
        elif line.startswith("READABILITY_SCORE:"):
            try:
                readability_score = float(line.split(":")[1].strip())
            except:
                pass
        elif line.startswith("ISSUES:"):
            current_section = "issues"
        elif line.startswith("SUGGESTIONS:"):
            current_section = "suggestions"
        elif line.startswith("LEARNING_TIPS:"):
            current_section = "tips"
        elif line.startswith("-"):
            if current_section == "issues":
                issues.append(line[1:].strip())
            elif current_section == "suggestions":
                suggestions.append(line[1:].strip())
            elif current_section == "tips":
                learning_tips.append(line[1:].strip())

    return {
        "score": quality_score,
        "readability_score": readability_score,
        "issues": issues,
        "suggestions": suggestions,
        "learning_tips": learning_tips
    }