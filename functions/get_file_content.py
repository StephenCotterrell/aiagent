import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.abspath(file_path)

        if not os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs:
            return f'Error: cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_path_abs):
            return f"Error: File not found or is not a regular file: {file_path}"

        with open(file_path_abs, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if len(file_content_string) == MAX_CHARS:
                return (
                    file_content_string
                    + f'[...File "{file_path}" truncated at 10000 characters'
                )

            return file_content_string
    except Exception as err:
        return f"Error: {err}. There was an error reading the file at {file_path}."
