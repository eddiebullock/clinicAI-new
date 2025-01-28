import openai

def generate_communication_report(text):
    prompt = f"""
    Generate the following sections of an autism assessment report based on the provided clinician's notes.
    **Ensure each section title is clearly separated and formatted in bold.** Do not use markdown-style headings.

    Sections:
    - Gesture
    - Social Imaginative Play
    - Conversational Interchange
    - Repetitive or Unusual Speech

    **Format Example:**
    Gesture:
    [Description]
    
    Social Imaginative Play:
    [Description]

    Conversational Interchange:
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
