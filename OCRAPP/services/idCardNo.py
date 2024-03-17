import re

def extract_idCard_no(cleaned_texts):
    idCard_numbers = ""
    pattern = re.compile(r'\b\d{5}-\d{7}-\d{1}\b')  # Pattern for "37405-2893005-7"

    for text in cleaned_texts:
        # Check if the text is a string and matches the pattern
        if isinstance(text, str) and pattern.match(text):
            # Append the matching text to the result string with a newline separator
            idCard_numbers += text + "\n"

    return idCard_numbers