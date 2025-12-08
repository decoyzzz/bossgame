import os, sys
import random
import arcade
import time

import ASCII
import sounds
from lib import s, get_key
from classesSpell import IceSpell

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

class Character:

    def __init__(self,name = "unnamed Charik", maxHp = 10):
        self.name = name
        self.maxHp = maxHp
        self.hp = maxHp
        self.alive = True
        self.freezebuildup = 0
        self.fire_dot_damage = 0

    def getDamage(self, damage): 
        self.hp = max(0, self.hp - damage)
        if self.hp <= 0:
            self.alive = False

    def getHealed(self, healPoints):
        self.hp = min(self.maxHp, self.hp + healPoints)

    def useMana(self, manaPoints):
        if self.mana >= manaPoints:
            self.mana -= manaPoints
            return True
        else:
            self.mana = 0

            clear()
            print(ASCII.drawtemplate)
            print(s("not_enough_mana"))
            return False

    def restoreMana(self, manaPoints):
        self.mana = min(self.maxMana, self.mana + manaPoints)

    def attack(self, target):
        self.damage = random.randint(1, 3)
        target.getDamage(self.damage)

        clear()
        print(ASCII.drawbossattack)
        arcade.play_sound(sounds.bossattack)
        print (f"{self.name} {s('dealt')} {target.name} {self.damage} {s('damage')}!")

    def makeMove(self, enemy):
        print(s("=enemys_turn="),end='')

        if self.alive == False:
            clear()
            print(ASCII.drawbossdead)
            print(f"{self.name} {s('is_dead!')}")
        
        else:

            if self.freezebuildup > 0:
                
                clear()
                print(ASCII.drawbossfreeze)
                print(f"{self.name} {s('is_freezed_and_skips_their_move!')}")
                
                self.freezebuildup -= 1

            else:
                self.attack(enemy)

            if self.fire_dot_damage > 0:
                time.sleep(1.9)
                clear()
                print(ASCII.drawbossfiredamage)
                arcade.play_sound(sounds.burningsound)
                print(f"{self.name} {s('takes')} {self.fire_dot_damage} {s('fire_damage!')}")

                self.getDamage(self.fire_dot_damage)
                self.fire_dot_damage -= 5


class Player(Character):

    def __init__(self, name="Player", maxHp=100, mana=0, maxMana = 100):
        super().__init__(name, maxHp)
        self.mana = mana
        self.maxMana = maxMana
        self.spells=[]
        self.weapons=[]
        self.potions=[]

    def castSpell(self, spell, target):
        spell.cast(self, target)

    def drinkPotion(self, potion):
        potion.affect(self)
        if potion.count < 1: self.potions.remove(potion)

    def attackWithWeapon(self, weapon, target):
        weapon.attack(self, target)

    def makeMove(self, enemy):
        if self.alive == False:

            clear()
            print(ASCII.drawplayerdead.format(playername=self.name))
            print(s('you_died'))

            # os.system("shutdown /s /t 5")
            # return
            print("Press any key to exit...")
            get_key()
            sys.exit()
        
        elif self.freezebuildup > 0:

            clear()
            print(ASCII.drawtemplate)
            arcade.play_sound(sounds.iceshardsound)
            print(f"{self.name} {s('is_freezed_for')} {self.freezebuildup} {s('more_moves!')}")
            
            self.freezebuildup -= 1

        else:
            #Variables for the player’s turn
            self.heal = random.randint(1, 3)
            
            #player’s turn
            while True:
                clear()
                print(s("=your_turn="),end='')
                print(ASCII.drawmain.format(playername=self.name, bossname=enemy.name))
                print(f"{s('your_hp')}: {self.hp}/{self.maxHp} | {s('your_mana')}: {self.mana}/{self.maxMana} | {s('enemys_hp')}: {enemy.hp}\n")
                print(s("action_menu"))
                action = get_key()
                arcade.play_sound(sounds.buttonsound)

                match action:
                    #Weapon menu
                    case 1:
                        print(f"\n{s('your_weapons')}:")
                        for i in range(len(self.weapons)):
                            weapon = self.weapons[i]
                            if weapon.minDamage != weapon.maxDamage:
                                print(f"[{i+1}] {weapon.name}! ({s('Damage')}: {weapon.minDamage}-{weapon.maxDamage}) ({s('crit')}: {int(weapon.critChance*100)}% x{weapon.critMultiplier})")
                            else : 
                                print(f"[{i+1}] {weapon.name}! ({s('Damage')}: {weapon.minDamage}) ({s('crit')}: {int(weapon.critChance*100)}% x{weapon.critMultiplier})")

                        print(f"[{len(self.weapons) + 1}] {s('back')}!")
                        
                        choice = get_key()
                        if choice in range(1, len(self.weapons)+1):
                            self.attackWithWeapon(self.weapons[choice-1], enemy)
                            return

                    #Potion meny
                    case 2:
                        print(f"\n{s('potion_bag')}:")
                        if not self.potions: print(s("empty"))
                        for i in range(len(self.potions)):
                            potion = self.potions[i]
                            print(f"[{i+1}] ({potion.count}){potion.name}! (+{potion.strength})")

                        print(f"[{len(self.potions) + 1}] {s('back')}!")
                        
                        choice = get_key()
                        if choice in range(1, len(self.potions)+1):
                            self.drinkPotion(self.potions[choice-1])
                            return


                    #Spell menu
                    case 3:
                        print(f"\n{s('your_spells')}:")
                        for i in range(len(self.spells)):
                            spell = self.spells[i]
                            print(f"[{i+1}] {spell.info()}")

                        print(f"[{len(self.spells) + 1}] {s('back')}!")
                        
                        choice = get_key()
                        if choice in range(1, len(self.spells)+1):
                            self.castSpell(self.spells[choice-1], enemy)
                            return
                        elif choice == 7:
                            self.castSpell(IceSpell(s('snow_avalanche'), 500, 500, 0, 1, 10), enemy)
                            return

class Enemy(Character):
    def __init__(self, name = "unnamed Enemy", hp = 10, minDamage = 1, maxDamage = 3):
        self.name = name
        self.hp = hp
        self.minDamage = minDamage
        self.maxDamage = maxDamage
        self.alive = True
        self.freezebuildup = 0
        self.fire_dot_damage = 0

    def attack(self, target):
        self.damage = random.randint(self.minDamage, self.maxDamage)
        target.getDamage(self.damage)

        clear()
        print(ASCII.drawbossattack)
        arcade.play_sound(sounds.bossattack)
        print (f"{self.name} {s('dealt')} {target.name} {self.damage} {s('damage')}!")