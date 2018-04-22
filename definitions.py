import math
import random

from options import *

def distance(vector1,vector2):
    return math.sqrt((vector2[0]-vector1[0])**2 + (vector2[1]-vector1[1])**2)

def flee(my_vector,flee_vector,distance):
    movable = [[x,y] for x in range(max(0,my_vector[0]-1), min(MAP_HEIGHT,my_vector[0]+2)) for y in range(max(0,my_vector[1]-1), min(MAP_WIDTH,my_vector[1]+2))]

    if my_vector[0] != flee_vector[0]:
        if flee_vector[0] > my_vector[0]:
            my_vector[0] = my_vector[0] - distance
        else:
            my_vector[0] = my_vector[0] + distance
    if my_vector[1] != flee_vector[1]:
        if flee_vector[1] > my_vector[1]:
            my_vector[1] = my_vector[1] - distance
        else:
            my_vector[1] = my_vector[1] + distance
    return my_vector if my_vector in movable else movable[random.randint(0,len(movable)-1)]

def move_to_target(my_vector,target_vector,distance):
    if my_vector[0] != target_vector[0]:
        if target_vector[0] > my_vector[0]:
            my_vector[0] = my_vector[0] + distance
        else:
            my_vector[0] = my_vector[0] - distance
    if my_vector[1] != target_vector[1]:
        if target_vector[1] > my_vector[1]:
            my_vector[1] = my_vector[1] + distance
        else:
            my_vector[1] = my_vector[1] - distance
    return my_vector

def straight_move(position,moving):
    movable = [[x,y] for x in range(max(0,position[0]-1), min(MAP_HEIGHT,position[0]+2)) for y in range(max(0,position[1]-1), min(MAP_WIDTH,position[1]+2))]
    move_pick = random.randint(1,len(movable))
                    
    if moving[0] != 0 or moving[1] != 0:
        go_straight = True if random.randint(1,10) <= 8 else False

        if go_straight:
            moves = []
            if moving == [-1,1]:
                moves = [move for move in movable if (position[0]-1<=move[0]<=position[0]) and (position[1]<=move[1]<=position[1]+1)]
            elif moving == [0,1]:
                moves = [move for move in movable if (position[0]-1<=move[0]<=position[0]+1) and (move[1]==position[1]+1)]
            elif moving == [1,1]:
                moves = [move for move in movable if (position[0]<=move[0]<=position[0]+1) and (position[1]<=move[1]<=position[1]+1)]
            elif moving == [1,0]:
                moves = [move for move in movable if (move[0]==position[0]+1) and (position[1]-1<=move[1]<=position[1]+1)]
            elif moving == [1,-1]:
                moves = [move for move in movable if (position[0]<=move[0]<=position[0]+1) and (position[1]-1<=move[1]<=position[1])]
            elif moving == [0,-1]:
                moves = [move for move in movable if (position[0]-1<=move[0]<=position[0]+1) and (move[1]==position[1]-1)]
            elif moving == [-1,-1]:
                moves = [move for move in movable if (position[0]-1<=move[0]<=position[0]) and (position[1]-1<=move[1]<=position[1])]
            elif moving == [-1,0]:
                moves = [move for move in movable if (move[0]==position[0]-1) and (position[1]-1<=move[1]<=position[1]+1)]

            if len(moves) > 0:
                move_pick = random.randint(1,len(moves))
                movable = moves
                        
    if movable[move_pick-1][0] > position[0]:
        moving[0] = 1
    elif movable[move_pick-1][0] < position[0]:
        moving[0] = -1
    else:
        moving[0] = 0

    if movable[move_pick-1][1] > position[1]:
        moving[1] = 1
    elif movable[move_pick-1][1] < position[1]:
        moving[1] = -1
    else:
        moving[1] = 0

    return [movable[move_pick-1],moving]

def tile_search(tilemap, position, lookup, distance):
    for n in range(1,distance+1):
        matching_tiles = []
        for row in range(max(0,position[0]-n), min(MAP_HEIGHT,position[0]+n+2), n):
            for column in range(max(0,position[1]-n), min(MAP_WIDTH,position[1]+n+2), n):
                if tilemap[row][column] == lookup:
                    matching_tiles.append([row,column])
                    
        if len(matching_tiles) > 0:
            return matching_tiles
    return matching_tiles

def update_map(tilemap):
    for row in range(MAP_HEIGHT):
        for column in range(MAP_WIDTH):
            if tilemap[row][column] == DIRT:
                grass_grow_chance = GRASS_GENERATION_CHANCE
                grass_grow_chance += GRASS_GROWTH_CHANCE * len(tile_search(tilemap, [row,column], GRASS, 1))
                grass_grow_chance += GRASS_WATER_GROWTH_CHANCE * len(tile_search(tilemap, [row,column], WATER, 1))
                if random.random() <= grass_grow_chance:
                    tilemap[row][column] = GRASS
    return tilemap

def get_grass_count(tilemap):
    grass_count = 0
    for row in range(MAP_HEIGHT):
        for column in range(MAP_WIDTH):
            if tilemap[row][column] == GRASS:
                grass_count += 1
    return grass_count
