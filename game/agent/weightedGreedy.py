import random
import numpy as np

from game.agent import AgentBase
from game.gameplay.environment import Environment


class WeightedGreedyAgent(AgentBase):
    """ Represents a Snake agent that takes a random action at every step. """

    def __init__(self, env):
        self.env = env
        self.name = "Weighted"

    def act(self):
        scores = self.env.weighted_score_after_next_steps(self.env.turn)
        moves = np.argwhere(scores == scores.max())
        move = moves[np.random.randint(len(moves))]
        return move

    def end_episode(self):
        pass
