import tcod as libtcod
from collections import deque

import textwrap


class Message:
    def __init__(self, text, color=libtcod.white):
        self.text = text
        self.color = color


class MessageLog:
    def __init__(self, x, width, height, screen_height):
        self.messages = []
        self.visible = []
        self.fullscreen_visible = []
        self.x = x
        self.width = width
        self.height = height
        self.fullscreen_height = screen_height
        self.scroll_index = 0
        self.fullscreen_scroll_index = 0

    # Adds message to the log, wrapping it if it's too long and making space if needed
    def add_message(self, message):
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            self.messages.append(Message(line, message.color))
            if len(self.messages) >= self.height:
                self.visible = self.messages[-self.height:]
            else:
                self.visible = self.messages
            # Fullscreen
            if len(self.messages) >= self.fullscreen_height: 
                self.fullscreen_visible = self.messages[-self.fullscreen_height:]
            else:
                self.fullscreen_visible = self.messages

    # Scrolls the message log up by one line
    def scroll_up(self):
        if len(self.messages) >= self.height and self.scroll_index < len(self.messages) - self.height:
            self.scroll_index += 1
            self.visible = self.messages[-self.height - self.scroll_index:-self.scroll_index]
        # Fullscreen
        if len(self.messages) >= self.fullscreen_height and self.scroll_index < len(self.messages) - self.fullscreen_height:
            self.fullscreen_scroll_index += 1
            self.fullscreen_visible = self.messages[-self.fullscreen_height - self.fullscreen_scroll_index:-self.fullscreen_scroll_index]

    # Scrolls the message log down by one line
    def scroll_down(self):
        if len(self.messages) >= self.height and self.scroll_index > 1:
            self.scroll_index -= 1
            self.visible = self.messages[-self.height - self.scroll_index:-self.scroll_index]
        elif len(self.messages) >= self.height and self.scroll_index == 1:
            self.scroll_index -= 1
            self.visible = self.messages[-self.height:]
        # Fullscreen
        if len(self.messages) >= self.fullscreen_height and self.fullscreen_scroll_index > 1:
            self.fullscreen_scroll_index -= 1
            self.fullscreen_visible = self.messages[-self.fullscreen_height - self.fullscreen_scroll_index:-self.fullscreen_scroll_index]
        elif len(self.messages) >= self.fullscreen_height and self.fullscreen_scroll_index == 1:
            self.fullscreen_scroll_index -= 1
            self.fullscreen_visible = self.messages[-self.fullscreen_height:]

