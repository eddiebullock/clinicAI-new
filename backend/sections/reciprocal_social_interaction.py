from utils.model import call_local_model

def generate_rsi_report(text):
    prompt = f"""
    Generate the following sections of an autism assessment report based on the provided clinician's notes. 

    Sections:
    - Nonverbal Behaviors to Regulate Emotion
    - Developing Peer Relationships
    - Shared Enjoyment
    - Socioemotional Reciprocity

    Clinician's Notes:
    ---
    {text}
    ---

    Ensure each section follows the format where the title is bolded and followed by a paragraph explaining the findings.
    """

    return call_local_model(prompt)
