from asd_structure import ASD_REPORT_STRUCTURE
from text_processing import extract_relevant_section
from openai_utils import call_openai_with_retries

def generate_asd_report(transcript):
    sections = []

    for category, content in ASD_REPORT_STRUCTURE.items():
        for section in content:
            section_title = section["title"]
            section_description = section.get("description", "Extract relevant details.")
            word_limit = section.get("word_limit", 600)

            relevant_text = extract_relevant_section(transcript, section_title)

            messages = [
                {"role": "system", "content": (
                    "You are a clinical psychologist specializing in autism assessments. "
                    "Your task is to extract relevant details from the provided transcript "
                    "to create a structured, narrative-style psychological assessment report."
                    "Use full sentences and paragraphs instead of bullet points. When possible, "
                    "include direct quotes from the transcript to provide authenticity. "
                    "Ensure that the section is detailed, informative, and consistent with "
                    "clinical reports."
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
            sections.append({
                "title": section_title,
                "content": response['choices'][0]['message']['content'].strip()
            })

    return sections
