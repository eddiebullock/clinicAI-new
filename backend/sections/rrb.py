from utils.model import call_local_model

def generate_rrb_report(text):
    prompt = f"""
    Generate a detailed autism assessment report section for the following topics based on the clinician's notes. 

    Sections:
    - Preoccupation
    - Routines
    - Repetitive Movements
    - Sensory Sensitivities
    - Development at and Before 36 Months

    Clinician's Notes:
    ---
    {text}
    ---

    **Ensure every section has a complete response and is not left empty.**
    """

    return call_local_model(prompt)
