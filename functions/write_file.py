import os


def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.join(working_dir_abs, file_path)

        is_file_path_inside_working_directory = (
            os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs
        )

        if not is_file_path_inside_working_directory:
            return f'Error: cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(os.path.dirname(file_path_abs)):
            os.makedirs(os.path.dirname(file_path_abs))

        with open(file_path_abs, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" {len(content)} characters written'
    except Exception as err:
        print(f"Error: {err}")
        return f"Error: {err}"
