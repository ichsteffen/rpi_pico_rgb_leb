import random
import time
import FrameBuffer
from Color import Color

class Snake:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        # Zufällige Startposition und Richtung
        self.snake = [(random.randint(0, self.width - 1), random.randint(0, self.height - 1))]
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.grow = False

    def move(self):
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Prüfen, ob die Schlange das Spielfeld verlässt
        if not (0 <= new_head[0] < self.width and 0 <= new_head[1] < self.height):
            raise Exception("Game Over: Collision with wall")

        # Prüfen, ob die Schlange mit sich selbst kollidiert
        if new_head in self.snake:
            raise Exception("Game Over: Collision with self")

        # Schlange bewegen
        self.snake.insert(0, new_head)
        if not self.grow:
            self.snake.pop()
        else:
            self.grow = False

    def grow_snake(self):
        self.grow = True

    def change_direction(self, new_direction):
        # Richtungsänderung nur zulassen, wenn sie nicht direkt umkehrt
        if (self.direction[0] + new_direction[0] != 0 or
            self.direction[1] + new_direction[1] != 0):
            self.direction = new_direction

    def get_snake_positions(self):
        return self.snake


class Berry:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = self.generate_new_position([])

    def generate_new_position(self, snake_positions):
        while True:
            new_position = (
                random.randint(0, self.width - 1),
                random.randint(0, self.height - 1)
            )
            if new_position not in snake_positions:
                return new_position

    def place_new_berry(self, snake_positions):
        self.position = self.generate_new_position(snake_positions)

    def get_position(self):
        return self.position


def calculate_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def shuffle_list(lst):
    # Einfacher Algorithmus zum zufälligen Mischen einer Liste
    for i in range(len(lst) - 1, 0, -1):
        j = random.randint(0, i)
        lst[i], lst[j] = lst[j], lst[i]

def is_valid_direction(head, direction, width, height):
    """Prüft, ob die Bewegung in die gegebene Richtung innerhalb des Spielfelds bleibt."""
    new_x = head[0] + direction[0]
    new_y = head[1] + direction[1]
    return 0 <= new_x < width and 0 <= new_y < height


# Spiel starten
def play_snake(framebuffer, display):
    width, height = 10, 10
    colorSnake = Color.RED.scale(0.02)  # Farbe für die Schlange
    colorBerry = Color.GREEN.scale(0.02)  # Farbe für die Beeren
    #framebuffer = None  # Annahme: Externe Framebuffer-Klasse mit `clear`, `set_pixel` und `display`-Methoden

    try:
        while True:
            snake = Snake(width, height)
            berry = Berry(width, height)

            try:
                while True:
                    # Framebuffer leeren und Inhalte rendern
                    framebuffer.clear()
                    for x, y in snake.get_snake_positions():
                        framebuffer.set_pixel(x, y, colorSnake)
                    framebuffer.set_pixel(*berry.get_position(), colorBerry)
                    framebuffer.render_to_display(display, rotation=0)

                    # Bewegung berechnen
                    head_x, head_y = snake.snake[0]
                    berry_x, berry_y = berry.get_position()

                    # 1. Richtung zur Beere ändern, wenn nah genug
                    if calculate_distance(snake.snake[0], berry.get_position()) <= 3:
                        if berry_x > head_x:
                            snake.change_direction((1, 0))
                        elif berry_x < head_x:
                            snake.change_direction((-1, 0))
                        elif berry_y > head_y:
                            snake.change_direction((0, 1))
                        elif berry_y < head_y:
                            snake.change_direction((0, -1))

                    # 2. Richtung ändern, wenn Gefahr besteht, das Spielfeld zu verlassen
                    elif (head_x == 0 and snake.direction == (-1, 0)) or \
                         (head_x == width - 1 and snake.direction == (1, 0)) or \
                         (head_y == 0 and snake.direction == (0, -1)) or \
                         (head_y == height - 1 and snake.direction == (0, 1)):
                        possible_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                        # Entferne die entgegengesetzte Richtung
                        opposite_direction = (-snake.direction[0], -snake.direction[1])
                        possible_directions = [d for d in possible_directions if d != opposite_direction]                                               
                        shuffle_list(possible_directions)
                        for new_dir in possible_directions:
                            if is_valid_direction(snake.snake[0], new_dir, width, height):
                                snake.change_direction(new_dir)
                                break

                    # 3. Zufällige Richtungsänderung, falls keine spezifischen Anforderungen
                    elif random.random() < 0.2:  # 20% Wahrscheinlichkeit für Richtungsänderung
                        possible_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                        # Entferne die entgegengesetzte Richtung
                        opposite_direction = (-snake.direction[0], -snake.direction[1])
                        possible_directions = [d for d in possible_directions if d != opposite_direction]
                        shuffle_list(possible_directions)
                        for new_dir in possible_directions:
                            if is_valid_direction(snake.snake[0], new_dir, width, height):
                                snake.change_direction(new_dir)
                                break

                    # Schlange bewegen
                    snake.move()

                    # Beere essen
                    if snake.snake[0] == berry.get_position():
                        snake.grow_snake()
                        berry.place_new_berry(snake.get_snake_positions())

                    # Kurze Pause für flüssige Animation
                    time.sleep(0.1)

            except Exception as e:
                print(f"{e}. Resetting game...")
                time.sleep(0.5)

    except KeyboardInterrupt:
        print("Spiel beendet.")
