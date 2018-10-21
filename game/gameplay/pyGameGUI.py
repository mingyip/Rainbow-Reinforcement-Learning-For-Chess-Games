import numpy as numpy
import textwrap
import pygame
import pdb
import os

from game.gameplay.environment import Environment, Event, Player
from pygame.draw import polygon as DrawPolygon
from pygame.draw import circle as DrawCircle
from pygame.draw import rect as DrawRect
from game.agent import HumanAgent

from config import GUIConfig


class PyGameGUI:
    """ Provides a Snake GUI powered by Pygame. """
    MARGIN = GUIConfig.CELL_MARGIN
    FPS_LIMIT = GUIConfig.FPS_LIMIT
    CELL_WIDTH = GUIConfig.CELL_WIDTH
    PANEL_HEIGHT = GUIConfig.PANEL_HEIGHT
    TIMESTEP_DELAY = GUIConfig.TIMESTEP_DELAY
    END_GAME_DELAY = GUIConfig.END_GAME_DELAY
    END_GAME_VIEW_DELAY = GUIConfig.END_GAME_VIEW_DELAY

    def __init__(self, env, agents):
        print("pygame init")

        self.env = env
        self.agents = agents
        self.fps_clock = None
        self.event = Event.NONE
        self.choice = (-1, -1)
        self.markerPos = (-1, -1)
        self.timestep_watch = Stopwatch()
        self.width = (self.CELL_WIDTH + self.MARGIN) * self.env.GRID_NUM + self.MARGIN
        self.height = self.width + self.PANEL_HEIGHT

        windowSize = [self.width, self.height]
        ico_img = pygame.image.load("logo.png")
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (500, 250)

        pygame.init()
        pygame.mouse.set_visible(True)
        pygame.display.set_icon(ico_img)
        pygame.display.set_caption("Reversi")
        self.screen = pygame.display.set_mode(windowSize)

    def load_environment(self, env):
        """ Load the Environment agent into the GUI. """
        self.env = env

    def load_agents(self, agents):
        """ Load the RL agent into the GUI. """
        self.agents = agents

    def get_mouse_coordinate(self):
        """ Return mouse grid coordinate """
        pos = pygame.mouse.get_pos()
        mov = pygame.mouse.get_rel()
        row = pos[0] // (self.CELL_WIDTH + self.MARGIN)
        col = (pos[1] - self.PANEL_HEIGHT) // (self.CELL_WIDTH + self.MARGIN)
        if mov != (0, 0) and not self.env.not_in_grid(row, col):
            return (row, col)
        return self.markerPos

    def handle_input_event(self):
        """ handle mouse and keyboard input """

        self.markerPos = self.get_mouse_coordinate()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise QuitRequestedError
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    raise QuitRequestedError
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Event.is_valid_placement_stage(self.event):
                    self.choice = self.get_mouse_coordinate()
                self.event = Event.next(self.event)
                self.timestep_watch.reset()

                liberties = self.env.liberty_after_next_steps(self.env.turn, self.env.getOpponent())
                self.env.printField(liberties)
                print()
                # self.env.printFlipNum(self.env.turn)
                # print(self.env.update_num_disks_can_filp(self.choice[0], self.choice[1], self.env.turn))

            # print("Click ", pos, "coordinates: ", row, col)

    def render_panel(self):
        """ Draw game info at the top """
        size = self.env.GRID_NUM
        panel = self.PANEL_HEIGHT
        margin = self.MARGIN
        screen = self.screen
        cellWidth = self.CELL_WIDTH

        radius = (panel - 2 * margin) // 2
        x_left = margin
        x_right = (cellWidth + margin) * (self.env.GRID_NUM // 2) + margin
        y = margin
        w = (cellWidth + margin) * (self.env.GRID_NUM // 2) - margin
        h = panel - margin
        screenWidth = (cellWidth + margin) * size + margin

        DrawRect(screen, Colors.GRAY, [x_left, y, w, h])
        DrawRect(screen, Colors.GRAY, [x_right, y, w, h])
        DrawCircle(screen, Colors.BLACK, (x_left + margin + radius, margin + h // 2), radius)
        DrawCircle(screen, Colors.WHITE, (x_right + margin + radius, margin + h // 2), radius)
        if self.env.isBlackTurn():
            DrawPolygon(screen, Colors.RED, ((margin, margin), (margin + panel // 3, margin), (margin, margin + panel // 3)))
        else:
            DrawPolygon(screen, Colors.RED, ((x_right, margin), (x_right + panel // 3, margin), (x_right, margin + panel // 3)))

        black_disks = self.env.num_black_disks()
        white_disks = self.env.num_white_disks()
        black_score = self.env.black_score
        white_score = self.env.white_score
        black_ai = self.agents[Player.BLACK].name
        white_ai = self.agents[Player.WHITE].name

        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 16)

        text = self.font.render(f'{black_ai} ({black_score}) {black_disks}', False, (255, 255, 255))
        text_rect = text.get_rect(midleft=(x_left + 2 * (margin + radius), panel // 2))
        self.screen.blit(text, text_rect)

        text = self.font.render(f'{white_ai} ({white_score}) {white_disks}', False, (255, 255, 255))
        text_rect = text.get_rect(midleft=(x_right + 2 * (margin + radius), panel // 2))
        self.screen.blit(text, (x_right + 2 * (margin + radius), panel // 2 - 10))

    def render_marker(self, makerPos, color):
        """ Draw a marker on the current focused grid """
        if makerPos is None:
            return

        screen = self.screen
        margin = self.MARGIN
        size = self.CELL_WIDTH
        panel = self.PANEL_HEIGHT

        width = 4
        row = makerPos[0]
        col = makerPos[1]
        length = size // 3
        x = (margin + size) * row + margin
        y = (margin + size) * col + margin + panel

        DrawRect(screen, color, [x, y, length, width])
        DrawRect(screen, color, [x, y, width, length])
        DrawRect(screen, color, [x + size - length, y, length, width])
        DrawRect(screen, color, [x + size - width, y, width, length])
        DrawRect(screen, color, [x, y + size - width, length, width])
        DrawRect(screen, color, [x, y + size - length, width, length])
        DrawRect(screen, color, [x + size - width, y + size - length, width, length])
        DrawRect(screen, color, [x + size - length, y + size - width, length, width])

    def render_possible_moves(self):
        """ Draw markers possible moves on grids """
        for move in self.env.possible_moves(self.env.turn):
            self.render_marker(move, Colors.BLUE)

    def render_cell(self, row, col):
        """ Draw the cell specified by the field coordinates. """
        env = self.env
        size = self.CELL_WIDTH
        panel = self.PANEL_HEIGHT
        margin = self.MARGIN
        screen = self.screen

        radius = (size - 2 * margin) // 2
        cellX = (margin + size) * row + margin
        celly = (margin + size) * col + margin + panel
        diskX = margin + size // 2 + row * (size + margin)
        diskY = margin + size // 2 + col * (size + margin) + panel

        DrawRect(screen, Colors.GREEN, [cellX, celly, size, size])
        if env.isWhite(row, col):
            DrawCircle(screen, Colors.WHITE, (diskX, diskY), radius)
        if env.isBlack(row, col):
            DrawCircle(screen, Colors.BLACK, (diskX, diskY), radius)

    def render_messages(self, msg):
        """ Draw a message on game screen """

        x = self.MARGIN + self.CELL_WIDTH
        y = self.height // 3
        w = self.width - 2 * (self.MARGIN + self.CELL_WIDTH)
        h = self.height // 3

        DrawRect(self.screen, Colors.DARK_BLUE, [x - self.MARGIN, y - self.MARGIN, w + 2 * self.MARGIN, h + 2 * self.MARGIN])
        DrawRect(self.screen, Colors.BLUE, [x, y, w, h])

        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 24)

        text = self.font.render(msg, False, Colors.WHITE)
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text, text_rect)

    def render(self):
        """ Draw the entire game frame. """
        self.screen.fill(Colors.BLACK)
        any_human_agents = isinstance(self.agents[Player.WHITE], HumanAgent) or \
                            isinstance(self.agents[Player.BLACK], HumanAgent)

        for col in range(self.env.GRID_NUM):
            for row in range(self.env.GRID_NUM):
                self.render_cell(row, col)

        self.render_panel()
        self.render_possible_moves()
        if self.env.turn_count > 0:
            self.render_marker(self.env.last_move(), Colors.RED)
        if any_human_agents:
            self.render_marker(self.markerPos, Colors.YELLOW)

        if self.event == Event.NO_POSSIBLE_MOVES:
            self.render_messages("No Possible Moves")

        if self.event == Event.END_GAME:
            if self.env.winning_player() == Player.BLACK:
                msg = "Black wins"
            elif self.env.winning_player() == Player.WHITE:
                msg = "White wins"
            else:
                msg = "Draw"
            self.render_messages(msg)

        self.pygame_clock.tick(60)
        pygame.display.flip()

    def place_a_disk(self):
        """ place a disk on the checkboard """
        if Event.is_valid_placement_stage(self.event):
            self.event = self.env.place_a_disk(self.choice[0], self.choice[1])

    def ai_event(self):
        """ ai picks an action """ 
        self.choice = (-1, -1)
        any_human_agents = isinstance(self.agents[Player.WHITE], HumanAgent) or \
                            isinstance(self.agents[Player.BLACK], HumanAgent)

        if self.timestep_watch.time() >= self.TIMESTEP_DELAY:
            self.timestep_watch.reset()
            if not any_human_agents:
                self.event = Event.next(self.event)
            if Event.is_valid_placement_stage(self.event):
                self.choice = self.agents[self.env.turn].act()

    def run_episode(self):
        """ Run the GUI player for a single episode. """
        self.pygame_clock = pygame.time.Clock()
        while True:
            pygame.event.pump()
            is_human_agent = isinstance(self.agents[self.env.turn], HumanAgent)

            # handle exit event
            self.handle_input_event()

            # pick the next action
            if is_human_agent:
                self.handle_input_event()
            else:
                self.ai_event()
            self.place_a_disk()
            self.render()

            if self.event == Event.END_GAME:
                pygame.time.wait(self.END_GAME_DELAY)

            if self.event == Event.END_GAME_VIEW:
                pygame.time.wait(self.END_GAME_VIEW_DELAY)
                break

    def run(self, num_episodes=1):
        """ Run the GUI player for the specified number of episodes. """
        pygame.display.update()
        self.fps_clock = pygame.time.Clock()

        try:
            for episode in range(num_episodes):
                self.run_episode()
                self.env.new_episode()
                self.event = Event.next(self.event)
        except QuitRequestedError:
            print("Exit Program")

        pygame.quit()        


class Stopwatch(object):
    """ Meaures the time elapse since the last checkpoint. """

    def __init__(self):
        self.start_time = pygame.time.get_ticks()

    def reset(self):
        self.start_time = pygame.time.get_ticks()

    def time(self):
        """ Get time (in milliseconds) since the last checkpoint. """
        return pygame.time.get_ticks() - self.start_time


class Colors:
    SCREEN_BACKGROUND = (170, 204, 153)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 100, 0)
    RED = (225, 34, 34)
    YELLOW = (160, 160, 0)
    BLUE = (95, 158, 160)
    DARK_BLUE = (68, 134, 156)
    GRAY = (64, 64, 64)


class QuitRequestedError(RuntimeError):
    """ Gets raised whenever the user wants to quit the game. """
    pass
