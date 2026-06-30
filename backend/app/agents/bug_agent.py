import ast
from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

def check_bugs_ast(code: str):
    issues = []
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    issues.append("Bare except clause detected — catches all exceptions including system exits")
            if isinstance(node, ast.Compare):
                for op in node.ops:
                    if isinstance(op, ast.Is):
                        if any(isinstance(c, ast.Constant) and isinstance(c.value, (int, str))
                               for c in node.comparators):
                            issues.append("Using 'is' to compare values — use '==' instead")
            if isinstance(node, ast.FunctionDef):
                if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                    issues.append(f"Empty function '{node.name}' detected")
    except SyntaxError:
        pass
    return issues

async def analyze_bugs(code: str):
    ast_issues = check_bugs_ast(code)

    prompt = f"""You are a Python bug detection expert.
Analyze this code for logic errors, edge cases, exception handling issues, and potential runtime errors.

Code:
{code}

Respond in this exact format:
BUG_SCORE: (number 0-100, higher means fewer bugs)
ISSUES: (list each issue on new line starting with -)
SUGGESTIONS: (list each suggestion on new line starting with -)
LEARNING_TIPS: (list each tip on new line starting with -)"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message.content

    bug_score = 70
    issues = ast_issues.copy()
    suggestions = []
    learning_tips = []

    lines = content.split("\n")
    current_section = None

    for line in lines:
        line = line.strip()
        if line.startswith("BUG_SCORE:"):
            try:
                bug_score = float(line.split(":")[1].strip())
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
        "score": bug_score,
        "issues": issues,
        "suggestions": suggestions,
        "learning_tips": learning_tips
    }