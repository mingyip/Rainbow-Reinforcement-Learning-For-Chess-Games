import random
import numpy as np

from game.agent import AgentBase
from game.gameplay.environment import Environment


class GreedyAgent(AgentBase):
    """ Represents a Snake agent that takes a random action at every step. """

    def __init__(self, env):
        self.env = env
        self.name = "Greedy"

    def act(self):
        flip_num = self.env.num_disks_can_filp(self.env.turn)
        max_flips_index = np.argwhere(flip_num == flip_num.max())
        return max_flips_index[np.random.randint(len(max_flips_index))]

    def end_episode(self):
        pass
