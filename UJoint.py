from SimpleGL import *

def drawUJointYoke(scale):
  size = 0.35*scale
  glTranslatef(-0.175*scale,0.0,0.0)
  glPushMatrix()
  glRotatef(90, 0, 1, 0)
  sglClosedCylinder(size, size, 5)
  glPopMatrix()

def drawUJointSpider(size, pinRadius):
  glPushMatrix()
  #sglClosedCylinder(pinRadius, size)
  glRotatef(90, 1, 0, 0)
  #sglClosedCylinder(pinRadius, size)
  glPopMatrix()

def drawUJoint(scale, angle1, angle2):
  glTranslatef(-0.25*scale,0.0,0.0)
  drawUJointYoke(scale)

  glTranslatef(0.25*scale,0.0,0.0)
  glRotatef(angle1, 0, 1, 0)
  drawUJointSpider(0.4*scale, 0.1*scale)
  glRotatef(angle2, 0, 0, 1)

  glTranslatef(0.25*scale,0.0,0.0)
  glRotatef(90, 1, 0, 0)
  glRotatef(180, 0, 1, 0)
  drawUJointYoke(scale)

