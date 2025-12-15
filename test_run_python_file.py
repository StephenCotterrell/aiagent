from functions.run_python_file import run_python_file

tests = [
    ["calculator", "main.py"],
    ["calculator", "main.py", "3 + 5"],
    ["calculator", "tests.py"],
    ["calculator", "../main.py"],
    ["calculator", "nonexistent.py"],
    ["calculator", "lorem.txt"],
]


def main():
    for index, test in enumerate(tests):
        print(f"Running test {index + 1}. Arguments: {str(test)}")
        try:
            working_directory, file_path, *args = test
            return_value = run_python_file(working_directory, file_path, args)
            if return_value:
                print(return_value)

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
