from enum import Enum

import necrobot.exception

class Category(Enum):
    ASO = 0
    LOW = 1
    ANY = 2
    HELL = 3
    LOWNG = 4
    CUSTOM = 5

    def __str__(self):
        return {
            'ASO': 'All Shortcuts + Olmec',
            'LOW': 'Low%',
            'ANY': 'Any%',
            'HELL': 'Hell%',
            'LOWNG': 'Low% No Gold',
            'CUSTOM': 'Custom Races'
        }[self.name]

    @staticmethod
    def fromstr(char_name):
        for cat in Category:
            if cat.name.lower() == char_name.lower():
                return cat
        raise necrobot.exception.ParseException(f'Error parsing {char_name} as a category.')
