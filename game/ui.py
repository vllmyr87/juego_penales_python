import pygame

from .config import BLACK, BRONZE, GOLD, SILVER, WHITE, YELLOW


def draw_medal(surface, x, y, level, small_font):
    pygame.draw.rect(surface, (116, 172, 223), (x - 12, y, 10, 25))
    pygame.draw.rect(surface, WHITE, (x - 2, y, 4, 25))
    pygame.draw.rect(surface, (116, 172, 223), (x + 2, y, 10, 25))
    if level == 1:
        color = BRONZE
    elif level == 2:
        color = SILVER
    elif level == 3:
        color = GOLD
    else:
        color = (100, 200, 255)
    medal_y = y + 30
    pygame.draw.circle(surface, color, (x, medal_y), 18)
    pygame.draw.circle(surface, BLACK, (x, medal_y), 18, 2)
    text = small_font.render(str(level), True, BLACK)
    surface.blit(text, text.get_rect(center=(x, medal_y)))


def draw_ranking(surface, database, table_font):
    panel = pygame.Surface((230, 160), pygame.SRCALPHA)
    panel.fill((10, 24, 38, 205))
    pygame.draw.rect(panel, (235, 198, 76), panel.get_rect(), 2, border_radius=6)
    surface.blit(panel, (550, 315))
    surface.blit(table_font.render("RANKING", True, (255, 220, 92)), (565, 325))
    surface.blit(table_font.render("Jugador       Pts  G", True, WHITE), (560, 350))
    for index, player in enumerate(database.get_ranking()):
        name = player["name"][:10].ljust(10)
        row = table_font.render(
            f"{index + 1}. {name} {player['points']:>4} {player['goals']:>2}",
            True,
            (245, 245, 238),
        )
        surface.blit(row, (560, 375 + index * 20))


def draw_message(surface, message, state, large_font):
    if not message:
        return
    color = YELLOW if state in ["LEVEL_END", "CELEBRATING"] else WHITE
    shadow = large_font.render(message, True, BLACK)
    surface.blit(shadow, shadow.get_rect(center=(403, 303)))
    text = large_font.render(message, True, color)
    surface.blit(text, text.get_rect(center=(400, 300)))
