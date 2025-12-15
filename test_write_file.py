from functions.write_file import write_file

tests = [
    ["calculator", "lorem.txt", "wait, this isn't lorem ipsum"],
    ["calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"],
    ["calculator", "/tmp/temp.txt", "this should not be allowed"],
]


def main():
    for test in tests:
        dir, file, content = test
        return_value = write_file(dir, file, content)
        if return_value:
            print(return_value)


if __name__ == "__main__":
    main()
