import tcod as libtcod
from collections import deque

import textwrap


class Message:
    def __init__(self, text, color=libtcod.white):
        self.text = text
        self.color = color


class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.visible = []
        self.x = x
        self.width = width
        self.height = height
        self.scroll_index = 0

    # Adds message to the log, wrapping it if it's too long and making space if needed
    def add_message(self, message):
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            self.messages.append(Message(line, message.color))
            if len(self.messages) >= self.height:
                self.visible = self.messages[-self.height:]
            else:
                self.visible = self.messages

        # Making old messages darker will need to grab how many messages appear during all enemy turns so it won't darken those before the player's next turn.
        # for i in range(len(self.visible)-1, len(new_msg_lines)-1, -1):
        #     self.visible[i].color = self.visible[i].color * libtcod.dark_gray

    # Scrolls the message log up by one line
    def scroll_up(self):
        if len(self.messages) >= self.height and self.scroll_index < len(self.messages) - self.height:
            self.scroll_index += 1
            self.visible = self.messages[-self.height - self.scroll_index:-self.scroll_index]

    # Scrolls the message log down by one line
    def scroll_down(self):
        if len(self.messages) >= self.height and self.scroll_index > 1:
            self.scroll_index -= 1
            self.visible = self.messages[-self.height - self.scroll_index:-self.scroll_index]
        elif len(self.messages) >= self.height and self.scroll_index == 1:
            self.scroll_index -= 1
            self.visible = self.messages[-self.height:]


