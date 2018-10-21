import random
import time
import os

import numpy as np
from copy import deepcopy
from enum import Enum

from config import EnvConfig


class Environment(object):
    """
    Represents the enivronment for the Reversi game that implements the
    game logic.
    """

    GRID_NUM = EnvConfig.DIMENSION_OF_GRID
    WEIGHTS = EnvConfig.GRID_WEIGHT_8x8
    DIRECTION = [[-1, 0], [-1, 1], [1, 1], [0, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]

    def __init__(self, output=".", verbose=1):
        """
        Create a new Reversi environment.
        """
        self.verbose = verbose
        self.field = np.zeros(shape=(self.GRID_NUM, self.GRID_NUM))
        self.sequence = []
        self.turn = Player.BLACK
        self.start = Player.BLACK
        self.new_episode()
        self.black_score = 0
        self.white_score = 0
        self.turn_count = 0

    def seed(self, value=42):
        """ 
        Initialize the random state of the environment to make result
        repoducible.
        """
        random.seed(value)
        np.random.seed(value)

    def last_move(self):
        if self.sequence is None:
            return None
        return self.sequence[-1]

    @property
    def observation_shape(self):
        # return self.field.size, self.field.size
        pass

    @property
    def num_actions(self):
        """ Get the number of actions the agent can take. """
        # return len(ALL_SNAKE_ACTION)
        pass

    def __is_opponent_in_valid_direction(self, row, col, direction, player, field=None):
        """ check if any valid opponent's disk on the path """
        if field is None:
            field = self.field
        x = row + direction[0]
        y = col + direction[1]

        # The first adjacent disk has to be an opponent's disk
        if self.not_in_grid(x, y) or not self.is_holded_by_opponent(player, x, y, field):
            return False

        # True if there is a same color disk placed at the end of the path
        while True:
            x += direction[0]
            y += direction[1]
            if self.not_in_grid(x, y) or self.is_grid_free(x, y, field):
                return False
            if self.is_holded_by_player(player, x, y, field):
                return True

    def __flip_disks(self, row, col, player, field=None):
        """
        Flip all opponent's disks
        1. Check all directions, if it is a valid filp,
        2. place the new disk
        3. Flip all disks in the path
        4. Until we find a disk is holded by player
        """
        if field is None:
            field = self.field

        field[row][col] = int(player.value)
        for direction in self.DIRECTION:
            x = row
            y = col

            if not self.__is_opponent_in_valid_direction(x, y, direction, player):
                continue

            while True:
                x += direction[0]
                y += direction[1]

                if self.is_holded_by_player(player, x, y):
                    break

                self.__flip_disk(x, y, field)

        return field

    def liberty_after_next_steps(self, current_player, target):
        """ return the numbers of liberty of next steps """
        liberty = np.zeros(shape=(self.GRID_NUM, self.GRID_NUM))
        moves = self.possible_moves(current_player)
        for move in moves:
            field = deepcopy(self.field)
            field = self.__flip_disks(move[0], move[1], current_player, field)
            liberty[move[0]][move[1]] = len(self.possible_moves(target, field, True))
        return liberty

    def weighted_score_after_next_steps(self, player):
        """ return the total of weighted score """
        scores = np.zeros(shape=(self.GRID_NUM, self.GRID_NUM))
        moves = self.possible_moves(player)
        for move in moves:
            score = 0
            field = deepcopy(self.field)
            field = self.__flip_disks(move[0], move[1], player, field)

            for col in range(self.GRID_NUM):
                for row in range(self.GRID_NUM):
                    if Player(field[row][col]) == player:
                        score += self.WEIGHTS[row][col]
                    elif Player(field[row][col]) == self.getOpponent(player):
                        score -= self.WEIGHTS[row][col]
            scores[move[0]][move[1]] = score + 1000
        return scores

    def num_disks_can_filp(self, player, field=None):
        """ return the numbers of disks can be filpped """
        if field is None:
            field = self.field
        flip_num = np.zeros(shape=(self.GRID_NUM, self.GRID_NUM))

        for row in range(self.GRID_NUM):
            for col in range(self.GRID_NUM):
                for direction in self.DIRECTION:
                    x = row
                    y = col

                    if not self.is_grid_free(x, y, field):
                        continue

                    if not self.__is_opponent_in_valid_direction(x, y, direction, player):
                        continue

                    while True:
                        x += direction[0]
                        y += direction[1]

                        if self.is_holded_by_player(player, x, y):
                            break

                        flip_num[row][col] += 1

        return flip_num

    def __flip_disk(self, row, col, field):
        """ flip one disk to opposite color """
        field[row][col] = self.getOpponent(Player(self.field[row][col])).value

    def is_grid_free(self, row, col, field=None):
        """ check if a grid is available """
        if field is None:
            field = self.field
        return Player(field[row][col]) == Player.NONE

    def is_holded_by_player(self, player, row, col, field=None):
        """ check if a grid is holded by a single player """
        if field is None:
            field = self.field
        return player == Player(field[row][col])

    def is_holded_by_opponent(self, player, row, col, field=None):
        """ check if a grid is holded by the opponent player """
        if field is None:
            field = self.field
        return self.getOpponent(player) == Player(field[row][col])

    def not_in_grid(self, row, col):
        """ Check if a coordinate is outside the checkboard """
        return row < 0 or col < 0 or row >= self.GRID_NUM or col >= self.GRID_NUM

    def isValidMove(self, row, col, player, field=None):
        """ Check if a move is valid """
        if field is None:
            field = self.field
        if self.not_in_grid(row, col) or not self.is_grid_free(row, col, field):
            return False

        for direction in self.DIRECTION:
            if self.__is_opponent_in_valid_direction(row, col, direction, player, field):
                return True

        return False

    def possible_moves(self, player, field=None, verbose=False):
        """ Get all possible of actions the agent can take. """
        if field is None:
            field = self.field
        tiles = []
        size = self.GRID_NUM

        for row in range(size):
            for col in range(size):
                if self.isValidMove(row, col, player, field):
                    tiles.append([row, col])

        return tiles

    def place_a_disk(self, row, col):
        """ place a disk on the checkboard """
        if not self.isValidMove(row, col, self.turn):
            return Event.NOT_VALID_MOVE

        self.__flip_disks(row, col, self.turn, self.field)
        self.turn_count += 1
        self.sequence.append((row, col))

        if self.is_end_game():
            if self.winning_player() == Player.BLACK:
                self.black_score += 1
            elif self.winning_player() == Player.WHITE:
                self.white_score += 1
            return Event.END_GAME

        if self.no_possible_moves(self.getOpponent(self.turn)):
            return Event.NO_POSSIBLE_MOVES
        self.turn = self.getOpponent(self.turn)

        return Event.PLACEMENT_SUCCESS

    def no_possible_moves(self, player):
        """ Check if player has possible moves """
        return not self.possible_moves(player)

    def winning_player(self):
        """ Return the winning_player """
        if self.num_black_disks() > self.num_white_disks():
            return Player.BLACK
        elif self.num_black_disks() < self.num_white_disks():
            return Player.WHITE
        else:
            return Player.NONE

    def is_end_game(self):
        """ Check if no possible moves for both players """
        return not self.possible_moves(Player.BLACK) and \
                not self.possible_moves(Player.WHITE)

    def new_episode(self):
        """ Reset the environment and begin a new episode. """
        size = self.GRID_NUM
        self.turn_count = 0
        self.sequence = []

        # init first four disks
        self.field = np.zeros(shape=(size, size))
        self.field[size // 2][size // 2] = Player.WHITE.value
        self.field[size // 2 - 1][size // 2 - 1] = Player.WHITE.value
        self.field[size // 2 - 1][size // 2] = Player.BLACK.value
        self.field[size // 2][size // 2 - 1] = Player.BLACK.value

        self.turn = self.getOpponent(self.start)
        self.start = self.getOpponent(self.start)

        return Event.NONE

    def isBlackTurn(self):
        """ Check if the current turn is black's turn """
        return Player.BLACK == self.turn

    def num_white_disks(self):
        """ Return number of white disks on field """
        return np.count_nonzero(self.field == int(Player.WHITE.value))

    def num_black_disks(self):
        """ Return number of black disks on field """
        return np.count_nonzero(self.field == int(Player.BLACK.value))

    def getOpponent(self, player=None):
        """ Return an enum to indicate player's opponent """
        if player is None:
            player = self.turn
        return Player(player.value % 2 + 1)

    def isWhite(self, row, col):
        """ Check if a disk is white """
        return Player(self.field[row][col]) == Player.WHITE

    def isBlack(self, row, col):
        """ Check if a disk is black """
        return Player(self.field[row][col]) == Player.BLACK

    def printField(self, field=None):
        """ Print checkerboard info in console log """
        if field is None:
            field = self.field
        for col in range(self.GRID_NUM):
            for row in range(self.GRID_NUM):
                print(f"{int(field[row][col])} ", end="")
            print()

    def printFlipNum(self, player):
        """ Print num of disks can be flipped info in console log """
        flip_num = self.num_disks_can_filp(player)
        for col in range(self.GRID_NUM):
            for row in range(self.GRID_NUM):
                print(f"{int(flip_num[row][col])} ", end="")
            print()
        print()

    def record_timestep_stats(self, result):
        """ Record environment statistics """
        pass

    def get_observation(self):
        """ Observe the state of the environment. """
        pass


class Player(Enum):
    NONE = 0
    WHITE = 1
    BLACK = 2


class Event(Enum):
    NONE = 0,
    PLACEMENT_SUCCESS = 1,
    NOT_VALID_MOVE = 2,
    NO_POSSIBLE_MOVES = 3,
    END_GAME = 4,
    END_GAME_VIEW = 5,
    START_NEW_GAME = 6

    @staticmethod
    def next(stage):
        return {
            Event.NO_POSSIBLE_MOVES: Event.NONE,
            Event.END_GAME: Event.END_GAME_VIEW,
            Event.END_GAME_VIEW: Event.START_NEW_GAME,
            Event.START_NEW_GAME: Event.NONE
        }.get(stage, Event.NONE)

    @staticmethod
    def is_valid_placement_stage(stage):
        return stage == Event.NONE or \
                stage == Event.PLACEMENT_SUCCESS or \
                stage == Event.NOT_VALID_MOVE or \
                stage == Event.START_NEW_GAME
