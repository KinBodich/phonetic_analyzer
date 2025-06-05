import os
import time
from reader import read_txt_file, get_txt_files_in_folder
from phonetic_analyzer import PhoneticAnalyzer
from syllabifier import Syllabifier
from statistics_calculator import StatisticsCalculator
from output_writer import OutputWriter

def process_text(name, words, writer, stats_collector, analyzer, syllabifier):
    phonemes_by_word = {w: analyzer.get_phonetic(w) for w in words}
    syllables_by_word = {w: syllabifier.syllabify(phonemes_by_word[w]) for w in words}

    writer.write_transcription(name, [(w, phonemes_by_word[w]) for w in words])
    writer.write_syllables(name, [(w, syllables_by_word[w]) for w in words])
    writer.write_syllables_cvv(name, [(w, syllables_by_word[w]) for w in words])
    writer.write_first_syllables(name, [(w, syllables_by_word[w]) for w in words])
    writer.write_first_syllables_cvv(name, [(w, syllables_by_word[w]) for w in words])

    all_phonemes = [ph for w in words for ph in phonemes_by_word[w]]
    all_syllables = [s for w in words for s in syllables_by_word[w]]
    syllables_by_word_list = [syllables_by_word[w] for w in words]

    row = stats_collector.compute(all_phonemes, all_syllables, syllables_by_word_list)
    row["Text"] = name
    row["Length"] = sum(len(w) for w in words)
    row["PhonemeCount"] = len(all_phonemes)
    total_syllables = sum(len(syllables_by_word[w]) for w in words)
    row["SyllablesCount"] = total_syllables
    if total_syllables:
        row["AverageSyllables"] = round(len(all_phonemes) / total_syllables, 5)
    else:
        row["AverageSyllables"] = 0.0

    return row

def main(input_path, output_path, log_callback=None):
    """
    Якщо log_callback передано, то кожен виклик log_callback(message)
    додасть message у лог GUI.
    """
    analyzer = PhoneticAnalyzer()
    syllabifier = Syllabifier()
    writer = OutputWriter(output_path)
    stats_collector = StatisticsCalculator(vowels=writer.vowels)

    results = []
    files_to_process = []

    if os.path.isdir(input_path):
        files_to_process = get_txt_files_in_folder(input_path)
    else:
        files_to_process = [input_path]

    total_files = len(files_to_process)
    processed_count = 0

    total_start = time.time()

    for idx, path in enumerate(files_to_process, start=1):
        name = os.path.splitext(os.path.basename(path))[0]
        file_label = f"[{idx}/{total_files}] {os.path.basename(path)}"
        try:
            file_start = time.time()
            words = read_txt_file(path)
        except UnicodeDecodeError:
            if log_callback:
                log_callback(f"{file_label} Пропущено (не UTF-8)")
            continue
        except Exception as e:
            if log_callback:
                log_callback(f"{file_label} Помилка при читанні: {e}")
            continue

        if log_callback:
            log_callback(f"{file_label} Початок обробки")
        try:
            row = process_text(name, words, writer, stats_collector, analyzer, syllabifier)
            results.append(row)
            processed_count += 1
            file_end = time.time()
            duration = round(file_end - file_start, 3)
            if log_callback:
                log_callback(f"{file_label} Час обробки {duration} сек.")
        except Exception as e:
            if log_callback:
                log_callback(f"{file_label} Помилка при обробці: {e}")
            continue

    total_end = time.time()
    total_duration = round(total_end - total_start, 3)
    writer.write_statistics("Statistics.xlsx", results)
    if log_callback:
        log_callback(f"Завершено: успішно оброблено {processed_count} з {total_files} файлів.")
        log_callback(f"Загальний час: {total_duration} сек.")
