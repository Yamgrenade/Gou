from equipment_slots import EquipmentSlots


class Equipment:
    def __init__(self, main_hand=None, off_hand=None, head=None, chest=None, hands=None, legs=None, feet=None):
        self.main_hand = main_hand
        self.off_hand = off_hand
        self.head = head
        self.chest = chest
        self.hands = hands
        self.legs = legs
        self.feet = feet

    # each of these could probably be put into a single function but I guess that might be less readable
    @property
    def max_hp_bonus(self):
        bonus = 0

        for slot in vars(self).values():
            if slot and slot.equippable:
                bonus += slot.equippable.max_hp_bonus

        return bonus

    @property
    def power_bonus(self):
        bonus = 0

        for slot in vars(self).values():
            if slot and slot.equippable:
                bonus += slot.equippable.power_bonus

        return bonus

    @property
    def defense_bonus(self):
        bonus = 0

        for slot in vars(self).values():
            if slot and slot.equippable:
                bonus += slot.equippable.defense_bonus

        return bonus

    def toggle_equip(self, equippable_entity):
        results = []

        slot = equippable_entity.equippable.slot     

        # There is 100% a way to combine each of these to reduce repetition
        if slot == EquipmentSlots.MAIN_HAND:
            if self.main_hand == equippable_entity:
                self.main_hand = None
                results.append({'unequipped': equippable_entity})
            else:
                if self.main_hand:
                    results.append({'unequipped': self.main_hand})

                self.main_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.OFF_HAND:
            if self.off_hand == equippable_entity:
                self.off_hand = None
                results.append({'unequipped': equippable_entity})
            else:
                if self.off_hand:
                    results.append({'unequipped': self.off_hand})

                self.off_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.HEAD:
            if self.head == equippable_entity:
                self.head = None
                results.append({'unequipped': equippable_entity})
            else:
                if self.head:
                    results.append({'unequipped': self.head})

                self.head = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.CHEST:
            if self.chest == equippable_entity:
                self.chest = None
                results.append({'unequipped': equippable_entity})
            else:
                if self.chest:
                    results.append({'unequipped': self.chest})

                self.chest = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.HANDS:
            if self.hands == equippable_entity:
                self.hands = None
                results.append({'unequipped': equippable_entity})
            else:
                if self.hands:
                    results.append({'unequipped': self.hands})

                self.hands = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.LEGS:
            if self.legs == equippable_entity:
                self.legs = None
                results.append({'unequipped': equippable_entity})
            else:
                if self.legs:
                    results.append({'unequipped': self.legs})

                self.legs = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.FEET:
            if self.feet == equippable_entity:
                self.feet = None
                results.append({'unequipped': equippable_entity})
            else:
                if self.feet:
                    results.append({'unequipped': self.feet})

                self.feet = equippable_entity
                results.append({'equipped': equippable_entity})

        return results
