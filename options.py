# FPS ###########################################################
FPS = 60

# COLORS ########################################################
BLACK = (0,0,0)
BLUE  = (0,0,255)
BROWN = (181, 142, 109)
GREEN = (0,255,0)
DARK_GREEN = (0,175,0)
RED   = (255,0,0)

# BLOCKS ########################################################
DIRT  = 0
GRASS = 1
WATER = 2
COAL  = 3
LONG_GRASS = 4

colours = {
    DIRT  : BROWN,
    GRASS : GREEN,
    WATER : BLUE,
    LONG_GRASS  : DARK_GREEN
}

# SIZES ########################################################
TILE_SIZE  = 12
MAP_WIDTH  = 40
MAP_HEIGHT = 40

# MAP GEN CHANCES ##############################################
MAP_GEN_GRASS_CHANCE = 22
MAP_GEN_WATER_CHANGE = 2

# GRASS GROWTH CHANCES #########################################
GRASS_GROWTH_CHANCE = 0.00005
GRASS_GENERATION_CHANCE = 0.000005
GRASS_WATER_GROWTH_CHANCE = 0.0005

# MISC #########################################################
MALE = 0
FEMALE = 1

PREY_START_COUNT = 10
PRED_START_COUNT = 1
