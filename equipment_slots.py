from enum import Enum, auto


class EquipmentSlots(Enum):
    MAIN_HAND = auto()
    OFF_HAND = auto()
    HEAD = auto()
    CHEST= auto()
    HANDS = auto()
    LEGS = auto()
    FEET = auto()

class EquipmentSlotGroups():
    WEAPONS = [EquipmentSlots.MAIN_HAND]
    ARMOR = [EquipmentSlots.HEAD, EquipmentSlots.CHEST, EquipmentSlots.HANDS, EquipmentSlots.LEGS, EquipmentSlots.FEET, EquipmentSlots.OFF_HAND]
    ALL = [EquipmentSlots.MAIN_HAND, EquipmentSlots.OFF_HAND, EquipmentSlots.HEAD, EquipmentSlots.CHEST, EquipmentSlots.HANDS, EquipmentSlots.LEGS, EquipmentSlots.FEET]
