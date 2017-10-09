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

#Playing a sound
def play_sound(path):
  global _sound_library
  sound = _sound_library.get(path)
  if sound == None:
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    sound = pygame.mixer.Sound(canonicalized_path)
    _sound_library[path] = sound
  sound.play()

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

#Draw a circle with center at position with size radius
def circle(pos, radius, color):
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

#Draw a x equal sided polygon at pos
def polygon(pos, size, sides, color):
    MainTurtle.stamp() #origin
    x_center = pos[0]
    y_center = pos[1]
    MainTurtle.up()
    MainTurtle.goto(x_center, y_center)
    MainTurtle.down()
    MainTurtle.color(color)
    for i in range(0, sides):
        MainTurtle.forward(size)
        MainTurtle.left(360/sides)

def koch_init(size):
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
    koch_init(size * math.sin(x))
    x += 1
    MainTurtle.left(60)
    koch_init(size* math.sin(x))
    x += 1
    MainTurtle.right(60*2)
    koch_init(size * math.sin(x))
    x += 1
    MainTurtle.left(60)
    koch_init(size * math.sin(x))
    
#Init of program (run once before main program cycle)
def init():
    polygon([0, 0], 60, 2, "green")
    polygon([50, 50], 60, 5, "white")
    MainTurtle.right(90)
    for i in range(1, 11):
        MainTurtle.setpos(0, 0)
        koch_generate(90 / i, 5, "red")
        koch_generate(90 / i*i, 5, "blue")
    #circle([0, 0], 10, "white")
    #circle([120, 120], 40, "green")
    #circle([25, 25], 80, "red")
    #circle([80, 25], 40, "blue")
    

    #MainTurtle.left(90)
    #MainTurtle.penup() 
    #MainTurtle.setpos(0, 0) 
    #MainTurtle.pendown() 
    #tree(35, MainTurtle)
    #pass
    

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
