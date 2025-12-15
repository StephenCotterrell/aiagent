import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.abspath(os.path.join(working_directory, file_path))

        if not os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(file_path_abs):
            return f'File "{file_path}" not found'

        if not os.path.splitext(file_path_abs)[1] == ".py":
            return f'Error: "{file_path}" is not a Python file.'

        completed_process = subprocess.run(
            ["uv", "run", file_path_abs, *args],
            timeout=30,
            capture_output=True,
            text=True,
        )

        return_string = (
            f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"
        )
        if not completed_process.returncode == 0:
            return_string += f"Process exited with code {completed_process.returncode}"

        if completed_process:
            return return_string
        else:
            return "No output produced"

    except Exception as e:
        return f"Error: {e}"
