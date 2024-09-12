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
def want(query, tier):
    hold = {}
    cond = parse_condition(query)
    for skill in SKILLS.values():
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
def wantmem(principles):
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
    tomes = []
    for book in save['CharacterCreationCommands'][0]['UniqueElementsManifested']:
        start = raw.find(book, 5000)
        end = raw.find('Illuminations', start)
        if 'mastery' in raw[start:end]:
            tomes.append(book)
    for i in tomes:
        print(i)
    P.tomes = tomes
    P.save()


if __name__ == '__main__':
    bohelper()