def calculate_percentage(total_marks, obtained_marks):
    if (total_marks is not None and obtained_marks is not None): 
        if (total_marks.replace('.', '', 1).isdigit() and obtained_marks.replace('.', '', 1).isdigit()):
            total_marks = int(total_marks)
            obtained_marks = int(obtained_marks)
            if total_marks > 0:
                percentage = (obtained_marks / total_marks) * 100
                return percentage
    
    return 0