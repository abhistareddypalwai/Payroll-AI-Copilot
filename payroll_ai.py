
# ZENVY - Payroll AI Copilot (Prototype)

import re


# System Prompt (Core Rules)

SYSTEM_PROMPT = """
You are ZENVY Payroll AI Copilot.
Answer only payroll-related questions.
Do not hallucinate or guess.
Redact sensitive data.
Follow legal and ethical payroll standards.
"""


# Role-Based Instructions

ROLE_PROMPTS = {
    "employee": """
    Explain payroll information in simple terms.
    Do not expose HR policies or other employee data.
    """,
    "hr": """
    Provide policy-level explanations.
    Focus on compliance and regulations.
    Maintain employee privacy.
    """
}


# Sensitive Data Redaction

def redact_sensitive_data(text):
    text = re.sub(r"\b\d{12,16}\b", "**** **** ****", text)  # Bank numbers
    text = re.sub(r"\b[A-Z]{5}\d{4}[A-Z]\b", "*****", text) # PAN
    return text


# Hallucination Prevention

def safe_response(answer, confidence=True):
    if not confidence:
        return "I don’t have enough verified payroll data to answer this accurately."
    return answer


# Main Response Generator

def generate_response(user_role, question, context):
    if user_role not in ROLE_PROMPTS:
        return "Invalid role. Access denied."

    # Context-aware logic
    if "salary less" in question.lower():
        response = (
            "Your net salary is lower due to increased statutory deductions "
            "such as tax or provident fund for this payroll period."
        )

    elif "pf" in question.lower():
        response = (
            "Provident Fund (PF) is a mandatory retirement contribution "
            "regulated by law to support long-term financial security."
        )

    elif "colleague salary" in question.lower():
        response = (
            "I can’t share that information. Employee salary data is confidential."
        )

    else:
        return safe_response("", confidence=False)

    # Redact sensitive data
    response = redact_sensitive_data(response)

    return response



# Example Usage

if __name__ == "__main__":
    context = {
        "country": "India",
        "payroll_month": "December 2025"
    }

    print(generate_response(
        user_role="employee",
        question="Why is my salary less this month?",
        context=context
    ))
