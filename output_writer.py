import os
from openpyxl import Workbook, load_workbook

class OutputWriter:
    def __init__(self, output_folder):
        self.output_folder = output_folder
        self.vowels = {
            "AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER",
            "EY", "IH", "IY", "OW", "OY", "UH", "UW"
        }

    def write_transcription(self, name, data):
        path = os.path.join(self.output_folder, "Transcribed", f"{name}.txt")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(" ".join(" ".join(phonemes) for _, phonemes in data))

    def write_syllables(self, name, data):
        path = os.path.join(self.output_folder, "Syllables", f"{name}.txt")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            result = []
            for _, syllables in data:
                syll_str = "/".join("-".join(p for p in s) for s in syllables)
                result.append(syll_str)
            f.write(" ".join(result))

    def write_syllables_cvv(self, name, data):
        path = os.path.join(self.output_folder, "SyllablesCVV", f"{name}.txt")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            output_line = " ".join(
                "/".join("".join("V" if p.rstrip("012") in self.vowels else "C" for p in syll)
                         for syll in syllables)
                for _, syllables in data
            )
            f.write(output_line)

    def write_first_syllables(self, name, data):
        path = os.path.join(self.output_folder, "FirstSyllables", f"{name}.txt")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            output_line = " ".join(
                "-".join(syllables[0]) if syllables else ""
                for _, syllables in data
            )
            f.write(output_line)

    def write_first_syllables_cvv(self, name, data):
        path = os.path.join(self.output_folder, "FirstSyllablesCVV", f"{name}.txt")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            output_line = " ".join(
                "".join("V" if p.rstrip("012") in self.vowels else "C" for p in syllables[0])
                if syllables else ""
                for _, syllables in data
            )
            f.write(output_line)

    def write_statistics(self, name, data):
        path = os.path.join(self.output_folder, "Statistics.xlsx")
        if not data:
            return

        # Збираємо всі ключі для заголовка
        all_keys = set()
        for row in data:
            all_keys.update(row.keys())

        fieldnames = ["Text", "Length", "SyllablesCount"] + sorted(
            k for k in all_keys if k not in {"Text", "Length", "SyllablesCount"}
        )

        # Створюємо папку, якщо треба
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Відкриваємо існуючий файл або створюємо новий
        if os.path.exists(path):
            wb = load_workbook(path)
            ws = wb.active
        else:
            wb = Workbook()
            ws = wb.active
            ws.append(fieldnames)

        # Додаємо рядки
        for row in data:
            ws.append([row.get(fn, "") for fn in fieldnames])

        wb.save(path)

    def write_unknown(self, name, unknown_list):
        path = os.path.join(self.output_folder, "UnknownWords", f"{name}_unknown.txt")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            for w in unknown_list:
                f.write(w + "\n")
