import json
import os.path
from typing import List


class Persist(object):
    tomes: List[str]
    skills: List[str]

    def load(self):
        if os.path.exists('persist.json'):
            persist = json.load(open('persist.json', encoding='utf-8'))
            self.tomes = persist['tomes']
            self.skills = persist['skills']
        else:
            print('no persist found, init')
            self.tomes = []
            self.skills = []

    def save(self):
        json.dump({
            'tomes': self.tomes,
            'skills': self.skills
        }, open('persist.json', 'w', encoding='utf-8'), ensure_ascii=False)
