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
   states['objectSpeed'] = 0.1
   return states

def updateStates(states, controls):
   # increment the angle
   states['angle'] += states['angleSpeed']

   #wrap the angle
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

   #user applied force and torque
   states["objectSpeed"] += controls["force"] * 0.005
   if states["objectSpeed"] < 0.0:
      states["objectSpeed"] = 0.0

   states["angleSpeed"] += controls["torque"] * 0.1
   if states["angleSpeed"] < 0.0:
      states["angleSpeed"] = 0.0
            

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


class Viewer:

   def __init__(self):
      self.run = True

   def setup(self):
      pygame.init()
      pygame.display.set_mode((800,600), DOUBLEBUF|OPENGL|RESIZABLE)
      pygame.display.set_caption("SimpleGL Demo App")
      windowSize = None
      fullscreen = False




def main():
   pygame.init()
   pygame.display.set_mode((800,600), DOUBLEBUF|OPENGL|RESIZABLE)
   pygame.display.set_caption("SimpleGL Demo App")
   windowSize = None

   sglInit()

   states = initStates()
   controller = Controller()

   fullscreen = False

   while controller.checkRunRequest():
      controller.update()

      #view.checkResize(controller.checkFullScreenRequest())

      if controller.checkFullScreenRequest() != fullscreen:
         pygame.display.toggle_fullscreen()
         fullscreen = not fullscreen

      # if the window has changed then compute the new perspective
      # and restore some basic intializations
      newWindowSize = pygame.display.get_window_size()
      if newWindowSize != windowSize:
         windowSize = newWindowSize
         glMatrixMode(GL_PROJECTION)
         glLoadIdentity()
         gluPerspective(45, (windowSize[0]/windowSize[1]), 0.1, 50.0)
         sglReInit()
         

      updateStates(states, controller.getOutputs())

      sglClear()
      drawScene(states)
      pygame.display.flip()

      pygame.time.wait(10)

   pygame.quit()
   sys.exit()

main()

