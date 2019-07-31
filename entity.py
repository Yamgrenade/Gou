import math
import tcod as libtcod

from components.usable import Usable

from render_functions import RenderOrder
"""
Class for generic objects, from usables to monsters. 
Some cleanup could reduce redundancy, specifically with the distance functions.
"""


class Entity:
    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None,
                 usable=None, inventory=None, stairs=None, level=None, equipment=None, equippable=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.usable = usable
        self.inventory = inventory
        self.stairs = stairs
        self.level = level
        self.equipment = equipment
        self.equippable = equippable

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.usable:
            self.usable.owner = self

        if self.inventory:
            self.inventory.owner = self

        if self.stairs:
            self.stairs.owner = self

        if self.level:
            self.level.owner = self

        if self.equipment:
            self.equipment.owner = self

        if self.equippable:
            self.equippable.owner = self

            # We can't have equippables that aren't also usables, so add it if it doesn't have it
            if not self.usable:
                usable = Usable()
                self.usable = usable
                self.usable.owner = self

    # move the entity by the specified dx, dy
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or
                get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)

    def distance(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def move_astar(self, target, entities, game_map):
        # Create another FOV map
        fov = libtcod.map_new(game_map.width, game_map.height)

        # Scan the map and set walls as blocked
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                libtcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight,
                                           not game_map.tiles[x1][y1].blocked)

        # Scan for entities to path around
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                libtcod.map_set_properties(fov, entity.x, entity.y, True, False)

        # Allocate a A* path
        # NOTE: The diagonal movement cost is defined here, might want to put in a config somewhere
        my_path = libtcod.path_new_using_map(fov, 1.41)

        # Compute the path
        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # If the path exists and is not too long, walk along
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                self.x = x
                self.y = y

        # Use dumber pathfinding to just get closer if there is no complete path
        else:
            self.move_towards(target.x, target.y, game_map, entities)

        # Deallocate path
        libtcod.path_delete(my_path)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def place(self, x, y):
        self.x = x
        self.y = y
        return self


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None

