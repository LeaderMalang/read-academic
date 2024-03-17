import re

def extract_matric_data(cleaned_texts):
    extracted_info = {
        "certified_name": None,
        "son_daughter_of": None,
        "total_marks": None,
        "obtained_marks": None,
        "roll_no": None,
        "board": None,
    }

    # Array to store lines containing 'TOTAL'
    for i, text in enumerate(cleaned_texts):

        if "Certified that" in text:
            certified_name_index = i + 1
            extracted_info["certified_name"] = cleaned_texts[certified_name_index].strip()

        # Look for the keywords "Son" or "Daughter" to extract the son/daughter of information
        if "Son" in text or "Daughter" in text:
            son_daughter_index = i + 1
            # Extract the text following "Son" or "Daughter" up to the next keyword
            while son_daughter_index < len(cleaned_texts) and not any(keyword in cleaned_texts[son_daughter_index] for keyword in ["of", "whose"]):
                if "Son" in cleaned_texts[son_daughter_index] or "Daughter" in cleaned_texts[son_daughter_index]:
                    # If "Son" or "Daughter" is found in the line, extract the name
                    extracted_info["son_daughter_of"] = cleaned_texts[son_daughter_index].replace("Son", "").replace("Daughter", "").strip()
                    break
                else:
                    if extracted_info["son_daughter_of"] is None:
                        extracted_info["son_daughter_of"] = cleaned_texts[son_daughter_index].strip()
                    else:
                        extracted_info["son_daughter_of"] += " " + cleaned_texts[son_daughter_index].strip()
                son_daughter_index += 1

        if "Roll No" in text:
            roll_no_index = i
            # Using regular expression to extract a 6-digit pattern following "Roll No"
            pattern = re.compile(r'(\d{6})')  # Adjust the pattern as needed
            match = pattern.search(cleaned_texts[roll_no_index])
            if match:
                extracted_info["roll_no"] = match.group(1)
            else:
                match2 = pattern.search(cleaned_texts[roll_no_index+1])
                if match2:
                    extracted_info["roll_no"] = match2.group(1)
            

        if "BOARD" in text:
            board_index = i
            extracted_info["board"] = cleaned_texts[board_index].strip()
        
        # Look for the keywords "TOTAL" to extract the total marks
        if "TOTAL" in text:
            total_index = i
            extracted_info["total_marks"] = cleaned_texts[total_index + 1]
            extracted_info["obtained_marks"] = cleaned_texts[total_index + 2]

    return extracted_info
