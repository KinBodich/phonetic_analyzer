import os
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
    row["SyllablesCount"] = sum(len(syllables_by_word[w]) for w in words)

    return row

def main(input_path, output_path):
    analyzer = PhoneticAnalyzer()
    syllabifier = Syllabifier()
    writer = OutputWriter(output_path)
    stats_collector = StatisticsCalculator(vowels=writer.vowels)

    results = []

    if os.path.isdir(input_path):
        files = get_txt_files_in_folder(input_path)
        for path in files:
            name = os.path.splitext(os.path.basename(path))[0]
            words = read_txt_file(path)
            row = process_text(name, words, writer, stats_collector, analyzer, syllabifier)
            results.append(row)
    else:
        name = os.path.splitext(os.path.basename(input_path))[0]
        words = read_txt_file(input_path)
        row = process_text(name, words, writer, stats_collector, analyzer, syllabifier)
        results.append(row)

    writer.write_statistics("Statistics.csv", results)
