from pathlib import Path
import json
from typing import Dict, List, Tuple

bhcontent = Path(r'C:\Program Files (x86)\Steam\steamapps\common\Book of Hours\bh_Data\StreamingAssets\bhcontent')


def json_read(path):
    return json.load(open(path, encoding='utf-8'))

def get_tome_mystery(tome: Dict) -> Tuple[str, int]:
    key = next(i for i in tome['aspects'].keys() if i.startswith('mystery.'))
    return key.removeprefix('mystery.'), tome['aspects'][key]

def get_recipe_skill(recipe: Dict) -> str:
    key = next(i for i in recipe['reqs'].keys() if i.startswith('s.'))
    return key

items = {}

skills = {}
for e in json_read(bhcontent / 'loc_zh-hans' / 'elements' / 'skills.json')['elements']:
    e['ID'] = e.pop('id')
    skills[e['ID']] = e
    e.pop('slots') # useless field
    e['recipes'] = [] # reserved for recipes resolving


# t.journalofsirdavidgreene1903 这本书没有中文数据
tomes = {}
for e in json_read(bhcontent / 'core' / 'elements' / 'tomes.json')['elements']:
    tomes[e['ID']] = e
    m, s = get_tome_mystery(e)
    e['mystery'] = m
    e['soph'] = s
    e['memory'] = e['xtriggers']['reading.' + m][0]['id']
    e['skill'] = e['xtriggers']['mastering.' + m][0]['id'].replace('x.', 's.') # replace course to skill
    items.setdefault(e['memory'], None)
    e.pop('xtriggers')
    if 'slots' in e:
        e['lang'] = e['slots'][0]['required'].popitem()[0]
        e.pop('slots')
    for key in ('xexts', 'aspects', 'inherits', 'unique', 'audio', 'manifestationtype'):
        e.pop(key)

for e in json_read(bhcontent / 'loc_zh-hans' / 'elements' / 'tomes.json')['elements']:
    # 补充汉化
    e['ID'] = e.pop('id')
    tomes[e['ID']]['Label'] = e['Label']
    tomes[e['ID']]['Desc'] = e['Desc']


# 配方
paths = [
    bhcontent / 'core' / 'recipes' / 'crafting_4b_prentice.json',
    bhcontent / 'core' / 'recipes' / 'crafting_3_scholar.json',
    bhcontent / 'core' / 'recipes' / 'crafting_2_keeper.json',
]
for tier, path in enumerate(paths):
    for e in json_read(path)['recipes']:
        skill = get_recipe_skill(e)
        input = e['reqs']
        input.pop('ability')
        input.pop(skill)
        output = e['effects'].popitem()[0]
        skills[skill]['recipes'].append({
            'input': input,
            'output': output,
            'tier': tier + 1
        })
        for i in input.keys():
            items.setdefault(i, None)
        items.setdefault(output, None)


# 性向
for e in json_read(bhcontent / 'loc_zh-hans' / 'elements' / 'aspecteditems.json')['elements']:
    e['ID'] = e.pop('id')
    if e['ID'] in items:
        items[e['ID']] = e
        if 'xexts' in e:
            e.pop('xexts')
for e in json_read(bhcontent / 'core' / 'elements' / 'aspecteditems.json')['elements']:
    if e['ID'] in items:
        aspects = e['aspects']
        items[e['ID']]['aspects'] = aspects
        toremove = []
        for i in aspects.keys():
            if i.startswith('boost.') or i.startswith('e.'):
                toremove.append(i)
        for i in toremove:
            aspects.pop(i)
        for i in aspects.keys():
            items.setdefault(i, None)
for e in json_read(bhcontent / 'loc_zh-hans' / 'elements' / '_aspects.json')['elements']:
    e['ID'] = e.pop('id')
    if 'label' in e:
        e['Label'] = e.pop('label')
    if e['ID'] in items:
        items[e['ID']] = e

json.dump({
    'skills': skills,
    'tomes': tomes,
    'items': items,
}, open('data.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)