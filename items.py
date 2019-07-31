import tcod as libtcod
from random_utils import random_choice_from_dict, from_dungeon_level
from entity import Entity
from render_functions import RenderOrder
from item_functions import *
from equipment_slots import EquipmentSlots
from components.usable import Usable
from components.equippable import Equippable
from components.fighter import Fighter
from components.ai import BasicMonster


class Item:
  def __init__(self, chance, entity):
    self.chance = chance
    self.entity = entity

items = {
  'healing_potion': Item([35], Entity(-1, -1, '!', libtcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM, 
    usable=Usable(use_function=heal, amount=40))),

  'dagger': Item([0], Entity(0, 0, "-", libtcod.sky, "Dagger", 
    equippable=Equippable(EquipmentSlots.MAIN_HAND, power_bonus=1))),

  'sword': Item([[5,4]], Entity(-1, -1, '/', libtcod.sky, 'Sword', 
    equippable=Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3))),

  'shield': Item([[15, 8]], Entity(-1, -1, '[', libtcod.darker_orange, 'Shield', 
    equippable=Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1))),

  'lightning_scroll': Item([[25, 4]], Entity(-1, -1, '#', libtcod.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM,
    usable=Usable(use_function=cast_lightning, damage=40, maximum_range=7))),

  'fireball_scroll': Item([[25, 6]], Entity(-1, -1, '#', libtcod.light_crimson, 'Fireball Scroll', render_order=RenderOrder.ITEM, 
    usable=Usable(use_function=cast_fireball, targeting=True, targeting_message=Message('You ready a fireball. (Left click to cast, right click to cancel.)', libtcod.light_cyan),damage=25,radius=3))),

  'confuse_scroll': Item([[10, 2]], Entity(-1, -1, '#', libtcod.light_purple, 'Confuse Scroll', render_order=RenderOrder.ITEM,
    usable=Usable(use_function=cast_confuse, targeting=True, targeting_message=Message('You prepare to daze a creature. (Left click to cast, right click to cancel.)', libtcod.light_cyan)))),

  'Conjure Orc Wand': Item([0], Entity(-1, -1, 'i', libtcod.dark_green, 'Conjure Orc Wand', render_order=RenderOrder.ITEM,
    usable=Usable(use_function=spawn_orc, targeting=True, targeting_message=Message('Left click to spawn an orc.', libtcod.light_cyan)))),

  'Book of Forbidden Knowledge': Item([0], Entity(-1, -1, '=', libtcod.purple, 'Book of Forbidden Knowledge', render_order=RenderOrder.ITEM,
    usable=Usable(use_function=give_xp))),
}