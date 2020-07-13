from random_utils import from_dungeon_level, random_choice_from_dict
from equipment_slots import EquipmentSlotGroups

class Modifier:
    def __init__(self, chance, bonus_dic=None, slot_restrictions=EquipmentSlotGroups.ALL):
        self.chance = chance
        self.bonus_dic = bonus_dic
        self.slot_restrictions = slot_restrictions

equippable_material = {
  'Wooden': Modifier([30], {'bonus': 0}), # The key here really does not matter since bonus type is determined by slot
  'Iron': Modifier([[15, 1], [50, 3]], {'bonus': 1}),
  'Steel': Modifier([[5, 1], [60, 5]], {'bonus': 2})
}

equippable_enchantment = {
  '': Modifier([70], {}), # No Enchantment
  'Flames': Modifier([10], EquipmentSlotGroups.WEAPONS, {'power_bonus': 2}),
  'Strength': Modifier([10], {'power_bonus': 1, 'defense_bonus': 1}),
  'Speed': Modifier([100], {'speed_bonus': -20})
}