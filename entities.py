'''
        IMPORT STATEMENTS
'''

import random
import turtle
import math
import copy


''' 
        Class Definitions 
'''

class Position :                        ### Position Class to store (x,y) coordinates
  def __init__(self, x, y):
    self.x = x
    self.y = y

class Vector:                           ### Vector Class to store vector data
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.angle = math.atan2(y,x)

class BaseClass:                        ### Base Class for Light and Creature
    def __init__(self,radius,velocity,MAX_XPOS,MAX_YPOS,color):
        self.radius = radius
        self.MAX_XPOS = MAX_XPOS
        self.MAX_YPOS = MAX_YPOS
        self.position = Position(random.randint(-MAX_XPOS,MAX_XPOS),random.randint(-MAX_YPOS,MAX_YPOS))
        self.heading = math.radians(random.randint(-180,180))
        self.instance = turtle.Turtle()
        self.instance.hideturtle()
        self.speed = velocity
        self.deltaX = 0
        self.deltaY = 0
        self.flag = 0
        self.color = color
        self.store = [copy.deepcopy(self.position),copy.deepcopy(self.heading)]
    
    def Velocity(self,angle, length):           ### Calculates Vector Velocity for the Instance
        x = length*math.cos(angle)
        y = length*math.sin(angle)
        return Vector(x,y)

    def DetermineNewHeading(self, creature, stationary_pos ):           ### Determine Heading for Object after Bouncing
        creature_vel = self.Velocity(creature[1],creature[2])
        collision = Vector( stationary_pos.x-creature[0].x, \
                            stationary_pos.y-creature[0].y )
        collision_tangent = Vector( stationary_pos.y-creature[0].y, \
                                    -(stationary_pos.x-creature[0].x))
        tangent_length = (collision_tangent.x**2 + collision_tangent.y**2)**0.5
        try:
            normal_tangent = Vector( collision_tangent.x/tangent_length, \
                                collision_tangent.y/tangent_length)
        except:
            normal_tangent = Vector( collision_tangent.x/tangent_length, \
                                collision_tangent.y/tangent_length)
        rel_velocity = creature_vel
        length = rel_velocity.x*normal_tangent.x + rel_velocity.y*normal_tangent.y
        tangent_velocity = Vector( normal_tangent.x*length, normal_tangent.y*length)
        perpendicular = Vector(rel_velocity.x-tangent_velocity.x, \
                                rel_velocity.y-tangent_velocity.y )
        new_heading = Vector( (creature_vel.x-2*perpendicular.x), \
                                (creature_vel.y-2*perpendicular.y))
        return new_heading.angle


    def move(self,dt):              ### Changes the Coordinates of the Object at every frame
        if ((self.position.x < self.MAX_XPOS) and (self.position.x > -self.MAX_XPOS)) and ((self.position.y < self.MAX_YPOS) and (self.position.y > -self.MAX_YPOS)):
            distance = dt*self.speed
            self.deltaX = distance*math.cos(self.heading)
            self.deltaY = distance*math.sin(self.heading)
            self.position.x += self.deltaX
            self.position.y += self.deltaY
            self.store = [copy.deepcopy(self.position),copy.deepcopy(self.heading)]
            self.flag = 0
        
        else:
            cret = [self.position,self.heading,self.speed]

            if (self.position.x < self.MAX_XPOS) and (self.position.x > -self.MAX_XPOS):
                stationary_pos = Position(self.position.x,self.MAX_YPOS)    
            else: 
                stationary_pos = Position(self.MAX_XPOS,self.position.y)
                    
            self.heading = self.DetermineNewHeading(cret,stationary_pos)
            distance = dt*self.speed
            self.deltaX = distance*math.cos(self.heading)
            self.deltaY = distance*math.sin(self.heading)
            self.position.x += self.deltaX
            self.position.y += self.deltaY
            

class Creature(BaseClass):              ### Creature Class inherited from Base Class
    def __init__(self,name,radius,velocity,space,MAX_XPOS,MAX_YPOS,attract):            ### Constructor
        self.name = name
        self.space = space
        self.attract = attract

        if self.attract:
            self.color = 'Yellow'           ### If the Creature attracts, change color to Yellow
        else:
            self.color = 'Blue'             ### If the Creature repels, change color to Blue

        MAX_XPOS = MAX_XPOS//2 - radius
        MAX_YPOS = MAX_YPOS//2 - radius

        BaseClass.__init__(self,radius,velocity,MAX_XPOS,MAX_YPOS,self.color)          ### Constructor for Base Class

    def draw(self):                 ### Draw the Creature after Updating Coordinates
            self.instance.clear()
            self.instance.penup()
            self.instance.color(self.color)
            self.instance.goto(self.position.x, self.position.y)
            self.instance.dot(self.radius*2)
            self.deltaX = self.radius*math.cos(self.heading)
            self.deltaY = self.radius*math.sin(self.heading)
            self.instance.goto(self.position.x+self.deltaX,self.position.y+self.deltaY)
            self.instance.dot(self.radius*0.75)
        
    def __str__(self):          ### String Function 
        return "{0} the creature is at ({1},{2}) heading angle {3}".format(self.name, self.position.x, self.position.y, self.heading)


class Light(BaseClass):         ### Light Class inherited from Base Class
    def __init__(self,light_number,radius,velocity,MAX_XPOS,MAX_YPOS):          ### Constructor
        MAX_XPOS = MAX_XPOS//2 - radius
        MAX_YPOS = MAX_YPOS//2 - radius

        BaseClass.__init__(self,radius,velocity,MAX_XPOS,MAX_YPOS,'White')

        self.light_number = light_number
        
        self.color = 'White'

    def draw(self):         ### Draw the Light after Updating Coordinates
        self.instance.clear()
        self.instance.penup()
        self.instance.color(self.color)
        self.instance.goto(self.position.x, self.position.y)
        self.instance.dot(self.radius*2)
        self.deltaX = self.radius*math.cos(self.heading)
        self.deltaY = self.radius*math.sin(self.heading)

    def __str__(self):          ### String Function
        return "Light Number {0} is at ({1},{2}) heading angle {3}".format(self.light_number, self.position.x, self.position.y, self.heading)

