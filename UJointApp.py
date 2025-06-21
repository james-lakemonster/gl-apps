from Model import Model
from Viewer import Viewer
from Controller import Controller
from UJoint import *
from SimpleGL import *


def drawScene(states):
  # Basic pre-draw steps
  sglClear()
  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()

  # Turn on a light
  sglBasicLight(1.0)

  # Set the drawing matrial
  sglYellowPlasticMaterial()

  #glTranslatef(0.0,-5.0,-20.0)
  #glRotatef(-90, 1, 0, 0)

  # make the screen coordinates X - right, Y in, Z up
  glRotatef(-90, 1, 0, 0)
  glTranslatef(0.0,10.0,0.0)
  # add a little perspective
  glRotatef(15, 1, 0, 0)
  glRotatef(-15, 0, 0, 1)

  # draw a reference triad off to the left
  glPushMatrix()
  glTranslatef(-3.0,0.0,-2.0)

  glPushMatrix()
  sglRedPlasticMaterial()
  glTranslatef(1.5,0.0,0.0)
  sglBox(3.0,0.1,0.1)
  glPopMatrix()

  glPushMatrix()
  sglGreenPlasticMaterial()
  glTranslatef(0.0,1.5,0.0)
  sglBox(0.1,3.0,0.1)
  glPopMatrix()
  
  glPushMatrix()
  sglBluePlasticMaterial()
  glTranslatef(0.0,0.0,1.5)
  sglBox(0.1,0.1,3.0)
  glPopMatrix()
  
  glPopMatrix()

  sglYellowPlasticMaterial()

  glPushMatrix()
  drawUJoint(1.0, 0.0, 0.0)
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

    # render the new scene
    drawScene(model.getStates())

    # finalize the loop
    controller.finalizeFrame()

  # done - shutdown
  controller.shutdown()

main()
