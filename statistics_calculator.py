from collections import Counter

class StatisticsCalculator:
    def __init__(self, vowels):
        self.vowels = vowels

    def is_vowel(self, ph):
        return ph.rstrip("012") in self.vowels

    def count_consonants_vowels(self, phonemes):
        v = sum(1 for p in phonemes if self.is_vowel(p))
        c = len(phonemes) - v
        return c, v

    def count_open_closed_syllables(self, syllables):
        open_s, closed_s = 0, 0
        for s in syllables:
            if s[-1].rstrip("012") in self.vowels:
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

    def count_first_syllables_patterns(self, syllables):
        first_counter = Counter()
        for word_sylls in syllables:
            if word_sylls:
                pattern = self.get_cvv_structure(word_sylls[0])
                first_counter[pattern] += 1
        return dict(first_counter)

    def compute(self, phonemes, syllables_flat, syllables_by_word):
        c, v = self.count_consonants_vowels(phonemes)
        open_s, closed_s = self.count_open_closed_syllables(syllables_flat)

        cvv_patterns = self.count_cvv_patterns(syllables_flat)
        first_syll_patterns = self.count_first_syllables_patterns(syllables_by_word)

        result = {
            "Total C": c,
            "Total V": v,
            "C/V": round(c / v, 4) if v else 0,
            "Opened": open_s,
            "Closed": closed_s,
            "Opened/Closed": round(open_s / closed_s, 4) if closed_s else 0
        }

        # Додати всі шаблони складів
        for pat, count in cvv_patterns.items():
            result[pat] = count

        # Додати шаблони перших складів
        for pat, count in first_syll_patterns.items():
            result[f"first_{pat}"] = count

        return result
