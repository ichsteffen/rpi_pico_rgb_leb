import pygame
import random
import time

# Konfiguration
WIDTH = 200  # Breite der Matrix
HEIGHT = 160   # Höhe der Matrix
INTENSITY_MAX = 64 # Maximale Intensität

PIXEL_SIZE = 4 # Größe eines simulierten Pixels
WIDTH_DISPLAY = WIDTH*PIXEL_SIZE # Breite des Pygame Fensters
HEIGHT_DISPLAY = HEIGHT*PIXEL_SIZE # Höhe des Pygame Fensters
WIDTH_SCALED = WIDTH_DISPLAY // PIXEL_SIZE
HEIGHT_SCALED = HEIGHT_DISPLAY // PIXEL_SIZE
if WIDTH_SCALED < WIDTH:
    print(f"Warnung: WIDTH_DISPLAY zu klein für Matrixbreite von {WIDTH}. Benutze {WIDTH*PIXEL_SIZE} statt {WIDTH_DISPLAY}")
    WIDTH_DISPLAY = WIDTH*PIXEL_SIZE
    WIDTH_SCALED = WIDTH_DISPLAY // PIXEL_SIZE
if HEIGHT_SCALED < HEIGHT:
    print(f"Warnung: HEIGHT_DISPLAY zu klein für Matrixhöhe von {HEIGHT}. Benutze {HEIGHT*PIXEL_SIZE} statt {HEIGHT_DISPLAY}")
    HEIGHT_DISPLAY = HEIGHT*PIXEL_SIZE
    HEIGHT_SCALED = HEIGHT_DISPLAY // PIXEL_SIZE

# Initialisierung der Matrix mit 0
matrix = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

# Konvolutionsmatrix (Gewichtungen für die Nachbarn)
kernel = [
#    [1, 2, 1],
#    [2, 4, 2],
#    [1, 2, 1]
    [0, 0, 0],
    [1, 0, 1],
    [0, 1.5, 0]
    
]
kernel_sum = sum(sum(row) for row in kernel)

def heat_to_color(heat):
    """Wandelt den Hitzewert in eine RGB-Farbe um."""
    
    color_bucket_size = INTENSITY_MAX / 4
    if heat <= 0:
        return (0, 0, 0)  # Schwarz
    elif heat < 1 * color_bucket_size:
#        red = int(128 * (heat / (INTENSITY_MAX / 4)))
        color_index = heat - (0*color_bucket_size) # heat minus lower boundery
        red = int(0x1F * color_index/color_bucket_size)
        return (red, 0, 0)  # Rot
    elif heat < 2 * color_bucket_size:
#        red = int(255 * (heat / (INTENSITY_MAX / 4)))
        color_index = heat - (1*color_bucket_size) # heat minus lower boundery
        red = int(0xFF * color_index/color_bucket_size)
        return (red, 0, 0)  # Rot
    elif heat < 3 * color_bucket_size:
#        green = int(255*((heat - 2*INTENSITY_MAX/4) / (INTENSITY_MAX/4)))
        color_index = heat - (2*color_bucket_size) # heat minus lower boundery
        green = int(0xFF * color_index/color_bucket_size)
        return (0xFF, green, 0)  # Gelb-Orange
    else:
#        blue = int(255*((heat - 3* INTENSITY_MAX/4) / (INTENSITY_MAX/4)))
        color_index = heat - (3*INTENSITY_MAX/4) # heat minus lower boundery
        blue = int(0xFF * color_index/color_bucket_size)
        return (0xFF, 0xFF, blue) # fast Weiss

def update_fire():
    """Aktualisiert die Feuersimulation."""
    global matrix
    new_matrix = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for x in range(5,WIDTH-5):
        new_matrix[HEIGHT - 1][x] = random.randint(2*INTENSITY_MAX//4, 3.5*INTENSITY_MAX//4)

    for y in range(HEIGHT - 2, -1, -1):
        for x in range(WIDTH):
            heat = 0
            for ky in range(-1, 2):
                for kx in range(-1, 2):
                    nx = x + kx
                    ny = y + ky
                    if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                      heat += matrix[ny][nx] * kernel[ky + 1][kx + 1]

            heat //= kernel_sum
            heat += random.randint(-4, 4)
            heat = max(0, min(INTENSITY_MAX, heat))
            new_matrix[y][x] = heat

    matrix = new_matrix

pygame.init()
screen = pygame.display.set_mode((WIDTH_DISPLAY, HEIGHT_DISPLAY))
pygame.display.set_caption("Feuersimulation")
clock = pygame.time.Clock() # für konstante Framerate

def display_fire_pygame(matrix):
    for y in range(min(HEIGHT_SCALED, HEIGHT)):
        for x in range(min(WIDTH_SCALED, WIDTH)):
            color = heat_to_color(matrix[y][x])
            pygame.draw.rect(screen, color, (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
    pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update_fire()
    display_fire_pygame(matrix)

    clock.tick(30)  # Begrenzung auf 30 FPS (Frames pro Sekunde)

pygame.quit()