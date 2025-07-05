from Model import Model
from Viewer import Viewer
from Controller import Controller
from SimpleGL import *
import math

class BasicModel(Model):
  def __init__(self):
    super().__init__()
    self.states["angle"] = 0.0
    self.states["angle_dot"] = 0.0
    self.states["z"] = 5.0
    self.states["z_speed"] = 0.0
    self.states["z_motion_direction"] = 1.0

  def update(self, dt, controls):
    self.time += dt
    states = self.states

    # integrate the states
    states['z'] += states['z_motion_direction'] * states['z_speed'] * dt;
    states['angle'] += states['angle_dot'] * dt
    states['z_speed'] += controls['force'] * 10.0 * dt
    states['angle_dot'] += controls['torque'] * 360.0 * dt

    # apply constraints (incase any states are out of bounds)

    # wrap the angle
    if states['angle'] > 360:
      states['angle'] -= 360
    if states['angle'] < -360:
      states['angle'] += 360

    # bounce off the near and far walls
    if states['z'] > 25.0:
      states['z'] = 25.0
      states['z_motion_direction'] = -1.0
    if states['z'] < 5.0:
      states['z'] = 5.0
      states['z_motion_direction'] = 1.0

    # do not admit backwards motion
    if states["z_speed"] < 0.0:
      states["z_speed"] = 0.0

    if states["angle_dot"] < 0.0:
      states["angle_dot"] = 0.0


  def draw(self, controls = None):
    states = self.states

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
  model = BasicModel()
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
