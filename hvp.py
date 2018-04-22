import pygame, sys
from pygame.locals import *
import random
import math

from options import *
from definitions import *

FPS_CLOCK = pygame.time.Clock()

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 12)

pygame.init()
DISPLAY_SURFACE = pygame.display.set_mode((MAP_WIDTH*TILE_SIZE,MAP_HEIGHT*TILE_SIZE))

# TILE MAP GENERATION
tilemap = []
for row in range(MAP_HEIGHT):
    new_row = []

    for column in range(MAP_WIDTH):
        roll = random.randint(1,100)
        new_row.append(WATER if roll <= MAP_GEN_WATER_CHANGE else GRASS if MAP_GEN_WATER_CHANGE < roll < MAP_GEN_GRASS_CHANCE else DIRT)

    tilemap.append(new_row)

class Prey:
    def __init__(self, name, pos):
        self.name = 'Prey '+str(name)
        self.color = BLACK
        self.size = TILE_SIZE // 3
        self.health = 1.0
        self.hunger = 0.5
        self.thirst = 0.5
        self.energy = 0.5
        self.sleep  = 0.5
        self.sleeping = False
        self.passed_out = False
        self.position = pos
        self.move_to = False
        self.moving = [0,0]
        self.view_distance = 3
        self.gender = random.randint(0,1)
        self.ready_to_mate = False
        self.gestation = 0.0
        self.pregnant = False
        self.target = False

    def update(self):
        self.hunger = max(0, self.hunger - random.uniform(0.0075,0.0125))
        self.sleep  = max(0, self.sleep - random.uniform(0.00375,0.00625))

        if self.pregnant == True:
            self.gestation = min(1, self.gestation + 0.0025)
            if self.gestation >= 1:
                prey_list.append(Prey(str(random.randint(1,100)),self.position))
                self.gestation = 0
                self.energy = max(0, self.energy - 0.9)
                self.pregnant = False 

        if self.hunger <= 0:
            self.health = max(0, self.health - 0.01)
        elif self.hunger >= 0.9 and 0 < self.health < 1.0:
            self.health = min(1.0, self.health + 0.05)
            
        if self.hunger > 0.25 and self.sleep > 0.1:
            self.energy = min(1, self.energy + random.uniform(0.0375,0.0625))

        if self.sleep == 0:
            self.passed_out = True
            self.move_to = False

        if self.hunger >= 0.75 and self.sleep >= 0.75 and self.energy >= 0.75 and self.pregnant == False:
            self.ready_to_mate = True
        else:
            self.ready_to_mate = False
            self.target = False

        nearby_hunters = []
        for hunter in predator_list:
            if distance(self.position,hunter.position) <= 3:
                nearby_hunters.append(hunter)
            
        if self.passed_out == True:
            self.sleep  = min(1, self.sleep + random.uniform(0.02,0.06))
            if self.sleep >= 0.95:
                self.passed_out = False
        elif self.sleeping == True:
            self.sleep  = min(1, self.sleep + random.uniform(0.02,0.06))
            if self.hunger < 0.2 or self.sleep >= 0.95 or len(nearby_hunters) > 0:
                self.sleeping = False
        elif len(nearby_hunters) > 0:
            self.position = flee(self.position,nearby_hunters[random.randint(0,len(nearby_hunters)-1)].position,1)
            self.target = False
            self.move_to = False
        elif self.hunger >= 0.6 and self.sleep <= 0.2:
            self.move_to = False
            self.sleeping = True
        elif self.ready_to_mate:
            if self.target == False:
                valid_targets = []
                for prey in prey_list:
                    if distance(self.position, prey.position) <= self.view_distance:
                        if prey.ready_to_mate == True and prey.pregnant != True and (self.gender != prey.gender):
                            valid_targets.append(prey)
                if len(valid_targets) > 0:
                    self.target = valid_targets[random.randint(0,len(valid_targets)-1)]
                else:
                    self.position,self.moving = straight_move(self.position,self.moving)
            elif self.target.ready_to_mate == False or distance(self.position,self.target.position) > 3:
                self.target = False
            elif self.position == self.target.position:
                if random.random() <= 0.25:
                    if self.gender == FEMALE:
                        self.pregnant = True
                    else:
                        self.target.pregnant = True
                self.ready_to_mate = False
                self.energy = max(0, self.energy - 0.75)
                self.target.ready_to_mate = False
                self.target.energy = max(0, self.target.energy - 0.75)
                
            elif self.target != False:
                self.position = move_to_target(self.position,self.target.position,1)
        elif self.hunger <= 1:
            if self.move_to != False and self.position == self.move_to:
                self.move_to = False
            if self.move_to != False:
                if tilemap[self.move_to[0]][self.move_to[1]] != GRASS:
                    self.move_to = False
            if tilemap[self.position[0]][self.position[1]] == GRASS:
                self.hunger += 0.1
                self.health = min(1.0, self.health + 0.05)
                tilemap[self.position[0]][self.position[1]] = DIRT
            elif self.move_to != False and self.position != self.move_to:
                if self.position[0] != self.move_to[0]:
                    if self.move_to[0] > self.position[0]:
                        self.position[0] = self.position[0] + 1
                    else:
                        self.position[0] = self.position[0] - 1
                if self.position[1] != self.move_to[1]:
                    if self.move_to[1] > self.position[1]:
                        self.position[1] = self.position[1] + 1
                    else:
                        self.position[1] = self.position[1] - 1
            else:
                grass_pos = tile_search(tilemap, self.position, GRASS, self.view_distance)

                if len(grass_pos) > 0:
                    grass_pick = random.randint(1,len(grass_pos))
                    self.move_to = grass_pos[grass_pick-1]
                else:
                    self.position,self.moving = straight_move(self.position,self.moving)

class Predator():
    def __init__(self, name, pos):
        self.name = 'Predator '+str(name)
        self.color = RED
        self.size = TILE_SIZE // 3
        self.health = 1.0
        self.hunger = 0.75
        self.thirst = 0.5
        self.energy = 0.5
        self.sleep  = 0.5
        self.sleeping = False
        self.passed_out = False
        self.position = pos
        self.move_to = False
        self.moving = [0,0]
        self.view_distance = 6
        self.gender = random.randint(0,1)
        self.ready_to_mate = False
        self.gestation = 0.0
        self.pregnant = False
        self.target = False

    def update(self):
        self.hunger = max(0, self.hunger - random.uniform(0.00375,0.00625))
        self.sleep  = max(0, self.sleep - random.uniform(0.00375,0.00625))
        
        if self.pregnant == True:
            self.gestation = min(1, self.gestation + 0.0025)
            if self.gestation >= 1:
                prey_list.append(Prey(str(random.randint(1,100)),self.position))
                self.gestation = 0
                self.energy = max(0, self.energy - 0.9)
                self.pregnant = False 

        if self.hunger <= 0:
            self.health = max(0, self.health - 0.01)
        elif self.hunger >= 0.9 and self.health < 1.0:
            self.health = min(1.0, self.health + 0.05)
            
        if self.hunger > 0.25 and self.sleep > 0.1:
            self.energy = min(1, self.energy + random.uniform(0.0375,0.0625))

        if self.sleep == 0:
            self.passed_out = True
            self.move_to = False
            
        if self.passed_out == True:
            self.sleep  = min(1, self.sleep + random.uniform(0.02,0.06))
            if self.sleep >= 0.95:
                self.passed_out = False
        elif self.sleeping == True:
            self.sleep  = min(1, self.sleep + random.uniform(0.02,0.06))
            if self.hunger < 0.2 or self.sleep >= 0.95:
                self.sleeping = False
        elif self.hunger >= 0.6 and self.sleep <= 0.2:
            self.move_to = False
            self.sleeping = True
        elif self.hunger <= 1:
            if self.target == False:
                valid_targets = []
                for prey in prey_list:
                    if distance(self.position, prey.position) <= self.view_distance:
                        valid_targets.append(prey)
                if len(valid_targets) > 0:
                    self.target = valid_targets[random.randint(0,len(valid_targets)-1)]
                else:
                    self.position,self.moving = straight_move(self.position,self.moving)
            elif distance(self.position,self.target.position) > self.view_distance:
                self.target = False
            elif self.position == self.target.position:
                 self.target.health = 0
                 self.hunger += 1.0
                 self.target = False
            elif self.target != False:
                self.position = move_to_target(self.position,self.target.position,1)

prey_list = [Prey(str(random.randint(1,100)),[random.randint(0,MAP_HEIGHT-1),random.randint(0,MAP_WIDTH-1)]) for i in range(0,PREY_START_COUNT)]
predator_list = [Predator(str(random.randint(1,100)),[random.randint(0,MAP_HEIGHT-1),random.randint(0,MAP_WIDTH-1)]) for i in range(0,PRED_START_COUNT)]

elapsed_time = 0
debug = 0
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    tilemap = update_map(tilemap)

    grass_tiles = []
    for row in range(MAP_HEIGHT):
        for column in range(MAP_WIDTH):
            pygame.draw.rect(DISPLAY_SURFACE, colours[tilemap[row][column]], (column*TILE_SIZE,row*TILE_SIZE,TILE_SIZE,TILE_SIZE))

    if elapsed_time > 120:
        for predator in predator_list:
            predator.update()
            
        for prey in prey_list:
            prey.update()

        predator_list = [predator for predator in predator_list if predator.health > 0]
        prey_list = [prey for prey in prey_list if prey.health > 0]
                
        elapsed_time = 0

        if len(prey_list) < 3:
            grass_count = get_grass_count(tilemap)
            if len(prey_list) < 1 and grass_count / (MAP_HEIGHT*MAP_WIDTH) >= .25:
                prey_list.append(Prey(str(random.randint(1,100)),[random.randint(0,MAP_HEIGHT-1),random.randint(0,MAP_WIDTH-1)]))
            if len(prey_list) < 2 and grass_count / (MAP_HEIGHT*MAP_WIDTH) >= .5:
                prey_list.append(Prey(str(random.randint(1,100)),[random.randint(0,MAP_HEIGHT-1),random.randint(0,MAP_WIDTH-1)]))
            if len(prey_list) < 3 and grass_count / (MAP_HEIGHT*MAP_WIDTH) >= .75:
                prey_list.append(Prey(str(random.randint(1,100)),[random.randint(0,MAP_HEIGHT-1),random.randint(0,MAP_WIDTH-1)]))

    for predator in predator_list:
        pygame.draw.circle(DISPLAY_SURFACE, predator.color, (predator.position[1]*TILE_SIZE+(TILE_SIZE//2),predator.position[0]*TILE_SIZE+(TILE_SIZE//2)),predator.size)
        
    for prey in prey_list:
        pygame.draw.circle(DISPLAY_SURFACE, prey.color, (prey.position[1]*TILE_SIZE+(TILE_SIZE//2),prey.position[0]*TILE_SIZE+(TILE_SIZE//2)),prey.size)

    prey_count = 0
    male_count = 0
    female_count = 0
    pregnant_count = 0
    starve_count = 0
    sleeping_count = 0
    passed_out_count = 0
    ready_to_mate_count = 0
    for prey in prey_list:
        prey_count += 1
        if prey.pregnant == True:
            pregnant_count += 1
        if prey.hunger == 0:
            starve_count += 1
        if prey.sleeping == True:
            sleeping_count += 1
        if prey.passed_out == True:
            passed_out_count += 1
        if prey.ready_to_mate == True:
            ready_to_mate_count += 1
        if prey.gender == MALE:
            male_count += 1
        else:
            female_count += 1
            
    textsurface = myfont.render(('prey: '+str(prey_count)), False, (0, 0, 0))
    DISPLAY_SURFACE.blit(textsurface,(1,0))
    textsurface = myfont.render(('male: '+str(male_count)), False, (0, 0, 0))
    DISPLAY_SURFACE.blit(textsurface,(1,10))
    textsurface = myfont.render(('female: '+str(female_count)), False, (0, 0, 0))
    DISPLAY_SURFACE.blit(textsurface,(1,20))
    textsurface = myfont.render(('pregnant: '+str(pregnant_count)), False, (0, 0, 0))
    DISPLAY_SURFACE.blit(textsurface,(1,30))
    textsurface = myfont.render(('ready: '+str(ready_to_mate_count)), False, (0, 0, 0))
    DISPLAY_SURFACE.blit(textsurface,(1,40))
    textsurface = myfont.render(('sleeping: '+str(sleeping_count)), False, (0, 0, 0))
    DISPLAY_SURFACE.blit(textsurface,(1,50))
    textsurface = myfont.render(('knocked: '+str(passed_out_count)), False, (0, 0, 0))
    DISPLAY_SURFACE.blit(textsurface,(1,60))
    textsurface = myfont.render(('starving: '+str(starve_count)), False, (0, 0, 0))
    DISPLAY_SURFACE.blit(textsurface,(1,70))
        
    pygame.display.update()
    dt = FPS_CLOCK.tick(FPS)
    elapsed_time += dt
    debug += dt
