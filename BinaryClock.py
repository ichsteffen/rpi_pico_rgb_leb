from Color import Color
import FrameBuffer

class BinaryClock:
    def __init__(self, framebuffer) :
        self.framebuffer = framebuffer
        self.color_sec = Color(0x00,0x02,0x00)
        self.color_min = Color(0x02,0x00,0x00)
        self.color_hour = Color(0x00,0x00,0x02)
        self.color_none = Color(0x01, 0x01, 0x01)
        return
    
    def showBinaryNumber(self, number, line, size_x, size_y, color=None, padX=0) :
        bitCounter = 0
        for bit_position in range(7):
            if number & (0x01 << bit_position):
                self.framebuffer.square(13 - bit_position*(size_x+padX), line ,size_x, size_y, color )
#        if (number & 0x02):
#            self.framebuffer.square(12, line ,size_x, size_y, color )
#        if (number & 0x04):
#            self.framebuffer.square(10, line ,size_x, size_y, color )
#        if (number & 0x08):
#            self.framebuffer.square( 8, line ,size_x, size_y, color )
#        if (number & 0x10):
#            self.framebuffer.square( 6, line ,size_x, size_y, color )
#        if (number & 0x20):
#            self.framebuffer.square( 4, line ,size_x, size_y, color )
#        if (number & 0x40):
#            self.framebuffer.square( 2, line ,size_x, size_y, color )
        
    def showSeconds(self, secBCD) :
        sec = ((secBCD &0xF0) >> 4) * 10 + (secBCD & 0x0F)
        self.showBinaryNumber(0x7F, 8, 1, 1, self.color_none,1)
        self.showBinaryNumber(sec, 8, 1, 1, self.color_sec,1)
       
    def showMinutes(self, minBCD) :
        minutes = ((minBCD &0xF0) >> 4) * 10 + (minBCD & 0x0F)
        self.showBinaryNumber(0x7F, 4, 1, 2, self.color_none,1)
        self.showBinaryNumber(minutes, 4, 1, 2, self.color_min,1)
        
    def showHours(self, hourBCD):
        hour = ((hourBCD &0xF0) >> 4) * 10 + (hourBCD & 0x0F)
        self.showBinaryNumber(0x1F, 1, 2, 2, self.color_none,1)
        self.showBinaryNumber(hour, 1, 2, 2, self.color_hour,1)