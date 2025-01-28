import openai

def generate_rrb_report(text):
    prompt = f"""
    Generate the following sections of an autism assessment report based on the provided clinician's notes.
    **Ensure each section title is clearly separated and formatted in bold.** Do not use numbered lists.

    Sections:
    - Preoccupation
    - Routines
    - Repetitive Movements
    - Sensory Sensitivities
    - Development at and Before 36 Months

    **Format Example:**
    Preoccupation:
    [Description]
    
    Routines:
    [Description]

    Repetitive Movements:
    [Description]

    Clinician's Notes:
    ---
    {text}
    ---

    Ensure each section is clearly formatted with a bold title followed by its content.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=700,
        temperature=0.5,
    )
    return response['choices'][0]['message']['content']
