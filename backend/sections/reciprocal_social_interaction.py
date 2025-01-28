import openai

def generate_rsi_report(text):
    prompt = f"""
    Generate the following sections of an autism assessment report based on the provided clinician's notes:
    
    1. Nonverbal Behaviors to Regulate Emotion
    2. Developing Peer Relationships
    3. Shared Enjoyment
    4. Socioemotional Reciprocity

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
