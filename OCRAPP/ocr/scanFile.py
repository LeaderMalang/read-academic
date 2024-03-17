def scan_file(file_path, reader):
    result = reader.readtext(file_path)
    cleaned_texts = [detection[1] for detection in result]
    print(">>>> File scanned")
    
    # UNCOMMENT THESE LINES TO GET OUTPUT ON CONSOLE
    # print("\n-------------------------------\n")
    # print(cleaned_texts)
    # print("\n-------------------------------")
    
    return cleaned_texts
