from Model import Model
from Viewer import Viewer
from Controller import Controller
from UJoint import *
from SimpleGL import *


def drawScene(states, controller):
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
  if controller.check('show_hidden'):
    glPushMatrix()
    glTranslatef(-3.0,0.0,-2.0)
    sglTriad(2.0)
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

  while controller.check('run'):
    # The controller updates the model and view states
    controller.update()

    # render the new scene
    drawScene(model.getStates(), controller)

    # finalize the loop
    controller.finalizeFrame()

  # done - shutdown
  controller.shutdown()

main()
