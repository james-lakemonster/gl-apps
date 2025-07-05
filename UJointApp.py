from Model import Model
from Viewer import Viewer
from Controller import Controller
from SimpleGL import *
import math

class UJointModel(Model):
  def __init__(self):
    super().__init__()
    self.states["angle"] = 0.0
    self.states["angle_dot"] = 0.0
    self.states["ujoint_angle1"] = 0.0
    self.states["ujoint_angle2"] = 0.0

  def update(self, dt, controls):
    self.time += dt
    states = self.states

    # integrate the states
    states['angle'] += states['angle_dot'] * dt
    states['angle_dot'] += controls['torque'] * 360.0 * dt

    # some specified motions for a U joint
    theta = states['angle']*math.pi/180.0
    phi   = -math.pi/4
    alpha = math.atan(math.cos(theta)*math.tan(phi))
    beta  = math.asin(-math.sin(theta)*math.sin(phi))

    states['ujoint_angle1'] = alpha * 180.0 / math.pi
    states['ujoint_angle2'] = beta * 180.0 / math.pi

    # apply constraints (incase any states are out of bounds)

    # wrap the angle
    if states['angle'] > 360:
      states['angle'] -= 360
    if states['angle'] < -360:
      states['angle'] += 360

    # do not admit backwards motion
    if states["angle_dot"] < 0.0:
      states["angle_dot"] = 0.0

  def draw(self, controller = None):
    states = self.states

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
  model = UJointModel()
  viewer = Viewer()
  controller = Controller(model, viewer)

  while controller.check('run'):
    # The controller updates the model and view states
    controller.update()

    # render the new scene
    model.draw(controller)

    # finalize the loop
    controller.finalizeFrame()

  # done - shutdown
  controller.shutdown()

main()
