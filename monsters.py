import tcod as libtcod
from random_utils import random_choice_from_dict, from_dungeon_level
from entity import Entity
from render_functions import RenderOrder
from components.fighter import Fighter
from components.ai import BasicMonster

monsters = {
    'orc': Entity([80], -1, -1, 'o', libtcod.desaturated_green, 'Orc', blocks=True, render_order=RenderOrder.ACTOR, fighter=Fighter(hp=20, defense=0, power=4, xp=35), ai=BasicMonster()),
    'troll': Entity([[15, 3], [30, 5], [60, 7]], -1, -1, 'T', libtcod.darker_green, 'Troll', blocks=True, render_order=RenderOrder.ACTOR, fighter=Fighter(hp=30, defense=2, power=8, xp=100), ai=BasicMonster()),
}
            