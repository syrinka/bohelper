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


def print_aspects(aspects: Dict, endl=True) -> int:
    zhext = 0
    result = []
    copies = aspects.copy()

    # show principle first
    for i in colors.keys():
        if i in copies:
            n = copies.pop(i)
            label = ITEMS[i]['Label']
            zhext += len(label)
            text = Text(label)
            text.stylize(colors[i])
            text.append('x' + str(n))
            result.append(text)

    for i, n in copies.items():
        label = ITEMS[i]['Label']
        zhext += len(label)
        text = Text(label)
        result.append(text)

    txt = Text(' ').join(result)
    rich.print(txt, end='\n' if endl else '')
    return zhext + len(txt)

