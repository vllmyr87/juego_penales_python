import math
import os
import random

import pygame

pygame.init()

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "Assets")
os.makedirs(ASSETS_DIR, exist_ok=True)
random.seed(403)


def save(surface, name):
    pygame.image.save(surface, os.path.join(ASSETS_DIR, name))


def stadium():
    image = pygame.Surface((800, 600))
    for y in range(600):
        t = y / 600
        color = (35 + int(35 * t), 100 + int(35 * t), 160 + int(45 * t))
        pygame.draw.line(image, color, (0, y), (800, y))

    pygame.draw.rect(image, (24, 29, 43), (0, 40, 800, 245))
    pygame.draw.rect(image, (230, 238, 242), (0, 38, 800, 7))
    rows = [(62, 26), (95, 30), (132, 34), (173, 38), (218, 42)]
    colors = [(235, 72, 70), (245, 191, 55), (73, 169, 108), (67, 135, 207), (231, 231, 220)]
    for row, spacing in rows:
        pygame.draw.rect(image, (43, 48, 62), (0, row + 17, 800, 8))
        for x in range(-10, 810, spacing):
            head_color = random.choice(colors)
            pygame.draw.circle(image, (238, 190, 145), (x + random.randint(-4, 4), row), 6)
            pygame.draw.rect(image, head_color, (x - 8, row + 6, 16, 15), border_radius=4)
            if random.random() > 0.55:
                pygame.draw.line(image, (245, 245, 245), (x - 10, row + 12), (x - 17, row + 4), 3)
                pygame.draw.line(image, (245, 245, 245), (x + 10, row + 12), (x + 17, row + 4), 3)
    pygame.draw.rect(image, (13, 17, 28), (0, 265, 800, 24))
    save(image, "stadium.png")


def pitch():
    image = pygame.Surface((800, 600), pygame.SRCALPHA)
    for y in range(270, 600):
        depth = (y - 270) / 330
        base = (30 + int(15 * depth), 112 + int(48 * depth), 52 + int(15 * depth), 255)
        pygame.draw.line(image, base, (0, y), (800, y))
    for y in range(285, 600, 34):
        pygame.draw.line(image, (116, 178, 75, 34), (0, y), (800, y), 14)
    for _ in range(850):
        x = random.randrange(800)
        y = random.randrange(286, 600)
        color = random.choice([(28, 100, 46, 90), (155, 205, 92, 70), (210, 225, 120, 45)])
        pygame.draw.line(image, color, (x, y), (x + random.randint(-2, 2), y - random.randint(2, 6)), 1)
    pygame.draw.line(image, (235, 242, 226, 220), (50, 280), (750, 280), 4)
    pygame.draw.line(image, (235, 242, 226, 220), (250, 280), (250, 430), 3)
    pygame.draw.line(image, (235, 242, 226, 220), (550, 280), (550, 430), 3)
    pygame.draw.arc(image, (235, 242, 226, 220), (340, 280, 120, 120), math.pi, 2 * math.pi, 3)
    save(image, "pitch.png")


def goal():
    image = pygame.Surface((540, 260), pygame.SRCALPHA)
    net = (150, 160, 166, 150)
    for x in range(10, 531, 25):
        pygame.draw.line(image, net, (x, 17), (x - 22, 245), 2)
    for y in range(20, 250, 24):
        pygame.draw.line(image, net, (8, y), (530, y + 2), 2)
    pygame.draw.line(image, (255, 255, 250), (9, 17), (531, 17), 10)
    pygame.draw.line(image, (255, 255, 250), (9, 17), (9, 248), 10)
    pygame.draw.line(image, (255, 255, 250), (531, 17), (531, 248), 10)
    pygame.draw.line(image, (203, 210, 211), (15, 24), (15, 248), 3)
    pygame.draw.line(image, (203, 210, 211), (537, 24), (537, 248), 3)
    pygame.draw.line(image, (255, 255, 250), (9, 248), (531, 248), 10)
    save(image, "goal.png")


def goalkeeper():
    image = pygame.Surface((170, 220), pygame.SRCALPHA)
    shadow = pygame.Surface((110, 24), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0, 0, 0, 90), shadow.get_rect())
    image.blit(shadow, (30, 190))
    skin = (190, 116, 78)
    dark_skin = (125, 68, 47)
    jersey = (31, 91, 173)
    jersey_light = (63, 139, 221)
    shorts = (22, 42, 83)
    pygame.draw.polygon(image, (18, 30, 48), [(59, 166), (78, 165), (70, 210), (54, 210)])
    pygame.draw.polygon(image, (18, 30, 48), [(91, 165), (110, 168), (121, 210), (105, 210)])
    pygame.draw.ellipse(image, (239, 240, 229), (44, 202, 30, 12))
    pygame.draw.ellipse(image, (239, 240, 229), (104, 202, 32, 12))
    pygame.draw.polygon(image, shorts, [(48, 118), (115, 118), (111, 166), (79, 160), (57, 166)])
    pygame.draw.polygon(image, jersey, [(49, 62), (112, 62), (126, 132), (38, 132)])
    pygame.draw.polygon(image, jersey_light, [(49, 62), (63, 65), (57, 128), (38, 132)])
    pygame.draw.line(image, (235, 235, 222), (80, 66), (80, 126), 4)
    pygame.draw.circle(image, skin, (80, 45), 27)
    pygame.draw.polygon(image, (35, 24, 22), [(53, 43), (57, 17), (83, 8), (108, 25), (105, 47), (94, 29), (73, 29)])
    pygame.draw.line(image, dark_skin, (66, 50), (75, 53), 2)
    pygame.draw.circle(image, (24, 22, 23), (70, 43), 3)
    pygame.draw.circle(image, (24, 22, 23), (91, 43), 3)
    pygame.draw.polygon(image, skin, [(48, 71), (27, 98), (13, 82), (7, 91), (29, 119), (61, 101)])
    pygame.draw.polygon(image, skin, [(112, 71), (137, 96), (155, 79), (163, 89), (137, 119), (101, 100)])
    pygame.draw.ellipse(image, (232, 88, 54), (3, 77, 27, 24))
    pygame.draw.ellipse(image, (232, 88, 54), (144, 77, 27, 24))
    pygame.draw.line(image, (249, 210, 158), (10, 82), (20, 91), 2)
    pygame.draw.line(image, (249, 210, 158), (160, 82), (150, 91), 2)
    save(image, "goalkeeper.png")


def ball():
    image = pygame.Surface((80, 80), pygame.SRCALPHA)
    for radius in range(31, 0, -1):
        shade = max(80, 248 - (31 - radius) * 5)
        pygame.draw.circle(image, (shade, shade, min(255, shade + 4), 255), (40, 40), radius)
    pygame.draw.circle(image, (38, 43, 48), (40, 40), 31, 2)
    center = [(40, 28), (29, 36), (33, 50), (48, 53), (55, 39)]
    pygame.draw.polygon(image, (38, 43, 48), center)
    for point in center:
        pygame.draw.line(image, (38, 43, 48), (40, 40), point, 2)
    pygame.draw.circle(image, (255, 255, 255, 155), (29, 25), 7)
    save(image, "ball.png")


stadium()
pitch()
goal()
goalkeeper()
ball()
pygame.quit()
