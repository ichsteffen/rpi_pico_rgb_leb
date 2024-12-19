import Font8

class FrameBuffer:
    def __init__(self, width, height, bgcolor=0):
        """
        Konstruktor für den FrameBuffer.
        :param width: Breite der Zeichenfläche in Pixeln.
        :param height: Höhe der Zeichenfläche in Pixeln.
        :param bgcolor: Standard-Hintergrundfarbe (z. B. 0 für Schwarz, 1 für Weiß).
        """
        self.width = width
        self.height = height
        self.bgcolor = bgcolor  # Hintergrundfarbe
        # Initialisierung des zweidimensionalen Arrays für die Pixel
        self.buffer = [[self.bgcolor for _ in range(width)] for _ in range(height)]

    def set_pixel(self, x, y, value):
        """
        Setzt den Wert eines Pixels an den Koordinaten (x, y).
        :param x: x-Koordinate des Pixels.
        :param y: y-Koordinate des Pixels.
        :param value: Wert des Pixels (z. B. 0 für Schwarz, 1 für Weiß).
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.buffer[y][x] = value

    def get_pixel(self, x, y):
        """
        Gibt den Wert eines Pixels an den Koordinaten (x, y) zurück.
        :param x: x-Koordinate des Pixels.
        :param y: y-Koordinate des Pixels.
        :return: Wert des Pixels oder None, wenn die Koordinaten außerhalb liegen.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.buffer[y][x]
        return None

    def fill(self, value=None):
        """
        Füllt den gesamten FrameBuffer mit einem bestimmten Wert.
        Wenn kein Wert angegeben ist, wird die Hintergrundfarbe verwendet.
        :param value: Der Wert, mit dem die Zeichenfläche gefüllt werden soll (Standard: Hintergrundfarbe).
        """
        fill_value = value if value is not None else self.bgcolor
        for y in range(self.height):
            for x in range(self.width):
                self.buffer[y][x] = fill_value

    def fill_row(self, row, color):
        """
        Füllt eine bestimmte Zeile mit einer angegebenen Farbe.
        :param row: Die Zeilennummer (0-basiert), die gefüllt werden soll.
        :param color: Die Farbe, mit der die Zeile gefüllt werden soll.
        """
        if 0 <= row < self.height:
            for x in range(self.width):
                self.buffer[row][x] = color

    def fill_column(self, column, color):
        """
        Füllt eine bestimmte Spalte mit einer angegebenen Farbe.
        :param column: Die Spaltennummer (0-basiert), die gefüllt werden soll.
        :param color: Die Farbe, mit der die Spalte gefüllt werden soll.
        """
        if 0 <= column < self.width:
            for y in range(self.height):
                self.buffer[y][column] = color

    def clear(self):
        """
        Setzt den gesamten FrameBuffer auf die Hintergrundfarbe zurück.
        """
        self.fill(self.bgcolor)

#    def render_to_display(self, display):
#        """
#        Gibt den FrameBuffer auf ein Display aus.
#        :param display: Ein Display-Objekt, das eine Methode wie `draw_pixel(x, y, value)` unterstützt.
#        """
#        for y in range(self.height):
#            for x in range(self.width):
#                display[y*16 + x] = self.buffer[y][x]
#                # display.draw_pixel(x, y, self.buffer[y][x])
#        display.write()
    def render_to_display(self, display, rotation=0):
        """
        Gibt den FrameBuffer auf ein Display aus, optional mit Rotation.
        :param display: Ein Display-Objekt, dessen Pixel linear in einem Array angesprochen werden können.
        :param rotation: Rotation des FrameBuffers in Grad (0, 90, 180, 270).
        """
        linear_pixels = display #[0] * (self.width * self.height)  # Linearer Array für das Display

        if rotation == 0:
            for y in range(self.height):
                for x in range(self.width):
                    linear_pixels[y * self.width + x] = self.buffer[y][x].values
        elif rotation == 90:
            for y in range(self.height):
                for x in range(self.width):
                    linear_pixels[x * self.height + (self.height - 1 - y)] = self.buffer[y][x].values
        elif rotation == 180:
            for y in range(self.height):
                for x in range(self.width):
                    linear_pixels[(self.height - 1 - y) * self.width + (self.width - 1 - x)] = self.buffer[y][x].values
        elif rotation == 270:
            for y in range(self.height):
                for x in range(self.width):
                    linear_pixels[(self.width - 1 - x) * self.height + y] = self.buffer[y][x].values

        # Übergabe der linearen Pixel-Daten an das Display
        display.write()


    def shift(self, direction, rotate=False):
        """
        Verschiebt den Inhalt des FrameBuffers um ein Pixel in die angegebene Richtung.
        :param direction: Richtung der Verschiebung ('up', 'down', 'left', 'right').
        :param rotate: Wenn True, werden die herausgeschobenen Pixel auf der anderen Seite wieder eingefügt (Rotation).
        """
        if direction == 'up':
            if rotate:
                row = self.buffer.pop(0)
                self.buffer.append(row)
            else:
                self.buffer.pop(0)
                self.buffer.append([self.bgcolor] * self.width)
        elif direction == 'down':
            if rotate:
                row = self.buffer.pop(-1)
                self.buffer.insert(0, row)
            else:
                self.buffer.pop(-1)
                self.buffer.insert(0, [self.bgcolor] * self.width)
        elif direction == 'left':
            for row in self.buffer:
                if rotate:
                    row.append(row.pop(0))
                else:
                    row.pop(0)
                    row.append(self.bgcolor)
        elif direction == 'right':
            for row in self.buffer:
                if rotate:
                    row.insert(0, row.pop(-1))
                else:
                    row.pop(-1)
                    row.insert(0, self.bgcolor)
     
     
    def blit(self, source_buffer, x_offset, y_offset):
        """
        Kopiert den Inhalt eines zweiten FrameBuffers an die Position (x_offset, y_offset).
        :param source_buffer: Der FrameBuffer, der kopiert werden soll.
        :param x_offset: X-Position, an der die Kopie beginnen soll.
        :param y_offset: Y-Position, an der die Kopie beginnen soll.
        """
        for y in range(source_buffer.height):
            for x in range(source_buffer.width):
                target_x = x + x_offset
                target_y = y + y_offset
                if 0 <= target_x < self.width and 0 <= target_y < self.height:
                    source_value = source_buffer.buffer[y][x]
                    if source_value is not None:
                        self.buffer[target_y][target_x] = source_value

    def draw_pattern(self, x, y, pattern, bit_width, color=1):
        """
        Zeichnet ein Muster an der Position (x, y) basierend auf einem Array von Zahlen.
        Die gesetzten Bits jeder Zahl geben an, welche Pixel in der entsprechenden Zeile gesetzt werden.
        :param x: X-Koordinate der oberen linken Ecke des Musters.
        :param y: Y-Koordinate der oberen linken Ecke des Musters.
        :param pattern: Ein Array von Zahlen, die das Muster definieren.
        :param bit_width: Die Anzahl der Bits, die in jeder Zahl verwendet werden.
        :param color: Die Farbe, die für gesetzte Bits verwendet wird (Standard: 1).
        """
        for row_index, row_value in enumerate(pattern):
            target_y = y + row_index
            if 0 <= target_y < self.height:
                for bit_position in range(bit_width):
                    if 0x80 & (row_value << bit_position):  # Prüft, ob das Bit an der Position gesetzt ist
                        target_x = x + bit_position
                        if 0 <= target_x < self.width:
                            self.buffer[target_y][target_x] = color

    def print8(self, s, offset_x, offset_y, color=None) :
        for i,c in enumerate(s) :
          index = (ord(c)-32)*Font8.Height
          self.draw_pattern(offset_x + i*5, offset_y, Font8.Table[index:index+Font8.Height], Font8.Width, color=color)

    def square(self, offset_x, offset_y, size_x, size_y, color=None) :
        # print("square ", offset_x, offset_y, size_x, size_y)
        for y in range(offset_y, offset_y + size_y):
            for x in range(offset_x, offset_x + size_x):
                self.buffer[y][x] = color
                
