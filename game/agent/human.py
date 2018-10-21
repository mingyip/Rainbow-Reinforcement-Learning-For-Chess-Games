from game.agent import AgentBase


class HumanAgent(AgentBase):
    """ Represents an agent that is operated by a human """

    def __init__(self):
        self.name = "Human"

    def begin_episode(self):
        pass

    def act(self, observation, reward):
        pass

    def end_episode(self):
        pass
