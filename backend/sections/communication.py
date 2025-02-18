from utils.model import call_local_model

def generate_communication_report(text):
    prompt = f"""
    Generate a detailed autism assessment report section for the following communication aspects based on the clinician's notes. 

    Sections to generate:
    - Gesture
    - Social Imaginative Play
    - Conversational Interchange
    - Repetitive or Unusual Speech

    Clinician's Notes:
    ---
    {text}
    ---

    **Ensure each section has a complete and detailed response. If any section is missing details, state this explicitly instead of leaving it blank.**
    """

    return call_local_model(prompt)
