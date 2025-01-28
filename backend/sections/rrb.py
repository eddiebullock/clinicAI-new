import openai

def generate_rrb_report(text):
    prompt = f"""
    Generate the following sections of an autism assessment report based on the provided clinician's notes:
    
    1. Preoccupation
    2. Routines
    3. Repetitive Movements
    4. Sensory Sensitivities
    5. Development at and Before 36 Months

    Clinician's Notes:
    ---
    {text}
    ---

    Generate each section clearly and concisely. Use professional language and separate each section with its title.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=700,
        temperature=0.5,
    )
    return response['choices'][0]['message']['content']
