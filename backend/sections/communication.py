import openai

def generate_communication_report(text):
    prompt = f"""
    Generate the following sections of an autism assessment report based on the provided clinician's notes:
    
    1. Gesture
    2. Social Imaginative Play
    3. Conversational Interchange
    4. Repetitive or Unusual Speech

    Clinician's Notes:
    ---
    {text}
    ---

    Generate each section clearly and concisely. Use professional language and separate each section with its title.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=700,  # Smaller max_tokens as fewer sections are included
        temperature=0.5,
    )
    return response['choices'][0]['message']['content']
