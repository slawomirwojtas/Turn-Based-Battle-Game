#from classes.game import Person, bcolors
#from classes.game import turn_end_step
from classes.game import *
from classes.game import turn_start_step
from classes.magic import Spell
from classes.inventory import Item
import random
from time import sleep



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


# Instantiate Characters (name, speed, hp, mp, dmgl, dmgh, magic, items)
player_spells = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{"item": potion, "quantity": 2},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 3},
                {"item": elixir, "quantity": 5},
                {"item": megaelixir, "quantity": 5},
                {"item": grenade, "quantity": 5}]
player1 = Person("Dessa", 3, 300, 65, 50, 50, player_spells, player_items)
player2 = Person("Yog", 3, 250, 30, 10, 70, player_spells, player_items)
player3 = Person("Kyrre", 2, 200, 20, 25, 40, player_spells, player_items)
enemy1 = Person("Vampire", 4, 3000, 80, 120, 250, [], [])
enemy2 = Person("Imp", 1, 1000, 100, 50, 150, [], [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2]

running = True
i = 0

# ======================================================================================================================
# START GAME




print("\n" + bcolors.FAIL + bcolors.BOLD + 40*"=" + " WAVE 1 " + 40*"=" + bcolors.ENDC + "\n")

while running:

    for turn in range(1,5):
        print("\n" + bcolors.FAIL + bcolors.BOLD + 40*"-" + "TURN", str(turn) + 40*"-" + bcolors.ENDC + "\n")
        #turn_ended = []
        turn_queue = turn_upkeep(players, enemies)

        # Actions for each player
        for player in turn_queue:

            if player.get_hp == 0: # Pass if player dead
                continue

            else:
                print("\n\n" + bcolors.UNDERLINE + bcolors.BOLD + (85 - len(player.name)) * " " + player.name + "'s turn" + bcolors.ENDC)
                print_stats(players=players, enemies=enemies)

                # Case: player is computer
                if player in enemies:
                    if len(players) == 0: # pass ifno valid target for attack
                        continue
                    else:
                        sleep(1)
                        enemy_ai(enemy=player, players=players)
                        score = turn_end_step(players=players, enemies=enemies)

                # Case: player is human
                else:
                    player.choose_action()
                    choice = int(input(
                        bcolors.BOLD + bcolors.UNDERLINE + "Choose action" + bcolors.ENDC + ": ")) - 1  # take 1 from the input to represent 0: indexing
                    # index = int(choice) - 1

                    # Choice Attack
                    if choice == 0:
                        enemy_idx = choose_target(enemies=enemies)
                        dmg = player.generate_damage()
                        enemies[enemy_idx].take_damage(dmg)
                        # Valos attacks Imp for 65 points of damage.
                        print("\n" + player.name, "attacks", enemies[enemy_idx].name, "for", dmg, "points of damage.")

                    # Choice Magic
                    elif choice == 1:
                        player.choose_magic()
                        magic_choice = int(
                            input(bcolors.BOLD + bcolors.UNDERLINE + "Choose spell" + bcolors.ENDC + ": ")) - 1

                        if magic_choice == -1:
                            continue

                        spell = player.magic[magic_choice]
                        current_mp = player.get_mp()

                        # MP check
                        if spell.cost > current_mp:
                            print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                            continue  # go back to the action choice

                        player.reduce_mp(spell.cost)
                        magic_dmg = spell.generate_damage()

                        if spell.type == "white":
                            player.heal(magic_dmg)
                            print(bcolors.OKBLUE + "\n" + spell.name, "heals for", str(magic_dmg), "HP." + bcolors.ENDC)
                        elif spell.type == "black":
                            enemy_idx = choose_target(enemies=enemies)
                            enemies[enemy_idx].take_damage(magic_dmg)
                            #
                            print("\n" + player.name + "'s", spell.name + " deals", str(magic_dmg), "points to",
                                  enemies[enemy_idx].name + "." + bcolors.ENDC)

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
                            enemy_idx = choose_target(enemies=enemies)
                            #dmg = player.generate_damage()
                            enemies[enemy_idx].take_damage(item.prop)
                            #enemy.take_damage(item.prop)
                            print(bcolors.FAIL + "\n" + item.name, "deals", str(item.prop),
                                  "points of damage." + bcolors.ENDC)

                    else:
                        print("Invalid input, choose again.")
                        continue  # select again when invalid input

                # Player turn end step
                score = turn_end_step(players=players, enemies=enemies)


                # CHECK WHEN BATTLE ENDS

                if len(enemies) == 0:
                    print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
                    running = False
                    break

                elif len(players) == 0:
                    print(bcolors.FAIL + "The enemy has defeated you!" + bcolors.ENDC)
                    running = False
                    break

