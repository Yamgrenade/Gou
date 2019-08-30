from random_utils import from_dungeon_level, random_choice_from_dict
from components.modifier import equippable_material, equippable_enchantment
from equipment_slots import EquipmentSlotGroups

class Equippable:
    def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0):
        self.slot = slot
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus
        # Modifiers are currently added directly instead of being their own attributes but it might actually be nice to know what kind of modifier an item is

    def generate_material(self, dungeon_level):
        "Generates a random material for the given item based on dungeon level. The modifier will potentially apply a bonus and change the name of the item. Bonus will usually be defensive for armor and offensive for weapons"
        modifierChances = {key: from_dungeon_level(value.chance, dungeon_level) for key, value in equippable_material.items() if self.slot in value.slot_restrictions}
        modifier_name = random_choice_from_dict(modifierChances)
        modifier = equippable_material.get(modifier_name)
        if modifier.bonus_dic:
            for _, value in modifier.bonus_dic.items():
                # Set power if weapon, defense if armor
                if self.slot in EquipmentSlotGroups.WEAPONS: setattr(self, 'power_bonus', getattr(self, 'power_bonus') + value)
                else: setattr(self, 'defense_bonus', getattr(self, 'defense_bonus') + value)
                return modifier_name + ' '
        return ''

    def generate_enchantment(self, dungeon_level):
        "Generates a random enchantment for the given item based on dungeon level. The modifier will potentially apply a bonus and change the name of the item"
        modifierChances = {key: from_dungeon_level(value.chance, dungeon_level) for key, value in equippable_enchantment.items() if self.slot in value.slot_restrictions}
        modifier_name = random_choice_from_dict(modifierChances)
        modifier = equippable_enchantment.get(modifier_name)
        if modifier.bonus_dic:
            for key, value in modifier.bonus_dic.items():
                # Bonus type is whatever is written in modifier
                setattr(self, key, getattr(self, key) + value)
                return ' of ' + modifier_name
        return ''