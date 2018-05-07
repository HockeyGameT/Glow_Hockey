from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 500, 800, 1)  # l,r,b,t,n,f

    glMatrixMode(GL_MODELVIEW)

def drawText(string, x, y):
    glLineWidth(2)
    glColor(1, 1, 0)  # Yellow Color
    glLoadIdentity()
    glTranslate(x, y, 0)
    glScale(0.13, 0.13, 1)
    string = string.encode()  # conversion from Unicode string to byte string
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)

init()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500,800)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Simple Ball Bat OpenGL game");
glutDisplayFunc(Display)
glutTimerFunc(time_interval, Timer, 1)
