import sys
import pygame
from pygame.locals import *

from SimpleGL import *
from Controller import *




def initStates():
   states = {}
   states['angle'] = 0.0
   states['distance'] = 5.0
   states['direction'] = 1.0

   states['angleSpeed'] = 1.0
   states['objectSpeed'] = 1.0
   return states

def updateStates(states, controls):
   # increment the angle
   states['angle'] += states['angleSpeed']
   if states['angle'] > 360:
      states['angle'] -= 360
   if states['angle'] < 360:
      states['angle'] += 360

   # update distance
   states['distance'] += states['objectSpeed']*states['direction'];

   # bounce off the near and far walls
   if states['distance'] > 25:
      states['direction'] = -1.0
   if states['distance'] < 5.0:
      states['direction'] = 1.0

   #user input to control specified states (objectSpeed and angleSpeed)
   # keys = controller.getKeyStates()
   # if keys["RIGHT"]:
   #       states["angleSpeed"] += 0.04
   # 
   # if keys["LEFT"]:
   #    states["angleSpeed"] -= 0.04
   #    if states["angleSpeed"] < 0.0:
   #       states["angleSpeed"] = 0.0
   # 
   # if keys["UP"]:
   #    states["objectSpeed"] += 0.01
   # 
   # if keys["DOWN"]:
   #    states["objectSpeed"] -= 0.01
   #    if states["objectSpeed"] < 0.0:
   #       states["objectSpeed"] = 0.0
            

def drawScene(states):
   glMatrixMode(GL_MODELVIEW)
   glLoadIdentity()

   sglBasicLight(1.0)

   glPushMatrix()
   glTranslatef(0.0,0.0, -states['distance'])
   glRotatef(states['angle'], 1, 1, 0)

   sglYellowPlasticMaterial()
   sglBox(1.0,1.0,1.0)
   sglClosedCylinder(0.2, 4)
   glPopMatrix()

   glPushMatrix()
   glTranslatef(-5.0,5.0, -20)
   sglYellowPlasticMaterial()
   sglCylinder(2, 2)
   glPopMatrix()

   glPushMatrix()
   glTranslatef(-5.0,-5.0, -20)
   sglCappedCylinder(1.45, 3.6)
   glPopMatrix()

   glPushMatrix()
   glTranslatef(5.0,5.0, -20)
   sglYellowPlasticMaterial()
   sglSphere(1.75)
   glPopMatrix()



def main():
   pygame.init()
   screen = pygame.display.set_mode((800,600), DOUBLEBUF|OPENGL|RESIZABLE)
   windowSize = None
   sglInit()

   states = initStates()
   controller = Controller()
   fullscreen = False

   while controller.checkRunRequest():
      controller.update()

      # if the window has changed then compute the new perspective
      # and restore some basic intializations
      newWindowSize = pygame.display.get_window_size()
      if newWindowSize != windowSize:
         windowSize = newWindowSize
         glMatrixMode(GL_PROJECTION)
         glLoadIdentity()
         gluPerspective(45, (windowSize[0]/windowSize[1]), 0.1, 50.0)
         sglReInit()
         
      if controller.checkFullScreenRequest() != fullscreen:
         print("fullscreen has toggled!")
         fullscreen = controller.checkFullScreenRequest()

      updateStates(states, controller.getOutputs())

      sglClear()
      drawScene(states)
      pygame.display.flip()

      pygame.time.wait(10)

   pygame.quit()
   sys.exit()

main()

