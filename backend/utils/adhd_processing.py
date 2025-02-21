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

            # Make OpenAI API call
            response = call_openai_with_retries(messages, max_tokens=word_limit * 2)

            # Ensure response contains valid data
            if not response or 'choices' not in response or not response['choices']:
                print(f"🚨 ERROR: OpenAI returned an empty or malformed response for section '{section_title}'")
                sections.append({
                    "title": section_title,
                    "content": "⚠️ Unable to generate content for this section due to insufficient data."
                })
                continue

            generated_text = response['choices'][0].get('message', {}).get('content', "").strip()

            # Ensure we have valid generated text
            if not generated_text:
                print(f"🚨 WARNING: Empty response received for section '{section_title}'")
                generated_text = "⚠️ No relevant information was provided in the transcript for this section."

            # Ensure consistent naming conventions
            generated_text = generated_text.replace("the individual", "Edward Bullock").replace("they", "he")

            sections.append({
                "title": section_title,
                "content": generated_text
            })

    return sections
