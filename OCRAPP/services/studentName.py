def extract_student_name(cleaned_texts):
    extracted_info = {
        "certified_name": None,
    }

    # Array to store lines containing 'TOTAL'
    for i, text in enumerate(cleaned_texts):

        if "RESULT CARD" in text:
            certified_name_index = i + 1
            extracted_info["certified_name"] = cleaned_texts[certified_name_index].strip()

    return extracted_info
