##Stuff to do:
#Make the sprite show kinda what weapon he's got
#Add to combat
#  -Title thing
#  -Text indicates attacks and damages, but keypresses do the attacks
#  -Text indicating damage appears when someone hit (possibly could be subsitiuted for numbers of health bar)
#Armour!
#Actual purpose to map
#Shop system + paying for healing? - All at towns
#  -Selling items?
#  -Stuff to buy?
#  -Enemies dropping money
##
import pygame, random

pygame.init()
win = pygame.display.set_mode((1500, 800))
pygame.display.set_caption("RPG")
clock = pygame.time.Clock()

screen = 0
room = 1
inventory = False
in_town = False
weapon_roll = False
roll = []
key_timer = 0

font = pygame.font.Font('Luminari-Regular.ttf', 100)
text = font.render('Title Placeholder', True, ((255, 255, 255)))
textRect = text.get_rect()
textRect.center = (750, 400)

turn = 0
inv_click_check = -1
inv_click_count = 0

counter_attack = -1
burn = False
player_burn = False

free = False
town_make = False
rolled = False
shop_darken = False

class player:
    def __init__(self):
        self.x = 50
        self.y = 350
        self.size = 50
        self.colour = (159, 89, 25)

        self.height = 250
        self.width = 100

        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

        self.weapon = 0
        self.accuracy = 0
        self.health = 200
        self.max_health = 200
        self.fake_health = self.health

        self.is_poisoned = False
        self.on_fire = 0

        self.money = 0

    def move(self):
        global key_timer, free
        keys = pygame.key.get_pressed()
        if key_timer <= 0:
            if keys[pygame.K_d]:
                if self.x < 1450 or free:
                    flat.x += 50
                    key_timer = 10
                    turn_change()
            if keys[pygame.K_a]:
                if self.x >= 50 or free:
                    flat.x -= 50
                    key_timer = 10
                    turn_change()
            if keys[pygame.K_w]:
                if self.y >= 50 or free:
                    flat.y -= 50
                    key_timer = 10
                    turn_change()
            if keys[pygame.K_s]:
                if self.y >= 0 or free:
                    flat.y += 50
                    key_timer = 10
                    turn_change()

        self.exit_check()
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.town_check()

    def exit_check(self):
        global free, room
        if self.x < 0:
            self.x = 1450
            room_change()
        if self.x >= 1500:
            self.x = 0
            room_change()
        if self.y < 0:
            self.y = 750
            room_change()
        if self.y >= 800:
            self.y = 0
            room_change()

    def town_check(self):
        global in_town, weapon_roll
        for town in towns:
            if self.rect.colliderect(town.rect):
                if not town.visited:
                    self.max_health += 50
                    self.health = self.max_health
                    town.visited = True
                    town.colour = (108, 108, 108)
                in_town = True
            else:
                in_town = False

    def death_check(self):
        global run
        if self.health <= 0:
            run = False

    def burn(self):
        if self.on_fire > 0:
            self.health -= 1
            self.on_fire -= 1

    def tool_change(self, type, place):
        if type == 1:
            self.weapon = place


    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.size, self.size))

    def battle_draw(self):
        pygame.draw.rect(win, self.colour, (350, 650 - self.height, self.width, self.height))
        pygame.draw.circle(win, (255, 229, 204), (round(350 + self.width / 2), 650 - self.height - 80), 55)


class enemy:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.size = 50
        self.type = type

        self.height = 250
        self.width = 100

        self.on_fire = -1
        self.poisoned = 0

        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

        if self.type == 1:
            self.colour = (240, 240, 240)
            self.head_colour = (240, 240, 240)
            self.clothes_colour = (105, 105, 105)
            self.sight = 1
            self.health = 50
            self.max_health = 50
        elif self.type == 2:
            self.colour = (0, 0, 52)
            self.head_colour = (240, 240, 240)
            self.clothes_colour = (0, 0, 52)
            self.sight = 1
            self.health = 100
            self.max_health = 100
        elif self.type == 3:
            self.colour = (120, 34, 34)
            self.head_colour = (255, 229, 204)
            self.clothes_colour = (120, 34, 34)
            self.sight = 1
            self.health = 165
            self.max_health = 165
        elif self.type == 4:
            self.colour = (65, 120, 44)
            self.head_colour = (120, 200, 120)
            self.clothes_colour = (65, 120, 44)
            self.sight = 1
            self.health = 200
            self.max_health = 200
        elif self.type == 5:
            self.colour = (140, 140, 220)
            self.head_colour = (240, 240, 140)
            self.clothes_colour = (140, 140, 220)
            self.sight = 1
            self.health = 250
            self.max_health = 250

        self.fake_health = self.health

    def assign_weapon(self):
        if self.type == 1:
            num = random.randint(1, 3)
            if num == 1:
                self.weapon_name = 'Dagger'
                self.weapon_damage = 8
                self.weapon_type = 'Normal'
            elif num == 2:
                self.weapon_name = 'Short Sword'
                self.weapon_damage = 11
                self.weapon_type = 'Normal'
            else:
                self.weapon_name = 'Short Bow'
                self.weapon_damage = 13
                self.weapon_type = 'Normal'
        elif self.type == 2:
            num = random.randint(1, 3)
            if num == 1:
                self.weapon_name = 'Staff'
                self.weapon_damage = 13
                self.weapon_type = 'Fire'
            elif num == 2:
                self.weapon_name = 'Great Sword'
                self.weapon_damage = 16
                self.weapon_type = 'Normal'
            else:
                self.weapon_name = 'Tipped Dagger'
                self.weapon_damage = 8
                self.weapon_type = 'Poison'
        elif self.type == 3:
            num = random.randint(1, 3)
            if num == 1:
                self.weapon_name = 'Fire Blast'
                self.weapon_damage = 15
                self.weapon_type = 'Fire'
            elif num == 2:
                self.weapon_name = 'Mysterious Shield'
                self.weapon_damage = 20
                self.weapon_type = 'Normal'
            else:
                self.weapon_name = 'Flaming Sword'
                self.weapon_damage = 16
                self.weapon_type = 'Fire'
        elif self.type == 4:
            num = random.randint(1, 3)
            if num == 1:
                self.weapon_name = 'Venomous Staff'
                self.weapon_damage = 22
                self.weapon_type = 'Poison'
            elif num == 2:
                self.weapon_name = 'Sticky Sword'
                self.weapon_damage = 20
                self.weapon_type = 'Poison'
            else:
                self.weapon_name = 'Slippery Bow'
                self.weapon_damage = 18
                self.weapon_type = 'Poison'
        elif self.type == 5:
            num = random.randint(1, 3)
            if num == 1:
                self.weapon_name = 'Fire Gauntlet'
                self.weapon_damage = 30
                self.weapon_type = 'Fire'
            elif num == 2:
                self.weapon_name = 'Harpe'
                self.weapon_damage = 40
                self.weapon_type = 'Normal'
            else:
                self.weapon_name = 'Hand Cannon'
                self.weapon_damage = 28
                self.weapon_type = 'Poison'

    def look(self):
        global screen, turn, fighter
        found = False
        if flat.y == self.y:
            if flat.x == self.x + 50 * self.sight:
                found = True
            if flat.x == self.x - 50 * self.sight:
                found = True
        if flat.x == self.x:
            if flat.y == self.y + 50 * self.sight:
                found = True
            if flat.y == self.y - 50 * self.sight:
                found = True
        if found:
            screen = 2
            fighter = enemies.index(self)
            self.assign_weapon()

    def move(self):
        pygame.time.delay(0)
        direction = random.randint(1, 20)
        if direction == 1 and self.y < 750:
            self.y += 50
        if direction == 2 and self.y >= 50:
            self.y -= 50
        if direction == 3 and self.x < 1450:
            self.x += 50
        if direction == 4 and self.x >= 50:
            self.x -= 50
        for enemy in enemies:
            if enemies.index(enemy) != enemies.index(self):
                if self.rect.colliderect(enemies[enemies.index(enemy)].rect):
                    if self.x >= 50:
                        self.x -= 50
                    else:
                        self.x += 50
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        for town in towns:
            if self.rect.colliderect(town.rect):
                self.x -= 50
                if self.rect.colliderect(town.rect):
                    self.x += 100
                    if self.rect.colliderect(town.rect):
                        self.x -= 50
                        self.y -= 50
                        if self.rect.colliderect(town.rect):
                            self.y += 100


    def burn(self):
        global burn
        self.fake_health = self.health
        if self.on_fire > 0:
            self.fake_health -= self.on_fire
            self.on_fire -= 1


    def death_check(self):
        global screen, counter_attack, turn, inventory

        if self.health <= 0:
            flat.money += round(self.weapon_damage / 2)
            weapons.append(weapon(self.weapon_name, self.weapon_damage, self.weapon_type))
            enemies.remove(self)
            screen = 1
            counter_attack = -1
            for enemy in enemies:
                found = False
            turn = 0
            flat.accuracy = 0
            flat.is_poisoned = False
            inventory = True
            flat.health += 50
            if flat.health > flat.max_health:
                flat.health = flat.max_health

    def draw(self):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.size, self.size))

    def battle_draw(self):
        pygame.draw.rect(win, self.clothes_colour, (1050, 650 - self.height, self.width, self.height))
        pygame.draw.circle(win, self.head_colour, (round(1050 + self.width / 2), 650 - self.height - 80), 55)


class weapon:
    def __init__(self, name, damage, type):
        self.name = name
        self.damage = damage
        self.type = type
        self.new_name_one = ""
        self.new_name_two = ""

        if len(self.name) > 12:
            flip = False
            for char in self.name:
                if char != " " and not flip:
                    self.new_name_one = self.new_name_one + char
                else:
                    flip = True
                    if char != " ":
                        self.new_name_two = self.new_name_two + char

        if self.type == 'Normal':
            self.colour = (255, 255, 255)
        if self.type == 'Fire':
            self.colour = (255, 153, 51)
        if self.type == 'Poison':
            self.colour = (133, 101, 196)

    def text_set_up(self):
        self.font = pygame.font.Font('Luminari-Regular.ttf', 15)
        if self.new_name_one == "":
            self.text = self.font.render(self.name, True, ((0, 0, 0)))
        else:
            self.text_one = self.font.render(self.new_name_one, True, ((0, 0, 0)))
            self.text_two = self.font.render(self.new_name_two, True, ((0, 0, 0)))

    def highlight_check(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x >= self.savedx and mouse_x <= self.savedx + 100:
            if mouse_y >= self.savedy and mouse_y <= self.savedy + 100:
                if self.type == 'Normal':
                    self.colour = (220, 220, 220)
                if self.type == 'Fire':
                    self.colour = (220, 140, 40)
                if self.type == 'Poison':
                    self.colour = (120, 90, 186)

                return True

        if self.type == 'Normal':
            self.colour = (255, 255, 255)
        if self.type == 'Fire':
            self.colour = (255, 153, 51)
        if self.type == 'Poison':
            self.colour = (133, 101, 196)

    def darken(self):
        if self.type == 'Normal':
            self.colour = (180, 180, 180)
        if self.type == 'Fire':
            self.colour = (180, 0, 0)
        if self.type == 'Poison':
            self.colour = (0, 0, 180)

    def draw(self):
        global x_offset, y_offset

        self.text_set_up()
        pygame.draw.rect(win, (self.colour), (x_offset, y_offset, 100, 100))
        if self.new_name_one == "":
            self.positioning = round(x_offset + (50 - self.text.get_width() / 2))
            win.blit(self.text, (self.positioning, y_offset + 75))
        else:
            self.positioning_one = round(x_offset + (50 - self.text_one.get_width() / 2))
            self.positioning_two = round(x_offset + (50 - self.text_two.get_width() / 2))
            win.blit(self.text_one, (self.positioning_one, y_offset + 60))
            win.blit(self.text_two, (self.positioning_two, y_offset + 75))

        self.savedx = x_offset
        self.savedy = y_offset


def click_check(level):
    global inv_click_count, inv_click_check, clicking, shop_darken
    if level == 1:
        if inv_click_check > -1:
            if inv_click_count < 10:
                clicking = True
                inv_click_count += 1
            else:
                clicking = False
                inv_click_count = 0
                inv_click_check = -1
    if level == 2:
        if clicking:
            flat.weapon = inv_click_check
            weapons[inv_click_check].darken()
            clicking = False
            inv_click_count = 0
            inv_click_check = -1
    if level == 3:
        shop_darken = True



class town:
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.width = 150
        self.height = 150
        self.colour = colour
        self.visited = False
        self.rect = (self.x, self.y, self.width, self.height)

    def draw(self):
        self.rect = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))

def turn_change():
    global turn
    turn += 1
    if turn == 2:
        turn = 0

def fight(type):
    global fighter, counter_attack, burn, player_burn
    hit = random.randint(1, 10 + flat.accuracy)
    if type == 'o':
        if hit in (1, 2, 3, 4, 5, 6, 7, 8):
            enemies[fighter].health -= weapons[flat.weapon].damage
            if weapons[flat.weapon].type == 'Fire':
                if enemies[fighter].on_fire < 4 + round(weapons[flat.weapon].damage / 6):
                    enemies[fighter].on_fire = 4 + round(weapons[flat.weapon].damage / 6)
            if weapons[flat.weapon].type == 'Poison' and enemies[fighter].poisoned == 0:
                if enemies[fighter].poisoned < 5 + round(weapons[flat.weapon].damage / 4):
                    enemies[fighter].poisoned = 5 + round(weapons[flat.weapon].damage / 4)
    elif type == 'p':
        if hit in (1, 2):
            enemies[fighter].health -= weapons[flat.weapon].damage * 4
            if weapons[flat.weapon].type == 'Fire':
                if enemies[fighter].on_fire < 15 + round(weapons[flat.weapon].damage / 3):
                    enemies[fighter].on_fire = 15 + round(weapons[flat.weapon].damage / 3)
            if weapons[flat.weapon].type == 'Poison' and enemies[fighter].poisoned > 0:
                if enemies[fighter].poisoned < 12 + round(weapons[flat.weapon].damage / 3):
                    enemies[fighter].poisoned = 12 + round(weapons[flat.weapon].damage / 3)
    counter_attack = 50
    if type == 'enemy':
        stab = random.randint(1, 10 + enemies[fighter].poisoned)
        if stab in (1, 2, 3, 4, 5, 6, 7, 8):
            flat.health -= enemies[fighter].weapon_damage
            if enemies[fighter].weapon_type == 'Fire':
                flat.on_fire = 3
            if enemies[fighter].weapon_type == 'Poison' and not flat.is_poisoned:
                flat.accuracy = 8 + round(enemies[fighter].weapon_damage / 4)
                flat.is_poisoned = True
        counter_attack = -1
        burn = True
        player_burn = True
    if type != 'enemy':
        burn = False
        player_burn = False
        enemies[fighter].burn()

def room_change():
    global room, town_make, rolled
    room += 1
    for town in towns:
        towns.remove(town)
    if room == 2:
        enemies.append(enemy(200, 200, 2))
        enemies.append(enemy(100, 700, 2))
        enemies.append(enemy(1400, 150, 3))
        enemies.append(enemy(600, 100, 3))
        enemies.append(enemy(1200, 300, 4))
    if room == 3:
        enemies.append(enemy(1200, 400, 5))
        enemies.append(enemy(200, 200, 4))
        enemies.append(enemy(200, 600, 4))
        enemies.append(enemy(200, 400, 3))
    town_make = True
    rolled = False

def draw_window():
    global screen, x_offset, y_offset, inv_click_count, inv_click_check, burn, room, in_town, weapon_roll, roll, rolled, weapon_buy_types, weapon_buy_names, weapon_buy_damages, shop_darken, weapon_buy_names_two, weapon_buy_costs
    if screen == 0:
        win.fill((139, 69, 19))
        win.blit(text, textRect)

    if screen == 1:
        if room == 1:
            win.fill((110,180,130))
        elif room == 2:
            win.fill((239, 221, 111))
        elif room == 3:
            win.fill((178, 190, 181))
        if turn == 0:
            flat.move()
        elif turn == 1:
            for enemy in enemies:
                enemy.move()
            turn_change()
        for enemy in enemies:
            enemy.look()
            enemy.draw()
        flat.draw()
        for town in towns:
            town.draw()



    if screen == 2:
        win.fill((135, 206, 235))
        pygame.draw.rect(win, (110,180,130), (0, 650, 1500, 150))

        if burn:
            enemies[fighter].health = enemies[fighter].fake_health
        flat.burn()
        enemies[fighter].battle_draw()
        flat.battle_draw()

        pygame.draw.rect(win, (255, 255, 255), (200, 100, 400, 50))
        pygame.draw.rect(win, (255, 0, 0), (210, 110, round((flat.health / flat.max_health) * 380), 30))

        pygame.draw.rect(win, (255, 255, 255), (900, 100, 400, 50))
        pygame.draw.rect(win, (255, 0, 0), (910, 110, round((enemies[fighter].health / enemies[fighter].max_health) * 380), 30))

        enemies[fighter].death_check()

    if inventory:
        pygame.draw.rect(win, (225, 198, 153), (50, 50, 1375, 700))
        pygame.draw.rect(win, (159, 89, 25), (60, 50, 1375, 700), 25)

        pygame.draw.rect(win, (239, 221, 111), (400, 225, 100, 100))
        write(450, 310, (0, 0, 0), 20, "Money")
        write(450, 265, (0, 0, 0), 50, str(flat.money))

        if in_town:
            for town in towns:
                if town.visited and not rolled:
                    weapon_buy_names = ["Long", "Sickle", "Spear", "Burning", "Fire", "Tipped", "Axe", "Battle", "Hammer", "Gun?"]
                    weapon_buy_names_two = ["Bow", "", "", "Mace", "Tome", "Spear", "", "Axe", "", ""]
                    weapon_buy_damages = [18, 20, 22, 22, 24, 26, 32, 36, 40, 100]
                    weapon_buy_types = ['Normal', 'Normal', 'Normal', 'Fire', 'Fire', 'Poison', 'Normal', 'Normal', 'Normal', 'Normal', 'Poison']
                    weapon_buy_costs = [16, 18, 20, 20, 24, 32, 28, 30, 36, 100]
                    weapon_buy_weights = [9, 12, 12, 13, 14, 13, 14, 14, 15, 4]
                    roll = random.choices(weapon_buy_names, weights = weapon_buy_weights, k = 3)
                    rolled = True

            if rolled:
                store_offset = 400
                for i in range(0, 3):
                    if weapon_buy_types[weapon_buy_names.index(roll[i])] == 'Normal':
                        colour = (255, 255, 255)
                    elif weapon_buy_types[weapon_buy_names.index(roll[i])] == 'Fire':
                        colour = (255, 153, 51)
                    else:
                        colour = (133, 101, 196)

                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x >= store_offset and mouse_x <= store_offset + 100:
                        if mouse_y >= 600 and mouse_y <= 600 + 100:
                            if weapon_buy_types[weapon_buy_names.index(roll[i])] == 'Normal':
                                colour = (220, 220, 220)
                            if weapon_buy_types[weapon_buy_names.index(roll[i])] == 'Fire':
                                colour = (220, 140, 40)
                            if weapon_buy_types[weapon_buy_names.index(roll[i])] == 'Poison':
                                colour = (120, 90, 186)


                            if shop_darken:
                                if weapon_buy_types[weapon_buy_names.index(roll[i])] == 'Normal':
                                    colour = (180, 180, 180)
                                if weapon_buy_types[weapon_buy_names.index(roll[i])] == 'Fire':
                                    colour = (180, 0, 0)
                                if weapon_buy_types[weapon_buy_names.index(roll[i])] == 'Poison':
                                    colour = (0, 0, 180)

                                if flat.money >= weapon_buy_costs[weapon_buy_names.index(roll[i])]:
                                    weapons.append(weapon(weapon_buy_names[weapon_buy_names.index(roll[i])] + " " + weapon_buy_names_two[weapon_buy_names.index(roll[i])], weapon_buy_damages[weapon_buy_names.index(roll[i])], weapon_buy_types[weapon_buy_names.index(roll[i])]))
                                    flat.money -= weapon_buy_costs[weapon_buy_names.index(roll[i])]
                    pygame.draw.rect(win, colour, (store_offset, 600, 100, 100))

                    if weapon_buy_names_two[weapon_buy_names.index(roll[i])] != "":
                        write(store_offset + 50, 688, (0, 0, 0), 17, str(weapon_buy_names_two[weapon_buy_names.index(roll[i])]))
                        store_yoffset = 672
                    else:
                        store_yoffset = 680
                    write(store_offset + 50, 640, (0, 0, 0), 40, str(weapon_buy_damages[weapon_buy_names.index(roll[i])]))
                    pygame.draw.rect(win, (239, 221, 111), (store_offset, 540, 100, 50))
                    write(store_offset + 50, 565, (0, 0, 0), 40,"$" + str(weapon_buy_costs[weapon_buy_names.index(roll[i])]))
                    write(store_offset + 50, store_yoffset, (0, 0, 0), 17, str(weapon_buy_names[weapon_buy_names.index(roll[i])]))
                    store_offset += 125
                shop_darken = False



        x_offset = 775
        y_offset = 125

        #Below needs account for 1.2* if added back
        #pygame.draw.rect(win, (153, 229, 255), (250, 175, flat.width + 125 * 2, flat.height + 50 + 80 + 95))
        pygame.draw.rect(win, flat.colour, (200, 600 - flat.height, round(flat.width), round(flat.height)))
        pygame.draw.circle(win, (255, 229, 204), (round(200 + flat.width / 2), round(600 - flat.height - 80)), 55)

        pygame.draw.rect(win, (255, 255, 255), (125, 125, 250, 50))
        pygame.draw.rect(win, (255, 0, 0), (135, 135, round((flat.health / flat.max_health) * 230), 30))

        for weapon_item in  weapons:
            weapon_item.draw()
            write(x_offset + 50, y_offset + 40, (0, 0, 0), 50, str(weapon_item.damage))
            x_offset += 125
            if x_offset >= 1351:
                x_offset = 775
                y_offset += 125
            if weapon_item.highlight_check():
                inv_click_check = weapons.index(weapon_item)
                inv_click_count = 0

    pygame.display.update()

def write(x, y, colour, size, text):
    font = pygame.font.Font('Luminari-Regular.ttf', size)
    text = font.render(text, True, (colour))
    textRect = text.get_rect()
    textRect.center = (x, y)
    win.blit(text, textRect)

enemies = []
weapons = []
towns = []

flat = player()
run = True
clicking = False
enemies.append(enemy(600, 300, 1))
enemies.append(enemy(400, 350, 1))
enemies.append(enemy(1200, 300, 2))

weapons.append(weapon('Longsword', 10, 'Normal'))

towns.append(town(700, 300, (128, 128, 128)))


while run:
    clock.tick(60)

    click_check(1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if screen == 0:
                screen = 1
            if inventory and in_town:
                click_check(3)
            click_check(2)


    keys = pygame.key.get_pressed()
    if key_timer <= 0:
        if keys[pygame.K_i]:
            if screen != 0:
                if inventory:
                    inventory = False
                else:
                    inventory = True
            key_timer = 10
        if screen == 2:
            if counter_attack < 0:
                if keys[pygame.K_o]:
                    fight('o')
                    key_timer = 10
                elif keys[pygame.K_p]:
                    fight('p')
                    key_timer = 10
    key_timer -= 1

    if counter_attack > 0:
        counter_attack -= 1
        if counter_attack == 0:
            fight('enemy')

    if len(enemies) == 0:
        free = True
    else:
        free = False

    if free and room == 3:
        if flat.colour != (255, 255, 0):
            flat.colour != (255, 255, 0)
        else:
            flat.colour = (0, 0, 0)

    if town_make:
        towns.append(town(700, 300, (128, 128, 128)))
        town_make = False

    flat.death_check()
    draw_window()

pygame.quit()