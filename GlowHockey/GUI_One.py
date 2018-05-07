from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame import *
from Game import *
from GUI_Two import *
class GUI_One:
    def __init__(self):
        self.textures = []
        self.Com_Step = 0
        self.Width_Size = 500
        self.Height_Size = 650
        self.time_interval = 1
        self.keystrokes = [False] * 255
    #to know which key is pressed
    def Key_Pressed(self, key, x, y):
        self.keystrokes[ord(key)] = True
    #to know whick key is not pressed
    def Key_Up(self, key, x, y):
        self.keystrokes[ord(key)] = False
    #intialization
    def InitGL(self, Width, Height):
        glClearColor(0.5, 0.5, 0.5, 0.0)  # Clear the background color to black.
        glClearDepth(1.0)  # Clear the Depth buffer.
        glDepthFunc(GL_LESS)  # The type Of depth test to do.
        glEnable(GL_DEPTH_TEST)  # Leave this Depth Testing and observe the visual weirdness.
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()  # Reset The Projection Matrix.
        gluPerspective(39, float(Width) / float(Height), 0.1, 100.0)
        gluLookAt(0, 0, 6, 0, 0, 0, 0, 1, 0)
        # Aspect ratio. Make window resizable.
        #glDisable(GL_COLOR_MATERIAL)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        #glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_ADD)
        glMatrixMode(GL_MODELVIEW)
    #loading Texture(background) loading image
    def LoadTextures(self):
        image = pygame.image.load('G3.png')
        image_x = image.get_width()
        image_y = image.get_height()
        raw_image = pygame.image.tostring(image, "RGBA", 1)
        self.textures = glGenTextures(1)
        self.Texture_Setup(raw_image, image_x, image_y, 0)
    #Setup Texture with his features
    def Texture_Setup(self, raw_image, x, y, idx):
        glBindTexture(GL_TEXTURE_2D, self.textures)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, x, y, 0, GL_RGBA, GL_UNSIGNED_BYTE, raw_image)
    #Puting texture in world
    def Draw_Background(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.textures)
        glBegin(GL_QUADS)
        glTexCoord(0, 0)
        glVertex3f(-2, -2.5, -1.0)  # Bottom Left of The Texture and Quad
        glTexCoord(1, 0)
        glVertex3f(2, -2.5, -1.0)  # Bottom Right of The Texture and Quad
        glTexCoord(1, 1)
        glVertex3f(2, 2.5, -1.0)  # Top Right of The Texture and Quad
        glTexCoord(0, 1)
        glVertex3f(-2.0, 2.5, -1.0)# Top Left of The Texture and Quad
        glEnd()
    #Controlling for Bottom_Player
    def keyboard(self):
        if self.keystrokes[ord('o')]:
            gui_two = GUI_Two()
            gui_two.main()
        elif self.keystrokes[ord('t')]:
            game = Game(False, False, 0)
            game.main()
    def Display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        #glColor4f(0.1, 0.1, 0.1, 1)
        self.Draw_Background()
        self.keyboard()
        glutSwapBuffers()


    def Timer(self, v):
        self.Display()
        glutTimerFunc(self.time_interval, self.Timer, 1)
    def main(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(self.Width_Size, self.Height_Size)
        glutInitWindowPosition(0, 0)
        glutCreateWindow(b"Simple Ball Bat OpenGL game")
        self.LoadTextures()
        glutDisplayFunc(self.Display)
        glutTimerFunc(self.time_interval, self.Timer, 1)
        glutKeyboardFunc(self.Key_Pressed)
        glutKeyboardUpFunc(self.Key_Up)
        #glutPassiveMotionFunc(MouseMotion)
        self.InitGL(self.Width_Size, self.Height_Size)
        glutMainLoop()
gui_one = GUI_One()
gui_one.main()
