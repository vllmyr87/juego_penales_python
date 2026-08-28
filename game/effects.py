import random

import pygame

from .config import CONFETTI_COLORS, WIDTH


def create_confetti():
    return [
        {
            "x": random.randint(0, WIDTH),
            "y": random.randint(-600, -50),
            "color": random.choice(CONFETTI_COLORS),
            "sy": random.uniform(4, 10),
            "sx": random.uniform(-3, 3),
            "size": random.randint(8, 15),
        }
        for _ in range(200)
    ]


def update_and_draw_confetti(surface, particles):
    for particle in particles:
        particle["y"] += particle["sy"]
        particle["x"] += particle["sx"]
        particle["sx"] += random.uniform(-0.5, 0.5)
        particle["sx"] = max(-3, min(3, particle["sx"]))
        pygame.draw.rect(
            surface,
            particle["color"],
            (particle["x"], particle["y"], particle["size"], particle["size"]),
        )
