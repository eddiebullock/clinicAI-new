import re
from fuzzywuzzy import fuzz

def extract_relevant_section(transcript, section_title):
    """
    Extracts relevant sections of text from the transcript based on section title.
    Uses keyword matching and fuzzy similarity to improve extraction accuracy.
    """
    keywords = section_title.lower().split()  
    extracted_sentences = []

    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", transcript)

    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in keywords):
            extracted_sentences.append(sentence)
        else:
            for keyword in keywords:
                if fuzz.partial_ratio(keyword, sentence.lower()) > 70:
                    extracted_sentences.append(sentence)
                    break  

    if extracted_sentences:
        return " ".join(extracted_sentences)
    
    return "The transcript does not contain direct references to this topic."
