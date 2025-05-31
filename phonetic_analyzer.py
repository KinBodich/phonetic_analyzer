import re
import nltk
import pronouncing
from nltk.stem import WordNetLemmatizer
from g2p_en import G2p

# Ensure required NLTK resources
nltk.download('cmudict', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# Фолбек-мапа: назви букв → фонеми (ARPAbet із цифрою стресу)
LETTER_NAME_MAP = {
    'a': ['EY1'],    'b': ['B','IY1'], 'c': ['S','IY1'], 'd': ['D','IY1'],
    'e': ['IY1'],    'f': ['EH1','F'], 'g': ['JH','IY1'], 'h': ['EY1','CH'],
    'i': ['AY1'],    'j': ['JH','EY1'], 'k': ['K','EY1'], 'l': ['EH1','L'],
    'm': ['EH1','M'], 'n': ['EH1','N'], 'o': ['OW1'],   'p': ['P','IY1'],
    'q': ['K','Y','UW1'], 'r': ['AA1','R'], 's': ['EH1','S'], 't': ['T','IY1'],
    'u': ['Y','UW1'], 'v': ['V','IY1'], 'w': ['D','AH1','B','AH0','L','Y','UW0'],
    'x': ['EH1','K','S'], 'y': ['W','AY1'], 'z': ['Z','IY1']
}

class PhoneticAnalyzer:
    def __init__(self):
        self.cmu = nltk.corpus.cmudict.dict()
        self.pronouncing = pronouncing
        self.g2p = G2p()
        self.lemmatizer = WordNetLemmatizer()
        self.phoneme_pattern = re.compile(r'^[A-Z]+[0-2]?$')
        self.unknown = set()

    def normalize(self, word):
        return word.lower().replace("’", "'").strip()

    def split_contraction(self, word):
        patterns = [
            (r"^([a-z]+)n't$", lambda m: [m.group(1), "not"]),
            (r"^([a-z]+)'ll$", lambda m: [m.group(1), "will"]),
            (r"^([a-z]+)'ve$", lambda m: [m.group(1), "have"]),
            (r"^([a-z]+)'re$", lambda m: [m.group(1), "are"]),
            (r"^([a-z]+)'d$", lambda m: [m.group(1), "would"]),
            (r"^([a-z]+)'m$", lambda m: [m.group(1), "am"]),
            (r"^([a-z]+)'s$", lambda m: [m.group(1), "possessive"])
        ]
        for pattern, f in patterns:
            m = re.match(pattern, word)
            if m:
                return f(m)
        return None

    def get_phonetic(self, word):
        key = self.normalize(word)
        # 1) Лематизація
        lemma_v = self.lemmatizer.lemmatize(key, pos='v')
        lemma = self.lemmatizer.lemmatize(lemma_v, pos='n')
        forms = [key] + ([lemma] if lemma != key else [])

        # 2) CMU lookup
        for form in forms:
            if form in self.cmu:
                return self.cmu[form][0]

        # 3) Pronouncing library
        for form in forms:
            phones_list = self.pronouncing.phones_for_word(form)
            if phones_list:
                return phones_list[0].split()

        # 4) Contraction handling
        parts = self.split_contraction(key)
        if parts:
            phones = []
            for part in parts:
                if part == "possessive":
                    phones.append("Z")
                else:
                    ph = self.get_phonetic(part)
                    if ph != ['UNK']:
                        phones.extend(ph)
            return phones or ['UNK']

        # 5) G2P fallback
        raw = []
        try:
            raw = self.g2p(key)
        except Exception:
            pass
        valid = [p for p in raw if self.phoneme_pattern.match(p)]
        if valid:
            return valid
        if raw:
            return raw

        # 6) Letter-to-phoneme fallback
        phones = []
        for ch in key:
            if ch in LETTER_NAME_MAP:
                phones.extend(LETTER_NAME_MAP[ch])
        if phones:
            return phones

        # 7) Mark unknown
        self.unknown.add(key)
        return ['UNK']

    def get_unknown_words(self):
        return list(self.unknown)

    def analyze_text(self, words):
        return [(w, self.get_phonetic(w)) for w in words]
