#!/usr/bin/python3

import sys
import time
import math
import numpy as np
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
np.random.seed(11)

class GameGL(object):
    config = None
    def __init__(self, config = None):
        self.config = config
    '''
    Is needed for the OpenGL-Library because standard strings are not allowed.
    '''
    def toCString(self, string):
        return bytes(string, "ascii")

class BasicGame(GameGL):

    def __init__(self, name ="PingPong", width = 360, height = 360, alpha = 0.15, gamma = 0.9):
        super
        self.pixelSize  = 30
        # init ball pos
        self.xBall = 5
        self.yBall = 1
        # init bat
        self.xBat = 5
        # init velocity
        self.xV = 1
        self.yV = 1
        # init score
        self.score = 0
        # init window params
        self.windowName = name
        self.width = width
        self.height = height
        # init gamestates and learning params
        self.Q = [[np.random.uniform(0,0.1)] * 3 for _ in range(1111911)]
        self.gamma = gamma
        self.alpha = alpha
        self.epsilon = 0.8
        # init game pixels
        self.fieldx      = 9
        self.fieldy      = 10
        # time per frame
        self.timer      = 0.0001
        # params
        self.le         = 0
        self.calc       = 0
        self.last       = 0
        self.show       = 0


    def keyboard(self, key, x, y):
        # ESC = \x1w
        if key == b'\x1b':
            sys.exit(0)


    def act(self):
        """calculates the possible paths and returns the most valuable action"""
        xBat = self.xBat
        xBall = self.xBall
        yBall = self.yBall
        yV = self.yV
        Vstate = {1:1,-1:0,2:1,-2:1}
        xV = self.xV
        # define state
        state = origin_state = int(100000*yBall + 1000*xBall + 100*xBat + 10*Vstate[xV] + Vstate[yV])

        while yBall:
            # all actions till ball touches y==0
            if np.random.random() < self.epsilon:
                # random action -1,0,1
                action = np.random.randint(-1,2)
            else:
                # own action
                if self.Q[state].index(max(self.Q[state])) == 2:
                    # action -1 is index 2
                    action = -1
                else:
                    action = self.Q[state].index(max(self.Q[state]))

            
            xBat += action
        
            # don't allow puncher to leave the pitch
            if xBat < 0:
                xBat = 0
            if xBat > 9:
                xBat = 9
            
            xBall += xV
            yBall += yV

            # change direction of ball if it's at wall
            if (xBall > self.fieldx or xBall < 1):
                xV = -xV
            if (yBall > self.fieldy or yBall < 1):
                yV = -yV

            # check whether ball on bottom line
            if yBall == 0:
                # check whether ball is at position of player
                if (xBat == xBall 
                    or xBat == xBall -1
                    or xBat == xBall -2):

                    # define rate
                    self.r = 1
                else:
                    self.r = -1
                    
            else:
                    self.r = 0

            # calculate new state
            new_state = int(10000*xBat + 1000*xBall + 100*yBall + 10*Vstate[xV] + Vstate[yV])
            
            # calculate Q
            self.Q[state][action] = self.Q[state][action] + self.alpha * (self.r + self.gamma * np.max(self.Q[new_state]) - self.Q[state][action])
            # set new state
            state = new_state    

        # define next action
        if self.Q[origin_state].index(max(self.Q[origin_state])) == 2:
            action = -1
        else:
            action = self.Q[origin_state].index(max(self.Q[origin_state]))

        # reduce randomness
        self.epsilon -= 0.001*self.epsilon

        return action


    def display(self):
        # clear the screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # reset position
        glLoadIdentity()
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, self.width, 0.0, self.height, 0.0, 1.0)
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity()

        act = self.act()
        self.xBat += act
        
        # don't allow puncher to leave the pitch
        if self.xBat < 0:
            self.xBat = 0
        if self.xBat > 9:
            self.xBat = 9
        
        self.xBall += self.xV
        self.yBall += self.yV

        # change direction of ball if it's at wall
        if (self.xBall > self.fieldx or self.xBall < 1):
            self.xV = -self.xV
        if (self.yBall > self.fieldy or self.yBall < 1):
            self.yV = -self.yV

        if self.yBall == 0 and self.xBall == 0:
            # let game run fast till 97% is done rigth for first time
            # then set slower frametime and let others watch
            if self.last == self.calc / self.le == 1 or not (self.last == self.calc / self.le):
                print("%.2f" % (100 * self.calc / self.le))
                if (self.calc/self.le) >= 0.975:
                    self.timer = 0.1
                    self.show = True

            self.last = self.calc/self.le
            
            self.calc = 0
            self.le = 0

        # check whether ball on bottom line
        if self.yBall == 0:
            # check whther ball is at position of player
            if (self.xBat == self.xBall 
                or self.xBat == self.xBall -1
                or self.xBat == self.xBall -2):
                self.calc += 1
            self.le += 1 

        # repaint
        self.drawBall()
        self.drawComputer()

        # timeout of 100 milliseconds
        time.sleep(self.timer)
        
        glutSwapBuffers()
    

    def start(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(self.toCString(self.windowName))
        #self.init()
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.onResize)
        glutIdleFunc(self.display)
        glutKeyboardFunc(self.keyboard)
        glutMainLoop() 
    
    def updateSize(self):
        self.width  = glutGet(GLUT_WINDOW_WIDTH)
        self.height = glutGet(GLUT_WINDOW_HEIGHT)
    
    def onResize(self, width, height):
        self.width  = width
        self.height = height
    
    def drawBall(self, width = 1, height = 1, x = 5, y = 6, color = (0.0, 1.0, 0.0)):
        x = self.xBall
        y = self.yBall
        xPos = x * self.pixelSize
        yPos = y * self.pixelSize
        # set color
        glColor3f(color[0], color[1], color[2])
        # start drawing a rectangle
        glBegin(GL_QUADS)
        # bottom left point
        glVertex2f(xPos, yPos)
        # bottom right point
        glVertex2f(xPos + (self.pixelSize * width), yPos)
        # top right point
        glVertex2f(xPos + (self.pixelSize * width), yPos + (self.pixelSize * height))
        # top left point
        glVertex2f(xPos, yPos + (self.pixelSize * height))
        glEnd()
    
    def drawComputer(self, width = 3, height = 1, x = 0, y = 0, color = (1.0, 0.0, 0.0)):
        x = self.xBat
        xPos = x * self.pixelSize
        # set a bit away from bottom
        yPos = y * self.pixelSize# + (self.pixelSize * height / 2)
        # set color
        glColor3f(color[0], color[1], color[2])
        # start drawing a rectangle
        glBegin(GL_QUADS)
        # bottom left point
        glVertex2f(xPos, yPos)
        # bottom right point
        glVertex2f(xPos + (self.pixelSize * width), yPos)
        # top right point
        glVertex2f(xPos + (self.pixelSize * width), yPos + (self.pixelSize * height / 4))
        # top left point
        glVertex2f(xPos, yPos + (self.pixelSize * height / 4))
        glEnd()

if __name__ == '__main__':
    game = BasicGame("PingPongQ")
    game.start()
