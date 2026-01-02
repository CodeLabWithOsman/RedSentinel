from redsentinel.core.ai_client import AIClient


def generate_remediation_roadmap(normalized_findings: dict) -> str:
    """
    Generate AI-based remediation roadmap using Gemini
    """
    if not normalized_findings:
        return "No findings detected. No remediation required."

    system_prompt = (
        "You are a senior cybersecurity consultant. "
        "Write remediation guidance in clear, non-technical English."
    )

    user_prompt = f"""
Analyze the following security findings and provide:
1. Overall risk explanation
2. Prioritized remediation steps
3. Short-term vs long-term fixes

Findings:
{normalized_findings}
"""

    try:
        client = AIClient()
        return client.generate(system_prompt, user_prompt)
    except Exception as e:
        return f"AI remediation unavailable: {e}"

