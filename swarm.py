import math
import random
import turtle
from entities import *
import configuration

class Arena:            ### Arena Class

    def __init__(self,configuration):       ### Constructor 
        self.attract_creature = configuration[0]
        self.repel_creature = configuration[1]
        self.light_config = configuration[2]

        self.WINDOW_XDIM = 900
        self.WINDOW_YDIM = 800
        
        self.SCREEN_XDIM = self.WINDOW_XDIM -150
        self.SCREEN_YDIM = self.WINDOW_YDIM -150

        self.creatures = []
        self.lights = []


    def drawRectangle(self,inTurtle, width, height):            ### Draw Rectangle
        inTurtle.begin_fill()
        inTurtle.begin_poly()  

        for el in [ width, height, width, height ]:
            inTurtle.fd(el)          
            inTurtle.left(90)

        inTurtle.end_poly()
        inTurtle.end_fill()

    def drawPlayArea(self):             ### Draw Play Area
        drawingWindow = turtle.Turtle()
        drawingWindow.hideturtle()
        drawingWindow.speed(0)
        drawingWindow.pu()
        drawingWindow.goto(-self.SCREEN_XDIM//2,-self.SCREEN_YDIM//2)
        drawingWindow.color('red','black')
        drawingWindow.pd()
        self.drawRectangle(drawingWindow, self.SCREEN_XDIM, self.SCREEN_YDIM )

    def drawCreatures(self):        ### Draw Creatures
        RADIUS = 7
        for x in range(self.attract_creature.count):
            creature = Creature('Attract : ' + str(x),RADIUS,self.attract_creature.speed,self.attract_creature.space,self.SCREEN_XDIM,self.SCREEN_YDIM,True)
            self.creatures.append(creature)
            print (creature)
        for x in range(self.repel_creature.count):
            creature = Creature('Repel : ' + str(x),RADIUS,self.repel_creature.speed,self.repel_creature.space,self.SCREEN_XDIM,self.SCREEN_YDIM,False)
            self.creatures.append(creature)
            print (creature)

    def distance(self,o1,o2):       ### Euclidian Distance Function
        o1 = o1.position
        o2 = o2.position
        distance = math.sqrt((o1.x-o2.x)**2 + (o1.y-o2.y)**2)
        return distance

    def Update(self):       ### Frame Update Function
        
        for x in range(len(self.lights)):           ### Bouncing Lights
            for y in range(len(self.lights)):
                if x != y:
                    light1 = self.lights[x]
                    light2 = self.lights[y]
                    if self.distance(light1,light2) <= light1.radius + light2.radius:
                        light1.heading = light1.DetermineNewHeading([light1.position,light1.heading,light1.speed],light2.position)
        
        for x in range(len(self.creatures)):        ### Bouncing Creatures
            for y in range(len(self.creatures)):
                if x != y:
                    creature1 = self.creatures[x]
                    creature2 = self.creatures[y]
                    if creature1.position == creature2.position:
                        creature1.position.x += creature1.radius
                        creature2.position.y += creature1.radius
                        creature2.position.x += creature1.radius
                        creature2.position.y += creature1.radius

        for creature in self.creatures:     ### Creature Attraction and Repulsion to Light
            for light in self.lights:  
                if self.distance(light,creature) <= creature.radius + light.radius:
                    creature.heading = creature.DetermineNewHeading( [ creature.position, creature.speed, creature.heading ], light.position)
                elif self.distance(light,creature) < creature.space + light.radius + creature.radius and creature.attract:
                    creature.heading = light.heading
                    creature.speed = light.speed *0.8
                elif self.distance(light,creature) < creature.space + light.radius + creature.radius and not creature.attract:
                    creature.heading = light.heading + math.radians(120)
                    creature.speed = light.speed *0.8
        
        for x in self.creatures:    ### Move and Draw Creatures
            x.move(1)
            x.draw()

        for y in self.lights:       ### Move and Draw Lights
            y.move(1)
            y.draw()
                    
    def drawLights(self):           ### Draw Lights
        RADIUS = 15
        for x in range(self.light_config.count):
            light = Light('Light : ' + str(x),RADIUS,self.light_config.speed,self.SCREEN_XDIM,self.SCREEN_YDIM)
            self.lights.append(light)
            print (light)
        

    def InitializeGraphics(self):           ### Initialize Graphics and Setup Screen
        screen = turtle.getscreen()
        screen.setup(self.WINDOW_XDIM,self.WINDOW_YDIM)
        screen.screensize(self.SCREEN_XDIM, self.SCREEN_YDIM)
        self.drawPlayArea()
        self.drawCreatures()
        self.drawLights()

def main() :
  turtle.tracer(0,0)        ### Initialize Turtle Tracer
  test_case = 1 
  arena = Arena(configuration.example[test_case])
  arena.InitializeGraphics()
  try:          ### Try Except Block for Error Handling

    while True:
      arena.Update()        ### Frame Update in Python Turtle
      turtle.update()

  except KeyboardInterrupt:

    print('Done swarming.')    

if __name__ == "__main__" :
  main()
