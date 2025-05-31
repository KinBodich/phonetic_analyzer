import re

SONORITY = {
    # Vowels
    'AA': 5, 'AE': 5, 'AH': 5, 'AO': 5, 'AW': 5, 'AY': 5,
    'EH': 5, 'ER': 5, 'EY': 5, 'IH': 5, 'IY': 5, 'OW': 5,
    'OY': 5, 'UH': 5, 'UW': 5,
    # Glides
    'Y': 4, 'W': 4,
    # Liquids
    'L': 3, 'R': 3,
    # Nasals
    'M': 2, 'N': 2, 'NG': 2,
    # Fricatives and affricates
    'F': 1, 'V': 1, 'TH': 1, 'DH': 1, 'S': 1, 'Z': 1,
    'SH': 1, 'ZH': 1, 'HH': 1, 'CH': 1, 'JH': 1,
    # Stops
    'P': 0, 'B': 0, 'T': 0, 'D': 0, 'K': 0, 'G': 0
}

class Syllabifier:
    def __init__(self):
        self.nucleus_pattern = re.compile(r'.*[0-2]$')

    def sonority(self, phone):
        base = phone.rstrip('012')
        return SONORITY.get(base, 0)

    def is_valid_onset(self, onset):
        for i in range(len(onset) - 1):
            if self.sonority(onset[i]) > self.sonority(onset[i + 1]):
                return False
        return True

    def find_onset_split(self, cluster):
        if len(cluster) == 1:
            return 1
        for split_point in range(len(cluster) + 1):
            onset = cluster[split_point:]
            if self.is_valid_onset(onset):
                return split_point
        return 0

    def syllabify(self, phonemes):
        nuclei = [i for i, p in enumerate(phonemes) if self.nucleus_pattern.match(p)]
        if not nuclei:
            return [phonemes]

        syllables = []
        prev_idx = 0

        for idx, nuc_idx in enumerate(nuclei):
            if idx < len(nuclei) - 1:
                next_nuc = nuclei[idx + 1]
                cluster = phonemes[nuc_idx + 1: next_nuc]
                split = self.find_onset_split(cluster)
                coda = cluster[:split]
            else:
                coda = phonemes[nuc_idx + 1:]

            onset = phonemes[prev_idx: nuc_idx]
            nucleus = [phonemes[nuc_idx]]
            syllables.append(onset + nucleus + coda)

            prev_idx = nuc_idx + 1 + len(coda)

        return syllables

    def format_syllables(self, phonemes):
        syls = self.syllabify(phonemes)
        return ['-'.join(s) for s in syls]