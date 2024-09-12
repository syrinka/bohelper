import json
import click
from typing import Dict
from bohelper.utils import *
from bohelper.persist import Persist


P = Persist()
P.load()


def print_recipe(recipe: Dict):
    print_aspects(recipe['input'], endl=False)
    print(' ==> ' + ITEMS[recipe['output']]['Label'])


@click.group()
def bohelper():
    pass


@bohelper.command()
@click.argument('name')
def recipe(name):
    name = skill2id.get(name, name)
    datum = SKILLS[name]
    for recipe in datum['recipes']:
        print(recipe)


@bohelper.command()
@click.argument('query')
@click.argument('tier', type=click.IntRange(0,3), default=0, required=False)
@click.option('--all', '-a', type=bool, is_flag=True, default=False,
    help='查询所有技艺的配方，默认只查询已习得的技艺。')
def want(query, tier, all):
    """
    查询合成指定条件的物品的配方。

    \b
    QUERY
    =====
    过滤条件。例：
      > 月
      > 蜜4，蛾2
      > 预兆，灯，心3
    将会显示查询性向高于条件的物品。

    \b
    TIER
    ====
    配方等级。可选取值与意义分别为：
    0 - 所有配方（默认值）
    1 - 入门级【5】
    2 - 学者级【10】
    3 - 秘授级【15】
    """
    hold = {}
    cond = parse_condition(query)
    for skill in SKILLS.values():
        if not (all or skill['ID'] in P.skills):
            continue
        label = skill['Label']
        for recipe in skill['recipes']:
            if tier != 0 and recipe['tier'] != tier:
                continue
            output = ITEMS[recipe['output']]
            if output['Label'] == query:
                # direct match
                hold.setdefault(label, [])
                hold[label].append(recipe)
                continue
            aspects = output['aspects']
            for a, n in cond:
                if a not in aspects or aspects[a] < n:
                    break
            else:
                hold.setdefault(label, [])
                hold[label].append(recipe)
    for label, recipes in hold.items():
        print('【%s】' % label)
        for recipe in recipes:
            print_recipe(recipe)


@bohelper.command()
@click.argument('principles', nargs=-1)
@click.option('--all', '-a', type=bool, is_flag=True, default=False,
    help='查询所有书籍的回忆，默认只查询已掌握的书籍。')
def wantmem(principles, all):
    for tome in TOMES.values():
        mem = ITEMS[tome['memory']]
        for p in principles:
            if p in mem['aspects']:
                print(tome['Label'], mem['Label'])
                print_aspects(mem['aspects'])
                break


@bohelper.command()
@click.argument('file')
def load(file):
    save = json.load(open(file, encoding='utf-8'))
    raw = json.dumps(save['RootPopulationCommand']['Spheres'])

    P.tomes.clear()
    for book in save['CharacterCreationCommands'][0]['UniqueElementsManifested']:
        start = raw.find(book, 5000)
        end = raw.find('Illuminations', start)
        if 'mastery' in raw[start:end]:
            P.tomes.append(book)

    P.skills.clear()
    for skill in SKILLS.keys():
        if raw.find(skill, 5000) != -1:
            P.skills.append(skill)

    P.save()


if __name__ == '__main__':
    bohelper()