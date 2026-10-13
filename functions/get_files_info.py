import os
full_path: str

def directory_item_printer(item_name: str) -> str:
    try:
        item_path = os.path.normpath(os.path.join(full_path, item_name))
        return f"    - {item_name}: file_size={os.path.getsize(item_path)}, is_dir={os.path.isdir(item_path)}"
    except Exception as e:
        return f"Error: {e}"

def get_files_info(working_directory: str, directory: str = ".") -> str:
    global full_path
    try:
        working_dir_abs = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, full_path]) == working_dir_abs
    except Exception as e:
        return f"Error: {e}"


    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'

    if valid_target_dir and os.path.isdir(full_path):
        try:
            contents = os.listdir(full_path)
            item_string = "\n".join(list(map(directory_item_printer, contents)))
        except Exception as e:
            return f"Error: {e}"

        return item_string
