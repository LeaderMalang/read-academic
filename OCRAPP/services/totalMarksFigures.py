def extract_total_marks_in_figures(cleaned_texts):
    extracted_info = {
        "total_marks": None,
        "obtained_marks": None,
    }

    # Array to store lines containing 'TOTAL'
    for i, text in enumerate(cleaned_texts):

        if "Total Marks" in text:
            total_index = i
            extracted_info["obtained_marks"] = cleaned_texts[total_index + 1]
            extracted_info["total_marks"] = cleaned_texts[total_index + 2]

    return extracted_info
