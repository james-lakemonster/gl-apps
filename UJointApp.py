from Model import *
from Viewer import *
from Controller import *
import math

class UJointController(Controller):
  def loadControls(self):
    super().loadControls()
    self.controls['show_triads'] = False
    self.controls['torque'] = 0.0

  def cyclicInit(self):
    self.controls["torque"] = 0.0

  def loadKeyCallbacks(self):
    super().loadKeyCallbacks()
    self.keyCallbacks[pygame.K_t] = {
      'key_help_name': 'T',
      'type': 'tap',
      'description': 'Show/Hide unit vector triads',
      'callback': lambda: self.toggleControl('show_triads')
      }
    self.keyCallbacks[pygame.K_RIGHT] = {
      'key_help_name': 'ARROW_RIGHT/LEFT',
      'type': 'held',
      'description': 'Increase/Decrease angular rotation speed',
      'callback': lambda: self.setControl('torque', self.controls['torque'] + 1.0)
      }
    self.keyCallbacks[pygame.K_LEFT] = {
      'key_help_name': None,
      'type': 'held',
      'description': '',  # this key is documented with the RIGHT ARROW
      'callback': lambda: self.setControl('torque', self.controls['torque'] - 1.0)
      }

class UJointModel(Model):
  def __init__(self):
    super().__init__()
    self._states["input_angle"] = 0.0
    self._states["input_angle_dot"] = 0.0
    self._states["angle1"] = 0.0
    self._states["angle2"] = 0.0

  def update(self, dt, controls: dict):
    super().update(dt, controls)
    states = self._states

    # integrate the states
    states['input_angle'] += states['input_angle_dot'] * dt
    states['input_angle_dot'] += controls['torque'] * 360.0 * dt

    # some specified motions for a U joint
    theta = states['input_angle']*math.pi/180.0
    phi   = -math.pi/4
    alpha = math.atan(math.cos(theta)*math.tan(phi))
    beta  = math.asin(-math.sin(theta)*math.sin(phi))

    states['angle1'] = alpha * 180.0 / math.pi
    states['angle2'] = beta * 180.0 / math.pi

    # apply constraints (incase any states are out of bounds)

    # wrap the angle
    if states['input_angle'] > 360:
      states['input_angle'] -= 360
    if states['input_angle'] < -360:
      states['input_angle'] += 360

    # do not admit backwards motion
    if states["input_angle_dot"] < 0.0:
      states["input_angle_dot"] = 0.0

class UJointViewer(Viewer):
  def __init__(self):
    super().__init__("A Universal Joint")

  def draw(self, modelStates: dict, controlStates: dict):
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
    if controlStates['show_triads']:
      glPushMatrix()
      glTranslatef(-3.0,3.0,-2.0)
      sglTriad(2.0)
      glPopMatrix()

    sglYellowPlasticMaterial()

    glPushMatrix()
    glRotatef(modelStates['input_angle'], 1, 0, 0)

    sglYellowPlasticMaterial()
    glPushMatrix()
    glTranslatef(-3.0,0.0,0.0)
    glRotatef(90, 0, 1, 0)
    sglClosedCylinder(0.2,5.3,8)
    glPopMatrix()

    sglYellowPlasticMaterial()
    sglAddUJoint(1.0, modelStates['angle1'], modelStates['angle2'])

    sglYellowPlasticMaterial()
    glPushMatrix()
    glTranslatef(3.0,0.0,0.0)
    glRotatef(90, 0, 1, 0)
    sglClosedCylinder(0.2,5.3,8)
    glPopMatrix()

    glPopMatrix()


def main():
  UJointController(UJointModel(), UJointViewer()).run()

main()
