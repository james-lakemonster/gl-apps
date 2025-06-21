import sys
import pygame
from pygame.locals import *

from Model import Model
from Viewer import Viewer
from Controller import Controller
from Timer import Timer
from SimpleGL import *


def drawScene(states):
   sglClear()
   glMatrixMode(GL_MODELVIEW)
   glLoadIdentity()

   sglBasicLight(1.0)

   glPushMatrix()
   glTranslatef(0.0,0.0, -states['z'])
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
   model = Model()
   viewer = Viewer()
   controller = Controller()
   controller.setModel(model)
   controller.setViewer(viewer)

   controller.setup()

   while controller.checkRunRequest():
      # The controller updates the model and view states
      controller.update()

      # respond to any window adjustments
      viewer.checkResize(controller.checkFullScreenRequest())

      # render the new scene
      drawScene(model.getStates())

      # publish
      viewer.publishView()

      # pad runtime as desired
      pygame.time.wait(10)

   pygame.quit()
   sys.exit()

main()

