# -*- coding: utf-8 -*-
"""
Langton's Ant Student Template Module.
"""
import numpy as np


def rules_from_string(rule_str):
    """
    Convenience helper: builds a rules dict from a compact ruleset string
    like 'RL' (classic ant), 'LLRR', 'LRRRRRLLR', etc.

    Each character in the string is the turn direction ('L' or 'R') taken
    when the ant is on a square of that character's index-color. Colors
    cycle in order: 0 -> 1 -> 2 -> ... -> len(rule_str)-1 -> 0.

    Args:
        rule_str (str): sequence of 'L'/'R' characters, one per color.

    Returns:
        dict: {current_color: (next_color, turn_direction)}
    """
    n_colors = len(rule_str)
    rules = {}
    for color, turn in enumerate(rule_str):
        if turn not in ('L', 'R'):
            raise ValueError(f"Invalid turn character '{turn}' in ruleset")
        next_color = (color + 1) % n_colors
        rules[color] = (next_color, turn)
    return rules


class LangtonsAnt:
    """
    Implements Langton's Ant / generalized "turmite" cellular automaton.

    Core rule (classic, 2-color):
      - On a white square: toggle color, turn clockwise ('R'), move forward.
      - On a black square: toggle color, turn counter-clockwise ('L'), move forward.

    Generalized to N colors via a rules dict:
      {current_color: (next_color, turn_direction)}
    """

    # Clockwise order of headings: Up, Right, Down, Left
    DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    DIRECTION_NAMES = ['UP', 'RIGHT', 'DOWN', 'LEFT']

    def __init__(self, N, ant_position, rules):
        """
        Initialize the Langton's Ant simulation.

        Args:
            N (int): The grid size (NxN).
            ant_position (tuple): Starting coordinate of the ant as (r, c).
            rules (dict): {current_color: (next_color, turn_direction)}
        """
        self.N = N
        self.grid = np.zeros((N, N), dtype=int)
        self.position = (ant_position[0] % N, ant_position[1] % N)
        self.rules = rules
        self.direction = 0  # start facing Up

    def get_states(self):
        """
        Returns the current state grid of the cells.

        Returns:
            np.ndarray: The NxN cellular grid.
        """
        return self.grid

    def get_current_position(self):
        """
        Returns the ant's current position as a tuple (r, c).

        Returns:
            tuple: Current coordinates of the ant.
        """
        return self.position

    def get_current_direction(self):
        """
        Returns the ant's current heading as a string, e.g. 'UP'.
        """
        return self.DIRECTION_NAMES[self.direction]

    def step(self):
        """
        Perform a single simulation step following the ruleset:
          1. Look up the color of the current cell.
          2. Toggle it to next_color per the rules.
          3. Turn left or right accordingly.
          4. Move forward one unit, wrapping toroidally.
        """
        r, c = self.position
        current_color = self.grid[r, c]

        if current_color not in self.rules:
            raise KeyError(
                f"No rule defined for color {current_color} at {self.position}"
            )

        next_color, turn = self.rules[current_color]
        self.grid[r, c] = next_color

        if turn == 'R':
            self.direction = (self.direction + 1) % 4
        elif turn == 'L':
            self.direction = (self.direction - 1) % 4
        else:
            raise ValueError(f"Unknown turn direction: {turn}")

        dr, dc = self.DIRECTIONS[self.direction]
        self.position = ((r + dr) % self.N, (c + dc) % self.N)

    def update(self):
        """
        Alias for step() to support standard animation.
        """
        self.step()