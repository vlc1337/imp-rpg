from random import randint
import keyboard, os, configparser, time

clear = lambda: os.system('cls') if os.name == 'nt' else os.system('clear')
move = True
def error():
    for i in range(4):
        print(f'Wrong argument(s) in settings.ini\nPlease recheck guide.py\nExiting in {3-i}...')
        time.sleep(1)
        clear()
    exit()

config = configparser.ConfigParser()
config.read("settings.ini")
try:
    scale = int(config['World Settings']['Map Scale']) - 1
    trees = int(config['World Settings']['Trees Spawn Chance'])
    path = config['World Settings']['Path']
    showenemies = config['World Settings']['Show Enemies']
    herohp = int(config['Gameplay']['Hero HP'])
    heroattack = list(map(int, str(config['Gameplay']['Hero Attack']).split(',')))
    heroheal = list(map(int, str(config['Gameplay']['Hero Heal']).split(',')))
    imphp = list(map(int, str(config['Gameplay']['Imp HP']).split(',')))
    impattack = list(map(int, str(config['Gameplay']['Imp Attack']).split(',')))
    enemiescount = int(config['Gameplay']['Enemies Count'])
    restore = config['Gameplay']['Restore Health After The Battle']
except:
    error()

def area():
    global move
    move = True
    clear()
    view = []
    for i in range(player['y'] - 4, player['y'] + 5):
        row = []
        for j in range(player['x'] - 4, player['x'] + 5):
            if i < 0 or i >= scale or j < 0 or j >= scale:
                row.append('~')
            else:
                row.append('X' if i == player['y'] and j == player['x'] else map[i][j])
        view.append(row)
    for n in view:
        for m in n:
            print(m, end=' ')
        print()

def fight():
    global move
    global imp
    move = False
    clear()
    imp = randint(imphp[0], imphp[1])
    print(f"Your hero was attacked!\nYou have {herohp} HP\nAn enemy imp has {imp} HP")

def heal():
    global herohp
    global move
    if not move:
        heal = randint(heroheal[0], heroheal[1])
        herohp += heal
        print(f"Your HP was restored for {heal} points\nYou have {herohp} HP")
        dmg = randint(impattack[0], impattack[1])
        herohp -= dmg
        print(f'The imp attacked you and you got -{dmg} HP\nYou have {herohp} HP')
        if herohp < 1:
            for i in range(4):
                clear()
                print(f'Imp killed you! The game is over\nExiting in {3-i}...')
                time.sleep(1)
                clear()
            exit()
        if imp < 1:
            move = True
            print(f'The wicked imp is dead! Press l to leave area')
            if restore == 'True':
                herohp = 100

def attack():
    global move
    global imp
    global herohp
    if not move:
        attack = randint(impattack[0], impattack[1])
        imp -= attack
        print(f"You attacked the enemy and he got -{attack}HP\nHe has {imp} HP")
        dmg = randint(impattack[0], impattack[1])
        herohp -= dmg
        print(f'The imp attacked you and you got -{dmg} HP\nYou have {herohp} HP')
        if herohp < 1:
            for i in range(4):
                print(f'Imp killed you! The game is over\nExiting in {3-i}...')
                time.sleep(1)
                clear()
            exit()
        if imp < 1:
            move = True
            print(f'The wicked imp is dead! Press l to leave area')
            if restore == 'True':
                herohp = 100

def up():
    global move
    if move:
        if player['y'] != 0:
            if map[player['y']-1][player['x']] == 'T':
                area()
                return
            else:
                if path == 'True':
                    map[player['y']][player['x']] = '.'
                else:
                    map[player['y']][player['x']] = 'o'
                player['y'] -= 1
                map[player['y']][player['x']] = 'X'
                area()
                for x, y in enemy.items():
                    if x == player['x'] and y == player['y']:
                        fight()
        else:
            area()
            return()

def left():
    global move
    if move:
        if player['x'] != 0:
            if map[player['y']][player['x']-1] == 'T':
                area()
                return
            else:
                if path == 'True':
                    map[player['y']][player['x']] = '.'
                else:
                    map[player['y']][player['x']] = 'o'
                player['x'] -= 1
                map[player['y']][player['x']] = 'X'
                area()
                for x, y in enemy.items():
                    if x == player['x'] and y == player['y']:
                        fight()
        else:
            area()
            return()

def down():
    global move
    if move:
        if player['y'] != scale - 1:
            if map[player['y']+1][player['x']] == 'T':
                area()
                return
            else:
                if path == 'True':
                    map[player['y']][player['x']] = '.'
                else:
                    map[player['y']][player['x']] = 'o'
                player['y'] += 1
                map[player['y']][player['x']] = 'X'
                area()
                for x, y in enemy.items():
                    if x == player['x'] and y == player['y']:
                        fight()
        else:
            area()
            return()

def right():
    global move
    if move:
        if player['x'] != scale - 1:
            if map[player['y']][player['x']+1] == 'T':
                area()
                return
            else:
                if path == 'True':
                    map[player['y']][player['x']] = '.'
                else:
                    map[player['y']][player['x']] = 'o'
                player['x'] += 1
                map[player['y']][player['x']] = 'X'
                area()
                for x, y in enemy.items():
                    if x == player['x'] and y == player['y']:
                        fight()
        else:
            area()
            return()

if trees > 100 or enemiescount > scale ** 2 or scale > 999 or scale < 10 or heroheal[0] > heroheal[1] or imphp[0] > imphp[1] or heroheal[0] > heroheal[1] or imphp[0] > imphp[1] or impattack[0] > impattack[1]:
    error()

map = [['o' for _ in range(scale+1)] for _ in range(scale+1)]
for _ in range(scale ** 2 * trees // 100):
    map[randint(0, scale)][randint(0, scale)] = 'T'
enemy = dict()
for _ in range(enemiescount):
    enemyx = randint(0, scale)
    enemyy = randint(0, scale)
    enemy[enemyx] = enemyy
    if showenemies == 'True':
        map[enemyy][enemyx] = 'E'
player = {'x': randint(0, scale), 'y': randint(0, scale)}
map[player['y']][player['x']] = 'X'
area()

keyboard.add_hotkey('w', up)
keyboard.add_hotkey('a', left)
keyboard.add_hotkey('s', down)
keyboard.add_hotkey('d', right)
keyboard.add_hotkey('f', attack)
keyboard.add_hotkey('h', heal)
keyboard.add_hotkey('l', area)
keyboard.wait()