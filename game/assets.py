import os

import pygame

from .config import ASSETS_DIR


def load_assets():
    def load(name):
        return pygame.image.load(os.path.join(ASSETS_DIR, name)).convert_alpha()

    return {
        "stadium": load("stadium.png"),
        "pitch": load("pitch.png"),
        "goal": load("goal.png"),
        "goalkeeper": load("goalkeeper.png"),
        "ball": load("ball.png"),
    }
