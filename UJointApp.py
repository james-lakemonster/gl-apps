from Model import *
from Viewer import *
from Controller import *
from PlayControls import FixedStepPC
import math

class UJointController(Controller):
  def loadControls(self):
    super().loadControls()
    self.controls['show_triads'] = False
    self.controls['velocity_constraint'] = False
    self.controls['torque'] = 0.0

  def cyclicInit(self):
    self.controls["torque"] = 0.0
    self.controls["stop"] = False

  def toggleVelocityConstaint(self):
    self.controls['velocity_constraint'] = not self.controls['velocity_constraint']
    if self.controls['velocity_constraint']:
      print("Velocity constraints are enabled")
    else:
      print("Position constraints are enabled")

  def loadKeyCallbacks(self):
    super().loadKeyCallbacks()
    self.keyCallbacks[pygame.K_t] = {
      'key_help_name': 'T',
      'type': 'tap',
      'description': 'Show/Hide unit vector triads',
      'callback': lambda: self.toggleControl('show_triads')
      }
    self.keyCallbacks[pygame.K_v] = {
      'key_help_name': 'V',
      'type': 'tap',
      'description': 'Toggle velocity/position constraints',
      'callback': self.toggleVelocityConstaint
      }
    self.keyCallbacks[pygame.K_SPACE] = {
      'key_help_name': 'SPACEBAR',
      'type': 'held',
      'description': 'Stop all rotation',
      'callback': lambda: self.setControl('stop', True)
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
    self._states["angle1"] = 0.0
    self._states["angle2"] = 0.0
    self.stop()

  def stop(self):
    self._states["input_angle_dot"] = 0.0

  def update(self, dt, controls: dict):
    super().update(dt, controls)

    if controls['stop']:
      controls['torque'] = 0.0
      self.stop()
    elif controls['velocity_constraint']:
      self.velocityUpdate(dt, controls)
    else:
      self.positionUpdate(dt, controls)

    self.wrapAngles()

  def positionUpdate(self, dt, controls: dict):
    states = self._states

    # compute the state derivatives
    states['input_angle_dot'] += controls['torque'] * 360.0 * dt

    # advance the states
    states['input_angle'] += states['input_angle_dot'] * dt

    # the remaining angles are direct functions of the input shaft state
    theta = states['input_angle']*math.pi/180.0
    phi   = -math.pi/4 # inclination angle
    alpha = math.atan(math.cos(theta)*math.tan(phi))
    beta  = math.asin(-math.sin(theta)*math.sin(phi))

    states['angle1'] = alpha * 180.0 / math.pi
    states['angle2'] = beta * 180.0 / math.pi

  def velocityUpdate(self, dt, controls: dict):
    states = self._states

    # compute the state derivatives
    states['input_angle_dot'] += controls['torque'] * 360.0 * dt
    theta_dot = states['input_angle_dot']*math.pi/180.0

    q1 = states['angle1']*math.pi/180.0
    q2 = states['angle2']*math.pi/180.0
    phi_dot = theta_dot * math.cos(q1) / math.cos(q2)

    q1_dot = phi_dot * math.sin(q2)
    q2_dot = -theta_dot * math.sin(q1)

    states['input_angle'] += states['input_angle_dot'] * dt
    states['angle1'] += q1_dot * dt * 180.0 / math.pi
    states['angle2'] += q2_dot * dt * 180.0 / math.pi

  def wrapAngles(self):
    states = self._states
    if states['input_angle'] > 360:
      states['input_angle'] -= 360
    if states['input_angle'] < -360:
      states['input_angle'] += 360

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
  UJointController(UJointModel(), UJointViewer(), FixedStepPC()).run()

main()
