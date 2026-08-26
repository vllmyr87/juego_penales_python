import pygame
import sys
import math
import random
import os

pygame.init()

# Configuraciones de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Penales - Edición Festejo")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
YELLOW = (255, 215, 0)
GRAY = (200, 200, 200)
SKIN_COLOR = (255, 224, 189)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)
CONFETTI_COLORS = [RED, BLUE, YELLOW, WHITE, (255, 105, 180), (0, 255, 255), (50, 205, 50), (255, 165, 0)]

# FPS y Reloj
clock = pygame.time.Clock()
FPS = 60

# Fuentes
font = pygame.font.SysFont("arial", 40, bold=True)
large_font = pygame.font.SysFont("arial", 60, bold=True)
small_font = pygame.font.SysFont("arial", 20, bold=True)

# --- Clases del Juego ---

class Goal:
    def __init__(self):
        self.rect = pygame.Rect(150, 80, 500, 200)
        self.color = WHITE
        self.thickness = 8

    def draw(self, surface):
        # Dibujar red
        for i in range(150, 650, 25):
            pygame.draw.line(surface, GRAY, (i, 80), (i, 280), 2)
        for i in range(80, 280, 25):
            pygame.draw.line(surface, GRAY, (150, i), (650, i), 2)
        # Postes
        pygame.draw.rect(surface, self.color, self.rect, self.thickness)

class Goalkeeper:
    def __init__(self, level):
        self.width = 100 + (level * 8) # Crece con los niveles
        self.height = 90
        self.x = WIDTH // 2 - self.width // 2
        self.y = 190
        self.speed = 6 + (level * 3.5) # Más rápido
        self.direction = 1 
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = BLUE

    def move(self):
        self.x += self.speed * self.direction
        if self.x <= 150 or self.x + self.width >= 650:
            self.direction *= -1
        self.rect.x = self.x

    def draw(self, surface):
        # Cuerpo
        pygame.draw.rect(surface, self.color, self.rect, border_radius=15)
        # Cabeza
        pygame.draw.circle(surface, SKIN_COLOR, (self.rect.centerx, self.rect.y - 20), 25)
        # Pelo
        pygame.draw.arc(surface, BLACK, (self.rect.centerx - 25, self.rect.y - 45, 50, 40), 0, 3.14, 10)
        # Guantes
        pygame.draw.circle(surface, RED, (self.rect.left - 15, self.rect.centery - 10), 22)
        pygame.draw.circle(surface, RED, (self.rect.right + 15, self.rect.centery - 10), 22)

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
        self.speed = 22 # Pelota un poco más rápida para compensar al arquero
        self.rotation = 0

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.is_moving = False
        self.rotation = 0

    def shoot(self, tx, ty):
        if not self.is_moving:
            self.target_x = tx
            self.target_y = ty
            self.is_moving = True

    def move(self):
        if self.is_moving:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.hypot(dx, dy)
            self.rotation += 15 # Simular giro
            
            if distance < self.speed:
                self.x = self.target_x
                self.y = self.target_y
                return True
            else:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
        return False

    def draw(self, surface):
        # Dibujo de pelota con patrón dinámico
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius)
        # Hexágono central rotando
        offset_x = math.cos(math.radians(self.rotation)) * (self.radius // 3)
        offset_y = math.sin(math.radians(self.rotation)) * (self.radius // 3)
        pygame.draw.circle(surface, BLACK, (int(self.x + offset_x), int(self.y + offset_y)), self.radius // 2)
        pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), self.radius, 2)

# --- Funciones de Efectos (Papeles Picados y Medallas) ---
confetti_particles = []

def create_confetti():
    confetti_particles.clear()
    for _ in range(200): # 200 papelitos
        p = {
            'x': random.randint(0, WIDTH),
            'y': random.randint(-600, -50), # Empiezan arriba
            'color': random.choice(CONFETTI_COLORS),
            'sy': random.uniform(4, 10),
            'sx': random.uniform(-3, 3),
            'size': random.randint(8, 15)
        }
        confetti_particles.append(p)

def update_and_draw_confetti(surface):
    for p in confetti_particles:
        p['y'] += p['sy']
        p['x'] += p['sx']
        # Movimiento de hoja de papel cayendo
        p['sx'] += random.uniform(-0.5, 0.5) 
        if p['sx'] > 3: p['sx'] = 3
        if p['sx'] < -3: p['sx'] = -3
        
        pygame.draw.rect(surface, p['color'], (p['x'], p['y'], p['size'], p['size']))

def draw_medal(surface, x, y, level):
    # Cinta de la medalla (Bandera Argentina)
    pygame.draw.rect(surface, (116, 172, 223), (x - 12, y, 10, 25))
    pygame.draw.rect(surface, WHITE, (x - 2, y, 4, 25))
    pygame.draw.rect(surface, (116, 172, 223), (x + 2, y, 10, 25))
    
    # Determinar color de la medalla (Bronce, Plata, Oro, Diamante)
    if level == 1: color = BRONZE
    elif level == 2: color = SILVER
    elif level == 3: color = GOLD
    else: color = (100, 200, 255) # Diamante para niveles altos
    
    # Medalla
    medal_y = y + 30
    pygame.draw.circle(surface, color, (x, medal_y), 18)
    pygame.draw.circle(surface, BLACK, (x, medal_y), 18, 2)
    
    # Nivel en el centro
    txt = small_font.render(str(level), True, BLACK)
    surface.blit(txt, txt.get_rect(center=(x, medal_y)))

# --- Variables del Sistema ---
current_level = 1
max_shots_per_level = 5
shots_taken = 0
level_goals = 0
goals_to_pass = 3
earned_medals = [] # Guarda los niveles completados

goal = Goal()
goalkeeper = Goalkeeper(current_level)
ball = Ball()

state = "PLAYING" # PLAYING, RESULT, CELEBRATING, LEVEL_END
message = f"Nivel {current_level} - ¡Gana tu medalla!"
result_timer = 0
celebration_timer = 0

def draw_background():
    screen.fill(GREEN)
    for i in range(0, HEIGHT, 50):
        if (i // 50) % 2 == 0:
            pygame.draw.rect(screen, DARK_GREEN, (0, i, WIDTH, 50))
    pygame.draw.rect(screen, WHITE, (50, 280, 700, 350), 5)
    pygame.draw.rect(screen, WHITE, (250, 280, 300, 150), 5)
    pygame.draw.circle(screen, WHITE, (WIDTH//2, 520), 8)
    pygame.draw.arc(screen, WHITE, (WIDTH//2 - 60, 280 - 60, 120, 120), 3.14, 6.28, 5) # Medialuna del área

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == "PLAYING" and not ball.is_moving:
                mx, my = pygame.mouse.get_pos()
                ball.shoot(mx, my)
                shots_taken += 1
                message = ""
            elif state == "LEVEL_END":
                if level_goals >= goals_to_pass:
                    # Pasar de nivel
                    current_level += 1
                
                shots_taken = 0
                level_goals = 0
                goalkeeper = Goalkeeper(current_level)
                state = "PLAYING"
                message = f"Nivel {current_level} - ¡Comienza!"

    if state == "PLAYING":
        goalkeeper.move()
        
        if ball.move():
            gk_hitbox = pygame.Rect(goalkeeper.rect.x - 25, goalkeeper.rect.y - 25, goalkeeper.width + 50, goalkeeper.height + 30)
            ball_rect = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, ball.radius*2, ball.radius*2)
            
            if ball_rect.colliderect(gk_hitbox):
                message = "¡ATAJADÓN!"
            elif goal.rect.collidepoint(ball.target_x, ball.target_y):
                message = "¡GOLAZO!"
                level_goals += 1
            else:
                message = "¡AFUERA!"
                
            state = "RESULT"
            result_timer = pygame.time.get_ticks()

    elif state == "RESULT":
        if pygame.time.get_ticks() - result_timer > 1500:
            ball.reset()
            if shots_taken >= max_shots_per_level:
                if level_goals >= goals_to_pass:
                    state = "CELEBRATING" # Activar festejo
                    create_confetti()
                    celebration_timer = pygame.time.get_ticks()
                    if current_level not in earned_medals:
                        earned_medals.append(current_level)
                    message = "¡NIVEL SUPERADO! ¡FESTEJO!"
                else:
                    state = "LEVEL_END"
                    message = "FIN DEL JUEGO. Clic para reintentar"
            else:
                state = "PLAYING"
                message = f"Tiro {shots_taken + 1} de {max_shots_per_level}"
                
    elif state == "CELEBRATING":
        # Festejar con papeles picados durante 3.5 segundos
        if pygame.time.get_ticks() - celebration_timer > 3500:
            state = "LEVEL_END"
            message = "¡Haz clic para el siguiente nivel!"

    # --- Renderizado ---
    draw_background()
    goal.draw(screen)
    goalkeeper.draw(screen)
    ball.draw(screen)

    # Dibujar Medallas ganadas
    for i, medal_level in enumerate(earned_medals):
        draw_medal(screen, WIDTH - 40 - (i * 50), 20, medal_level)

    # Dibujar Papeles picados si está festejando
    if state == "CELEBRATING":
        update_and_draw_confetti(screen)

    # UI (Textos)
    hud_text = font.render(f"Nivel: {current_level} | Goles: {level_goals} / {max_shots_per_level}", True, WHITE)
    screen.blit(hud_text, (20, 20))
    
    if message:
        msg_color = YELLOW if state in ["LEVEL_END", "CELEBRATING"] else WHITE
        shadow_text = large_font.render(message, True, BLACK)
        shadow_rect = shadow_text.get_rect(center=(WIDTH//2 + 3, HEIGHT//2 + 3))
        screen.blit(shadow_text, shadow_rect)
        msg_text = large_font.render(message, True, msg_color)
        msg_rect = msg_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(msg_text, msg_rect)
        
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
