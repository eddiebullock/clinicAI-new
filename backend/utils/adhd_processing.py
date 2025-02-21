from adhd_structure import ADHD_REPORT_STRUCTURE
from text_processing import extract_relevant_section
from openai_utils import call_openai_with_retries

def generate_adhd_report(transcript):
    sections = []

    for category, content in ADHD_REPORT_STRUCTURE.items():
        for section in content:
            section_title = section["title"]
            section_description = section.get("description", "Extract relevant details.")
            word_limit = section.get("word_limit", 600)

            relevant_text = extract_relevant_section(transcript, section_title)

            messages = [
                {"role": "system", "content": (
                    "You are a clinical psychologist specializing in ADHD assessments. "
                    "Your task is to extract relevant details from the provided transcript "
                    "to create a structured, narrative-style psychological assessment report. "
                    "Only use details explicitly mentioned in the transcript. Do not assume "
                    "information that is not present. If a section lacks sufficient detail, "
                    "acknowledge this briefly without making assumptions or providing generic advice. "
                    "Do not diagnose or conclude that the individual has ADHD; simply document their assessment responses. "
                    "Ensure consistency by referring to the individual as 'Edward' in personal sections and 'the individual' in formal sections."
                )},
                {"role": "user", "content": (
                    f"Write a detailed and structured section for '{section_title}' based on the transcript.\n\n"
                    f"**Guidance:**\n{section_description}\n\n"
                    f"**Transcript:**\n{relevant_text}\n\n"
                    f"**Formatting Notes:**\n"
                    f"- The section should read like a clinical assessment report with full sentences.\n"
                    f"- If applicable, include direct quotes from the transcript to provide authenticity.\n"
                    f"- Maintain a professional, formal tone while preserving the personal nature of the assessment.\n"
                    f"- If no relevant details are found, indicate this subtly (e.g., 'The transcript does not contain direct references to...').\n"
                )}
            ]

            response = call_openai_with_retries(messages, max_tokens=word_limit * 2)
            generated_text = response['choices'][0]['message']['content'].strip()

            # If the AI response is too generic, modify it
            if "The transcript does not provide specific details" in generated_text or len(generated_text) < 100:
                generated_text = f"The transcript does not contain sufficient information for a full analysis of '{section_title}'. Further details may be required to assess this aspect properly."

            generated_text = response['choices'][0]['message']['content'].strip()

            # Ensure consistent naming conventions
            generated_text = generated_text.replace("the individual", "Edward Bullock").replace("they", "he")

            sections.append({
                "title": section_title,
                "content": generated_text
            })

    return sections
