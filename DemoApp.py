from Model import Model
from Viewer import Viewer
from Controller import Controller
from SimpleGL import *
import math

class DemoModel(Model):
  def __init__(self):
    super().__init__()
    self._states["angle"] = 0.0
    self._states["angle_dot"] = 0.0
    self._states["z"] = 5.0
    self._states["z_speed"] = 0.0
    self._states["z_motion_direction"] = 1.0

  def update(self, dt, controls: dict):
    super().update(dt, controls)
    states = self._states

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


class DemoViewer(Viewer):
  def __init__(self):
    super().__init__("SimpleGL First Demo")

  def draw(self, modelStates: dict, controlStates: dict):
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
    glTranslatef(0.0,0.0, -modelStates['z'])
    glRotatef(modelStates['angle'], 1, 1, 0)
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
  Controller(DemoModel(), DemoViewer()).run()


main()
