#cmd to create exe file
#python -m PyInstaller --onefile bossgame.py --add-data "sounds;sounds" --add-data "lang;lang"

import os
import time
import arcade

import sounds
import ASCII
from lib import chooseLanguage, get_key, s

from classesCharacter import Player, Enemy, Mage
from classesSpell import FireSpell, IceSpell, HealSpell
from classesWeapon import Weapon
from classesPotion import HealPotion, ManaPotion

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

#LOX 4

#Language selection
chooseLanguage()

#Playername's input and validating
clear()
playername = input(s("enter_your_name"))
while len(playername) > 5 or len(playername) < 3:
    clear()
    print(s("name_restriction"))
    playername = input(s("enter_your_name"))

#Usernames for tests
match playername:
    case "Аллах" | "Allah":
        player = Player(playername, 9999, 9999, 9999)
    case "dodik":
        player = Player(playername, 1, 0)
    case _:
        player = Player(playername, 100, 0)

# Giving the player a weapon: Weapon(name, minDamage, maxDamage, +manaPerHit, critChance, critMultiplier, image, critImage, sound)
stick = Weapon(s("wooden_stick"), 5, 5, 5, 0.2, 5, None, None, sounds.sticksound)
player.weapons.append(stick)

# Giving the player a potion
player.potions.append(HealPotion(s("heal_potion"), 2, 20))
player.potions.append(ManaPotion(s("magic_potion"), 2, 25))

player.spells.append(HealSpell(s("healing"), 20, 20))
    
# Creating the first enemy
worm = Enemy(s("worm"), 25, 5, 5)

while worm.alive == True:
    player.makeMove(worm)
    time.sleep(1.9)

    worm.makeMove(player)
    time.sleep(1.9)


#First victory screen
clear()
print(ASCII.drawtrophy)
arcade.play_sound(sounds.victorysound)
print(f"{s('you_defeated')}: {worm.name}!")
time.sleep(3)

#Giving the player a sword 
clear()
print(ASCII.drawtemplate)
sword = Weapon(s("sword"), 8, 12, 10, 0.5, 2, ASCII.drawsword, ASCII.drawswordcrit, sounds.swordsound)
player.weapons.append(sword)
print(f"{s('new_weapon_recieved')}: {sword.name}!")
time.sleep(1.9)

# Creating the second enemy
fatWorm = Enemy(s("fat_worm"), 75, 5, 10)

while fatWorm.alive == True:
    player.makeMove(fatWorm)
    time.sleep(1.9)

    fatWorm.makeMove(player)
    time.sleep(1.9)

# Second victory screen
clear()
print(ASCII.drawtrophy)
arcade.play_sound(sounds.victorysound)
print(f"{s('you_defeated')}: {fatWorm.name}!")
time.sleep(3)

# Giving the player 1 spell to choose
while len(player.spells) == 1:
    clear()
    print(ASCII.drawtemplate)
    print(f"{s('choose_a_spell')}:")
    print(f"[1]{s('fireball')}! [2]{s('iceshard')}")
    choice = get_key()
    match choice:
        case 1: player.spells.append(FireSpell(s("fireball"), 10, 20, 15, 0.5, 15))
        case 2: player.spells.append(IceSpell(s("iceshard"), 5, 10, 15, 0.5, 2))
        case _: pass

#Third enemy creating
wormKing = Enemy(s("worm_king"), 150, 10, 15)

while wormKing.alive == True:
    player.makeMove(wormKing)
    time.sleep(1.9)

    wormKing.makeMove(player)
    time.sleep(1.9)

#Third victory screen
clear()
print(ASCII.drawtrophy)
arcade.play_sound(sounds.victorysound)
print(f"{s('you_defeated')}: {wormKing.name}!")
time.sleep(3)


# Giving the player spells: Spell(name, minDamage, maxDamage, manaCost)
# For FireSpell, the last two values are burn chance and strength; for IceSpell, freeze chance and duration
# player.spells.append(FireSpell(s("fireball"), 2, 4, 3, 0.5, 3))
# player.spells.append(IceSpell(s("iceshard"), 1, 2, 3, 0.5, 2))
# player.spells.append(FireSpell(s("ignition"), 0, 1, 2, 1, 2))

#4th enemy creating
evilMage = Mage(s('evil_mage'), 200)
evilMage.spells.append(FireSpell(s("ignition"), 1, 5, 0, 0.9, 10))

# giving evil mage the spell, that player didnt choose
if any(spell.name == s("fireball") for spell in player.spells):
    evilMage.spells.append(IceSpell(s("iceshard"), 5, 10, 15, 0.4, 2))
else:
    evilMage.spells.append(FireSpell(s("fireball"), 10, 20, 15, 0.4, 15))

while evilMage.alive == True:
    player.makeMove(evilMage)
    time.sleep(1.9)

    evilMage.makeMove(player)
    time.sleep(1.9)

#4th victory screen
clear()
print(ASCII.drawtrophy)
arcade.play_sound(sounds.victorysound)
print(f"{s('you_defeated')}: {evilMage.name}!")
time.sleep(3)

print("Press any key to exit...")
get_key()