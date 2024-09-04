
import json
import rich
from rich.console import Console

console = Console()

tomes = json.load(open('data/tomes.json', encoding='utf-8'))
mems = json.load(open('data/mems.json', encoding='utf-8'))

aspect = dict(
	灯=('lantern', 'bright_yellow'),
	蛾=('moth', 'cyan'),
	刃=('edge', 'yellow3'),
	铸=('forge', 'dark_orange3'),
	冬=('winter', 'white'),
	月=('moon', 'cyan1'),
	穹=('sky', 'deep_sky_blue1'),
	心=('heart', 'bright_red'),
	杯=('grail', 'red3'),
	启=('knock', 'blue_violet'),
	引=('rose', 'blue_violet'),
	鳞=('scale', 'dark_goldenrod'),
	蜜=('nectar', 'green3'),
	声=('sound', 'magenta')
)

id2label = {v['id']: k for k, v in tomes.items()}

aspect_rev = {v2[0]: (v1, v2[1]) for v1, v2 in aspect.items()}


def lsaspect():
    for text, asp in aspect.items():
        console.print(text, style=asp[1], end=' ')

def printaspect(asp):
    for i, v in asp.items():
        console.print(aspect_rev[i][0], style=aspect_rev[i][1], end='')
        print('·' + str(v), end='  ')
    print()

def printmem(mem):
    print('「%s」' % mem['Label'], end=' ')
    printaspect(mem['aspects'])

def printlabel(label):
	console.print(label, style='i')

def printbook(data):
    printlabel(data['Label'])
    mem = mems[data['memory']]
    printmem(mem)
