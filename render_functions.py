import tcod as libtcod

from enum import Enum, auto

from game_states import GameStates

from menus import inventory_menu, level_up_menu, character_screen, message_box

from input_handlers import handle_popup

from camera import Camera

class RenderOrder(Enum):
    STAIRS = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()


def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '{0}: {1}/{2}'.format(name, value, maximum))


# Render all entities in the given list
def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height,
               bar_width, panel_height, panel_y, mouse, colors, game_state, camera):
    # Draw the tiles in the given map
    if fov_recompute:
        libtcod.console_clear(con) # This was required to get screen scrolling working. There may be a more efficient way to update the screen but I can't think of one.
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight
                x_in_camera, y_in_camera = camera.apply(x, y)

                if visible:
                    if wall:
                        libtcod.console_set_char_background(con, x_in_camera, y_in_camera, colors.get('light_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x_in_camera, y_in_camera, colors.get('light_ground'), libtcod.BKGND_SET)

                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(con, x_in_camera, y_in_camera, colors.get('dark_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x_in_camera, y_in_camera, colors.get('dark_ground'), libtcod.BKGND_SET)

    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map, camera)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    y = 1
    for message in message_log.visible:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y += 1

    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               libtcod.light_red, libtcod.darker_red)
    libtcod.console_print_ex(panel, 1, 3, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Dungeon level: {0}'.format(game_map.dungeon_level))

    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT,
                             get_names_under_mouse(mouse, entities, fov_map))

    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it. Press Esc to cancel.\n'
        else:
            inventory_title = 'Press the key next to an item to drop it. Press Esc to cancel.\n'

        inventory_menu(con, inventory_title, player, 50, screen_width, screen_height)

    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(con, 'Level up! Choose a stat to increase:', player, 40, screen_width, screen_height)

    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 10, screen_width, screen_height)  # TODO: More constants all over the place here
    
    elif game_state == GameStates.FULLSCREEN_CONSOLE:
        window = libtcod.console_new(screen_width, screen_height)

        z = 1
        for message in message_log.fullscreen_visible:
            libtcod.console_set_default_foreground(window, message.color)
            libtcod.console_print_ex(window, 0, z, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
            z += 1

        libtcod.console_blit(window, 0, 0, screen_width, screen_height, 0, 0, 0)

# Displays a popup with the given size and message. Is dismissed when any key is pressed. 
# TODO This should probably be refactored and put into menus.py
def popup(con, message, width, height):
    dismiss = False
    
    while not dismiss:
        message_box(con, message, 50, width, height)
        libtcod.console_flush()
        key = libtcod.console_wait_for_keypress(True)
        action = handle_popup(key)
        dismiss = action.get('dismiss')


# erase all entities in the given list
def clear_all(con, entities, camera):
    for entity in entities:
        clear_entity(con, entity, camera)


# draw an entity's char
def draw_entity(con, entity, fov_map, game_map, camera):
    x, y = camera.apply(entity.x, entity.y)
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y) \
            or (entity.stairs and game_map.tiles[entity.x][entity.y].explored):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, x, y, entity.char, libtcod.BKGND_NONE)


# erase an entity's char
def clear_entity(con, entity, camera):
    x, y = camera.apply(entity.x, entity.y)
    libtcod.console_put_char(con, x, y, ' ', libtcod.BKGND_NONE)
