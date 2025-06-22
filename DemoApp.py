from Model import Model
from Viewer import Viewer
from Controller import Controller
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

  # draw a dynamic object
  glPushMatrix()
  glTranslatef(0.0,0.0, -states['z'])
  glRotatef(states['angle'], 1, 1, 0)
  sglBox(1.0,1.0,1.0)
  sglClosedCylinder(0.2, 4)
  glPopMatrix()

  # draw an open cylinder in the top left
  glPushMatrix()
  glTranslatef(-5.0,5.0, -20)
  sglCylinder(2, 2)
  glPopMatrix()

  # draw a capped cylinder in the bottom left
  glPushMatrix()
  glTranslatef(-5.0,-5.0, -20)
  sglCappedCylinder(1.45, 3.6)
  glPopMatrix()

  # draw a sphere in the top right
  glPushMatrix()
  glTranslatef(5.0,5.0, -20)
  sglSphere(1.75)
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
    drawScene(model.getStates())

    # finalize the loop
    controller.finalizeFrame()

  # done - shutdown
  controller.shutdown()

main()
