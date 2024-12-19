import random
import time
from Color import Color

# Konfiguration
WIDTH = 16  # Breite der Matrix
HEIGHT = 11   # Höhe der Matrix
INTENSITY_MAX = 64 # Maximale Intensität

# Initialisierung der Matrix mit 0
matrix = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

# Konvolutionsmatrix (Gewichtungen für die Nachbarn)
kernel = [
    [1, 2, 1],
    [2, 4, 2],
    [1, 2, 1]
]
kernel_sum = sum(sum(row) for row in kernel)

def heat_to_color(heat):
    """Wandelt den Hitzewert in eine RGB-Farbe um."""
    if heat <= 0:
        return Color(0, 0, 0)  # Schwarz
    elif heat < INTENSITY_MAX / 3:
        red = int(255 * (heat / (INTENSITY_MAX / 3)))
        return Color(0, red, 0)  # Rot
    elif heat < 2 * INTENSITY_MAX / 3:
        red = 255 #int(255 - 255*((heat - INTENSITY_MAX/3) / (INTENSITY_MAX/3)))
        green = int(255*((heat - INTENSITY_MAX/3) / (INTENSITY_MAX/3)))
        return Color(green, red, 0)  # Gelb-Orange
    else:
        blue = int(255 - 255 * ((heat - 2* INTENSITY_MAX / 3)/(INTENSITY_MAX/3)))
        return Color(255, 255, blue) # fast Weiss

def update_fire():
    """Aktualisiert die Feuersimulation."""
    global matrix
    new_matrix = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for x in range(WIDTH):
        new_matrix[HEIGHT - 1][x] = random.randint(INTENSITY_MAX//2, INTENSITY_MAX//1)

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
            heat += random.randint(max(-heat,-4), min(heat,4))
            heat = max(0, min(INTENSITY_MAX, heat))
            new_matrix[y][x] = heat

    matrix = new_matrix

def display_fire_pygame(matrix, framebuffer, display):
    for y in range(HEIGHT-1):
        for x in range(WIDTH):
            color = heat_to_color(matrix[y][x])
            framebuffer.set_pixel(x,y, color.scale(0.2))
    framebuffer.render_to_display(display, rotation=0)

def run_fire(framebuffer, display):
    running = True
    while running:
        print("fire loop") 
        update_fire()
        display_fire_pygame(matrix, framebuffer, display)
        time.sleep_ms(10)


