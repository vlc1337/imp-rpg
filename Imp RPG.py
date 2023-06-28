from random import randint
import keyboard, os, configparser, time

clear = lambda: os.system('cls') if os.name == 'nt' else os.system('clear')

def error():
    for i in range(4):
        print(f'Wrong argument(s) in settings.ini\nPlease recheck info.py\nExiting in {3-i}...')
        time.sleep(1)
        clear()
    exit()

config = configparser.ConfigParser()
config.read("settings.ini")
scale = int(config['World Settings']['Map Scale']) - 1
trees = int(config['World Settings']['Trees Spawn Chance'])
path = config['World Settings']['Path']
showenemies = config['World Settings']['Show Enemies']
tshow = config['World Settings']['Show Treasures']
starthp = int(config['Gameplay']['Hero HP'])
herohp = int(config['Gameplay']['Hero HP'])
hpboost = int(config['Gameplay']['Level HP Boost'])
imphp = list(map(int, str(config['Gameplay']['Imp HP']).split(',')))
impattack = list(map(int, str(config['Gameplay']['Imp Attack']).split(',')))
impboost = int(config['Gameplay']['Imp Level Boost'])
enemiescount = int(config['Gameplay']['Enemies Count'])
greward = list(map(int, str(config['Gameplay']['Victory Gold Reward']).split(',')))
xreward = list(map(int, str(config['Gameplay']['Victory XP Reward']).split(',')))
newlvl = int(config['Gameplay']['XP For New Level'])
money = int(config['Gameplay']['Start Balance'])
healcost = int(config['Gameplay']['Healing Cost'])
battleheal = int(config['Gameplay']['Battle Healing Cost'])
healamount = list(map(int, str(config['Gameplay']['Healing Amount']).split(',')))
tcount = int(config['Gameplay']['Treasures Count'])
treward = list(map(int, str(config['Gameplay']['Treasure Reward']).split(',')))
weaponcfg = config['Gameplay']['Weapons']
weaponq = weaponcfg.split('|')
weapons = []
for i in weaponq:
    i = i.split(',')
    weapons.append(i)

move = True
shop = False
heali = False
fight = False
buy = 1

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
    print(f'\nWeapon: {weapons[weapon][0]}    HP: {herohp}    Gold: {money}    Level: {lvl}    XP: {xp}/{newlvl}')

def check():
    global money
    global treward
    for x, y in enemy.items():
        if x == player['x'] and y == player['y']:
            del enemy[player['x']]
            fight()
            return
    for x, y in t.items():
        if x == player['x'] and y == player['y']:
            re = randint(treward[0], treward[1])
            money += re
            del t[player['x']]
            print(f'\nYou found a treasure and you got {re} gold!')
            return

def buyitem():
    global shop
    global money
    global weapon
    global weapons
    global move
    global buy
    if shop:
        if money >= int(weapons[buy][1]):
            try:
                weapon = buy
                print(f'You bought {weapons[buy][0]} for {weapons[buy][1]} gold\nPress l to leave the shop')
                money -= int(weapons[buy][1])
            except:
                print(f'Wrong number! Try again or press l to leave the shop')
        else:
            print(f'Not enough gold! Press l to leave the shop')
        move = True
        shop = False

def shopup():
    global shop
    if shop:
        global buy
        if buy == 1:
            pass
        else:
            buy -= 1
            shopping()

def shopdown():
    global shop
    if shop:
        global buy
        if buy == len(weapons) - 1:
            pass
        else:
            buy += 1
        shopping()

def shopping():
    clear()
    global move
    global shop
    global weapon
    global money
    global buy
    move = False
    shop = True
    print('Weapons list(buy an item using B, scroll items list using ↑, ↓):')
    for i in range(1, len(weapons)):
        if i == buy: 
            print('>  ', end = '')
        print(f'{i}) Weapon: {weapons[i][0]}    Price: {weapons[i][1]}    Critical chance: {weapons[i][2]}    Damage: {weapons[i][3]}-{weapons[i][4]}')

def leave():
    global move
    global shop
    if move or shop:
        area()
        

def fight():
    global move
    global imp
    move = False
    clear()
    imp = randint(imphp[0], imphp[1]) + impboost * (lvl - 1)
    print(f"Your hero was attacked!\nYou have {herohp} HP\nAn enemy imp has {imp} HP")

def heal():
    global herohp
    global money
    global move
    global shop
    global heali
    global starthp
    if not shop and move:
        if herohp >= starthp + hpboost * (lvl - 1):
            print('You have full HP, no need to heal')
        else:
            print(f"Do you want to heal for {healcost} gold? Press y is yes")
            heali = True
    if not move and not shop:
        if herohp >= starthp + hpboost * (lvl - 1):
            print('You have full HP, no need to heal') 
        else:
            print(f"Do you want to heal for {battleheal} gold? Press y is yes")
            heali = True

def y():
    global heali
    global money
    global healcost
    global herohp
    global healamount
    if heali and move:
        if money >= healcost:
            money -= healcost
            healamoun = randint(healamount[0], healamount[1])
            if healamoun + herohp >= starthp + hpboost * (lvl - 1):
                healamoun = starthp + hpboost * (lvl - 1) - herohp
            herohp += healamoun
            print(f"Your HP was restored for {healamoun} points\nYou have {herohp} HP and {money} gold now")
        else:
            print(f'Not enough gold!')
    if heali and not move:
        if money >= battleheal:
            money -= battleheal
            healamoun = randint(healamount[0], healamount[1])
            if healamoun + herohp >= starthp + hpboost * (lvl - 1):
                healamoun = starthp + hpboost * (lvl - 1) - herohp
            herohp += healamoun
            print(f"Your HP was restored for {healamoun} points\nYou have {herohp} HP and {money} gold now")
        else:
            print(f'Not enough gold!')
    heali = False

def attack():
    global move
    global imp
    global herohp
    global money
    global xp
    global lvl
    if not move:
        attack = randint(int(weapons[weapon][3]), int(weapons[weapon][4]))
        if randint(0, 100) < int(weapons[weapon][2]): attack *= 2
        clear()
        imp -= attack
        if imp > 0: print(f"You attacked the enemy and he got -{attack}HP\nHe has {imp} HP")
        dmg = randint(impattack[0], impattack[1]) + impboost // 2 * (lvl - 1)
        herohp -= dmg
        if imp > 0: print(f'The imp attacked you and you got -{dmg} HP\nYou have {herohp} HP')
        if herohp < 1:
            for i in range(4):
                print(f'Imp killed you! The game is over\nExiting in {3-i}...')
                time.sleep(1)
                clear()
            exit()
        if imp < 1:
            move = True
            g = randint(greward[0], greward[1])
            x = randint(xreward[0], xreward[1])
            money += g
            xp += x
            if xp >= newlvl:
                xp = xp % newlvl
                lvl += 1
                herohp = herohp + hpboost * (lvl - 1)
                print(f'You got {lvl} lvl! Now you have {herohp} HP')
            print(f'The wicked imp is dead! You got {g} gold and {x} XP. Press l to leave area')

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
                check()
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
                check()
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
                check()
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
                check()
        else:
            area()
            return()

if trees > 100 or enemiescount > scale ** 2 or scale > 999 or scale < 10 or imphp[0] > imphp[1] or impattack[0] > impattack[1] or greward[0] > greward[1] or xreward[0] > xreward[1]:
    error()

map = [['o' for _ in range(scale+1)] for _ in range(scale+1)]
weapon = 0
xp = 0
lvl = 1
for _ in range(scale ** 2 * trees // 100):
    map[randint(0, scale)][randint(0, scale)] = 'T'
enemy = dict()
t = dict()
for _ in range(enemiescount):
    enemyx = randint(0, scale)
    enemyy = randint(0, scale)
    enemy[enemyx] = enemyy
    if showenemies == 'True':
        map[enemyy][enemyx] = 'E'
for _ in range(tcount):
    tx = randint(0, scale)
    ty = randint(0, scale)
    t[tx] = ty
    if tshow == 'True':
        map[ty][tx] = 'G'
player = {'x': randint(0, scale), 'y': randint(0, scale)}
map[player['y']][player['x']] = 'X'
area()

keyboard.add_hotkey('w', up)
keyboard.add_hotkey('a', left)
keyboard.add_hotkey('s', down)
keyboard.add_hotkey('d', right)
keyboard.add_hotkey('f', attack)
keyboard.add_hotkey('h', heal)
keyboard.add_hotkey('l', leave)
keyboard.add_hotkey('o', shopping)
keyboard.add_hotkey('y', y)
keyboard.add_hotkey('up', shopup)
keyboard.add_hotkey('down', shopdown)
keyboard.add_hotkey('b', buyitem)
keyboard.wait()