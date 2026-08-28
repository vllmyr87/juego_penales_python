import pygame

from database.database import GameDatabase

from .assets import load_assets
from .config import FPS, HEIGHT, WHITE, WIDTH
from .effects import create_confetti, update_and_draw_confetti
from .entities import Ball, Goal, Goalkeeper
from .ui import draw_medal, draw_message, draw_ranking


class PenaltyGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Juego de Penales - Edición Festejo")
        self.assets = load_assets()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 40, bold=True)
        self.large_font = pygame.font.SysFont("arial", 60, bold=True)
        self.small_font = pygame.font.SysFont("arial", 20, bold=True)
        self.table_font = pygame.font.SysFont("arial", 17, bold=True)
        self.database = GameDatabase()
        self.goal = Goal()
        self.goalkeeper = Goalkeeper(1)
        self.ball = Ball()
        self.current_level = 1
        self.max_shots_per_level = 5
        self.shots_taken = 0
        self.level_goals = 0
        self.goals_to_pass = 3
        self.earned_medals = []
        self.state = "PLAYING"
        self.message = "Nivel 1 - ¡Gana tu medalla!"
        self.result_timer = 0
        self.celebration_timer = 0
        self.confetti = []

    def draw_background(self):
        self.screen.blit(self.assets["stadium"], (0, 0))
        self.screen.blit(self.assets["pitch"], (0, 0))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type != pygame.MOUSEBUTTONDOWN:
                continue
            if self.state == "PLAYING" and not self.ball.is_moving:
                self.ball.shoot(*pygame.mouse.get_pos())
                self.shots_taken += 1
                self.message = ""
            elif self.state == "LEVEL_END":
                if self.level_goals >= self.goals_to_pass:
                    self.current_level += 1
                self.shots_taken = 0
                self.level_goals = 0
                self.goalkeeper = Goalkeeper(self.current_level)
                self.state = "PLAYING"
                self.message = f"Nivel {self.current_level} - ¡Comienza!"
        return True

    def update(self):
        if self.state == "PLAYING":
            self.goalkeeper.move()
            if self.ball.move():
                hitbox = pygame.Rect(
                    self.goalkeeper.rect.x - 25,
                    self.goalkeeper.rect.y - 25,
                    self.goalkeeper.width + 50,
                    self.goalkeeper.height + 30,
                )
                ball_rect = pygame.Rect(
                    self.ball.x - self.ball.radius,
                    self.ball.y - self.ball.radius,
                    self.ball.radius * 2,
                    self.ball.radius * 2,
                )
                if ball_rect.colliderect(hitbox):
                    self.message = "¡ATAJADÓN!"
                elif self.goal.rect.collidepoint(self.ball.target_x, self.ball.target_y):
                    self.message = "¡GOLAZO!"
                    self.level_goals += 1
                else:
                    self.message = "¡AFUERA!"
                self.database.register_shot(self.message == "¡GOLAZO!", self.current_level)
                self.state = "RESULT"
                self.result_timer = pygame.time.get_ticks()
        elif self.state == "RESULT":
            if pygame.time.get_ticks() - self.result_timer > 1500:
                self.ball.reset()
                if self.shots_taken >= self.max_shots_per_level:
                    if self.level_goals >= self.goals_to_pass:
                        self.state = "CELEBRATING"
                        self.confetti = create_confetti()
                        self.celebration_timer = pygame.time.get_ticks()
                        if self.current_level not in self.earned_medals:
                            self.earned_medals.append(self.current_level)
                            self.database.register_achievement(self.current_level)
                        self.message = "¡NIVEL SUPERADO! ¡FESTEJO!"
                    else:
                        self.state = "LEVEL_END"
                        self.message = "FIN DEL JUEGO. Clic para reintentar"
                else:
                    self.state = "PLAYING"
                    self.message = f"Tiro {self.shots_taken + 1} de {self.max_shots_per_level}"
        elif self.state == "CELEBRATING":
            if pygame.time.get_ticks() - self.celebration_timer > 3500:
                self.state = "LEVEL_END"
                self.message = "¡Haz clic para el siguiente nivel!"

    def draw(self):
        self.draw_background()
        self.goal.draw(self.screen, self.assets)
        self.goalkeeper.draw(self.screen, self.assets)
        self.ball.draw(self.screen, self.assets)
        for index, medal_level in enumerate(self.earned_medals):
            draw_medal(self.screen, WIDTH - 40 - index * 50, 20, medal_level, self.small_font)
        if self.state == "CELEBRATING":
            update_and_draw_confetti(self.screen, self.confetti)
        draw_ranking(self.screen, self.database, self.table_font)
        hud = self.font.render(
            f"Nivel: {self.current_level} | Goles: {self.level_goals} / {self.max_shots_per_level}",
            True,
            WHITE,
        )
        self.screen.blit(hud, (20, 20))
        draw_message(self.screen, self.message, self.state, self.large_font)
        pygame.display.flip()

    def run(self):
        running = True
        try:
            while running:
                running = self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(FPS)
        finally:
            self.database.close()
            pygame.quit()
