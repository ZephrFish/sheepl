"""
TypeWriter - Realistic keystroke simulation with configurable typing behaviour.

Generates AutoIT Send() sequences that mimic human typing imperfections:
  - Thresholds: epic / good / average / poor — controls error rate and speed variance
  - Realistic typos followed by backspace corrections
  - Random inter-keystroke delays within the chosen threshold

Issue #12: https://github.com/lorentzenman/sheepl/issues/12
"""

__author__ = "Matt Lorentzen @lorentzenman"
__license__ = "MIT"

import random

# Keyboard adjacency map for realistic typo generation.
# Each key maps to its physical neighbours on a QWERTY layout.
_ADJACENCY = {
    'a': 'sqwz', 'b': 'vghn', 'c': 'xdfv', 'd': 'serfcx', 'e': 'wrsd',
    'f': 'drtgvc', 'g': 'ftyhbv', 'h': 'gyujnb', 'i': 'ujko', 'j': 'huikmn',
    'k': 'jiolm', 'l': 'kop', 'm': 'njk', 'n': 'bhjm', 'o': 'iklp',
    'p': 'ol', 'q': 'wa', 'r': 'edft', 's': 'qweadzx', 't': 'rfgy',
    'u': 'yhji', 'v': 'cfgb', 'w': 'qase', 'x': 'zsdc', 'y': 'tghu',
    'z': 'asx',
}

THRESHOLDS = {
    'epic':    {'error_rate': 0.01, 'min_delay': 20,  'max_delay': 60},
    'good':    {'error_rate': 0.03, 'min_delay': 30,  'max_delay': 120},
    'average': {'error_rate': 0.06, 'min_delay': 40,  'max_delay': 250},
    'poor':    {'error_rate': 0.12, 'min_delay': 80,  'max_delay': 500},
}


class TypeWriter:
    """
    Generates a realistic AutoIT typing block for a given string.

    Usage:
        tw = TypeWriter(threshold='average')
        autoit_block = tw.generate("ipconfig /all")
    """

    def __init__(self, threshold='good'):
        if threshold not in THRESHOLDS:
            raise ValueError("threshold must be one of: {}".format(', '.join(THRESHOLDS)))
        cfg = THRESHOLDS[threshold]
        self.error_rate = cfg['error_rate']
        self.min_delay = cfg['min_delay']
        self.max_delay = cfg['max_delay']

    def _typo_char(self, char):
        """Return an adjacent key for the given character, or the char itself."""
        neighbours = _ADJACENCY.get(char.lower(), '')
        if neighbours:
            typo = random.choice(neighbours)
            return typo.upper() if char.isupper() else typo
        return char

    def _delay(self):
        return random.randint(self.min_delay, self.max_delay)

    def _escape(self, char):
        """Escape AutoIT Send() special characters."""
        specials = {'+': '{+}', '!': '{!}', '^': '{^}', '{': '{{}', '}': '{}}', '#': '{#}'}
        return specials.get(char, char)

    def generate(self, text, indent='    '):
        """
        Generate AutoIT Send() statements for the given text with realistic
        typing behaviour (random delays, occasional typo + backspace).

        Returns a string of AutoIT code ready to embed in a Func block.
        """
        lines = []
        for char in text:
            if char == '\n':
                lines.append('{}Send("{{ENTER}}")'.format(indent))
                lines.append('{}Sleep({})'.format(indent, self._delay()))
                continue

            # Introduce a typo then correct it
            if char.lower() in _ADJACENCY and random.random() < self.error_rate:
                typo = self._typo_char(char)
                lines.append('{}Send("{}")'.format(indent, self._escape(typo)))
                lines.append('{}Sleep({})'.format(indent, self._delay()))
                lines.append('{}Send("{{BACKSPACE}}")'.format(indent))
                lines.append('{}Sleep({})'.format(indent, self._delay()))

            if char == '"':
                lines.append('{}Send(Chr(34))'.format(indent))
            else:
                lines.append('{}Send("{}")'.format(indent, self._escape(char)))
            lines.append('{}Sleep({})'.format(indent, self._delay()))

        return '\n'.join(lines)

    def generate_command(self, command, indent='    '):
        """
        Generate AutoIT code to type a shell command and press Enter.
        Wraps generate() and appends an ENTER keystroke.
        """
        block = self.generate(command, indent)
        block += '\n{}Send("{{ENTER}}")'.format(indent)
        block += '\n{}Sleep({})'.format(indent, self._delay())
        return block
