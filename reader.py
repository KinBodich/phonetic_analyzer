import os
import re

class Reader:
    def __init__(self, text):
        self.text = text
        self.token_pattern = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?")

    def tokenize(self):
        return self.token_pattern.findall(self.text)


def read_txt_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    reader = Reader(text)
    return reader.tokenize()


def get_txt_files_in_folder(folder_path):
    files = []
    for fname in os.listdir(folder_path):
        if fname.lower().endswith('.txt'):
            files.append(os.path.join(folder_path, fname))
    return files
