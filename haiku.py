import io
from random import randint, choice


def _generate_syllable_mapping(min_syllables=None, max_syllables=None):
    lines = io.open('mhyph.txt', mode='rU', encoding='ISO-8859-1').read().split('\n')
    mapping = {}
    split_char = '\xa5'
    for line in lines:
        if not len(line):
            continue
        line = line.encode('ISO-8859-1')
        components = line.split(split_char)
        syllables = len(components)
        if min_syllables and syllables < min_syllables:
            continue
        if max_syllables and syllables > max_syllables:
            continue
        word = "".join(components)
        if mapping.has_key(syllables):
            mapping[syllables].append(word)
        else:
            mapping[syllables] = [word]
    return mapping

SYLLABLE_MAPPING = _generate_syllable_mapping(max_syllables=7)


class Haiku:

    def __init__(self):
        self.line_1 = self._create_line(5)
        self.line_2 = self._create_line(7)
        self.line_3 = self._create_line(5)

    def __str__(self):
        return self.to_str('\n')

    def to_str(self, separator):
        return separator.join([self.line_1, self.line_2, self.line_3])

    def _create_line(self, num_syllables):
        s = []
        while num_syllables > 0:
            syllables = randint(1, num_syllables)
            word = self._get_word(syllables)
            if not word:
                continue
            s.append(word)
            num_syllables -= syllables
        return " ".join(s)

    def _get_word(self, syllables):
        if SYLLABLE_MAPPING.has_key(syllables):
            return choice(SYLLABLE_MAPPING[syllables])
        else:
            return None