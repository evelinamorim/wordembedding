import json
import sys


def fix_json(json_file, nlines):
    new_json_fd = open("new_%s" % json_file, "w")
    json_fd = open(json_file, "r")

    new_json_fd.write('[')

    for i in range(0, nlines-1):
        l = json_fd.readline()
        new_json_fd.write(l)
        new_json_fd.write(',')

    l = json_fd.readline()
    new_json_fd.write(l)
    new_json_fd.write(']')
    new_json_fd.close()
    json_fd.close()


def read_review(json_file):
    json_data = open(json_file, "r").read()
    data = json.loads(json_data)

    text_data = open("reviewcomment.txt", "w")

    for r in data:
        text_data.write(r["reviewComment"].lower())
    text_data.close()

if __name__ == "__main__":
    option = sys.argv[1]
    if (option == '-f'):
        file_name = sys.argv[2]
        nlines = int(sys.argv[3])
        fix_json(file_name, nlines)
    else:
        if (option == '-r'):
            file_name = sys.argv[2]
            read_review(file_name)
