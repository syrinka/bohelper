import re
import json
import rich
from rich.text import Text
from typing import Dict

data = json.load(open('data.json', encoding='utf-8'))

TOMES = data['tomes']
SKILLS = data['skills']
ITEMS = data['items']

tome2id = {i['Label']: i['ID'] for i in TOMES.values()}
skill2id = {i['Label']: i['ID'] for i in SKILLS.values()}
item2id = {i['Label']: i['ID'] for i in ITEMS.values()}

colors = {
	'lantern': 'bright_yellow',
	'moth': 'cyan',
	'edge': 'yellow3',
	'forge': 'dark_orange3',
	'winter': 'white',
	'moon': 'cyan1',
	'sky': 'deep_sky_blue1',
	'heart': 'bright_red',
	'grail': 'red3',
	'knock': 'blue_violet',
	'rose': 'blue_violet',
	'scale': 'dark_goldenrod',
	'nectar': 'green3',
	'sound': 'magenta'
}


def parse_condition(query: str):
    cond = []
    fields = re.split(' |,|，', query)
    for field in fields:
        match = re.match(r'(.+?)(\d+)', field)
        if match is None:
            cond.append([item2id.get(field, field), 1])
        else:
            a, n = match.groups()
            cond.append([item2id.get(a, a), int(n)])

    return cond


def print_aspects(aspects: Dict, endl=True):
    result = []
    for i, n in aspects.items():
        text = Text(ITEMS[i]['Label'])
        if i in colors:
            text.stylize(colors[i])
        text.append('x' + str(n))
        result.append(text)
    rich.print(Text(' ').join(result), end='\n' if endl else '')
