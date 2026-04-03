import os

def save_temp_file(upload_file, filename: str) -> str:
    path = f"temp_{filename}"
    with open(path, "wb") as f:
        f.write(upload_file)
    return path

def delete_file(path: str):
    if os.path.exists(path):
        os.remove(path)