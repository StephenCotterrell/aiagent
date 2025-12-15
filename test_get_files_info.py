from functions.get_files_info import get_files_info

test_directories = [
    ["calculator", "."],
    ["calculator", "pkg"],
    ["calculator", "/bin"],
    ["calculator", "../"],
]


def main():
    for dirs in test_directories:
        print(get_files_info(dirs[0], dirs[1]))


if __name__ == "__main__":
    main()
