from random import randint


# TODO: I don't love this because it still requires manual assignment for dungeon progression, but it works for now
def from_dungeon_level(table, dungeon_level):
    """Returns the probablility of somthing spawning in a given dungeon level. 
    Table is formatted [[probability, lowest possible level], [probability, next lowest possible level], etc]"""
    if isinstance(table[0], int):
        return table[0]
    for (value, level) in reversed(table):
        if dungeon_level >= level:
            return value

    return 0


def random_choice_index(chances):
    random_chance = randint(1, sum(chances))

    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w

        if random_chance <= running_sum:
            return choice
        choice += 1


def random_choice_from_dict(choice_dict):
    choices = list(choice_dict.keys())
    chances = list(choice_dict.values())

    return choices[random_choice_index(chances)]
