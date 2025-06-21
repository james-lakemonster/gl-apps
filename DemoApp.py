import sys
import pygame
from pygame.locals import *

from SimpleGL import *
from Viewer import *
from Controller import *
from Timer import *

def initStates():
   states = {}
   states['angle'] = 0.0
   states['distance'] = 5.0
   states['direction'] = 1.0

   states['angleSpeed'] = 90.0
   states['objectSpeed'] = 0.0
   return states

def updateStates(states, dt, controls):
   # increment the angle
   states['angle'] += states['angleSpeed'] * dt

   #wrap the angle
   if states['angle'] > 360:
      states['angle'] -= 360
   if states['angle'] < 360:
      states['angle'] += 360

   # update distance
   states['distance'] += states['objectSpeed'] * states['direction'] * dt;

   # bounce off the near and far walls
   if states['distance'] > 25:
      states['direction'] = -1.0
   if states['distance'] < 5.0:
      states['direction'] = 1.0

   #
   #user applied force and torque
   #

   # m/s^2 acceleration
   states["objectSpeed"] += controls["force"] * 10.0 * dt
   if states["objectSpeed"] < 0.0:
      states["objectSpeed"] = 0.0

   # deg/s^2 angular acceleration
   states["angleSpeed"] += controls["torque"] * 360.0 * dt
   if states["angleSpeed"] < 0.0:
      states["angleSpeed"] = 0.0
            

def drawScene(states):
   sglClear()
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
   states = initStates()
   viewer = Viewer()
   controller = Controller()
   timer = Timer()

   viewer.setup()

   while controller.checkRunRequest():
      # get the elapsed time since last render start
      dt = timer.mark()

      # get user inputs
      controller.update(dt)

      # update the model
      updateStates(states, dt, controller.getOutputs())

      # respond to any window adjustments
      viewer.checkResize(controller.checkFullScreenRequest())

      # render the new scene
      drawScene(states)

      # publish
      viewer.publishView()

      # pad runtime as desired
      pygame.time.wait(10)

   pygame.quit()
   sys.exit()

main()

