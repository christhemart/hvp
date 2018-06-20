My WIP attempt at learning about pygame which currently features:
1. simple tile map generation
row/column square based tiles
generation chances are 2% water, 20% grass, 78% dirt
2. simple grass growth simulation
dirt has a small chance to turn to grass
the more grass that surrounds a dirt tile, the higher the chance to turn into grass
dirt next to water has significant chance to grow grass
3. a prey class
contains various stats like health, hunger, sleep, energy, gender, etc.
stats degrade over time
has view distance of 3 tiles away
will look for grass tiles when hunger drops below threshold, eating grass off a tile turns it into dirt
will sleep if tired but only if hunger is satisfied and no hunters near
will knock out if sleep stat reaches 0 even if hungry or close to hunters
slowly loses health if starving
will die if health loses 0 or if caught by hunter
will run away from predators
will try to find and mate with opposite gender if both have satisfied stats, 25% to succeed
females have a gestation period
4. a hunter class
contains various stats like health, hunger, sleep, energy, gender, etc.
stats degrade over time
has view distance of 6 tiles away
hunts prey for food if hunger drops below threshold
will sleep if tired but only if hunger is satisfied
will knock out if sleep stat reaches 0 even if hungry
slowly loses health if starving
will die if health loses 0
