#A graphics turtle program for experimenting with sacred geometry
#Requirements:
#Python 2.7.1, pygame

#Imports
import sys
import os
import traceback
import math
import random
import turtle
try:
    import pygame
    from pygame.locals import *
except ImportError:
    sys.stderr.write("Pygame was not found.\n")
    raw_input("Ready to quit... ")
    sys.exit()

#Pygame and turtle init
if sys.platform in ["win32","win64"]: 
    os.environ["SDL_VIDEO_CENTERED"]="1"
pygame.init()
pygame.mixer.init() #Pygame sound engine
screen_size = [1024, 600]
screen_surface = turtle.Screen()
screen_surface.setup(width=screen_size[0], height=screen_size[1], startx=None, starty=None)
screen_surface.bgcolor("black")
screen_surface.colormode(255)
title = "Experiment37"
version = "1.0 (Turtle) Oktober 2017"
screen_surface.title(title + " " + version)
screen_center = [screen_size[0] / 2, screen_size[1] / 2]
MainTurtle = turtle.Turtle()
MainTurtle.color("white")
#MainTurtle.shape("triangle")
MainTurtle.speed(0) #0 is fastest animation speed
MainTurtle.pensize(1)
#MainTurtle.mode("standard")

#Variable declarations

#Assets
_sound_library = {}

#Constants

#Framerate
FPS = 60
#Gravitational Acceleration (meters per second squared)
GA = 9.80665
#Default polygon shapes 
TRIANGLE = 3
SQUARE = 4
PENTAGON = 5
HEXAGON = 6
#Default directions
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0

#Playing a sound
def play_sound(path):
  global _sound_library
  sound = _sound_library.get(path)
  if sound == None:
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    sound = pygame.mixer.Sound(canonicalized_path)
    _sound_library[path] = sound
  sound.play()

#Clears the screen and resets the direction(left)and position(0,0) and speed(0) of the turtle 
#For a complete reset use: MainTurtle.reset()
def soft_reset():
    MainTurtle.home()
    MainTurtle.clear()
    MainTurtle.speed(0)

#Convert a string to turtle commands:
def string_to_turtle(string, defaultLength, color="white"):
    #Make uppercase and Convert to array
    string = list(string.upper())
    MainTurtle.color(color)
    MainTurtle.setheading(UP)
    
    for i in range(0, len(string)):
        #Move north
        if string[i] == 'N':
            MainTurtle.setheading(UP)
            MainTurtle.forward(defaultLength)
        #Move south
        if string[i] == 'S':
            MainTurtle.setheading(DOWN)
            MainTurtle.forward(defaultLength)
        #Move west
        if string[i] == 'W':
            MainTurtle.setheading(LEFT)
            MainTurtle.forward(defaultLength)
        #Move east
        if string[i] == 'E':
            MainTurtle.setheading(RIGHT)
            MainTurtle.forward(defaultLength)
        #Move forward
        if string[i] == 'F':
            MainTurtle.forward(defaultLength)
        #Rotate left by 10 degress
        if string[i] == '-':
            MainTurtle.left(10)
        #Rotate right by 10 degrees
        if string[i] == '+':
            MainTurtle.right(10)

#Draw a sine wave starting at pos
def wave(pos=[0,0], length=360, frequancy=10, amplitude=30, offsetX=0, offsetY=0, color="white"):
    MainTurtle.color(color)
    MainTurtle.penup()
    MainTurtle.setpos(pos[0], pos[1])    
    for x in range(pos[0] + (-length/2), pos[0] + (length/2)):
        y = pos[1] + (math.sin(math.radians(x * frequancy)) * amplitude)
        MainTurtle.goto(x + offsetX, y + offsetY)
        MainTurtle.pendown()

#Draw simple line with color
def line(source, destination, color="white"):
    MainTurtle.color(color)
    MainTurtle.penup()
    MainTurtle.setpos(source[0], source[1])
    MainTurtle.pendown()
    MainTurtle.setpos(destination[0], destination[1])

#Draw x and y axes in range
def axes(x_start, x_end, y_start, y_end):
    #Draw x-axis
    line([x_start, 0], [x_end, 0], "blue")
    #Draw y-axis    
    line([0, y_start], [0, y_end], "red")
    MainTurtle.color("white")
    MainTurtle.penup()
    MainTurtle.home()
    MainTurtle.pendown()

#Draw a star: Note: only odd numbers work
def star(numberOfPoints, defaultLength, color="white", enableSound=False, soundPath="mechanical-clonk-1.wav"):
    MainTurtle.color(color)
    for i in range(0, numberOfPoints):
        angle = 180.0 - 180.0 / numberOfPoints
        MainTurtle.forward(defaultLength)
        MainTurtle.right(angle)
        MainTurtle.forward(defaultLength)
        if enableSound == True:        
            play_sound(soundPath)

#Generate and draw fractal tree with the base starting at pos
def tree(size): 
    #MainTurtle.setpos(pos)    
    MainTurtle.pensize(size / 10)     
    if size < random.randint(1,2) * 20:         
        MainTurtle.color("green")     
    else:         
        MainTurtle.color("brown")     
    if size > 5:         
        MainTurtle.forward(size)         
        MainTurtle.left(25)         
        tree(size - random.randint(10, 20))         
        MainTurtle.right(50)         
        tree(size - random.randint(10, 20))
        MainTurtle.backward(size)         
        MainTurtle.pendown() 

#Draw a x equal sided polygon at pos
def polygon(pos, size, sides, color="white"):
    #MainTurtle.stamp() #origin
    x_center = pos[0]
    y_center = pos[1]
    MainTurtle.up()
    MainTurtle.goto(x_center, y_center)
    MainTurtle.down()
    MainTurtle.color(color)
    for i in range(0, sides):
        MainTurtle.forward(size)
        MainTurtle.left(360/sides)

#Draw a circle with center at position with size radius
def circle(pos, radius, color="white"):
    x_center = pos[0]
    y_center = pos[1]    
    MainTurtle.up()
    # go to (0, radius)
    MainTurtle.goto(x_center, y_center + radius)
    MainTurtle.down()    
    MainTurtle.color(color)
    # number of times the y axis has been crossed
    times_crossed_y = 0
    x_sign = 1.0
    while times_crossed_y <= 1:
        # move by 1/360 circumference
        MainTurtle.forward(2*math.pi*radius/360.0)
        # rotate by one degree (there will be
        # approx. 360 such rotations)
        MainTurtle.right(1.0)
        # use the copysign function to get the sign
        # of MainTurtle's x coordinate
        x_sign_new = math.copysign(1, MainTurtle.xcor())        
        if(x_sign_new != x_sign):
            times_crossed_y += 1
        x_sign = x_sign_new
    return  

#Draw polar coordinates grid in range with step
#Note: Its best to use a multiple of 20 for the step number
def polar_grid(x_start, x_end, y_start, y_end, step=40, numbrOfCircles=8):
    #Draw horizontal line
    line([x_start, 0], [x_end, 0], "white")
    #Draw vertical line
    line([0, y_start], [0, y_end], "white")
    #Draw line from Southwest to Northeast
    line([x_start, y_start], [x_end, y_end], "white")
    #Draw line from Southeast to Northwest
    line([x_end, y_start], [x_start, y_end], "white")
    #Draw circles
    for i in xrange(step, step*numbrOfCircles, step):
        circle([0,0], i, "white")

#Draw cartesian coordinates grid in range with step
#Note: Its best to use a multiple of 10 for the step number
def cartesian_grid(x_start, x_end, y_start, y_end, step=10):
    #Draw horizontal lines
    for i in xrange(y_start, y_end, step):
        line([x_start, i], [x_end, i], "white")
    #Draw vertical lines    
    for i in xrange(x_start, x_end, step):
        line([i, y_start], [i, y_end], "white")
    #Draw x and y axes
    axes(x_start, x_end, y_start, y_end)    

    #Draw lower horizontal lines:
#    for i in xrange(y_start, 0, step):
#        line([x_start, i], [x_end, i], "violet")    
    #Draw upper horizontal lines:
#    for i in xrange(0, y_end, step):
#        line([x_start, i], [x_end, i], "violet")
    #Draw left vertical lines    
#    for i in xrange(x_start, 0, step):
#        line([i, y_start], [i, y_end], "violet")    
    #Draw right vertical lines    
#    for i in xrange(0, x_end, step):
#        line([i, y_start], [i, y_end], "violet")


def koch_init(size, iterations):
    for i in range(0, iterations):
        MainTurtle.forward(size)
        play_sound("beep-7.wav")
        MainTurtle.left(60)
        MainTurtle.forward(size)
        play_sound("beep-3.wav")
        MainTurtle.right(60*2)
        MainTurtle.forward(size)
        play_sound("beep-7.wav")
        MainTurtle.left(60)
        MainTurtle.forward(size)

def koch_generate(size, iterations, color):
    MainTurtle.color(color)
    x = 1
    x += 1
    koch_init(size * math.sin(x), 1)
    x += 1
    MainTurtle.left(60)
    koch_init(size* math.sin(x), 2)
    x += 1
    MainTurtle.right(60*2)
    koch_init(size * math.sin(x), 2)
    x += 1
    MainTurtle.left(60)
    koch_init(size * math.sin(x), 1)

#Draw random lines with optional random colors
#area = [x_start, x_end, y_start, y_end] if area is not given it draws over entire screen
def random_lines(iterations, color="white", isRandomColor=0, area=[-(screen_surface.window_width() / 2), (screen_surface.window_width() / 2), -(screen_surface.window_height() / 2), (screen_surface.window_height() / 2)]):
    MainTurtle.color(color)
    MainTurtle.home
    for i in range(0, iterations):
        if isRandomColor == 1:
            MainTurtle.color((random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)))
        x = random.randint(area[0], area[1])
        y = random.randint(area[2], area[3])
        MainTurtle.goto(x, y)
    
#Init of program (run once before main program cycle)
def init():
    axes(-350, 350, -250, 250) 
    wave()
    koch_generate(50, 20, "violet")    
    test_debug()

#Testing and debugging
def test_debug():
    soft_reset()
    polar_grid(-350, 350, -250, 250)
    cartesian_grid(-350, 350, -250, 250)
    wave()
    wave([0,0], 360, 20, 60, 0, 0, "red")
    soft_reset()
    polygon([30, 30], 60, 6, "green")
    polygon([50, 50], 60, 5, "white")
    polygon([70, 70], 60, 4, "red")
    polygon([90, 90], 60, 3, "violet")
    polygon([-50, -50], 60, 12, "violet")
    soft_reset()
    for i in range(3, 8):
        star(3, 50 * (i / 2), "blue", True)
        star(5, 70 * (i / 2), "red", True)
        star(7, 90 * (i / 2), "green", True)
        star(9, 110 * (i / 2), "white", True)
 #   MainTurtle.right(90)
    soft_reset()
    for i in range(0, 10):
        string_to_turtle("NNNNNNNNEEEEEEEEEESSSSSSSSSSWWWWWWWWWW+W-", 5, "yellow")
    MainTurtle.home
    for i in range(0, 10):
        string_to_turtle("NNWWSSEN", 20, "orange")
    soft_reset()    
    random_lines(200, "white", 1)
    soft_reset()
    random_lines(337)
    soft_reset()
    #koch_curve(10, 100)
    for i in range(1, 11):
        MainTurtle.setpos(0, 0)
        koch_generate(90 / i, 5, "violet")
        koch_generate(90 / i*i, 5, "red")
    soft_reset()
    circle([0, 0], 10, "white")
    soft_reset()
    tree(10)
    return
    circle([120, 120], 40, "green")
    circle([25, 25], 80, "red")
    circle([80, 25], 40, "blue")

#Update (main) loop
def process():
    pass

#Drawing
def draw():
    pass

#Stop game
def stop():
    #global isRunning
    isRunning = False

#Input handler 
#NOTE: pygame input does not work without initializing the pygame screen
def get_input():
    #Inputs
    turtle.onkey(stop, "q")

#Main function
def main():
    print("Starting program...")
    print("SDL Version: " + str(pygame.get_sdl_version()))
    print("Program title: " + title)
    print("Program version: " + version)
    print("Screen size: " + str(screen_surface.window_width()) + " X " + str(screen_surface.window_height()))
    random.seed()    
    clock = pygame.time.Clock()
    #Frame skipping for quicker animation
    animation_speed = 0
   # screen_surface.tracer(animation_speed)
    #Listen for input
    turtle.listen()  
    init()
    #Program cycle
    global isRunning
    isRunning = True
    #while isRunning == True:
    #    get_input()
    #    process()
    #    draw()
        #Update clock
    #    clock.tick(FPS)
    #Exit program
 #   exitonclick()
    user_input = raw_input("Press enter to close: ")
    print("Closing program...")
    pygame.mixer.quit()
    pygame.quit()
    turtle.bye() 
   # user_input = raw_input("Some input please: ")

#Program start
if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.mixer.quit()
        pygame.quit()
        turtle.bye()        
        #input()
