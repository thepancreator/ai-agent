import os
from config import *
full_path: str

def write_file(working_directory: str, file_path: str, content: str) -> str:
    global full_path
    try:
        working_dir_abs = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, full_path]) == working_dir_abs
    except Exception as e:
        return f"Error: {e}"

    if not valid_target_file:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(full_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    try:
        with open(full_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
