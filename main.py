import machine, neopixel
import FrameBuffer
from time import sleep_ms,sleep
from Color import Color
from BinaryClock import BinaryClock
import Font8
import ds3231
from random import random
import snake
import fire

#BLACK = (0x00,0x00,0x00)
#WHITE = (0x1F,0x1F,0x1F)
#RED   = (0x00,0x1F,0x00)

bg = Color(0x03, 0x03, 0x03)
np = neopixel.NeoPixel(machine.Pin(6), 16*10)

DARK_GREY = Color.WHITE.clone().scale(0.05)
fb_star = FrameBuffer.FrameBuffer(3,3,bgcolor=None)
fb_star.fill_column(1, DARK_GREY)
fb_star.fill_row(1, DARK_GREY)

fb = FrameBuffer.FrameBuffer(width=16, height=10, bgcolor=Color.BLACK)

def shifts() :
    fb.fill(Color.BLACK)
    fb.fill_column(0, Color.GREEN.scale(16/256))
    fb.fill_row(0, Color.RED.scale(16/256))
    fb.bgcolor=Color(0x00,0x00,0x03)

    fb.render_to_display(display=np)
    for i in range(0,2*fb.height,1):
        fb.shift('down', rotate=True)
        fb.shift('right', rotate=True)
        fb.render_to_display(display=np, rotation=0)
        sleep_ms(50)

    for i in range(0,2*fb.width,1):
        fb.shift('up', rotate=True)
        fb.shift('left', rotate=True)
        fb.render_to_display(display=np, rotation=0)
        sleep_ms(50)

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

def rainbow(iterations = 100) :
    s = "... rainbow show ..."
    swidth = len(s)*Font8.Width
    c = Color(0,0,0)
    offset_y = 1
    for i in range(0,iterations,1) :
        for y in range(0,10,1):
            for x in range(0,16,1):
                c.set_from_hsv(-i*5 + y*8 - x*8, 1.0, 16/256)
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

rtc = ds3231.ds3231(ds3231.I2C_PORT,ds3231.I2C_SCL,ds3231.I2C_SDA)
def clock(i):
    fb.fill(Color.BLACK)
    h,mi,s,d,m,y = rtc.read_time_()
    s = "%02x:%02x" %(h,mi)
    fb.print8(s,16 - i%40,1, DARK_GREY.scale(1/10))
    fb.render_to_display(np,0)
    
def binaryClock(iterations):
    binaryClock = BinaryClock(fb)    
    for i in range(0,iterations,1):
        h,mi,s,d,m,y = rtc.read_time_()
        fb.fill(Color.BLACK)
        binaryClock.showSeconds(s)
        binaryClock.showMinutes(mi)
        binaryClock.showHours(h)
        fb.render_to_display(np,0)
        sleep_ms(1000)

def snowflaks(fb, rot, iterations, p):
    for i in range(0,iterations):
      fb.shift("down")
      for x in range(10):          
          if (random() < (p/100)/10) :
              fb.set_pixel( x ,0, DARK_GREY)
      fb90.render_to_display(np, rotation=rot)
      sleep_ms(250)

# Define PacMan shape with binary values (Yellow = 1, Black = 0)
pacman_open = [
    [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

pacman_closed = [
    [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]


def play_pacman(framebuffer,display):
    for offset_x in range(-10,26):
        if (offset_x % 2 == 1):
            pacman = pacman_closed
        else:
            pacman = pacman_open
        fb.clear()
        for y in range(10):
            for x in range(10):
                if pacman[y][x] > 0:
                    framebuffer.set_pixel(offset_x +x, y, Color(0x0F, 0x0F, 0))  # Yellow for PacMan
                else:
                    framebuffer.set_pixel(offset_x +x, y, Color(0, 0, 0))  # Black for background
    
        framebuffer.render_to_display(display,0)
        sleep_ms(500)
    
#gradients()
#shifts()
        
#binaryClock(12) # 120 sek

for i in range(0,40,1):
    clock(i)
    sleep_ms(100)
    
#marry_xmas()
#rainbow()

fb.bgcolor = Color.BLACK
fb.fill()
play_pacman(fb,np)

fire.run_fire(200, framebuffer=fb, display=np)

snake.play_snake(framebuffer=fb, display=np, iterations=5)

fb.fill(Color.BLACK)
fb.set_pixel(1,1, Color.WHITE)
fb.render_to_display(display=np, rotation=180)
sleep_ms(10)

fb90 = FrameBuffer.FrameBuffer(width=10, height=16, bgcolor=Color.BLACK)
fb90.set_pixel(1,1, Color.DARK_GREY)
fb90.render_to_display(display=np, rotation=270)

snowflaks(fb=fb90,rot=90,iterations=250, p=100)

for i in range(0,60*4,1):
    fb90.fill(Color.BLACK)
    h,mi,s,d,m,y = rtc.read_time_()
    s = "%02x:%02x" %(h,mi)
    fb90.print8(s,16 - i%40,1, DARK_GREY.scale(1/8))
    fb90.render_to_display(np, rotation=90)
    sleep_ms(250)
sleep_ms(10)

fb.fill(Color.BLACK)
fb.render_to_display(display=np, rotation=0)


