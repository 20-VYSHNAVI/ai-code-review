import ast
from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

def check_security_ast(code: str):
    issues = []
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ["eval", "exec"]:
                        issues.append(f"Dangerous function '{node.func.id}' detected — security risk")
                    if node.func.id == "input":
                        issues.append("Unvalidated user input detected")
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "pickle":
                        issues.append("Use of 'pickle' detected — potential security risk")
    except SyntaxError:
        pass
    return issues

async def analyze_security(code: str):
    ast_issues = check_security_ast(code)

    prompt = f"""You are a Python security expert.
Analyze this code for security vulnerabilities, unsafe practices, and potential exploits.

Code:
{code}

Respond in this exact format:
SECURITY_SCORE: (number 0-100)
ISSUES: (list each issue on new line starting with -)
SUGGESTIONS: (list each suggestion on new line starting with -)
LEARNING_TIPS: (list each tip on new line starting with -)"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message.content

    security_score = 70
    issues = ast_issues.copy()
    suggestions = []
    learning_tips = []

    lines = content.split("\n")
    current_section = None

    for line in lines:
        line = line.strip()
        if line.startswith("SECURITY_SCORE:"):
            try:
                security_score = float(line.split(":")[1].strip())
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
        "score": security_score,
        "issues": issues,
        "suggestions": suggestions,
        "learning_tips": learning_tips
    }