import machine, neopixel
import FrameBuffer
from time import sleep_ms,sleep
from Color import Color
import Font8

#BLACK = (0x00,0x00,0x00)
#WHITE = (0x1F,0x1F,0x1F)
#RED   = (0x00,0x1F,0x00)

bg = Color(0x03, 0x03, 0x03)
np = neopixel.NeoPixel(machine.Pin(6), 16*10)

DARK_GREY = Color.WHITE.clone().scale(0.05)
fb_star = FrameBuffer.FrameBuffer(3,3,bgcolor=None)
fb_star.fill_column(1, DARK_GREY)
fb_star.fill_row(1, DARK_GREY)

fb = FrameBuffer.FrameBuffer(width=16, height=10, bgcolor=bg)

def shifts() :
    fb.fill(Color.BLACK)
    fb.fill_column(0, Color.GREEN)
    fb.fill_row(0, Color.RED)
    fb.bgcolor=Color(0x00,0x00,0x03)

    fb.render_to_display(display=np)
    for i in range(0,2*fb.height,1):
        fb.shift('down', rotate=True)
        fb.shift('right', rotate=True)
        fb.render_to_display(display=np, rotation=0)
        sleep_ms(500)

    for i in range(0,2*fb.width,1):
        fb.shift('up', rotate=True)
        fb.shift('left', rotate=True)
        fb.render_to_display(display=np, rotation=0)
        sleep_ms(500)

def marry_xmas():
    s = "Marry Xmas"
    offset_y = 1
    for offset_x in range(fb.width, -len(s)*Font8.Width, -1):
        fb.fill(Color.BLACK)
        fb.print8( s, offset_x, offset_y, DARK_GREY)
        #for i,c in enumerate(s) :
        #  index = (ord(c)-32)*Font8.Height
        #  fb.draw_pattern(offset_x + i*5, offset_y, Font8.Table[index:index+Font8.Height], Font8.Width, color=DARK_GREY)
        fb.render_to_display(display=np, rotation=0)
        sleep_ms(100)

def rainbow() :
    s = "... rainbow show ..."
    swidth = len(s)*Font8.Width
    c = Color(0,0,0)
    offset_y = 1
    for i in range(0,1000,1) :
        for y in range(0,10,1):
            for x in range(0,16,1):
                c.set_from_hsv(i*5 + y*8 - x*8, 1.0, 0.04)
                fb.set_pixel(x,y,c.clone())
        #fb.blit(fb_star,2,2)
        fb.print8( s, 16-(i% (swidth+16)) , offset_y, Color.BLACK)
        fb.render_to_display(np,0)

def gradients() :
    fb.fill(Color.BLACK)
    colors = ( (Color.RED, Color.GREEN), (Color.GREEN, Color.BLUE), (Color.BLUE, Color.RED))
    for c1,c2 in colors :
        for i in range(0,10,1):
            c = (c1.scale(i/9) + c2.scale( (9-i)/9)).scale(0.1)
            fb.fill_row(i,c)
        fb.render_to_display(np,0)
        sleep_ms(2500)


#gradients()
#shifts()
marry_xmas()
rainbow()

fb.fill(Color.BLACK)
fb.set_pixel(1,1, Color.WHITE)
fb.render_to_display(display=np, rotation=180)
sleep_ms(10)

fb90 = FrameBuffer.FrameBuffer(width=10, height=16, bgcolor=Color.RED)
fb90.set_pixel(1,1, Color.WHITE)
fb90.render_to_display(display=np, rotation=270)
sleep_ms(10)

fb.fill(Color.BLACK)
fb.render_to_display(display=np, rotation=0)



