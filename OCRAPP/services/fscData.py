def extract_fsc_data(fsc_sanat_details):
    extracted_info = {
        "total_marks": None,
        "obtained_marks": None,
        "roll_no": None,
        "board": None,
    }
    
    roll_no_line = ""  # Initialize the variable outside the loop
    roll_no_index = -1  # Initialize the index before the loop

    for i, text in enumerate(fsc_sanat_details):
    # Look for the keywords "TOTAL" to extract the total marks
        if "TOTAL" in text:
            total_index = i
            extracted_info["total_marks"] = fsc_sanat_details[total_index + 1]
            extracted_info["obtained_marks"] = fsc_sanat_details[total_index + 2]

        if "Roll No" in text:
            roll_no_index = i
            roll_no = fsc_sanat_details[roll_no_index + 1]
            extracted_info["roll_no"] = roll_no
            


        if "BOARD" in text:
            board_index = i
            extracted_info["board"] = fsc_sanat_details[board_index].strip()

        

    return extracted_info
