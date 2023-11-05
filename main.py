#from classes.game import Person, bcolors
#from classes.game import turn_end_step
from classes.game import *
from classes.game import turn_start_step
from classes.magic import Spell
from classes.inventory import Item
import random

# print("\n\n")
# print("NAME                     HP                                     MP")
# print("                         _________________________              __________")
# print(bcolors.BOLD + "Valos:        460/460   |" + bcolors.OKGREEN +"████████                 " + bcolors.ENDC + bcolors.BOLD + "|    65/65   |" + bcolors.OKBLUE + "███       " + bcolors.ENDC + bcolors.BOLD + "|" + bcolors.ENDC)




# Instantiate Spells (name, cost, dmg, type)
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 13, 120, "black")
cure = Spell("Cure", 13, 120, "white")
cura = Spell("Cura", 18, 200, "white")

# Instatiate Items (name, type, description, prop)
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super-Potion", "potion", "Heals 500 HP", 500)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 9999)
megaelixir = Item("Mega-Elixir", "elixir", "Fully restores HP/MP of each party member", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)


# Instantiate Characters (name, hp, mp, atk, df, magic, items)
player_spells = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{"item": potion, "quantity": 2},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 3},
                {"item": elixir, "quantity": 5},
                {"item": megaelixir, "quantity": 5},
                {"item": grenade, "quantity": 5}]
player1 = Person("Valos", 300, 65, 60, 34, player_spells, player_items)
player2 = Person("Nick", 350, 65, 60, 34, player_spells, player_items)
player3 = Person("Robot", 200, 65, 60, 34, player_spells, player_items)
enemy1 = Person("Magus", 3000, 100, 150, 250, [], [])
enemy2 = Person("Imp", 1000, 100, 50, 250, [], [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)
while running:
    print("============================================================================================")

    print("NAME                       HP                                     MP")
    # for player in players:
    #     player.get_stats()
    #
    # for enemy in enemies:
    #     enemy.get_enemy_stats()


    for player in players:

        turn_start_step(players=players, enemies=enemies)
        print(player.name, "turn")

        player.choose_action()
        choice = int(input("Choose action: ")) - 1 # take 1 from the input to represent 0: indexing
        #index = int(choice) - 1

        # Choice Attack
        if choice == 0:
            dmg = player.generate_damage()
            enemy_idx = choose_target(enemies=enemies)

            enemies[enemy_idx].take_damage(dmg)
            print(player.name, "attacks", enemies[enemy_idx].name, "for", dmg, "points of damage.")

            score = turn_end_step(players=players, enemies=enemies)
            # if enemies[enemy].get_hp() == 0:
            #     print(enemies[enemy.name, "dies."])
            #     del enemies[enemy]

        # Choice Magic
        elif choice == 1:
            print("Spells")
            player.choose_magic()
            magic_choice = int(input("Choose spell: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            current_mp = player.get_mp()

            # MP check
            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue # go back to the action choice

            player.reduce_mp(spell.cost)
            magic_dmg = spell.generate_damage()

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name, "heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy.take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage." + bcolors.ENDC)

        # Choice Item
        elif choice == 2:
            player.choose_item()
            item_choice = int(input("Choose item: ")) - 1

            if item_choice == -1:
                continue


            item = player.items[item_choice]["item"]
            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1


            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name, "heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixir":
                if item.name == "Mega-Elixir":
                    for player in players:
                        player.hp = player.maxhp
                        player.mp = player.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name, "fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy.take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name, "deals", str(item.prop), "points of damage." + bcolors.ENDC)

        else:
            print("Invalid input, choose again.")
            continue # select again when invalid input

    # ENEMY TURN

    for enemy in enemies:

        turn_start_step(players, enemies)
        print(enemy.name, "turn")
        #enemy_choice = 1
        # implement different actions
        # use random for actions
            # spell points
            # dont use white magic unless health lower than 0.5 etc
        # dont use magic
        # create AI as of collection of exceptions rather than strict paths

        target = random.randrange(0,len(players))
        enemy_dmg = enemy.generate_damage()
        players[target].take_damage(enemy_dmg)
        #print(enemies[enemy].name, "Enemy attacks", players[target].name, "for", enemy_dmg, "points of damage.")
        score = turn_end_step(players=players, enemies=enemies)
        print("end step ok")


    # print("--------------------------------------")
    # print("Enemy HP:", bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + bcolors.ENDC + "\n")
    # print("Player HP:", bcolors.OKGREEN + str(player.get_hp()) + "/" + str(player.get_max_hp()) + bcolors.ENDC)
    # print("Player MP:", bcolors.OKBLUE + str(player.get_mp()) + "/" + str(player.get_max_mp()) + bcolors.ENDC + "\n")

    # CHECK WHEN BATTLE ENDS

    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False

    elif defeated_players == 2:
        print(bcolors.FAIL + "The enemy has defeated you!" + bcolors.ENDC)
        running = False




# https://github.com/nickgermaine?tab=repositories