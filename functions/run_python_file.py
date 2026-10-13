import os
import subprocess
from config import *

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs python file within working directory, and accepts optional arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path of targeted python file, relative to the working directory",
                }
                "args": {
                    "type": "list[string]",
                    "desciption": "Optional list of arguments to pass to python file",
                },
            },
        },
    }
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, full_path]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(full_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", full_path]
        if args is not None and len(args) > 0:
            command.extend(args)

        completed_process = subprocess.run(command, text=True, timeout=30, capture_output=True)
        return_text = ""
        if completed_process.returncode != 0:
            return_text += f"Process exited with code {completed_process.returncode}"
        if completed_process.stdout == "" and completed_process.stderr == "":
            return_text += f"\nNo output produced"
        else:
            return_text += f"\nSTDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"

        return return_text

    except Exception as e:
        return f"Error: executing python file: {e}"
