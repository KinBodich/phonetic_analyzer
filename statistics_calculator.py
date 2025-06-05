from collections import Counter

# Мапа ARPAbet (без цифри стресу) → IPA
ARPABET_TO_IPA = {
    "AA": "ɑ",   "AE": "æ",  "AH": "ʌ",  "AO": "ɔ",
    "AW": "aʊ",  "AY": "aɪ", "EH": "ɛ",  "ER": "ɝ",
    "EY": "eɪ",  "IH": "ɪ",  "IY": "i",  "OW": "oʊ",
    "OY": "ɔɪ",  "UH": "ʊ",  "UW": "u",

    "B": "b",    "CH": "tʃ", "D": "d",   "DH": "ð",
    "F": "f",    "G": "g",   "HH": "h",  "JH": "dʒ",
    "K": "k",    "L": "l",   "M": "m",   "N": "n",
    "NG": "ŋ",   "P": "p",   "R": "ɹ",   "S": "s",
    "SH": "ʃ",   "T": "t",   "TH": "θ",  "V": "v",
    "W": "w",    "Y": "j",   "Z": "z",   "ZH": "ʒ"
}

class StatisticsCalculator:
    def __init__(self, vowels):
        self.vowels = vowels  # ARPAbet-символи голосних із цифрами (наприклад, "AH0", "IH1")
        # Усі можливі IPA-символи, що відповідають ARPAbet
        self.all_ipa_symbols = sorted(set(ARPABET_TO_IPA.values()))

    def is_vowel(self, ph):
        return ph.rstrip("012") in self.vowels

    def count_consonants_vowels(self, phonemes):
        v = sum(1 for p in phonemes if self.is_vowel(p))
        c = len(phonemes) - v
        return c, v

    def count_open_closed_syllables(self, syllables):
        open_s, closed_s = 0, 0
        for s in syllables:
            last_ph = s[-1].rstrip("012")
            if last_ph in self.vowels:
                open_s += 1
            else:
                closed_s += 1
        return open_s, closed_s

    def get_cvv_structure(self, syllable):
        return ''.join(['V' if self.is_vowel(p) else 'C' for p in syllable])

    def count_cvv_patterns(self, syllables):
        cvv_counter = Counter()
        for s in syllables:
            pattern = self.get_cvv_structure(s)
            cvv_counter[pattern] += 1
        return dict(cvv_counter)

    def count_first_syllables_patterns(self, syllables_by_word):
        first_counter = Counter()
        for word_sylls in syllables_by_word:
            if word_sylls:
                pattern = self.get_cvv_structure(word_sylls[0])
                first_counter[pattern] += 1
        return dict(first_counter)

    def arpabet_to_ipa(self, phoneme):
        """
        Перетворює ARPAbet (з цифрою стресу) на символ IPA.
        Якщо немає у мапі — повертає оригінальний ARPAbet як заповнювач.
        """
        key = phoneme.rstrip("012")
        return ARPABET_TO_IPA.get(key, phoneme)

    def compute(self, phonemes, syllables_flat, syllables_by_word):
        # 1) Підрахунок приголосних і голосних
        c, v = self.count_consonants_vowels(phonemes)

        # 2) Відкриті / закриті склади
        open_s, closed_s = self.count_open_closed_syllables(syllables_flat)

        # 3) CVV-шаблони для всіх складів
        cvv_patterns = self.count_cvv_patterns(syllables_flat)
        first_syll_patterns = self.count_first_syllables_patterns(syllables_by_word)

        

        # 7) Формуємо результуючий словник у порядку:
        #    1) базові метрики 
        #    2) CVV-шаблони (відсортовані за ключем) 
        #    3) шаблони перших складів (відсортовані за key) 
        #    4) усі IPA-символи (в порядку self.all_ipa_symbols)
        result = {
            "Total C": c,
            "Total V": v,
            "C/V": round(c / v, 4) if v else 0,
            "Opened": open_s,
            "Closed": closed_s,
            "Opened/Closed": round(open_s / closed_s, 4) if closed_s else 0
        }

        # Додаємо CVV-шаблони
        for pat in sorted(cvv_patterns.keys()):
            result[pat] = cvv_patterns[pat]

        # Додаємо шаблони перших складів (sorted по ключу)
        for pat in sorted(first_syll_patterns.keys()):
            result[f"first_{pat}"] = first_syll_patterns[pat]

        # 4) Підрахунок ARPAbet-фонем
        phoneme_counts = Counter(phonemes)
        total_phonemes = len(phonemes) if phonemes else 1  # щоб уникнути ділення на нуль

        # 5) Конвертація ARPAbet → IPA та підрахунок кількості IPA
        ipa_counts = Counter()
        for arp, cnt in phoneme_counts.items():
            ipa_sym = self.arpabet_to_ipa(arp)
            ipa_counts[ipa_sym] += cnt

        # 6) Обчислення частоти IPA як пропорції (0.00000) для всіх IPA-символів
        ipa_frequencies = {}
        for ipa_sym in self.all_ipa_symbols:
            cnt = ipa_counts.get(ipa_sym, 0)
            ipa_frequencies[ipa_sym] = round(cnt / total_phonemes, 5)

        # Вкінці — додаємо всі IPA-символи (sorted по self.all_ipa_symbols)
        for ipa_sym in self.all_ipa_symbols:
            result[ipa_sym] = ipa_frequencies[ipa_sym]

        return result
