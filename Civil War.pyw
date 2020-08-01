# Civil War Game

from livewires import games, color
import random, math

# games.init(950, 700, 300, "Civil War")
games.init(950, 700, 300)

class Color_clicker(games.Text):
    def __init__(self, value, size, color1, color2=None, nonact_color=None,
                 activated=True, x=0, y=0, top=None, bottom=None, left=None,
                 right=None, is_collideable=False):

        self._color1 = color1
        if color2 == None:
            self._color2 = color1
        else:
            self._color2 = color2
        if nonact_color == None:
            self._nonact_color = color1
        else:
            self._nonact_color = nonact_color
        self._activated = activated
        if games.mouse.is_pressed(0):
            self._can_press = False
        else:
            self._can_press = True

        super(Color_clicker, self).__init__(value=value, size=size, color=color1,
                                         x=x, y=y, top=top, bottom=bottom,
                                         left=left, right=right,
                                         is_collideable=is_collideable)

    def tick(self):
        if self._activated:
            if self.left <= games.mouse.x <= self.right and self.top <= games.mouse.y <= self.bottom:
                self.color = self._color2
                if games.mouse.is_pressed(0):
                    if self._can_press:
                        self.func()
            else:
                self.color = self._color1
        else:
            self.color = self._nonact_color

        if games.mouse.is_pressed(0):
            self._can_press = False
        else:
            self._can_press = True

    def func(self):
        pass

    #------Properties------#

    ## color1
    def get_color1(self):
        return self._color1

    def set_color1(self, new_color):
        self._color1 = new_color

    color1 = property(get_color1, set_color1)

    ## color2
    def get_color2(self):
        return self._color2

    def set_color2(self, new_color):
        self._color2 = new_color

    color2 = property(get_color2, set_color2)

    ## nonact_color
    def get_nonact_color(self):
        return self._nonact_color

    def set_nonact_color(self, new_color):
        self._nonact_color = new_color

    nonact_color = property(get_nonact_color, set_nonact_color)

    ## activated
    def get_activated(self):
        return self._activated

    def set_activated(self, new_status):
        if new_status:
            self._activated = True
        else:
            self._activated = False

    activated = property(get_activated, set_activated)

class Side_text(Color_clicker):
    def __init__(self, game, side):
        self.game = game
        self.side = side
        if self.side == "u":
            value = "Union"
            y = games.screen.height / 3
        else:
            value = "Confederate"
            y = games.screen.height * 2 / 3
        super(Side_text, self).__init__(value, 80, color.white, color.red,
                                        x=games.screen.width / 2, y=y)

    def func(self):
        if self.side == "u":
            self.game.sides = "uc"
        else:
            self.game.sides = "cu"

        self.game.start()

class Adjuster(games.Sprite):
    def update(self):
        if games.mouse.y <= 10:
            self.y += 4
        elif games.mouse.y <= 20:
            self.y += 3
        elif games.mouse.y >= games.screen.height - 10:
            self.y -= 4
        elif games.mouse.y >= games.screen.height - 20:
            self.y -= 3
        if games.mouse.x <= 10:
            self.x += 4
        elif games.mouse.x <= 20:
            self.x += 3
        elif games.mouse.x >= games.screen.width - 10:
            self.x -= 4
        elif games.mouse.x >= games.screen.width - 20:
            self.x -= 3

class Adjuster1(games.Animation):
    def update(self):
        if games.mouse.y <= 10:
            self.y += 4
        elif games.mouse.y <= 20:
            self.y += 3
        elif games.mouse.y >= games.screen.height - 10:
            self.y -= 4
        elif games.mouse.y >= games.screen.height - 20:
            self.y -= 3
        if games.mouse.x <= 10:
            self.x += 4
        elif games.mouse.x <= 20:
            self.x += 3
        elif games.mouse.x >= games.screen.width - 10:
            self.x -= 4
        elif games.mouse.x >= games.screen.width - 20:
            self.x -= 3

class Basic_man(Adjuster):
    def get_speed(self):
        overlaps_water = False
        overlaps_bridge = False
        overlaps_solid = False
        if self.overlapping_sprites:
            self.if_overlaps()
            for sprite in self.overlapping_sprites:
                if not sprite.go_through:
                    overlaps_solid = True
                if sprite.is_bridge:
                    overlaps_bridge = True
                if sprite.is_water:
                    overlaps_water = True

            if overlaps_solid:
                if self.top == sprite.bottom - 1:
                    self.y += 1
                elif self.right == sprite.left + 1:
                    self.x -= 1
                elif self.bottom == sprite.top + 1:
                    self.y -= 1
                elif self.left == sprite.right - 1:
                    self.x += 1
                self.moving = False
                return 0
            if overlaps_bridge:
                return self.BASE_SPEED
            if overlaps_water:
                if self.WATER_SPEED == 0:
                    if self.top == sprite.bottom - 1:
                        self.y += 1
                    elif self.right == sprite.left + 1:
                        self.x -= 1
                    elif self.bottom == sprite.top + 1:
                        self.y -= 1
                    elif self.left == sprite.right - 1:
                        self.x += 1
                    self.moving = False
                return self.WATER_SPEED

            return self.BASE_SPEED

        else:
            return self.BASE_SPEED

    def move(self):
        speed = self.get_speed()

        self.x += speed * math.sin(math.radians(self.angle))
        self.y += speed * -math.cos(math.radians(self.angle))

    def if_overlaps(self):
        pass

class Player_man(Basic_man):
    def update(self):
        super(Player_man, self).update()
        if self.activated:
            # allows player to change sprite angle
            if games.keyboard.is_pressed(games.K_KP8) or games.keyboard.is_pressed(games.K_UP):
                self.angle = 0

            if games.keyboard.is_pressed(games.K_KP9):
                self.angle = 45

            if games.keyboard.is_pressed(games.K_KP6) or games.keyboard.is_pressed(games.K_RIGHT):
                self.angle = 90

            if games.keyboard.is_pressed(games.K_KP3):
                self.angle = 135

            if games.keyboard.is_pressed(games.K_KP2) or games.keyboard.is_pressed(games.K_DOWN):
                self.angle = 180

            if games.keyboard.is_pressed(games.K_KP1):
                self.angle = 225

            if games.keyboard.is_pressed(games.K_KP4) or games.keyboard.is_pressed(games.K_LEFT):
                self.angle = 270

            if games.keyboard.is_pressed(games.K_KP7):
                self.angle = 315

            # allows player to order sprite to move
            if games.keyboard.is_pressed(games.K_w):
                self.activated = False
                self.moving = True

            if games.keyboard.is_pressed(games.K_r):
                self.rotating = True

            if self.rotating:
                self.angle = 90 + math.degrees(math.atan2(games.mouse.y - self.y, games.mouse.x - self.x))

        # makes sprite move
        if self.moving:
            self.move()

    def destroy(self):
        try:
            self.game.friends.remove(self)
        except(ValueError):
            pass
        super(Player_man, self).destroy()

class Comp_man(Basic_man):
    def update(self):
        super(Comp_man, self).update()
        if self.moving:
            self.move()
            self.covered += self.get_speed()

    def destroy(self):
        try:
            self.game.enemies.remove(self)
        except(ValueError):
            pass
        super(Comp_man, self).destroy()

class Building_bridge1(Adjuster):
    def __init__(self, game, x=0, y=0, top=None, bottom=None,
                 right=None, left=None, angle=0):
        image = games.load_image("bridge1(building).bmp")
        super(Building_bridge1, self).__init__(image=image, x=x, y=y, top=top,
                                               bottom=bottom, right=right,
                                               left=left, angle=angle)
        self.game = game
        self.timer = 2000
        self.go_through = True
        self.is_man = False
        self.is_water = True
        self.is_bridge = False
        self.is_bullet = False
        self.is_tent = False

        PlayerE.bridges.append(self)

    def update(self):
        super(Building_bridge1, self).update()
        if self.timer <= 0:
            self.bridge = Bridge1(self.game, x=self.x, y=self.y,
                                  angle=self.angle)
            games.screen.add(self.bridge)
            for sprite in self.overlapping_sprites:
                if sprite.is_water:
                    self.bridge.elevate(sprite)

            try:
                PlayerE.bridges.remove(self)
            except(ValueError):
                pass
            self.destroy()

class Bridge1(Adjuster):
    def __init__(self, game, x, y, angle=0):
        image = games.load_image("bridge1.bmp", False)
        super(Bridge1, self).__init__(image, angle, x, y)
        self.game = game
        self.go_through = True
        self.is_man = False
        self.is_water = False
        self.is_bridge = True
        self.is_bullet = False
        self.is_tent = False

        self.game.bridges.append(self) # append self to list of bridges

class Wall_rect(Adjuster):
    def __init__(self, x, y, angle):
        super(Wall_rect, self).__init__(games.load_image("wall_rectangle.bmp"),
                                        angle, x, y)
        self.go_through = True
        self.is_man = False
        self.is_water = False
        self.is_bridge = False
        self.is_bullet = False
        self.is_tent = False

class Stone_wall(Adjuster):
    def __init__(self, game, x, y, angle=0):
        image = games.load_image("stone_wall.bmp", False)
        super(Stone_wall, self).__init__(image, angle, x, y)
        self.game = game
        self.go_through = False
        self.is_man = False
        self.is_water = False
        self.is_bridge = False
        self.is_bullet = False
        self.is_tent = False
        self.health = 40
        self.rect = Wall_rect(x=self.x, y=self.y, angle=self.angle)
        games.screen.add(self.rect)

        self.game.walls.append(self)

    def die(self):
        if self.health <= 0:
            self.is_collideable = False
            self.rect.destroy()
            try:
                self.game.walls.remove(self)
            except(ValueError):
                pass
            self.image = games.load_image("stone_wall_destroyed.bmp")
            self.lower()

    def destroy(self):
        try:
            self.game.walls.remove(self)
        except(ValueError):
            pass
        super(Stone_wall, self).destroy()

class Explosion1(Adjuster1):
    def __init__(self, x, y):
        super(Explosion1, self).__init__(images=["explosion20.bmp",
                                                 "explosion21.bmp",
                                                 "explosion22.bmp",
                                                 "explosion23.bmp",
                                                 "explosion24.bmp",
                                                 "explosion25.bmp",
                                                 "explosion26.bmp",
                                                 "explosion27.bmp",
                                                 "explosion28.bmp"],
                                         x=x, y=y, n_repeats=1,
                                         repeat_interval=1,
                                         is_collideable=False)

class River1(Adjuster):
    def __init__(self, image, x, y, angle=0):
        if image == 0:
            image = games.load_image("river1.bmp", False)
        elif image == 1:
            image = games.load_image("river2.bmp", False)
        super(River1, self).__init__(image, angle, x, y)
        self.go_through = True
        self.is_man = False
        self.is_water = True
        self.is_bridge = False
        self.is_bullet = False
        self.is_tent = False

class Bush(Adjuster):
    def __init__(self, image, x, y):
        if image == 1:
            image = games.load_image("bush.bmp")
        super(Bush, self).__init__(image, x=x, y=y)
        self.go_through = False
        self.is_man = False
        self.is_water = False
        self.is_bridge = False
        self.is_bullet = False
        self.is_tent = False
        self.image = image

class Tent1(Adjuster):
    def __init__(self, game, x, y):
        image = games.load_image("tent.bmp", False)
        image1 = games.load_image("tent(destroyed).bmp", False)
        super(Tent1, self).__init__(image, x=x, y=y)
        self.game = game
        self.go_through = False
        self.is_man = True
        self.is_water = False
        self.is_bridge = False
        self.is_bullet = False
        self.is_tent = True
        self.health = 5
        self.can_build = True
        self.is_building = False
        self.building = ""
        self.activated = False
        self.image_destroyed = image1
        self.timer = 0

    def update(self):
        super(Tent1, self).update()
        if games.mouse.is_pressed(0):
            if self.get_left() <= games.mouse.x <= self.get_right() and self.get_top() <= games.mouse.y <= self.get_bottom() and games.mouse.is_pressed(0):
                self.activated = True
                rectangle = Rectangle(image=5, x=self.x, y=self.y)
                games.screen.add(rectangle)
            else:
                self.activated = False

        if self.activated and self.can_build:
            if games.keyboard.is_pressed(games.K_i):
                self.is_building = True
                self.building = "i"
                self.timer = 1500
            elif games.keyboard.is_pressed(games.K_c):
                self.is_building = True
                self.building = "c"
                self.timer = 2000
            elif games.keyboard.is_pressed(games.K_a):
                self.is_building = True
                self.building = "a"
                self.timer = 2250
            elif games.keyboard.is_pressed(games.K_e):
                self.is_building = True
                self.building = "e"
                self.timer = 1000

        if self.is_building and self.can_build:
            if self.timer > 0:
                self.timer -= 1
            else:
                if self.building == "i":
                    infantry = PlayerI(game=self.game, x=self.x,
                                              y=self.top - 13)
                    games.screen.add(infantry)
                    self.is_building = False
                    self.building = ""
                elif self.building == "c":
                    cav = PlayerC(game=self.game, x=self.x,
                                        y=self.y - 50)
                    games.screen.add(cav)
                    self.is_building = False
                    self.building = ""
                elif self.building == "a":
                    artillery1 = PlayerA(game=self.game, x=self.x,
                                                 y=self.y - 52)
                    games.screen.add(artillery1)
                    self.is_building = False
                    self.building = ""
                elif self.building == "e":
                    engineer1 = PlayerE(game = self.game,
                                               x = self.x, y = self.y - 38)
                    games.screen.add(engineer1)
                    self.is_building = False
                    self.building = ""

    def die(self):
        if self.health <= 0:
            self.set_image(self.image_destroyed)
            self.can_build = False

class Tent2(Adjuster):
    def __init__(self, game, x, y, angle=0):
        image = games.load_image("tent.bmp", False)
        image1 = games.load_image("tent(destroyed).bmp", False)
        super(Tent2, self).__init__(image, angle, x, y)
        self.game = game
        self.starting_y = y
        self.go_through = False
        self.is_man = True
        self.is_water = False
        self.is_bridge = False
        self.is_bullet = False
        self.is_tent = True
        self.health = 5
        self.can_build = True
        self.is_building = False
        self.building = ""
        self.activated = False
        self.image_destroyed = image1
        self.timer = 0

        self.game.enemies.append(self)

    def update(self):
        super(Tent2, self).update()
        if self.can_build and not self.is_building:
            self.random = random.randrange(6)
            if self.random <= 4:
                self.building = "i"
                self.timer = 1500
            else:
                self.building = "a"
                self.timer = 2250
            self.is_building = True

        if self.is_building and self.can_build:
            if self.timer > 0:
                self.timer -= 1
            else:
                if self.building == "i":
                    infantry = CompI(game=self.game,
                                                    x=self.x - 25,
                                                    y=self.y + 40, order=3,
                                                    angle=180,
                                             to_cover = -self.starting_y + 240)
                    games.screen.add(infantry)
                elif self.building == "a":
                    artillery = CompA(game = self.game,
                                                      x = self.x + 25,
                                                      y = self.y + 60, order = 3,
                                                      set_angle = 180,
                                            to_cover = -self.starting_y + 240)
                    games.screen.add(artillery)

                self.is_building = False
                self.building = ""

    def die(self):
        if self.health <= 0:
            self.set_image(self.image_destroyed)
            self.can_build = False

class Flash1(Adjuster):
    def __init__(self, image, x, y, angle):
        if image == 1:
            image = games.load_image("gun_flash.bmp", False)
        if image == 2:
            image = games.load_image("cannon_flash.bmp")
        super(Flash1, self).__init__(image, angle, x, y, is_collideable=False)

        self.timer = 5

    def update(self):
        super(Flash1, self).update()
        if self.timer > 0:
            self.timer -= 1

        if self.timer == 0:
            self.destroy()

class Bullet(Adjuster):
    def __init__(self, game, x, y, dy, dx, timer=50, thru_wall=True):
        image = games.load_image("bullet1.bmp")
        super(Bullet, self).__init__(image, x=x, y=y, dx=dx, dy=dy)
        self.game = game
        self.go_through = True
        self.is_man = False
        self.timer = timer
        self.is_water = False
        self.is_bridge = False
        self.is_bullet = True
        self.is_tent = False
        self.points = 1
        self.rect = False
        if thru_wall:
            for wall in self.game.walls:
                if self.overlaps(wall.rect):
                    self.rect = True
                    break

    def update(self):
        super(Bullet, self).update()
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                if sprite.is_man and sprite not in self.game.walls:
                    sprite.health -= self.points
                    sprite.die()
                    self.destroy()
                if not sprite.go_through:
                    if sprite in self.game.walls:
                        if not self.rect:
                            sprite.health -= self.points
                            sprite.die()
                            self.destroy()
                    else:
                        self.destroy()

        if self.timer > 0:
            self.timer -= 1
        else:
            self.destroy()

class Cannon_ball(Adjuster):
    def __init__(self, game, x, y, dx, dy):
        image = games.load_image("cannon_ball.bmp", False)
        super(Cannon_ball, self).__init__(image, x=x, y=y, dx=dx, dy=dy)
        self.game = game
        self.go_through = True
        self.is_man = False
        self.timer = 90
        self.is_water = False
        self.is_bridge = False
        self.is_bullet = True
        self.is_tent = False
        self.points = 3
        for wall in self.game.walls:
            if self.overlaps(wall.rect):
                self.rect = True
                break
        else:
            self.rect = False

    def update(self):
        super(Cannon_ball, self).update()
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                if sprite.is_man:
                    sprite.health -= self.points
                    sprite.die()
                if not sprite.go_through and not sprite.is_man:
                    if sprite in self.game.walls:
                        if not self.rect:
                            sprite.health -= self.points
                            sprite.die()
                            self.die()
                    else:
                        self.die()
                if sprite.is_tent:
                    self.die()

        if self.timer > 0:
            self.timer -= 1
        else:
            self.die()

    def die(self):
        bullet = Bullet(self.game, self.x - 1, self.y - 1, -5, -5, 4, False)
        games.screen.add(bullet)
        bullet = Bullet(self.game, self.x, self.y - 1, 0, -5, 4, False)
        games.screen.add(bullet)
        bullet = Bullet(self.game, self.x + 1, self.y - 1, 5, -5, 4, False)
        games.screen.add(bullet)
        bullet = Bullet(self.game, self.x - 1, self.y, -5, 0, 4, False)
        games.screen.add(bullet)
        bullet = Bullet(self.game, self.x + 1, self.y, 5, 0, 4, False)
        games.screen.add(bullet)
        bullet = Bullet(self.game, self.x - 1, self.y + 1, -5, 5, 4, False)
        games.screen.add(bullet)
        bullet = Bullet(self.game, self.x, self.y + 1, 0, 5, 4, False)
        games.screen.add(bullet)
        bullet = Bullet(self.game, self.x + 1, self.y + 1, 5, 5, 4, False)
        games.screen.add(bullet)
        explosion = Explosion1(x=self.x, y=self.y)
        games.screen.add(explosion)
        self.destroy()

class Rock1(Adjuster):
    def __init__(self, image, x, y):
        if image == 1:
            image = games.load_image("rock1.bmp")
        super(Rock1, self).__init__(image, x=x, y=y)
        self.go_through = False
        self.is_man = False
        self.is_water = False
        self.is_bridge = False
        self.is_bullet = False
        self.is_tent = False

class Rectangle(Adjuster):
    def __init__(self, image, x, y):
        if image == 1 or image == 4:
            self.rectangle_image = games.load_image("activated_rectangle.bmp")
        elif image == 2:
            self.rectangle_image = games.load_image("activated_rectangle2.bmp")
        elif image == 3:
            self.rectangle_image = games.load_image("activated_rectangle3.bmp")
        elif image == 5:
            self.rectangle_image = games.load_image("activated_rectangle1.bmp")
        super(Rectangle, self).__init__(self.rectangle_image, x=x, y=y,
                                        is_collideable=False)
        self.number = image

    def update(self):
        super(Rectangle, self).update()
        if self.get_left() > games.mouse.x or self.get_right() < games.mouse.x or self.get_top() > games.mouse.y or self.get_bottom() < games.mouse.y:
            if games.mouse.is_pressed(0):
                self.destroy()

        if games.keyboard.is_pressed(games.K_s) and self.number <= 3:
            self.destroy()

        if games.keyboard.is_pressed(games.K_w) and self.number <= 4:
            self.destroy()

        elif self.number == 5:
            if games.keyboard.is_pressed(games.K_i) or games.keyboard.is_pressed(games.K_c) or games.keyboard.is_pressed(games.K_a) or games.keyboard.is_pressed(games.K_e):
                self.destroy()

class PlayerI(Player_man):
    """ A Union Infantry Sprite """
    def __init__(self, game, x, y):
        """ Initialize sprite """
        self.infantry_image = games.load_image(game.sides[0] + "i.bmp")
        super(PlayerI, self).__init__(self.infantry_image, x=x, y=y)
        self.game = game
        self.game.friends.append(self)
        self.activated = False
        self.go_through = False
        self.is_shooting = False
        self.timer = 0
        self.is_man = True
        self.is_water = False
        self.moving = False
        self.rotating = False
        self.is_bridge = False
        self.is_bullet = False
        self.is_tent = False
        self.health = 1
        self.order = ""
        self.BASE_SPEED = .5
        self.WATER_SPEED = .1

    def update(self):
        super(PlayerI, self).update()
        if games.mouse.is_pressed(0):
            if self.get_left() <= games.mouse.x <= self.get_right() and self.get_top() <= games.mouse.y <= self.get_bottom():
                self.activated = True
                self.is_shooting = False
                self.moving = False
                self.rotating = False
                self.order = ""
                rectangle = Rectangle(image=1, x=self.x, y=self.y)
                games.screen.add(rectangle)
            else:
                self.activated = False
                self.rotating = False

        if games.mouse.is_pressed(2):
            if self.get_left() <= games.mouse.x <= self.get_right() and self.get_top() <= games.mouse.y <= self.get_bottom():
                self.activated = True
                self.is_shooting = False
                self.moving = False
                self.rotating = False
                self.order = ""
                rectangle = Rectangle(image=1, x=self.x, y=self.y)
                games.screen.add(rectangle)

        # timer for shooting
        if self.timer > 0:
            self.timer -= 1

        if self.activated:
            # allows player to order sprite to shoot
            if games.keyboard.is_pressed(games.K_f):
                self.is_shooting = True

            if games.keyboard.is_pressed(games.K_s):
                self.order = "s"
                self.activated = False

        if "s" in self.order:
            for man in self.game.enemies:
                if self.x - 200 < man.x < self.x + 200 and self.y - 200 < man.y < self.y + 200 and ((man.is_tent and man.can_build) or not man.is_tent):
                    self.angle = 90 + math.degrees(math.atan2(man.y - self.y, man.x - self.x))
                    self.is_shooting = True
                    break
            else:
                self.is_shooting = False

        # makes sprite shoot
        if self.is_shooting and self.timer == 0:
            bullet_x = 12 * math.sin(math.radians(self.angle + 20)) + self.x
            bullet_y = 12 * -math.cos(math.radians(self.angle + 20)) + self.y
            bullet_dx = 5 * math.sin(math.radians(self.angle))
            bullet_dy = 5 * -math.cos(math.radians(self.angle))

            flash = Flash1(image=1, x=bullet_x,
                           y=bullet_y, angle=self.angle)
            games.screen.add(flash)

            bullet = Bullet(self.game, x=bullet_x, y=bullet_y, dx=bullet_dx, dy=bullet_dy,
                            timer=40)
            games.screen.add(bullet)
            self.timer = 250

    def die(self):
        if self.health <= 0:
            self.destroy()

class PlayerC(Player_man):
    def __init__(self, game, x, y):
        image = games.load_image(game.sides[0] + "c.bmp")
        super(PlayerC, self).__init__(image=image, x=x, y=y)
        self.game = game
        self.game.friends.append(self)
        self.activated = False
        self.go_through = False
        self.is_man = True
        self.is_water = False
        self.moving = False
        self.rotating = False
        self.is_bridge = False
        self.is_bullet = False
        self.is_tent = False
        self.overlaps_bridge = False
        self.health = 1
        self.order = ""
        self.BASE_SPEED = 1
        self.WATER_SPEED = .5
        self.destroying = None

    def update(self):
        super(PlayerC, self).update()
        if games.mouse.is_pressed(0):
            if self.get_left() <= games.mouse.x <= self.get_right() and self.get_top() <= games.mouse.y <= self.get_bottom():
                self.activated = True
                self.moving = False
                self.rotating = False
                self.destroying = None
                self.order = ""
                rectangle = Rectangle(image=3, x=self.x, y=self.y)
                games.screen.add(rectangle)
            else:
                self.activated = False
                self.rotating = False

        if games.mouse.is_pressed(2):
            if self.get_left() <= games.mouse.x <= self.get_right() and self.get_top() <= games.mouse.y <= self.get_bottom():
                self.activated = True
                self.moving = False
                self.rotating = False
                self.destroying = None
                self.order = ""
                rectangle = Rectangle(image=3, x=self.x, y=self.y)
                games.screen.add(rectangle)

        if self.activated:
            if games.keyboard.is_pressed(games.K_s):
                    self.order = "s"
                    self.activated = False

        if "s" in self.order:
            for man in self.game.enemies:
                if self.x - 300 < man.x < self.x + 300 and self.y - 300 < man.y < self.y + 300 and ((man.is_tent and man.can_build) or not man.is_tent):
                    self.angle = 90 + math.degrees(math.atan2(man.y - self.y, man.x - self.x))
                    self.moving = True
                    break
            else:
                self.moving = False

        if self.destroying != None:
            sprite = self.destroying
            if sprite.is_tent:
                sprite.health -= .01
                if sprite.health <= 0:
                    self.destroying = None
                sprite.die()
            elif sprite.is_man:
                sprite.health -= .1
                if sprite.health <= 0:
                    self.destroying = None
                sprite.die()

    def if_overlaps(self):
        """ Allows sprite to "kill" enemies """
        if self.destroying == None:
            for sprite in self.overlapping_sprites:
                if sprite in self.game.enemies:
                    self.destroying = sprite
                    try:
                        if sprite.destroying == None:
                            sprite.destroying = self
                    except(AttributeError):
                        pass
                    break

    def die(self):
        if self.health <= 0:
            self.destroy()

class PlayerA(Player_man):
    def __init__(self, game, x, y):
        image = games.load_image(game.sides[0] + "a.bmp")
        super(PlayerA, self).__init__(image, x=x, y=y)
        self.game = game
        self.game.friends.append(self)
        self.activated = False
        self.go_through = False
        self.is_shooting = False
        self.timer = 0
        self.is_man = True
        self.is_water = False
        self.moving = False
        self.rotating = False
        self.is_bridge = False
        self.is_bullet = False
        self.is_tent = False
        self.overlaps_bridge = False
        self.health = 1
        self.is_enemy = False
        self.order = ""
        self.BASE_SPEED = .1
        self.WATER_SPEED = 0

    def update(self):
        super(PlayerA, self).update()
        if games.mouse.is_pressed(0):
            if self.get_left() <= games.mouse.x <= self.get_right() and self.get_top() <= games.mouse.y <= self.get_bottom():
                self.activated = True
                self.is_shooting = False
                self.moving = False
                self.rotating = False
                self.order = ""
                rectangle = Rectangle(image=2, x=self.x, y=self.y)
                games.screen.add(rectangle)
            else:
                self.activated = False
                self.rotating = False

        if games.mouse.is_pressed(2):
            if self.get_left() <= games.mouse.x <= self.get_right() and self.get_top() <= games.mouse.y <= self.get_bottom():
                self.activated = True
                self.is_shooting = False
                self.moving = False
                self.rotating = False
                self.order = ""
                rectangle = Rectangle(image = 2, x = self.x, y = self.y)
                games.screen.add(rectangle)

        # timer for shooting
        if self.timer > 0:
            self.timer -= 1

        if self.activated:
            # allows player to order sprite to shoot
            if games.keyboard.is_pressed(games.K_f):
                self.is_shooting = True

            if games.keyboard.is_pressed(games.K_s):
                self.order = "s"
                self.activated = False

        if "s" in self.order:
            for man in self.game.enemies:
                if self.x - 360 < man.x < self.x + 360 and self.y - 360 < man.y < self.y + 360 and ((man.is_tent and man.can_build) or not man.is_tent):
                    self.angle = 90 + math.degrees(math.atan2(man.y - self.y, man.x - self.x))
                    self.is_shooting = True
                    break
            else:
                self.is_shooting = False

        # makes sprite shoot
        if self.is_shooting and self.timer == 0:
            bullet_x = 28 * math.sin(math.radians(self.angle)) + self.x
            bullet_y = 28 * -math.cos(math.radians(self.angle)) + self.y
            bullet_dx = 4 * math.sin(math.radians(self.angle))
            bullet_dy = 4 * -math.cos(math.radians(self.angle))

            flash = Flash1(image=2, x=bullet_x,
                           y=bullet_y, angle=self.angle)
            games.screen.add(flash)

            ball = Cannon_ball(self.game, x=bullet_x, y=bullet_y,
                               dx=bullet_dx, dy=bullet_dy)
            games.screen.add(ball)
            self.timer = 350

    def die(self):
        if self.health <= 0:
            self.destroy()

class PlayerE(Player_man):

    bridges = []

    def __init__(self, game, x, y):
        image = games.load_image(game.sides[0] + "e.bmp")
        super(PlayerE, self).__init__(image, x=x, y=y)
        self.game = game
        self.game.friends.append(self)
        self.activated = False
        self.go_through = False
        self.is_man = True
        self.is_water = False
        self.moving = False
        self.rotating = False
        self.is_bridge = False
        self.is_bullet = False
        self.is_tent = False
        self.is_building = False
        self.working_on = None
        self.health = 1
        self.BASE_SPEED = .5
        self.WATER_SPEED = .1

    def update(self):
        super(PlayerE, self).update()
        if games.mouse.is_pressed(0):
            if self.get_left() <= games.mouse.x <= self.get_right() and self.get_top() <= games.mouse.y <= self.get_bottom():
                self.activated = True
                self.is_shooting = False
                self.moving = False
                self.rotating = False
                self.is_building = False
                self.working_on = None
                rectangle = Rectangle(image=4, x=self.x, y=self.y)
                games.screen.add(rectangle)
            else:
                self.activated = False
                self.rotating = False

        if games.mouse.is_pressed(2):
            if self.get_left() <= games.mouse.x <= self.get_right() and self.get_top() <= games.mouse.y <= self.get_bottom():
                self.activated = True
                self.is_shooting = False
                self.moving = False
                self.rotating = False
                self.is_building = False
                self.working_on = None
                rectangle = Rectangle(image=4, x=self.x, y=self.y)
                games.screen.add(rectangle)

        # allow self to build bridge
        if self.activated:
            if not self.is_building:
                if games.keyboard.is_pressed(games.K_RSHIFT) or games.keyboard.is_pressed(games.K_LSHIFT):
                    if games.keyboard.is_pressed(games.K_b):
                        for bridge in PlayerE.bridges:
                            if self.overlaps(bridge):
                                self.working_on = bridge
                                self.is_building = True
                                break
                        else:
                            for sprite in self.overlapping_sprites:
                                if sprite.is_water:
                                    bridge = Building_bridge1(self.game, x=self.x,
                                                              y=self.y,
                                                              angle=self.angle)
                                    games.screen.add(bridge)
                                    self.working_on = bridge

                                    for sprite in self.overlapping_sprites:
                                        if sprite.is_water and sprite != bridge:
                                            bridge.elevate(sprite)

                                    self.is_building = True
                                    break

        if self.is_building:
            if self.working_on.timer > 0:
                self.working_on.timer -= 1
            else:
                self.working_on = None
                self.is_building = False

    def die(self):
        if self.health <= 0:
            self.destroy()

class CompI(Comp_man):

    total = 0

    def __init__(self, game, x, y, order, angle=0, to_cover=0):
        image = games.load_image(game.sides[1] + "i.bmp")
        super(CompI, self).__init__(image, angle, x, y)
        self.go_through = False
        self.is_man = True
        self.timer = 0
        self.is_water = False
        self.order = order
        self.is_bridge = False
        self.game = game
        self.covered = 0
        self.to_cover = to_cover
        self.moving = False
        self.is_bullet = False
        self.is_tent = False
        if self.order == 5:
            self.is_shooting = False
        else:
            self.is_shooting = True
        self.health = 1
        self.BASE_SPEED = .5
        self.WATER_SPEED = .1

        CompI.total += 1
        self.game.enemies.append(self)

    def update(self):
        super(CompI, self).update()
        if self.timer > 0:
            self.timer -= 1

        if self.order == 1:
            # makes sprite rotate
            if self.timer == 0:
                self.angle += 1

        elif self.order == 3:
            if self.covered >= self.to_cover:
                self.angle = 0
                self.moving = False
            else:
                self.moving = True

        elif self.order == 4:
            if self.covered >= self.to_cover:
                self.angle = 0
                self.moving = False
            elif random.randrange(5000) == 0 and self.covered < self.to_cover:
                self.moving = True

        elif self.order == 5:
            for man in self.game.friends:
                if self.x - 200 < man.x < self.x + 200 and self.y - 200 < man.y < self.y + 200:
                    self.angle = 90 + math.degrees(math.atan2(man.y - self.y, man.x - self.x))
                    self.is_shooting = True
                    break
            else:
                self.is_shooting = False

        # makes sprite shoot
        if self.timer == 0 and self.is_shooting:
            bullet_x = 12 * math.sin(math.radians(self.angle + 20)) + self.x
            bullet_y = 12 * -math.cos(math.radians(self.angle + 20)) + self.y
            bullet_dx = 5 * math.sin(math.radians(self.angle))
            bullet_dy = 5 * -math.cos(math.radians(self.angle))

            flash = Flash1(image=1, x=bullet_x, y=bullet_y, angle=self.angle)
            games.screen.add(flash)

            bullet = Bullet(self.game, x=bullet_x, y=bullet_y, dx=bullet_dx, dy=bullet_dy,
                            timer=40)
            games.screen.add(bullet)
            self.timer = 250

    def die(self):
        if self.health <= 0:
            CompI.total -= 1
            if CompI.total == 0:
                self.game.win()
            self.destroy()

class CompC(Comp_man):
    def __init__(self, game, x, y, order, angle=0, to_cover=0):
        image = games.load_image(game.sides[1] + "c.bmp")
        super(CompC, self).__init__(image, angle, x, y)
        self.go_through = False
        self.is_man = True
        self.is_water = False
        self.order = order
        self.is_bridge = False
        self.game = game
        self.covered = 0
        self.to_cover = to_cover
        self.moving = False
        self.is_bullet = False
        self.is_tent = False
        self.health = 1
        self.BASE_SPEED = 1
        self.WATER_SPEED = .5
        self.destroying = None

        CompI.total += 1
        self.game.enemies.append(self)

    def update(self):
        super(CompC, self).update()
        if self.order == 1:
            if self.destroying == None:
                for man in self.game.friends:
                    if self.x - 300 < man.x < self.x + 300 and self.y - 300 < man.y < self.y + 300 and ((man.is_tent and man.can_build) or not man.is_tent):
                        self.angle = 90 + math.degrees(math.atan2(man.y - self.y, man.x - self.x))
                        self.moving = True
                        break
                else:
                    self.moving = False

        if self.destroying != None:
            sprite = self.destroying
            if sprite.is_tent:
                sprite.health -= .01
                if sprite.health <= 0:
                    self.destroying = None
                sprite.die()
            elif sprite.is_man:
                sprite.health -= .1
                if sprite.health <= 0:
                    self.destroying = None
                sprite.die()

    def if_overlaps(self):
        """ Allows sprite to "kill" enemies """
        if self.destroying == None:
            for sprite in self.overlapping_sprites:
                if sprite in self.game.friends:
                    self.destroying = sprite
                    try:
                       if sprite.destroying == None:
                           sprite.destroying = self
                    except(AttributeError):
                        pass
                    break

    def die(self):
        if self.health <= 0:
            CompI.total -= 1
            if CompI.total == 0:
                self.game.win()
            self.destroy()

class CompA(Comp_man):
    def __init__(self, game, x, y, order, set_angle=0, to_cover=0):
        image = games.load_image(game.sides[1] + "a.bmp")
        super(CompA, self).__init__(image, set_angle, x, y)
        self.go_through = False
        self.is_man = True
        self.timer = 0
        self.is_water = False
        self.order = order
        self.set_angle = set_angle
        self.is_bridge = False
        self.game = game
        self.covered = 0
        self.to_cover = to_cover
        self.speed = 0
        self.moving = False
        self.is_bullet = False
        self.is_tent = False
        self.health = 1
        if self.order == 5:
            self.is_shooting = False
        else:
            self.is_shooting = True
        self.BASE_SPEED = .1
        self.WATER_SPEED = 0

        CompI.total += 1
        self.game.enemies.append(self)

    def update(self):
        super(CompA, self).update()
        if self.timer > 0:
            self.timer -= 1

        if self.order == 1:
            # makes sprite rotate
            if self.timer == 0:
                self.angle += 1

        elif self.order == 2:
            self.angle = self.set_angle

        elif self.order == 3:
            self.angle = self.set_angle
            if self.covered >= self.to_cover:
                self.moving = False
            else:
                self.moving = True

        elif self.order == 4:
            self.angle = self.set_angle
            if self.covered >= self.to_cover:
                self.angle = 0
                self.moving = False
            elif random.randrange(5000) == 0 and self.covered < self.to_cover:
                self.moving = True

        elif self.order == 5:
            for man in self.game.friends:
                if self.x - 360 < man.x < self.x + 360 and self.y - 360 < man.y < self.y + 360:
                    self.angle = 90 + math.degrees(math.atan2(man.y - self.y, man.x - self.x))
                    self.is_shooting = True
                    break
            else:
                self.is_shooting = False

        # makes sprite shoot
        if self.timer == 0 and self.is_shooting:
            bullet_x = 28 * math.sin(math.radians(self.angle)) + self.x
            bullet_y = 28 * -math.cos(math.radians(self.angle)) + self.y
            bullet_dx = 4 * math.sin(math.radians(self.angle))
            bullet_dy = 4 * -math.cos(math.radians(self.angle))

            flash = Flash1(image=2, x=bullet_x,
                           y=bullet_y, angle=self.angle)
            games.screen.add(flash)

            ball = Cannon_ball(self.game, x=bullet_x, y=bullet_y,
                            dx=bullet_dx, dy=bullet_dy)
            games.screen.add(ball)
            self.timer = 350

    def die(self):
        if self.health <= 0:
            CompI.total -= 1
            if CompI.total == 0:
                self.game.win()
            self.destroy()

class Game(object):
    def __init__(self):
        self.sides = ""
        self.bridges = []
        self.friends = []
        self.enemies = []
        self.walls = []

        self.pick_side()

    def pick_side(self):
        for i in ["u", "c"]:
            text = Side_text(self, i)
            games.screen.add(text)

    def start(self):
        games.screen.clear()

        # establish background
        games.screen.background = games.load_image("grass1.bmp", False)

        self.river1 = River1(image=0, x=(games.screen.width / 2) + 1750, y=-200)
        games.screen.add(self.river1)

        self.river2 = River1(image=1, x=self.river1.left, y=-200,
                             angle=90)
        games.screen.add(self.river2)

        bridge1 = Bridge1(game=self, x=500, y=-200)
        games.screen.add(bridge1)

        x = 200
        y = 240
        for j in range(4):
            infantry = PlayerI(game=self, x=x, y=y)
            games.screen.add(infantry)
            x += 100

        tent = Tent1(game=self, x=-750, y=-775)
        games.screen.add(tent)

        cavalry = PlayerC(self, x=-650, y=-775)
        games.screen.add(cavalry)

        cavalry = PlayerC(self, x=-850, y=-775)
        games.screen.add(cavalry)

        tent1 = Tent1(game=self, x=350, y=450)
        games.screen.add(tent1)

        cavalry = PlayerC(self, x=450, y=450)
        games.screen.add(cavalry)

        cavalry = PlayerC(self, x=250, y=450)
        games.screen.add(cavalry)

        x = 190
        y = 145
        for j in range(9):
            wall = Stone_wall(self, x, y)
            games.screen.add(wall)
            x += 40

        x = 200
        y = -300
        for j in range(3):
            infantry2 = CompI(self, x=x, y=y, order=3, angle=180,
                                             to_cover=520)
            games.screen.add(infantry2)
            x += 100

        artillery = CompA(self, x=500, y=-300, order=5,
                                          set_angle=180)
        games.screen.add(artillery)

        x = 200
        y = -600
        for j in range(2):
            for j in range(6):
                infantry2 = CompI(self, x=x, y=y, order=4,
                                                 angle=180, to_cover=1010)
                games.screen.add(infantry2)
                x += 50
            x = 125
            y = -650

        x = -125
        y = -850
        for j in range(5):
            infantry = CompI(game=self, x=x, y=y, angle=270,
                                            order=5)
            games.screen.add(infantry)
            y += 25

        x = 250
        y = -775
        for j in range(2):
            tent = Tent2(game=self, x=x, y=y)
            games.screen.add(tent)
            x += 100

        x = 200
        y = -765
        for j in range(3):
            infantry2 = CompI(game=self, x=x, y=y,
                                                 order=2, angle=180)
            games.screen.add(infantry2)

            infantry = CompI(game=self, x=x, y=y - 20,
                                                 order=2, angle=0)
            games.screen.add(infantry)
            x += 100

        x = random.choice([-1, 1]) * 900
        y = random.choice([-1, 1]) * 1200
        for j in range(2):
            for k in range(5):
                cavalry = CompC(self, x=x, y=y, order=1)
                games.screen.add(cavalry)
                x += 50
            x -= 250
            y += 50

        for j in range(5):
            x = random.randrange(200, 500)
            y = random.randrange(500, 600)
            bush = Bush(image=1, x=x, y=y)
            games.screen.add(bush)

        for j in range(8):
            x = random.randrange(-2000, 2000)
            y = random.randrange(-2000, 2000)
            bush = Bush(image=1, x=x, y=y)
            games.screen.add(bush)
            for sprite in bush.overlapping_sprites:
                if sprite.is_water or sprite.is_man:
                    bush.destroy()

        for j in range(5):
            x = random.randrange(-2000, 2000)
            y = random.randrange(-2000, 2000)
            rock = Rock1(image=1, x=x, y=y)
            games.screen.add(rock)
            for sprite in rock.overlapping_sprites:
                if sprite.is_man:
                    rock.destroy()

    def win(self):
        self.won_message = games.Message(value="You Won!", size=90,
                                         color=color.red,
                                         x=games.screen.width/2,
                                         y=games.screen.height/2, lifetime=500,
                                         is_collideable=False)
        games.screen.add(self.won_message)

def main():
    civil_war = Game()
    games.screen.mainloop()

main()
