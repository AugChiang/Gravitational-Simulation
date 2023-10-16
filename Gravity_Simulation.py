import pygame as pg
import math
import random
import os

pg.init()

WIDTH, HEIGHT = 800, 600
STAT_WIDTH = 200
STAT_MARGIN_LEFT = 20
STAT_FONT = pg.font.SysFont("comicsans", 32)
SHIP_FONT = pg.font.SysFont("Times New Roman", 12)
WIN = pg.display.set_mode((WIDTH+STAT_WIDTH, HEIGHT))
pg.display.set_caption("Gravity Simulation")

PLANET_MASS = 200
PLANET_SIZE = 50 # planet radius
SHIP_MASS = 5
OBJ_SIZE = 5
G = 5
VEL_SCALE = 50
FPS = 60

# load img and adjust the size
BG = pg.transform.scale(pg.image.load("img/bg2.jpg"), (WIDTH, HEIGHT)).convert_alpha()
PLANET = pg.transform.scale(pg.image.load("img/planet.png"), (PLANET_SIZE*2, PLANET_SIZE*2))

# colors
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
BLACK = (0,0,0)

class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self):
        WIN.blit(PLANET, (self.x - PLANET_SIZE, self.y - PLANET_SIZE))

class Spacecraft:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass
        self.id = random.randint(0,1e4)

    def move(self, planet=None):
        dist = math.hypot(self.x-planet.x, self.y-planet.y)
        force = (G*self.mass*planet.mass) / dist**2
        acceleration = force / self.mass
        angle = math.atan2(planet.y-self.y, planet.x-self.x)
        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)
        self.vel_x += acceleration_x
        self.vel_y += acceleration_y
        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self):
        obj_id = SHIP_FONT.render(f"ID: {self.id}", 1, WHITE)
        pg.draw.circle(WIN, RED, (int(self.x), int(self.y)), OBJ_SIZE)
        WIN.blit(obj_id, (int(self.x)-OBJ_SIZE, int(self.y)-OBJ_SIZE*4))

def draw_statbar(win, objs):
    # total number of current obj
    total_label = STAT_FONT.render(f"Total = {len(objs)}", 1, BLACK)
    planet_label = STAT_FONT.render(f"Planet: Earth", 1, BLACK)
    win.blit(planet_label, (WIDTH+STAT_MARGIN_LEFT, 10))
    win.blit(total_label, (WIDTH+STAT_MARGIN_LEFT, 40))
    for idx, obj in enumerate(objs):
        id_label = STAT_FONT.render(f"Object ID: {obj.id}", 1, BLACK)
        vx_label = STAT_FONT.render(f"X VEL. = {round(obj.vel_x, 2)}", 1, BLACK)
        vy_label = STAT_FONT.render(f"Y VEL. = {round(-obj.vel_y, 2)}", 1, BLACK)

        win.blit(id_label, (WIDTH+STAT_MARGIN_LEFT, (idx+1)*90))
        win.blit(vx_label, (WIDTH+STAT_MARGIN_LEFT, (idx+1)*90+25))
        win.blit(vy_label, (WIDTH+STAT_MARGIN_LEFT, (idx+1)*90+50))


def create_ship(loc, mouse_pos):
    x, y = loc
    mx, my = mouse_pos
    # math.hypot(*vector) returns the Euclidean norm
    vel_x = (mx-x)/VEL_SCALE
    vel_y = (my-y)/VEL_SCALE
    obj = Spacecraft(x, y, vel_x, vel_y,SHIP_MASS)
    return obj



# main loop
def main():
    run = True
    clock = pg.time.Clock()

    objs = []
    temp_obj_pos = None # pos of objects that not yet launched

    while run:
        clock.tick(FPS)
        mouse_pos = pg.mouse.get_pos()
        planet = Planet(WIDTH//2, HEIGHT//2, PLANET_MASS)
        WIN.fill('grey')

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
            if event.type == pg.MOUSEBUTTONDOWN:
                # if already place a spacecraft
                # then create it.
                if temp_obj_pos:
                    # temp_x, temp_y = temp_obj_pos
                    # obj = Spacecraft(temp_x, temp_y, 0, 0, SHIP_MASS)
                    obj = create_ship(loc=temp_obj_pos, mouse_pos=mouse_pos)
                    objs.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos
        # draw background
        WIN.blit(BG, (0,0))

        if temp_obj_pos:
            pg.draw.line(WIN, WHITE, temp_obj_pos, mouse_pos, 2)
            pg.draw.circle(WIN, RED, temp_obj_pos, OBJ_SIZE)
            
        for obj in objs[:]: # iter the copy of objs
            obj.draw()
            obj.move(planet)
            # clear obj that is off-screen
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            # check if collide with planet
            collided = math.hypot(obj.x-planet.x, obj.y-planet.y) <= PLANET_SIZE
            if off_screen or collided:
                objs.remove(obj)
        draw_statbar(WIN, objs)

        planet.draw()
        
        pg.display.update()

    pg.quit()

if __name__ == '__main__':
    main()