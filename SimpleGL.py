from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

sglQuadric = gluNewQuadric()
sglClearColor = (0.3, 0.3, 0.3, 1.0)

#
# Initialization Functions
#

def sglSetClearColor(r,g,b,a):
  global sglClearColor
  sglClearColor = (r,g,b,a)
  glClearColor(sglClearColor[0],sglClearColor[1],sglClearColor[2],sglClearColor[3])

def sglClear():
  glClearColor(sglClearColor[0],sglClearColor[1],sglClearColor[2],sglClearColor[3])
  glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

def sglReInit():
  glShadeModel(GL_SMOOTH)
  glEnable(GL_DEPTH_TEST)
  glDepthFunc(GL_LESS)
  glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
  glPolygonMode(GL_FRONT, GL_FILL)

def sglInit():
  glutInit()
  sglReInit()
  sglClear()
  glClearDepth(1.0)

def sglBasicLight(light_scale = 0.8):
  LightAmbient  = GLfloat_4( 0.5*light_scale, 0.5*light_scale, 0.5*light_scale, 1.0)
  LightDiffuse  = GLfloat_4( 0.8*light_scale, 0.8*light_scale, 0.8*light_scale, 1.0)
  LightSpecular = GLfloat_4( 0.5*light_scale, 0.5*light_scale, 0.5*light_scale, 1.0)
  LightPosition = GLfloat_4( 10000.0, 10000.0, 10000.0, 1.0)

  glLightfv(GL_LIGHT1, GL_AMBIENT, LightAmbient)
  glLightfv(GL_LIGHT1, GL_DIFFUSE, LightDiffuse)
  glLightfv(GL_LIGHT1, GL_SPECULAR, LightSpecular)
  glLightfv(GL_LIGHT1, GL_POSITION, LightPosition)

  glEnable(GL_LIGHT1)
  glEnable(GL_LIGHTING)
  glEnable(GL_BLEND)
  glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


#
# Basic Shapes Library
#

def sglBox(length,height,width):
  l2 = length*0.5
  h2 = height*0.5
  w2 = width*0.5

  glBegin(GL_QUADS);
  # Front Face
  glNormal3f( 0.0, 0.0, 1.0)  # Normal Pointing forward
  glVertex3f(-l2, -h2,  w2)   # Point 1 (Front)
  glVertex3f( l2, -h2,  w2)   # Point 2 (Front)
  glVertex3f( l2,  h2,  w2)   # Point 3 (Front)
  glVertex3f(-l2,  h2,  w2)   # Point 4 (Front)
  # Back Face
  glNormal3f( 0.0, 0.0,-1.0)  # Normal Pointing backward
  glVertex3f(-l2, -h2, -w2)   # Point 1 (Back)
  glVertex3f(-l2,  h2, -w2)   # Point 2 (Back)
  glVertex3f( l2,  h2, -w2)   # Point 3 (Back)
  glVertex3f( l2, -h2, -w2)   # Point 4 (Back)
  # Top Face
  glNormal3f( 0.0, 1.0, 0.0)  # Normal Pointing Up
  glVertex3f(-l2,  h2, -w2)   # Point 1 (Top)
  glVertex3f(-l2,  h2,  w2)   # Point 2 (Top)
  glVertex3f( l2,  h2,  w2)   # Point 3 (Top)
  glVertex3f( l2,  h2, -w2)   # Point 4 (Top)
  # Bottom Face
  glNormal3f( 0.0,-1.0, 0.0)  # Normal Pointing Down
  glVertex3f(-l2, -h2, -w2)   # Point 1 (Bottom)
  glVertex3f( l2, -h2, -w2)   # Point 2 (Bottom)
  glVertex3f( l2, -h2,  w2)   # Point 3 (Bottom)
  glVertex3f(-l2, -h2,  w2)   # Point 4 (Bottom)
  # Right face
  glNormal3f( 1.0, 0.0, 0.0)  # Normal Pointing Right
  glVertex3f( l2, -h2, -w2)   # Point 1 (Right)
  glVertex3f( l2,  h2, -w2)   # Point 2 (Right)
  glVertex3f( l2,  h2,  w2)   # Point 3 (Right)
  glVertex3f( l2, -h2,  w2)   # Point 4 (Right)
  # Left Face
  glNormal3f(-1.0, 0.0, 0.0)  # Normal Pointing Left
  glVertex3f(-l2, -h2, -w2)   # Point 1 (Left)
  glVertex3f(-l2, -h2,  w2)   # Point 2 (Left)
  glVertex3f(-l2,  h2,  w2)   # Point 3 (Left)
  glVertex3f(-l2,  h2, -w2)   # Point 4 (Left)
  glEnd()

def sglCylinder(radius, height, res = 32):
  global sglQuadric
  h2 = 0.5*height

  glPushMatrix()
  glTranslatef(0.0,0.0, -h2)
  gluCylinder(sglQuadric,radius,radius,height,res,res)
  glPopMatrix()

def sglCappedCylinder(radius, height, res = 32):
  global sglQuadric
  h2 = 0.5*height

  glPushMatrix()
  glTranslatef(0.0,0.0, -h2)
  gluCylinder(sglQuadric,radius,radius,height,res,res)
  glPopMatrix()

  glPushMatrix()
  glTranslatef(0.0,0.0,h2)
  gluDisk(sglQuadric,0.0,radius,res,3)
  glPopMatrix()

def sglClosedCylinder(radius, height, res = 32):
  global sglQuadric
  h2 = 0.5*height

  glPushMatrix()
  glTranslatef(0.0,0.0, -h2)
  gluCylinder(sglQuadric,radius,radius,height,res,res)
  glRotatef(180.0,0.0,1.0,0.0)
  gluDisk(sglQuadric,0.0,radius,res,3)
  glPopMatrix()

  glPushMatrix()
  glTranslatef(0.0,0.0,h2)
  gluDisk(sglQuadric,0.0,radius,res,3)
  glPopMatrix()

def sglSphere(radius, res = 32):
  glutSolidSphere(radius,res,res)

#
# Materials Library
#
def sglBlackPlasticMaterial():
  glMaterialfv(GL_FRONT, GL_AMBIENT, GLfloat_4( 0.15, 0.15, 0.15, 1.0))
  glMaterialfv(GL_FRONT, GL_DIFFUSE, GLfloat_4( 0.15, 0.15, 0.15, 1.0))
  glMaterialfv(GL_FRONT, GL_SPECULAR, GLfloat_4( 0.5, 0.5, 0.5, 1.0))
  glMaterialfv(GL_FRONT, GL_SHININESS, 32)

def sglRedPlasticMaterial():
  glMaterialfv(GL_FRONT, GL_AMBIENT, GLfloat_4( 0.8, 0.0, 0.0, 1.0))
  glMaterialfv(GL_FRONT, GL_DIFFUSE, GLfloat_4( 0.8, 0.0, 0.0, 1.0))
  glMaterialfv(GL_FRONT, GL_SPECULAR, GLfloat_4( 0.8, 0.0, 0.0, 1.0))
  glMaterialfv(GL_FRONT, GL_SHININESS, 50)

def sglGreenPlasticMaterial():
  glMaterialfv(GL_FRONT, GL_AMBIENT, GLfloat_4( 0.0, 0.8, 0.0, 1.0))
  glMaterialfv(GL_FRONT, GL_DIFFUSE, GLfloat_4( 0.0, 0.8, 0.0, 1.0))
  glMaterialfv(GL_FRONT, GL_SPECULAR, GLfloat_4( 0.0, 0.8, 0.0, 1.0))
  glMaterialfv(GL_FRONT, GL_SHININESS, 50)

def sglBluePlasticMaterial():
  glMaterialfv(GL_FRONT, GL_AMBIENT, GLfloat_4( 0.0, 0.0, 0.8, 1.0))
  glMaterialfv(GL_FRONT, GL_DIFFUSE, GLfloat_4( 0.0, 0.0, 0.8, 1.0))
  glMaterialfv(GL_FRONT, GL_SPECULAR, GLfloat_4( 0.0, 0.0, 0.8, 1.0))
  glMaterialfv(GL_FRONT, GL_SHININESS, 50)

def sglYellowPlasticMaterial():
  glMaterialfv(GL_FRONT, GL_AMBIENT, GLfloat_4( 0.6, 0.4, 0.0, 1.0))
  glMaterialfv(GL_FRONT, GL_DIFFUSE, GLfloat_4( 0.6, 0.4, 0.0, 1.0))
  glMaterialfv(GL_FRONT, GL_SPECULAR, GLfloat_4( 0.6, 0.4, 0.04, 1.0))
  glMaterialfv(GL_FRONT, GL_SHININESS, 50)

def sglLED_OFF_Material():
  glMaterialfv(GL_FRONT, GL_AMBIENT, GLfloat_4( 0.2, 0.2, 0.3, 1.0))
  glMaterialfv(GL_FRONT, GL_DIFFUSE, GLfloat_4( 0.2, 0.2, 0.3, 1.0))
  glMaterialfv(GL_FRONT, GL_SPECULAR, GLfloat_4( 0.2, 0.2, 0.3, 1.0))
  glMaterialfv(GL_FRONT, GL_SHININESS, 32)

def sglLED_ON_Material():
  glMaterialfv(GL_FRONT, GL_AMBIENT, GLfloat_4( 0.4, 0.4, 0.6, 1.0))
  glMaterialfv(GL_FRONT, GL_DIFFUSE, GLfloat_4( 0.4, 0.4, 0.6, 1.0))
  glMaterialfv(GL_FRONT, GL_SPECULAR, GLfloat_4( 0.0, 0.0, 0.0, 0.0))
  glMaterialfv(GL_FRONT, GL_SHININESS, 32)

def sglLightBeamMaterial():
  glMaterialfv(GL_FRONT, GL_AMBIENT, GLfloat_4( 0.4, 0.4, 0.6, 0.5))
  glMaterialfv(GL_FRONT, GL_DIFFUSE, GLfloat_4( 0.4, 0.4, 0.6, 0.5))
  glMaterialfv(GL_FRONT, GL_SPECULAR, GLfloat_4( 0.0, 0.0, 0.0, 0.0))
  glMaterialfv(GL_FRONT, GL_SHININESS, 0)

def sglLogoMaterial():
  glMaterialfv(GL_FRONT, GL_AMBIENT, GLfloat_4( 0.4, 0.4, 0.4, 1.0))
  glMaterialfv(GL_FRONT, GL_DIFFUSE, GLfloat_4( 0.4, 0.4, 0.4, 1.0))
  glMaterialfv(GL_FRONT, GL_SPECULAR, GLfloat_4( 0.4, 0.4, 0.04, 1.0))
  glMaterialfv(GL_FRONT, GL_SHININESS, 50)

def sglTableMaterial():
  glMaterialfv(GL_FRONT, GL_AMBIENT, GLfloat_4( 0.3, 0.25, 0.2, 1.0))
  glMaterialfv(GL_FRONT, GL_DIFFUSE, GLfloat_4( 0.3, 0.25, 0.2, 1.0))
  glMaterialfv(GL_FRONT, GL_SPECULAR, GLfloat_4( 0.3, 0.25, 0.2, 1.0))
  glMaterialfv(GL_FRONT, GL_SHININESS, 50)

#
# Custom Shapes
#

def sglTriad(scale):
  halfScale = 0.5 * scale
  lineScale = 0.033 * scale

  glPushMatrix()

  sglRedPlasticMaterial()
  glTranslatef(halfScale,0.0,0.0)
  sglBox(scale,lineScale,lineScale)

  sglGreenPlasticMaterial()
  glTranslatef(-halfScale,halfScale,0.0)
  sglBox(lineScale,scale,lineScale)

  sglBluePlasticMaterial()
  glTranslatef(0.0,-halfScale,halfScale)
  sglBox(lineScale,lineScale,scale)

  glPopMatrix()

def sglAddUJoint(scale, angle1, angle2):
  drawUJointYoke(scale)

  glRotatef(angle1, 0, 1, 0)
  drawUJointSpider(scale)
  glRotatef(angle2, 0, 0, 1)

  glPushMatrix()
  glRotatef(90, 1, 0, 0)
  glRotatef(180, 0, 1, 0)
  drawUJointYoke(scale)
  glPopMatrix()

def drawUJointYoke(scale):
  size = 0.28*scale
  glPushMatrix()
  glTranslatef(-0.25*scale,0.0,0.0)
  glTranslatef(-0.25*scale + 0.5*size,0.0,0.0)
  glRotatef(90, 0, -1, 0)
  sglClosedCylinder(size, size)
  glPopMatrix()

  glPushMatrix()
  glTranslatef(-0.22*scale,0.0,0.0)
  glPushMatrix()
  glTranslatef(0.0,0.22*scale,0.0)
  sglBox(0.56*scale,0.05*scale,0.2*scale)
  glPopMatrix()
  glPushMatrix()
  glTranslatef(0.0,-0.22*scale,0.0)
  sglBox(0.56*scale,0.05*scale,0.2*scale)
  glPopMatrix()
  glPopMatrix()

def drawUJointSpider(scale):
  glPushMatrix()
  sglClosedCylinder(0.03*scale, 0.505*scale)
  glRotatef(90, 1, 0, 0)
  sglClosedCylinder(0.03*scale, 0.505*scale)
  glPopMatrix()
