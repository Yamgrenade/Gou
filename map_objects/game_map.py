import tcod as libtcod

from entity import Entity
from game_messages import Message
from components.ai import BasicMonster
from components.equipment import EquipmentSlots
from components.equippable import Equippable
from components.fighter import Fighter
from components.item import Item
from item_functions import heal, cast_lightning, cast_fireball, cast_confuse
from map_objects.tile import Tile
from map_objects.rectangle import Rect
from render_functions import RenderOrder
from components.stairs import Stairs
from random_utils import random_choice_from_dict, from_dungeon_level

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
        down_stairs = Entity(last_room_center_x, last_room_center_y, '>', libtcod.white, 'Stairs down',
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

        monster_chances = {
            'orc': 80,
            'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.dungeon_level)
            # , 'dragon': 5
        }
        item_chances = {
            'healing_potion': 35,
            'sword': from_dungeon_level([[5, 4]], self.dungeon_level),
            'shield': from_dungeon_level([[15, 8]], self.dungeon_level),
            'lightning_scroll': from_dungeon_level([[25, 4]], self.dungeon_level),
            'fireball_scroll': from_dungeon_level([[25, 6]], self.dungeon_level),
            'confuse_scroll': from_dungeon_level([[10, 2]], self.dungeon_level)
        }

        for i in range(num_monsters):
            # Place randomly
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            # Check that an existing entity isn't in this space
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)

                if monster_choice == 'orc':
                    fighter_component = Fighter(hp=20, defense=0, power=4, xp=35)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'o', libtcod.desaturated_green, 'Orc', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                elif monster_choice == 'troll':
                    fighter_component = Fighter(hp=30, defense=2, power=8, xp=100)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'T', libtcod.darker_green, 'Troll', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                elif monster_choice == 'dragon':
                    fighter_component = Fighter(hp=40, defense=2, power=6, xp=250)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'D', libtcod.darker_red, 'Dragon', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

                entities.append(monster)

        for i in range(num_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_choice = random_choice_from_dict(item_chances)

                if item_choice == 'healing_potion':
                    item_component = Item(use_function=heal, amount=40)
                    item = Entity(x, y, '!', libtcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'sword':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
                    item = Entity(x, y, '/', libtcod.sky, 'Sword', equipment=equippable_component)
                elif item_choice == 'shield':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1)
                    item = Entity(x, y, '[', libtcod.darker_orange, 'Shield', equippable=equippable_component)
                elif item_choice == 'fireball_scroll':
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                        'You ready a fireball. (Left click to cast, right click to cancel.)', libtcod.light_cyan),
                                          damage=25,radius=3)
                    item = Entity(x, y, '#', libtcod.light_crimson, 'Fireball Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'confuse_scroll':
                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                        'You prepare to daze a creature. (Left click to cast, right click to cancel.)',
                        libtcod.light_cyan))
                    item = Entity(x, y, '#', libtcod.light_purple, 'Confuse Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                else:
                    item_component = Item(use_function=cast_lightning, damage=40, maximum_range=7)
                    item = Entity(x, y, '#', libtcod.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)

                entities.append(item)

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
