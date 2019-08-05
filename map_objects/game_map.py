import tcod as libtcod
import copy

from entity import Entity
from game_messages import Message
from components.ai import BasicMonster
from components.equipment import EquipmentSlots
from components.equippable import Equippable
from components.fighter import Fighter
from components.usable import Usable
from item_functions import heal, cast_lightning, cast_fireball, cast_confuse, spawn_orc, give_xp
from map_objects.tile import Tile
from map_objects.rectangle import Rect
from render_functions import RenderOrder
from components.stairs import Stairs
from random_utils import random_choice_from_dict, from_dungeon_level
from monsters import monsters
from items import items
from random import randint


class GameMap:
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

        self.dungeon_level = dungeon_level

    def initialize_tiles(self):
        # Generate array of blocked tiles to dig a dungeon out of
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    # Create a random map (Rectangles joined by tunnels)
    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities):
        rooms = []
        num_rooms = 0

        last_room_center_x = None
        last_room_center_y = None

        # generate random size rooms
        for r in range(max_rooms):
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # ensure map boundaries aren't crossed
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            new_room = Rect(x, y, w, h)

            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # if we got here, then the room did not intersect with existing rooms
                self.create_room(new_room)
                (new_x, new_y) = new_room.center()

                last_room_center_x = new_x
                last_room_center_y = new_y

                # player starts in first room
                if num_rooms == 0:
                    player.x = new_x
                    player.y = new_y
                else:
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    if randint(0, 1) == 1:
                        # move h then v
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # move v then h
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room, entities)

                # add to room list
                rooms.append(new_room)
                num_rooms += 1

        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity([], last_room_center_x, last_room_center_y, '>', libtcod.white, 'Stairs down',
                                 render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)

    # go through the tiles in the given room and make them passable
    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    # TODO: This should probably get split up so it's easier to add new monsters just by keeping their stats somewhere
    # Probably with **kwargs, if I had to guess
    def place_entities(self, room, entities):
        max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [5, 6]], self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1, 1], [2, 4]], self.dungeon_level)

        num_monsters = randint(0, max_monsters_per_room)
        num_items = randint(0, max_items_per_room)

        monster_chances = {key: from_dungeon_level(value.chance, self.dungeon_level) for key, value in monsters.items()}

        item_chances = {key: from_dungeon_level(value.chance, self.dungeon_level) for key, value in items.items()}

        for i in range(num_monsters):
            # Place randomly
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            # Check that an existing entity isn't in this space. If not choose one randomly (based on dungeon level) and place it
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)
                # monster = monster.entity for monster in monsters if monster.name == monster_choice
                monster_instance = None
                for name, monster in monsters.items():
                    if name == monster_choice:
                        monster_instance = copy.deepcopy(monster)
                        monster_instance.place(x, y)
                        break
                entities.append(monster_instance)

        for i in range(num_items):
            # Place randomly
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            # Check that an existing entity isn't in this space. If not choose one randomly (based on dungeon level) and place it
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_choice = random_choice_from_dict(item_chances)

                item_instance = None
                for name, item in items.items():
                    if name == item_choice:
                        item_instance = copy.deepcopy(item)
                        item_instance.place(x, y)
                entities.append(item_instance)

    def next_floor(self, player, message_log, constants):
        self.dungeon_level += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You rest briefly in the staircase and feel restored.'))

        return entities

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
    
    # Generates the test arena, which has some hard coded cheaty items for testing
    def make_arena(self, entities):
        self.dungeon_level = -1
        self.create_room(Rect(0, 0, self.width - 1, self.height - 1))

        arena_sword = copy.deepcopy(items['sword'])
        arena_sword.place(4, 2)

        arena_xp_book = copy.deepcopy(items['Book of Forbidden Knowledge'])
        arena_xp_book.place(3, 2)
        
        arena_orc_wand = copy.deepcopy(items['Conjure Orc Wand'])
        arena_orc_wand.place(2, 2)
        
        entities.append(arena_sword)
        entities.append(arena_xp_book)
        entities.append(arena_orc_wand)
