import os

def save_file(uploads_dir, file):
    file_path = os.path.join(uploads_dir, file.name)
    with open(file_path, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    print(">>> File saved")
    return file_path