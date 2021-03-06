import tcod as libtcod

from game_messages import Message
from entity import Entity
from components.ai import ConfusedMonster, BasicMonster
from components.fighter import Fighter
from components.level import Level
from render_functions import RenderOrder


def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get("amount")

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append(
            {
                "consumed": False,
                "message": Message("You are at full health already.", libtcod.yellow),
            }
        )
    else:
        entity.fighter.heal(amount)
        results.append(
            {
                "consumed": True,
                "message": Message(
                    "You gulp down the vial and your woulds start to close.",
                    libtcod.green,
                ),
            }
        )

    return results

def cast_lightning(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get("entities")
    fov_map = kwargs.get("fov_map")
    damage = kwargs.get("damage")
    maximum_range = kwargs.get("maximum_range")

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if (
            entity.fighter
            and entity != caster
            and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)
        ):
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append(
            {
                "consumed": True,
                "message": Message(
                    "A bolt of lightning strikes the {0} for {1} damage!".format(
                        target.name, damage
                    )
                ),
            }
        )
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append(
            {
                "consumed": False,
                "target": None,
                "message": Message("There are no enemies nearby.", libtcod.yellow),
            }
        )

    return results


def cast_fireball(*args, **kwargs):
    entities = kwargs.get("entities")
    fov_map = kwargs.get("fov_map")
    damage = kwargs.get("damage")
    radius = kwargs.get("radius")
    target_x = kwargs.get("target_x")
    target_y = kwargs.get("target_y")

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append(
            {
                "consumed": False,
                "message": Message(
                    "You must target a tile in your line of sight.", libtcod.yellow
                ),
            }
        )
        return results

    results.append(
        {
            "consumed": True,
            "message": Message(
                "The fireball explodes violently, burning everything within {0} tiles!".format(
                    radius
                ),
                libtcod.orange,
            ),
        }
    )

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append(
                {
                    "message": Message(
                        "The {0} is burned for {1} damage.".format(entity.name, damage),
                        libtcod.orange,
                    )
                }
            )
            results.extend(entity.fighter.take_damage(damage))

    return results


def cast_confuse(*args, **kwargs):
    entities = kwargs.get("entities")
    fov_map = kwargs.get("fov_map")
    target_x = kwargs.get("target_x")
    target_y = kwargs.get("target_y")

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append(
            {
                "consumed": False,
                "message": Message(
                    "You must target a tile in your line of sight.", libtcod.yellow
                ),
            }
        )
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 10)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append(
                {
                    "consumed": True,
                    "message": Message(
                        "The {0} is stuck by a flash of light and starts to stumble around.".format(
                            entity.name
                        ),
                        libtcod.lighter_purple,
                    ),
                }
            )

            break
    else:
        results.append(
            {
                "consumed": False,
                "message": Message(
                    "There are no targetable enemies there.", libtcod.yellow
                ),
            }
        )

    return results


# Should only be used in the test arena.
def spawn_orc(*args, **kwargs):
    entities = kwargs.get("entities")
    target_x = kwargs.get("target_x")
    target_y = kwargs.get("target_y")

    fighter_component = Fighter(hp=20, defense=0, power=4, speed=150, xp=35)
    ai_component = BasicMonster()
    orc = Entity([], target_x, target_y, 'o', libtcod.desaturated_green, 'Orc', blocks=True,
                    render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

    entities.append(orc)

    results = []
    results.append(
            {
                "consumed": False,
                "message": Message(
                    "A conjured orc springs into the room!", libtcod.yellow
                ),
            }
        )

    return results


# Should only be used in the test arena.
def give_xp(*args, **kwargs):
    entity = args[0]

    amount = entity.level.experience_to_next_level + 1

    results = []
    results.append(
            {
                "consumed": False,
                "message": Message("You pore through the tome and shudder.", libtcod.yellow),
                "xp": amount
            }
    )

    return results
