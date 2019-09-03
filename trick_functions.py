from game_messages import Message


def halfmoon_slash(*args, **kwargs):
    user = args[0] # As in fighter using the trick, want to attempt to keep it open for AI to use
    facing = kwargs.get("facing") # -1 or +1
    entities = kwargs.get("entities")
    damage = kwargs.get("damage")

    results = []
    hit_zone = [(user.x + facing, user.y),
                (user.x + facing, user.y + 1),
                (user.x + facing, user.y - 1),
                (user.x, user.y + 1),
                (user.x, user.y - 1)]

    for entity in entities:
        if (entity.x, entity.y) in hit_zone and entity.fighter:
            results.append({'message': Message('The {0} takes {1} damage from your half-moon slash.'.format(
                entity.name, damage))})
            results.extend(entity.fighter.take_damage(damage))

    return results
