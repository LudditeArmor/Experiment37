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
    MainTurtle.pendown()
    for x in range(0, length):
        y = math.sin(math.radians(x * frequancy)) * amplitude
        MainTurtle.goto(x + offsetX, y + offsetY)

#Draw simple line
def line(source, destination, color="white"):
    MainTurtle.color(color)
    MainTurtle.penup()
    MainTurtle.setpos(source[0], source[1])
    MainTurtle.pendown()
    MainTurtle.setpos(destination[0], destination[1])

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
    
#Init of program (run once before main program cycle)
def init():
    koch_generate(50, 20, "violet")
    test_debug()

#Testing and debugging
def test_debug():
    MainTurtle.reset()
    wave()
    wave([0,0], 360, 20, 60, 0, 0, "red")
    MainTurtle.reset()
    polygon([30, 30], 60, 6, "green")
    polygon([50, 50], 60, 5, "white")
    polygon([70, 70], 60, 4, "red")
    polygon([90, 90], 60, 3, "violet")
    polygon([-50, -50], 60, 12, "violet")
    MainTurtle.reset()
    for i in range(3, 8):
        star(3, 50 * (i / 2), "blue", True)
        star(5, 70 * (i / 2), "red", True)
        star(7, 90 * (i / 2), "green", True)
        star(9, 110 * (i / 2), "white", True)
 #   MainTurtle.right(90)
    MainTurtle.reset()
    for i in range(0, 10):
        string_to_turtle("NNNNNNNNEEEEEEEEEESSSSSSSSSSWWWWWWWWWW+W-", 5, "yellow")
    MainTurtle.home
    for i in range(0, 10):
        string_to_turtle("NNWWSSEN", 20, "orange")
    MainTurtle.reset()    
    #koch_curve(10, 100)
    for i in range(1, 11):
        MainTurtle.setpos(0, 0)
        koch_generate(90 / i, 5, "violet")
        koch_generate(90 / i*i, 5, "red")
    MainTurtle.reset()
    circle([0, 0], 10, "white")
    MainTurtle.reset()
    tree(40)
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
