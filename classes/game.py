import random
from .magic import Spell
import math

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    # def generate_spell_damage(self, i):
    #     mgl = self.magic[i]["dmg"] - 5
    #     mgh = self.magic[i]["dmg"] + 5
    #     return random.randrange(mgl, mgh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp
        return self.hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    # def get_spell_name(self, i):
    #     return self.magic[i]["name"]
    #
    # def get_spell_mp_cost(self, i):
    #     return self.magic[i]["cost"]

    def choose_action(self):
        i = 1
        print("\n\n" + bcolors.UNDERLINE + bcolors.BOLD + 40*" " + self.name + "'s turn" + bcolors.ENDC)
        print("\n" + bcolors.BOLD + "ACTIONS:" + bcolors.ENDC)
        for item in self.actions:
            print("    " + str(i) + ".", item)
            i += 1

    def choose_magic(self):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "SPELLS:" + bcolors.ENDC)
        for spell in self.magic:
            print("    " + str(i) + ".", spell.name, "(cost:", str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print("\n" + bcolors.OKGREEN + bcolors.BOLD + "ITEMS:" + bcolors.ENDC)
        for item in self.items:
            print("    " + str(i) + ".", item["item"].name, ":", item["item"].description, "(x" + str(item["quantity"]) + ")")
            i += 1


    def get_stats(self):
        filler1 = (25 - len(self.name)  - len(str(self.hp)) - 1 - len(str(self.maxhp))) * " "
        hp_fill = math.ceil((self.hp * 25 / self.maxhp)) * "█"
        while len(hp_fill) < 25:
            hp_fill += " "
        filler2 = (10 - len(str(self.mp)) - 1 - len(str(self.maxmp))) * " "
        mp_fill = math.ceil((self.mp * 25 / self.maxmp)) * "█"
        while len(mp_fill) < 25:
            mp_fill += " "
        #print("NAME                       HP                                     MP")
        print("                           _________________________              _________________________")
        print(bcolors.BOLD + self.name  + filler1 + str(self.hp) + "/" + str(self.maxhp) + " |" + bcolors.OKGREEN + hp_fill + bcolors.ENDC + bcolors.BOLD + "| " + filler2 + str(self.mp) + "/" + str(self.maxmp) + " |" + bcolors.OKBLUE + mp_fill + bcolors.ENDC + bcolors.BOLD + "|" + bcolors.ENDC)

    def get_enemy_stats(self):
        filler1 = (25 - len(self.name)  - len(str(self.hp)) - 1 - len(str(self.maxhp))) * " "
        hp_fill = math.ceil((self.hp * 25 / self.maxhp)) * "█"
        while len(hp_fill) < 25:
            hp_fill += " "
        filler2 = (10 - len(str(self.mp)) - 1 - len(str(self.maxmp))) * " "
        mp_fill = math.ceil((self.mp * 25 / self.maxmp)) * "█"
        while len(mp_fill) < 25:
            mp_fill += " "
        #print("NAME                       HP                                     MP")
        print("                           _________________________              _________________________")
        print(bcolors.BOLD + self.name  + filler1 + str(self.hp) + "/" + str(self.maxhp) + " |" + bcolors.FAIL + hp_fill + bcolors.ENDC + bcolors.BOLD + "| " + filler2 + str(self.mp) + "/" + str(self.maxmp) + " |" + bcolors.OKBLUE + mp_fill + bcolors.ENDC + bcolors.BOLD + "|" + bcolors.ENDC)




# =====================================================================================
# GAME DEFINITIONS


def turn_start_step(players, enemies):
    for player in players:
        player.get_stats()

    for enemy in enemies:
        enemy.get_enemy_stats()



def turn_end_step(players, enemies):
    score = 0

    for player in players:
        if player.get_hp() == 0:
            print("Party member", player.name, "dies.")
            players.remove(player)

    for enemy in enemies:
        if enemy.get_hp() == 0:
            print(enemy.name, "dies.")
            score =+ random.randrange(1,4)
            enemies.remove(enemy)

    return score


def choose_target(enemies):
    """Lists enemies and takes target for action."""
    i = 1
    print("\n" + bcolors.BOLD + "TARGET:" + bcolors.ENDC)
    for enemy in enemies:
        print(str(i) + ".", enemy.name)
        i += 1
    choice = int(input(bcolors.BOLD + bcolors.UNDERLINE + "Choose target" + bcolors.ENDC + ": ")) - 1
    return choice


def start_turn(players, enemies):
    print('Turn 1')



