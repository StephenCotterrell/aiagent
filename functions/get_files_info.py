import os

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if not os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs:
            return f'Error: cannot list "{directory}" as it  is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        def get_file_info(file):
            abs_file_path = os.path.join(target_dir, file)
            size = os.path.getsize(abs_file_path)
            is_dir = os.path.isdir(abs_file_path)
            return f"- {file}: file_size={size} bytes, is_dir={is_dir}"

        info = []
        for file in os.listdir(target_dir):
            info.append(get_file_info(file))

        return "\n".join(info[::-1])

    except Exception as e:
        return f"Error: {e}"
