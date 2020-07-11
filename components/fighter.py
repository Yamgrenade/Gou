import tcod as libtcod

from game_messages import Message

class Fighter:
    def __init__(self, hp, defense, power, speed, xp=0):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.base_speed = speed
        self.xp = xp

    # Equipment might want a rework so that it supports many mort effects easier.

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0

        return self.base_power + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus

    @property
    def speed(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.speed_bonus
        else:
            bonus = 0

        return self.base_speed + bonus

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})

        return results

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        results = []

        damage = self.power - target.fighter.defense

        if damage > 0:
            results.append({'message': Message('{0} attacks {1} for {2} damage.'.format(
                self.owner.name, target.name, str(damage)))})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                self.owner.name, target.name))})

        return results

    # def damage_over_time(self, damage, turns):
    #     for turn in turns:
    #         self.take_damage(damage)

    # def stun(self, turns):
    #     for turn in turns:
    #         skip turn