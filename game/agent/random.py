import random
import numpy as np

from game.agent import AgentBase
from game.gameplay.environment import Environment


class RandomAgent(AgentBase):
    """ Represents a Snake agent that takes a random action at every step. """

    def __init__(self, env):
        self.env = env
        self.name = "Random"

    def act(self):
        moves = self.env.possible_moves(self.env.turn)
        if not moves:
            return (-1, -1)
        return moves[np.random.randint(len(moves))]

    def end_episode(self):
        pass
