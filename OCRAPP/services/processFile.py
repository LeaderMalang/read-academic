# import ocr (scan the sanat/idCard files)
from ..ocr.scanFile import scan_file
# import utils (utility functions)
from ..utils.saveFile import save_file

def process_file(uploads_dir, file, reader):
    file_path = save_file(uploads_dir, file) # saved file path
    file_data = scan_file(file_path, reader) # extracted data
    return file_data