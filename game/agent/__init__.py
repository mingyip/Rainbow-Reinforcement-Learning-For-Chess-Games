class AgentBase(object):
    """ Represesnts an intelligent angent for the snake environment. """

    def begin_episode(self):
        """ Reset the agent for a new episode. """
        pass

    def act(self, observation, reward):
        return None

    def end_episode(self):
        pass


from .human import HumanAgent
from .random import RandomAgent
from .greedy import GreedyAgent
from .weightedGreedy import WeightedGreedyAgent
