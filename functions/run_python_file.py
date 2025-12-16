import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified python file, with arguments, if provided. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the python file to be run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A list of strings representing the command-line arguments to be passed to the python file.",
            ),
        },
    ),
)


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
            f"STDOUT: {completed_process.stdout} \n STDERR: {completed_process.stderr}"
        )
        if not completed_process.returncode == 0:
            return_string += f"Process exited with code {completed_process.returncode}"

        if completed_process:
            return return_string
        else:
            return "No output produced"

    except Exception as e:
        return f"Error: {e}"
