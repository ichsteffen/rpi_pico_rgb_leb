class Color:
    def __init__(self, g, r, b):
        self.values = (g, r, b)

    def __add__(self, other):
        if isinstance(other, Color):
            return Color(
                self.values[0] + other.values[0],
                self.values[1] + other.values[1],
                self.values[2] + other.values[2]
            )
        return NotImplemented

    def scale(self, scalar):
        return Color(
            int(self.values[0] * scalar),
            int(self.values[1] * scalar),
            int(self.values[2] * scalar)
        )
    
    def clone(self):
        return Color(*self.values)
    
    def set_from_hsv(self, h, s, v):
        h = h % 360  # Sicherstellen, dass h zwischen 0 und 360 liegt
        s = max(0, min(1, s))  # Begrenzen von s auf den Bereich [0, 1]
        v = max(0, min(1, v))  # Begrenzen von v auf den Bereich [0, 1]

        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c

        if 0 <= h < 60:
            r_, g_, b_ = c, x, 0
        elif 60 <= h < 120:
            r_, g_, b_ = x, c, 0
        elif 120 <= h < 180:
            r_, g_, b_ = 0, c, x
        elif 180 <= h < 240:
            r_, g_, b_ = 0, x, c
        elif 240 <= h < 300:
            r_, g_, b_ = x, 0, c
        else:
            r_, g_, b_ = c, 0, x

        self.values = (
            int((g_ + m) * 255),
            int((r_ + m) * 255),
            int((b_ + m) * 255)
        )
    
    def __repr__(self):
        return f"Color(g={self.values[0]}, r={self.values[1]}, b={self.values[2]})"

# Vordefinierte Farben
Color.WHITE = Color(255, 255, 255)
Color.BLACK = Color(0, 0, 0)
Color.RED = Color(0, 255, 0)
Color.GREEN = Color(255, 0, 0)
Color.BLUE = Color(0, 0, 255)

