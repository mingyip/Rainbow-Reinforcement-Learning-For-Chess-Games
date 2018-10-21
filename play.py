#!/usr/bin/env python3.6

""" Front-end script for Reversi game. """

import json
import sys
import numpy as np
import pygame
import argparse

from game.gameplay.environment import Environment
from game.gameplay.pyGameGUI import PyGameGUI
from game.gameplay.environment import Player
from game.agent import HumanAgent, RandomAgent, GreedyAgent, WeightedGreedyAgent


def parse_command_line_args(args):
    """ Parse command-line arguments and organize them into a single structured object. """

    parser = argparse.ArgumentParser(description='A Reinforcement Chess Game Ai.')
    # parser = HelpOnFailArgumentParser(
    #     description='',
    #     epilog='Example: play.py --agent dqn --model dqn-final.model --level 10x10.json'
    # )

    parser.add_argument(
        '--interface',
        type=str,
        choices=['cli', 'gui'],
        default='gui',
        help='Interface mode (command-line or GUI).',
    )
    parser.add_argument(
        '--agent1',
        type=str,
        choices=['human', 'random', 'greedy', 'weighted'],
        default='weighted',
        help='Agent1 to use.',
    )
    parser.add_argument(
        '--agent2',
        type=str,
        choices=['human', 'random', 'greedy', 'weighted'],
        default='weighted',
        help='Agent2 to use.',
    )
    parser.add_argument(
        '--num-episodes',
        type=int,
        default=100,
        help='The number of episodes to run consecutively.',
    )

    return parser.parse_args(args)


def create_agent(name, env):
    """
    Create a specific type of Snake AI agent.
    Returns:
        An instance of Ai agent.
    """
    if name == 'human':
        return HumanAgent()
    if name == 'random':
        return RandomAgent(env)
    if name == 'greedy':
        return GreedyAgent(env)
    if name == 'weighted':
        return WeightedGreedyAgent(env)

    raise KeyError(f'Unknown agent type: "{name}"')


def play_gui(interface, agent1, agent2, num_episodes):
    env = Environment()
    agents = {}
    agents[Player.BLACK] = create_agent(agent1, env)
    agents[Player.WHITE] = create_agent(agent2, env)

    gui = PyGameGUI(env, agents)
    gui.run(num_episodes=num_episodes)


def main():
    args = parse_command_line_args(sys.argv[1:])
    play_gui(args.interface, args.agent1, args.agent2, args.num_episodes)

if __name__ == '__main__':
    main()
