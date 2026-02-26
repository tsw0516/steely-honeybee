# models.py
# This file defines the core data structures for the board game shelf allocation problem.
# Tyler Walker - 2026-02-25

class BoardGame:
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height

    def __repr__(self):
        return f"{self.name} (W:{self.width}, H:{self.height})"


class Stack:
    def __init__(self, base_width, max_height):
        self.base_width = base_width
        self.remaining_height = max_height
        self.games = []

    def can_fit(self, game):
        return game.width <= self.base_width and game.height <= self.remaining_height

    def add_game(self, game):
        self.games.append(game)
        self.remaining_height -= game.height

    def __repr__(self):
        return f"Stack(base_width={self.base_width}, remaining_height={self.remaining_height})"


class Shelf:
    def __init__(self, max_length, max_height):
        self.max_length = max_length
        self.max_height = max_height
        self.remaining_length = max_length
        self.stacks = []

    def can_start_new_stack(self, game):
        return game.width <= self.remaining_length

    def start_new_stack(self, game):
        stack = Stack(game.width, self.max_height)
        stack.add_game(game)
        self.stacks.append(stack)
        self.remaining_length -= game.width

    def __repr__(self):
        return f"Shelf(remaining_length={self.remaining_length})"