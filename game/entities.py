import math

import pygame

from .config import WIDTH


class Goal:
    def __init__(self):
        self.rect = pygame.Rect(150, 80, 500, 200)

    def draw(self, surface, assets):
        surface.blit(assets["goal"], (130, 60))


class Goalkeeper:
    def __init__(self, level):
        self.width = 100 + (level * 8)
        self.height = 90
        self.x = WIDTH // 2 - self.width // 2
        self.y = 190
        self.speed = 6 + (level * 3.5)
        self.direction = 1
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.x += self.speed * self.direction
        if self.x <= 150 or self.x + self.width >= 650:
            self.direction *= -1
        self.rect.x = self.x

    def draw(self, surface, assets):
        display_size = (self.width + 70, 190)
        image = pygame.transform.smoothscale(assets["goalkeeper"], display_size)
        surface.blit(image, (self.rect.centerx - display_size[0] // 2, 105))


class Ball:
    def __init__(self):
        self.radius = 18
        self.start_x = WIDTH // 2
        self.start_y = 520
        self.x = self.start_x
        self.y = self.start_y
        self.is_moving = False
        self.target_x = 0
        self.target_y = 0
        self.speed = 22
        self.rotation = 0
        self.trail = []

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.is_moving = False
        self.rotation = 0
        self.trail.clear()

    def shoot(self, target_x, target_y):
        if not self.is_moving:
            self.target_x = target_x
            self.target_y = target_y
            self.is_moving = True
            self.trail.clear()

    def move(self):
        if not self.is_moving:
            return False
        delta_x = self.target_x - self.x
        delta_y = self.target_y - self.y
        distance = math.hypot(delta_x, delta_y)
        self.rotation += 15
        self.trail.append((self.x, self.y))
        if len(self.trail) > 7:
            self.trail.pop(0)
        if distance < self.speed:
            self.x = self.target_x
            self.y = self.target_y
            return True
        self.x += (delta_x / distance) * self.speed
        self.y += (delta_y / distance) * self.speed
        return False

    def draw(self, surface, assets):
        for index, (trail_x, trail_y) in enumerate(self.trail):
            alpha = 20 + index * 8
            trail_surface = pygame.Surface((48, 48), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, (255, 255, 255, alpha), (24, 24), 8 + index)
            surface.blit(trail_surface, (trail_x - 24, trail_y - 24))
        image = pygame.transform.rotozoom(assets["ball"], self.rotation, 0.62)
        surface.blit(image, image.get_rect(center=(int(self.x), int(self.y))))
