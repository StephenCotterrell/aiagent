from functions.get_file_content import get_file_content

test_file_paths = [
    ["calculator", "lorem.txt"],
    ["calculator", "main.py"],
    ["calculator", "../main.py"],
    ["calculator", "test/test/test/pkg/calculator.py"],
    ["calculator", "pkg/calculator.py"],
    ["calculator", "/bin/cat"],
    ["calculator", "pkg/does_not_exist.py"],
]


def main():
    for file_path in test_file_paths:
        print(get_file_content(file_path[0], file_path[1]))


if __name__ == "__main__":
    main()
