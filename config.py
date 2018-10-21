class EnvConfig:
    DIMENSION_OF_GRID = 8
    GRID_WEIGHT_8x8 = [
        [120, -20, 20, 5, 5, 20, -20, 120],
        [-20, -40, -5, -5, -5, -5, -40, -20],
        [20, -5, 15, 3, 3, 15, -5, 20],
        [5, -5, 3, 3, 3, 3, -5, 5],
        [5, -5, 3, 3, 3, 3, -5, 5],
        [20, -5, 15, 3, 3, 15, -5, 20],
        [-20, -40, -5, -5, -5, -5, -40, -20],
        [120, -20, 20, 5, 5, 20, -20, 120]
    ]


class GUIConfig:
    CELL_MARGIN = 4
    FPS_LIMIT = 60
    CELL_WIDTH = 33
    PANEL_HEIGHT = 20
    TIMESTEP_DELAY = 100
    END_GAME_DELAY = 100
    END_GAME_VIEW_DELAY = 10

    # VERSION = 1.06
    # MEMORY_SIZE = 100000
    # NUM_LAST_FRAMES = 4
    # LEVEL = "snakeai/levels/10x10-blank.json"
    # NUM_EPISODES = -1
    # BATCH_SIZE = 64
    # DISCOUNT_FACTOR = 0.95
    # USE_PRETRAINED_MODEL = False
    # PRETRAINED_MODEL = "dqn-00000000.model"
    # # Either sarsa, dqn, ddqn
    # LEARNING_METHOD = "dqn"
    # MULTI_STEP_REWARD = False
    # MULTI_STEP_SIZE = 5
    # PRIORITIZED_REPLAY = False
    # PRIORITIZED_RATING = 1
    # DUEL_NETWORK = False
    # #foodspeed =0 no movement. foodspeed =2 food moves one step every 2 timesteps
    # FOODSPEED = 0
