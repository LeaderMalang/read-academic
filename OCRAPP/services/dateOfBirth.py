import re

def extract_date_of_birth(cleaned_texts):
    # Updated date pattern to match the specific format in the cleaned text
    date_pattern = re.compile(r'date of birth Is (\d{2}-\d{2}-\d{4})', re.IGNORECASE)

    for text in cleaned_texts:
        match = date_pattern.search(text)
        if match:
            return match.group(1)

    return None
