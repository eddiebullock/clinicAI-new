from transformers import pipeline
import numpy as np

# Debugging: Check if numpy is available
print("Numpy Version:", np.__version__)

# Load Hugging Face NER pipeline
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", grouped_entities=True)

def preprocess_text(text):
    """Normalize whitespace in the input text."""
    return " ".join(text.split())

def anonymize_text_with_huggingface(file_path):
    """Anonymize sensitive information using Hugging Face NER."""
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    # Run NER and debug results
    ner_results = ner_pipeline(text)
    print("NER Results:", ner_results)

    redacted_text = text
    for entity in ner_results:
        entity_text = entity["word"]
        entity_label = entity["entity_group"]
        if entity_label in ["PER", "LOC", "ORG", "MISC"]:
            redacted_text = redacted_text.replace(entity_text, f"[REDACTED {entity_label}]")

    return redacted_text