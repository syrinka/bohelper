import json
import rich
import click
import utils
from utils import tomes, mems

persist = json.load(open('persist.json', encoding='utf-8'))


@click.group()
def bohelper():
	pass


@bohelper.command()
@click.argument('book')
def search(book: str):
	print(tomes[book])


@bohelper.group()
def lib():
	pass

@lib.command()
@click.argument('book')
def add(book: str):
	if book in persist['lib']:
		print('duplicated!')
	elif book in tomes:
		print('added')
		persist['lib'].append(tomes[book]['Label'])
		json.dump(persist, open('persist.json', 'w', encoding='utf-8'), ensure_ascii=False)
	else:
		print('not found!')


@lib.command()
@click.argument('book')
def rm(book: str):
	if book in persist['lib']:
		print('removed')
		persist['lib'].remove(book)
		json.dump(persist, open('persist.json', 'w', encoding='utf-8'), ensure_ascii=False)
	else:
		print('not found!')


@lib.command()
def ls():
	for book in persist['lib']:
		utils.printbook(tomes[book])


@lib.command()
@click.argument('element', type=click.Choice(utils.aspect.keys()))
def find(element: str):
	aid = utils.aspect[element][0]
	stash = {}

	for i in persist['lib']:
		bdata = tomes[i]
		mem = mems[bdata['memory']]
		memid = mem['id']
		if aid in mem['aspects']:
			stash.setdefault(memid, [])
			stash[memid].append(bdata)

	for memid in stash:
		mem = mems[memid]
		utils.printmem(mem)
		for bdata in stash[memid]:
			print('  ', end='')
			utils.printlabel(bdata['Label'])


@lib.command()
@click.argument('file')
def load(file):
	save = json.load(open(file, encoding='utf-8'))
	raw = json.dumps(save['RootPopulationCommand']['Spheres'])
	books = []
	for book in save['CharacterCreationCommands'][0]['UniqueElementsManifested']:
		start = raw.find(book, 5000)
		end = raw.find('Illuminations', start)
		if 'mastery' in raw[start:end]:
			books.append(utils.id2label[book])
	for i in books:
		print(i)
	persist['lib'] = books
	json.dump(persist, open('persist.json', 'w', encoding='utf-8'), ensure_ascii=False)


@bohelper.command()
def lsaspects():
	utils.lsaspect()

@bohelper.command()
def lstomes():
	for book in tomes.values():
		utils.printbook(book)


if __name__ == '__main__':
	bohelper()
