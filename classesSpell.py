import os
import random
import arcade
import time

import ASCII
import sounds
from lib import s

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

class Spell:
    def __init__(self, name, minDamage, maxDamage, manaCost):
        self.name = name
        self.minDamage = minDamage
        self.maxDamage = maxDamage
        self.manaCost = manaCost

class FireSpell(Spell):
    def __init__(self, name, minDamage, maxDamage, manaCost, burningChance, burningStrength):
        super().__init__(name, minDamage, maxDamage, manaCost)
        self.burningChance = burningChance
        self.burningStrength = burningStrength

    def cast(self, spellcaster, target):
        if spellcaster.mana >= self.manaCost:
            
            self.damage = random.randint(self.minDamage, self.maxDamage)
            target.getDamage(self.damage)
            spellcaster.mana -= self.manaCost
            
            clear()
            print(spellcaster.drawfireball)
            arcade.play_sound(sounds.fireballsound)
            print (f"{spellcaster.name} {s('casts')} {self.name} {s('and_deals')} {self.damage} {s('damage')}! {s('health')} {target.name}: {target.hp}")
            
            #chance to trigger fire DOT damage
            if random.random() < self.burningChance:
                target.fire_dot_damage = max(self.burningStrength, target.fire_dot_damage + 5)

                time.sleep(1.9)
                clear()
                print(target.drawfiredamage)
                arcade.play_sound(sounds.burningsound)
                print(f"{target.name} {s('caught_fire_and_will_take_burn_damage')}!")
        
        #If there is not enough mana
        else:
            spellcaster.getDamage(5)
           
            clear()
            print(spellcaster.drawfireballfailed)
            print (f"{self.name} {s('exploded_in')} {spellcaster.name}{s('s_hand')} {s('and_dealt_5_damage')}! {s('health')}: {spellcaster.hp}")

    def info(self):
        if self.minDamage == self.maxDamage:
            text = f"{self.name}! ({s('Damage')}: {self.minDamage}) ({s('ignition')}: {int(self.burningChance * 100)}%) ({s('cost')}: {self.manaCost})"
        else:
            text = f"{self.name}! ({s('Damage')}: {self.minDamage}-{self.maxDamage}) ({s('ignition')}: {int(self.burningChance * 100)}%) ({s('cost')}: {self.manaCost})"
        return text

class IceSpell(Spell):
    def __init__(self, name, minDamage, maxDamage, manaCost, freezeChance, freezeStrength):
        super().__init__(name, minDamage, maxDamage, manaCost)
        self.freezeChance = freezeChance
        self.freezeStrength = freezeStrength

    def cast(self, spellcaster, target):
        if spellcaster.mana >= self.manaCost:
            
            self.damage = random.randint(self.minDamage, self.maxDamage)
            spellcaster.mana -= self.manaCost
            target.getDamage(self.damage)

            clear()
            print(spellcaster.drawiceshard)
            arcade.play_sound(sounds.iceshardsound)
            print(f"{spellcaster.name} {s('casts')} {self.name} {s('and_deals')} {self.damage} {s('damage')}! {s('health')} {target.name}: {target.hp}")

            if random.random() < self.freezeChance:
                target.freezebuildup = self.freezeStrength

                time.sleep(1.9)
                clear()
                print(target.drawfreeze)
                print(f"{self.name} {s('freezed')} {target.name} {s('for')} {self.freezeStrength} {s('turns')}!")
                                    
            return
                                
        #If there is not enough mana
        else:
            spellcaster.getDamage(5)

            clear()
            print(ASCII.drawfireballfailed)
            print(f"{self.name} {s('froze_the_hand_and_dealt_5_damage')}! {s('health')}: {spellcaster.hp} ")
            return
    
    def info(self):
        if self.minDamage == self.maxDamage:
            text = f"{self.name}! ({s('Damage')}: {self.minDamage}) ({s('freeze')}: {int(self.freezeChance * 100)}%) ({s('cost')}: {self.manaCost})"
        else:
            text = f"{self.name}! ({s('Damage')}: {self.minDamage}-{self.maxDamage}) ({s('freeze')}: {int(self.freezeChance * 100)}%) ({s('cost')}: {self.manaCost})"
        return text
        
class HealSpell(Spell):
    def __init__(self, name, healPoints, manaCost):
        self.name = name
        self.healPoints = healPoints
        self.manaCost = manaCost

    def cast(self, spellcaster, target):
        if spellcaster.useMana(self.manaCost):
            
            spellcaster.getHealed(self.healPoints)

            clear()
            print(ASCII.drawfireballfailed)
            print(f"{spellcaster.name} {s('casts_healing_spell_and_restores')} {self.healPoints}! {s('health')} {spellcaster.name}: {spellcaster.hp}")                 
            return
        
    def info(self):
        text = f"{self.name}! ({s('heals')}: {self.healPoints}) ({s('cost')}: {self.manaCost})"
        return text