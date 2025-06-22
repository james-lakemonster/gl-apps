from Model import Model
from Viewer import Viewer
from Controller import Controller
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

  # make the screen coordinates X - right, Y in, Z up
  glRotatef(-90, 1, 0, 0)
  # push the origin away 10 units in Y
  glTranslatef(0.0,3.0,0.0)

  # add a tilt for little off angle viewing perspective
  glRotatef(15, 1, 0, 0)
  glRotatef(-15, 0, 0, 1)

  # draw a reference triad off to the left
  if controller.check('show_hidden'):
    glPushMatrix()
    glTranslatef(-3.0,3.0,-2.0)
    sglTriad(2.0)
    glPopMatrix()

  sglYellowPlasticMaterial()

  glPushMatrix()
  glRotatef(states['angle'], 1, 0, 0)

  sglYellowPlasticMaterial()
  glPushMatrix()
  glTranslatef(-3.0,0.0,0.0)
  glRotatef(90, 0, 1, 0)
  sglClosedCylinder(0.2,5.3,8)
  glPopMatrix()

  sglYellowPlasticMaterial()
  sglAddUJoint(1.0, states['ujoint_angle1'], states['ujoint_angle2'])

  sglYellowPlasticMaterial()
  glPushMatrix()
  glTranslatef(3.0,0.0,0.0)
  glRotatef(90, 0, 1, 0)
  sglClosedCylinder(0.2,5.3,8)
  glPopMatrix()

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
