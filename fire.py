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
kernel1 = [
    [1, 2, 1],
    [2, 4, 2],
    [1, 2, 1]
]
kernel2 = [
    [0, 0, 0],
    [1, 0, 1],
    [0, 2, 0]
]
cooling = 1.1
kernel=kernel2
kernel_sum = sum(sum(row) for row in kernel)

def heat_to_color(heat):
    """Wandelt den Hitzewert in eine RGB-Farbe um."""
    color_bucket_size = INTENSITY_MAX / 4
    if heat <= 0:
        return Color(0, 0, 0)  # Schwarz
    elif heat < 1 * color_bucket_size:
        color_index = heat - (0*color_bucket_size) # heat minus lower boundery
        red = int(0x1F * color_index/color_bucket_size)
        return Color(0, red, 0)  # Rot
    elif heat < 2 * color_bucket_size:
        color_index = heat - (1*color_bucket_size) # heat minus lower boundery
        red = int(0xFF * color_index/color_bucket_size)
        return Color(0, red, 0)  # Rot
    elif heat < 3 * color_bucket_size:
        color_index = heat - (2*color_bucket_size) # heat minus lower boundery
        green = int(0xFF * color_index/color_bucket_size)
        return Color(green, 0xFF, 0)  # Gelb-Orange
    else:
        color_index = heat - (3*INTENSITY_MAX/4) # heat minus lower boundery
        blue = int(0xFF * color_index/color_bucket_size)
        return Color(0xFF, 0xFF, blue) # fast Weiss


def update_fire():
    """Aktualisiert die Feuersimulation."""
    global matrix
    new_matrix = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for x in range(WIDTH):
        new_matrix[HEIGHT - 1][x] = random.randint(5*INTENSITY_MAX//10, 7*INTENSITY_MAX//10)

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
            heat //= cooling
            #heat += random.randint(max(-heat,-4), min(heat,4))
            heat += random.randint(-4,4)
            heat = max(0, min(INTENSITY_MAX, heat))
            new_matrix[y][x] = heat

    matrix = new_matrix

def display_fire_pygame(matrix, framebuffer, display):
    for y in range(HEIGHT-1):
        for x in range(WIDTH):
            color = heat_to_color(matrix[y][x])
            framebuffer.set_pixel(x,y, color.scale(0.5))
    framebuffer.render_to_display(display, rotation=0)

def run_fire(iterations, framebuffer, display):
    running = True
    counter = 0
    while running:
        print("fire loop") 
        update_fire()
        display_fire_pygame(matrix, framebuffer, display)
        #time.sleep_ms(10)
        counter += 1
        if iterations != -1 :
            running = counter < iterations
            print(running, counter, iterations)
        else:
            running = true

