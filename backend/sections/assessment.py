from utils.model import call_local_model

def generate_assessment_report(text):
    prompt = f"""
    Generate the following sections of an autism assessment report based on the provided clinician's notes:

    1. Background (500 words)
    2. Key Mental Health Topic: Anxiety (approx. 200 words)
    3. Challenging Behavior (approx. 200 words)
    4. Key Mental Health Topic: Mood (approx. 200 words)
    5. Academic History/Scholarly Skills (250 words)
    6. Family History (approx. 200 words)
    7. Past Medical History (approx. 200 words)
    8. Developmental History (250 words)

    Clinician's Notes:
    ---
    {text}
    ---

    Generate each section clearly and concisely. Use professional language and separate each section with its title.
    """

    return call_local_model(prompt)
