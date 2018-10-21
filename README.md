# Rainbow Reinforcement Learning
A simple implementation of Rainbow reinforcement learning to improve the learning performance of DL agents. 
This project basically follows the idea of the paper 
Rainbow: Combining Improvements in Deep Reinforcement Learning [[arxiv]](https://arxiv.org/pdf/1710.02298.pdf)

<p align="center">
  <img src="https://raw.githubusercontent.com/mingyip/Rainbow-Reinforcement-Learning-For-Chess-Games/master/demo.gif" width="200px">
</p>

## Requirements
The environment is run in python 3.6

## Getting Started
To start a reversi game, run:
```
$ python play.py
```

In default setting, two A.I agents have been set to play against each other. You may select agents and/or human players to be player1 and player2. 
```
  --interface {cli,gui}
      Interface mode (command-line or GUI).
                        
  --agent1 {human,random,greedy,weighted}
      Agent1 to use.
                        
  --agent2 {human,random,greedy,weighted}
      Agent2 to use.
                        
  --num-episodes NUM_EPISODES
      The number of episodes to run consecutively.
```
