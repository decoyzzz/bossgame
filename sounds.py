import sys, os
import arcade

if getattr(sys, 'frozen', False):  
    basedir = sys._MEIPASS
else:
    basedir = os.path.dirname(os.path.abspath(__file__))


#Sounds
swordsound = arcade.load_sound(f"{basedir}/sounds/sword.wav")
healsound = arcade.load_sound(f"{basedir}/sounds/heal.wav")
bossattack = arcade.load_sound(f"{basedir}/sounds/bossattack.wav")
fireballsound = arcade.load_sound(f"{basedir}/sounds/fireball.wav")
iceshardsound = arcade.load_sound(f"{basedir}/sounds/iceshard.wav")
burningsound = arcade.load_sound(f"{basedir}/sounds/burning.wav")
sticksound = arcade.load_sound(f"{basedir}/sounds/stick.wav")
victorysound = arcade.load_sound(f"{basedir}/sounds/victory.wav")
buttonsound = arcade.load_sound(f"{basedir}/sounds/button.wav")
mimimisound = arcade.load_sound(f"{basedir}/sounds/mimimi.wav")