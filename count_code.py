import os
import re
from argparse import ArgumentParser

def get_filepaths(path):
    files = []

    for f in [os.path.join(path, i) for i in os.listdir(path)]:
        ext = f.split(".")[-1]
        if ext == "py": files.append(f)

        if os.path.isdir(f):
            files.extend(get_filepaths(os.path.join(path, f)))

    return files

def lines_of_code(filename):
    data = None
    with open(filename, "r") as f: data = f.read()

    # cut multiline comments
    data = "".join(data.split("\"\"\"")[::2])

    lines = data.split("\n")

    # cut one line comments
    lines = [line for line in lines if not line.startswith("#")]

    # remove empty lines
    lines = [line for line in lines if line.strip() != ""]

    return len(lines)

def main():
    parser = ArgumentParser(description="Count lines of python code in a certain folder")
    parser.add_argument("-p", "--path", action="append", dest="paths",
                        help="specify subdirectories to scan, defaults to current directory")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="show more information on screen")
    parser.add_argument("-o", "--ordered", action="store_true",
                        help="show files ordered number of lines (crescent)")
    args = parser.parse_args()
    if not args.paths:
        args.paths = [os.getcwd()]

    # get all files to count
    files = []
    for path in args.paths:
        start_dir = os.getcwd()
        os.chdir("".join(["." for _ in range(path.count("."))]))

        files.extend(get_filepaths(os.path.join(os.getcwd(), path.replace(".", ""))))

        os.chdir(start_dir)

    # count number of lines
    lines = list(map(lines_of_code, files))

    if args.verbose:
        pretty = dict(zip(files, lines))
        if args.ordered:
            # sort by number of lines
            keys = sorted(pretty.keys(), key=lambda k: pretty[k], reverse=True)
        else:
            keys = sorted(pretty.keys())

        # print info
        for k in keys:
            filename = "/".join(k.split("\\")[-2:])
            print(filename, "-->", pretty[k], "line" if pretty[k] == 1 else "lines")

    print(sum(lines), "lines of code in total")

if __name__ == "__main__":
    main()
