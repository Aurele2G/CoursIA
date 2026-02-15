# settings.py

# Dimensions de la grille
ROWS = 15
COLS = 15
MINES_COUNT = 30

# Paramètres d'affichage
CELL_SIZE = 40
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE
TOOLBAR_HEIGHT = 50

# Couleurs (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
DARK_GRAY = (160, 160, 160)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Couleurs des chiffres (1, 2, 3, etc.)
NUM_COLORS = {
    1: BLUE,
    2: GREEN,
    3: RED,
    4: (0, 0, 128),
    5: (128, 0, 0),
    6: (0, 128, 128),
    7: (0, 0, 0),
    8: (128, 128, 128)
}
