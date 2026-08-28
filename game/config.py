import os

WIDTH, HEIGHT = 800, 600
FPS = 60
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "Assets")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (30, 144, 255)
YELLOW = (255, 215, 0)
RED = (220, 20, 60)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)
CONFETTI_COLORS = [RED, BLUE, YELLOW, WHITE, (255, 105, 180), (0, 255, 255), (50, 205, 50), (255, 165, 0)]
