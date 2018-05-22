from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *
from Ball import *
from Wall import *
import pyglet
from pygame import *
import pygame
from winsound import *
import winsound
from pygame.tests.base_test import pygame_quit
class Game:
    def __init__(self, option1, option2, speed):
        self.Flag_For_Computer = option1
        self.Flag_For_Mouse = option2
        self.Computer_Step = speed
        self.Width_Size = 500
        self.Height_Size = 650
        self.WINDOW_WIDTH = 4
        self.WINDOW_HEIGHT = 5
        self.Width = 800
        self.Height = 800
        self.ac_Bottom_Player = 0.001
        self.ac_Top_Player = 0.001
        self.Flag_Collision_Top_Player = True
        self.Flag_Collision_Bottom_Player = True
        self.width_wall = 0.32
        self.radius_goal = 0.8
        self.radius_center = 100
        self.radius_ball = 0.15
        self.radius_player_ex = 0.2
        self.radius_player_in = 0.1
        self.Player_Bottom_Score = 0
        self.Player_Top_Score = 0
        self.Center_Player_Top_x = self.WINDOW_WIDTH / 2 - self.WINDOW_WIDTH / 2
        self.Center_Player_Top_y = self.WINDOW_HEIGHT - ((self.WINDOW_HEIGHT - 2 * self.width_wall) / 4) - self.width_wall - self.WINDOW_HEIGHT / 2
        self.Center_Player_Bottom_x = self.WINDOW_WIDTH / 2 - self.WINDOW_WIDTH / 2
        self.Center_Player_Bottom_y = (self.WINDOW_HEIGHT- 2 * self.width_wall) / 4 + self.width_wall - self.WINDOW_HEIGHT / 2
        self.Center_Player_Bottom_x_Prev = self.Center_Player_Bottom_x
        self.Center_Player_Bottom_y_Prev = self.Center_Player_Bottom_y
        self.Center_Player_Top_x_Prev = self.Center_Player_Top_x
        self.Center_Player_Top_y_Prev = self.Center_Player_Top_y
        self.Center_Ball_x = self.WINDOW_WIDTH / 2 - self.WINDOW_WIDTH / 2
        self.Center_Ball_y = self.WINDOW_HEIGHT / 2 - self.WINDOW_HEIGHT / 2 - 0.05
        self.Center_Line = self.WINDOW_HEIGHT / 2 - self.WINDOW_HEIGHT / 2 - 0.05
        self.Center_Ball_x_Prev = self.Center_Ball_x
        self.Center_Ball_y_Prev = self.Center_Ball_y
        self.step_x_ball = 0
        self.step_y_ball = 0
        self.step_x_Top_Player = 0.005
        self.step_y_Top_Player = 0.005
        self.step_x_Bottom_Player = 0.005
        self.step_y_Bottom_Player = 0.005
        self.time_interval = 5
        self.deltat = 1
        self.From_Right = 1
        self.From_Left = 2
        self.From_Top = 3
        self.From_Bottom = 4
        self.Goal_For_Top_Player = 1
        self.Goal_For_Bottom_Player = 2
        self.Collision_Ball_Top_Player = 1
        self.Collision_Ball_Bottom_Player = 2
        self.First_Quarter = 1
        self.Second_Quarter = 2
        self.Third_Quarter = 3
        self.Fourth_Quarter = 4
        self.dist_radius = self.radius_player_ex + self.radius_player_in + self.radius_ball
        self.textures = []
        self.time = 11
        self.keystrokes = [False] * 255
        self.Left_Wall = Wall(0 - self.WINDOW_WIDTH / 2, self.width_wall - self.WINDOW_WIDTH / 2, self.width_wall - self.WINDOW_HEIGHT / 2, self.WINDOW_HEIGHT - self.width_wall - self.WINDOW_HEIGHT / 2)
        self.Right_Wall = Wall(self.WINDOW_WIDTH - self.width_wall - self.WINDOW_WIDTH / 2, self.WINDOW_WIDTH - self.WINDOW_WIDTH / 2, self.width_wall - self.WINDOW_HEIGHT / 2, self.WINDOW_HEIGHT - self.width_wall - self.WINDOW_HEIGHT / 2)
        self.Bottom_Wall = Wall(self.width_wall - self.WINDOW_WIDTH / 2, self.WINDOW_WIDTH - self.width_wall - self.WINDOW_WIDTH / 2, 0 - self.WINDOW_HEIGHT / 2, self.width_wall - self.WINDOW_HEIGHT / 2)
        self.Top_Wall = Wall(self.width_wall - self.WINDOW_WIDTH / 2, self.WINDOW_WIDTH - self.width_wall - self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT - self.width_wall - self.WINDOW_HEIGHT / 2, self.WINDOW_HEIGHT - self.WINDOW_HEIGHT / 2)
        self.Center_Circle = Circle(0, self.radius_center, self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT / 2, self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT / 2, 0, 2 * pi)
        self.Goal_keeper_Bottom = Circle(0, self.radius_goal, self.WINDOW_WIDTH / 2 - self.WINDOW_WIDTH / 2, 0 - self.WINDOW_HEIGHT / 2, self.WINDOW_WIDTH / 2 - self.WINDOW_WIDTH / 2, 0 - self.WINDOW_HEIGHT / 2, 0, pi)
        self.Goal_keeper_Top = Circle(0, self.radius_goal, self.WINDOW_WIDTH / 2 - self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT - self.WINDOW_HEIGHT / 2, self.WINDOW_WIDTH / 2 - self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT - self.WINDOW_HEIGHT / 2, pi, 2 * pi)
        self.Player_Top = Circle(self.radius_player_in, self.radius_player_ex, self.Center_Player_Top_x, self.Center_Player_Top_y, self.Center_Player_Top_x, self.Center_Player_Top_y, 0, 2 * pi)
        self.Player_Bottom = Circle(self.radius_player_in, self.radius_player_ex, self.Center_Player_Bottom_x, self.Center_Player_Bottom_y, self.Center_Player_Bottom_x, self.Center_Player_Bottom_y, 0, 2 * pi)
        self.Ball = Circle(0, self.radius_ball, self.Center_Ball_x, self.Center_Ball_y, self.Center_Ball_x, self.Center_Ball_y, 0, 2 * pi)
    # fn for drawing text
    def drawText(self, string, x, y):
        glLineWidth(2)
        glColor(1, 1, 0)  # Yellow Color
        glLoadIdentity()
        glTranslate(x, y, 0)
        glScale(0.0012, 0.0012, 0.13)
        #glWindowPos3d(0, 1, -0.5)
        string = string.encode()  # conversion from Unicode string to byte string
        for c in string:
            glutStrokeCharacter(GLUT_STROKE_ROMAN, c)
    #fn for prediction for computer player
    def Computer_Player(self, step):
        if self.Ball.y < self.Center_Line:
            if self.Player_Top.x > self.Ball.x:
                self.Player_Top.x -= step
            elif self.Player_Top.x < self.Ball.x:
                self.Player_Top.x += step
        else:
             if self.Player_Top.x > self.Ball.x + self.dist_radius:
                self.Player_Top.x -= step
             elif self.Player_Top.x < self.Ball.x - self.dist_radius:
                self.Player_Top.x += step
             if self.Player_Top.y >= self.Ball.y + self.dist_radius:
                self.Player_Top.y -= step
             elif self.Player_Top.y < self.Ball.y:
                self.Player_Top.y += step
        if not(self.Player_Top.y >= self.Center_Line + self.Player_Top.re + self.Player_Top.ri):
            self.Player_Top.y = self.Center_Line + self.Player_Top.re + self.Player_Top.ri
        if self.Test_Wall(self.Player_Top) == self.From_Right:
            self.Player_Top.x = self.Right_Wall.left - self.Player_Top.re - self.Player_Top.ri
        elif self.Test_Wall(self.Player_Top) == self.From_Left:
            self.Player_Top.x = self.Left_Wall.right + self.Player_Top.re + self.Player_Top.ri
        if self.Test_Wall(self.Player_Top) == self.From_Top:
            self.Player_Top.y = self.Top_Wall.bottom - self.Player_Top.re - self.Player_Top.ri
        elif self.Test_Wall(self.Player_Top) == self.From_Bottom:
            self.Player_Top.y = self.Top_Wall.top + self.Player_Top.re + self.Player_Top.ri
            if (self.Player_Top.x <= self.Left_Wall.right + self.dist_radius):
                self.Player_Top.x += self.step_x_Top_Player
            elif self.Player_Top.x >= self.Right_Wall.left - self.dist_radius:
                self.Player_Top.x -= self.step_x_Top_Player
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
        image = pygame.image.load('ground.jpg')
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
    #Definig Wall
    def DrawWall(self, Wall):
        glLoadIdentity()
        glBegin(GL_QUADS)
        glVertex3f(Wall.left, Wall.bottom, 0)  # Left - Bottom
        glVertex3f(Wall.right, Wall.bottom, 0)
        glVertex3f(Wall.right, Wall.top, 0)
        glVertex3f(Wall.left, Wall.top, 0)
        glEnd()
    #Defining Circle
    def DrawCircle(self, Circle, type):
        glLoadIdentity()
        glBegin(type)
        for i in arange(Circle.s, Circle.e, 0.001):
            x = Circle.r * cos(i) + Circle.x
            y = Circle.r * sin(i) + Circle.y
            glVertex3f(x, y, 0)
        glEnd()
    #Making fn for two players
    def Draw_Player(self, Circle):
        glLoadIdentity()
        glTranslate(Circle.x, Circle.y, -0.5)
        glutSolidTorus(Circle.ri, Circle.re, 30, 30)
    #Making fn for ball
    def Draw_Ball(self, Circle):
        glLoadIdentity()
        glTranslate(Circle.x, Circle.y, -0.5)
        glutSolidSphere(Circle.re, 30, 30)
    #Defining self.Centerline
    def line(self, x, y, x1, y1, r, g, b, typ):
        glColor(r, g, b)
        glBegin(typ)
        glVertex2d(x,y)
        glVertex2d(x1, y1)
        glEnd()
    #Determing Goal or nor and for whom
    def Ball_Goal(self):
        self.sqrt1 = (self.Ball.x - self.Goal_keeper_Bottom.x) ** 2
        self.sqrt2 = (self.Ball.y - self.Goal_keeper_Bottom.y) ** 2
        self.sqrt3 = (self.Ball.x - self.Goal_keeper_Top.x) ** 2
        self.sqrt4 = (self.Ball.y - self.Goal_keeper_Top.y) ** 2
        self.dist1 = sqrt(self.sqrt1 + self.sqrt2)
        self.dist2 = sqrt(self.sqrt3 + self.sqrt4)
        if self.dist1 <= self.Goal_keeper_Bottom.re:
            return self.Goal_For_Top_Player
        if self.dist2 <= self.Goal_keeper_Top.re:
            return self.Goal_For_Bottom_Player
        return 0
    #Determing control for Top Player
    def arrow_press(self, key, x, y):
        if key == GLUT_KEY_RIGHT:
            if self.step_x_Bottom_Player + self.ac_Bottom_Player >= 0.09:
                self.step_x_Bottom_Player += self.ac_Bottom_Player
            if self.step_y_Bottom_Player + self.ac_Bottom_Player >= 0.09:
                self.step_y_Bottom_Player += self.ac_Bottom_Player
        elif key == GLUT_KEY_LEFT:
            if self.step_x_Bottom_Player - self.ac_Bottom_Player >= 0.05:
                self.step_x_Bottom_Player -= self.ac_Bottom_Player
            if self.step_y_Bottom_Player - self.ac_Bottom_Player >= 0.05:
                self.step_y_Bottom_Player -= self.ac_Bottom_Player
        if key == GLUT_KEY_UP:
            if self.step_x_Top_Player + self.ac_Top_Player >= 0.09:
                self.step_x_Top_Player += self.ac_Top_Player
            if self.step_y_Top_Player + self.ac_Top_Player >= 0.09:
                self.step_y_Top_Player += self.ac_Top_Player
        elif key == GLUT_KEY_DOWN:
            if self.step_x_Top_Player - self.ac_Top_Player >= 0.05:
                self.step_x_Top_Player -= self.ac_Top_Player
            if self.step_y_Top_Player - self.ac_Top_Player >= 0.05:
                self.step_y_Top_Player -= self.ac_Top_Player
    #Calculating Sin theta
    def Sin_Theta(self, x, y, x1, y1):
        l = y1 - y
        sqrt1 = (x1 - x) ** 2
        sqrt2 = (y1 - y) ** 2
        dist = sqrt(self.sqrt1 + self.sqrt2)
        return l / dist
    #Calculating cos theta
    def Cos_Theta(self, x, y, x1, y1):
        k = x1 - x
        sqrt1 = (x1 - x) ** 2
        sqrt2 = (y1 - y) ** 2
        dist = sqrt(sqrt1 + sqrt2)
        return k / dist
    #Testing the quarter
    def Test_Quarter(self, x, y, x1, y1):
        if (self.Sin_Theta(x, y, x1, y1) >= 0) and (self.Cos_Theta(x, y, x1, y1) >= 0):
            return self.First_Quarter
        elif (self.Sin_Theta(x, y, x1, y1) >= 0) and (self.Cos_Theta(x, y, x1, y1) <= 0):
            return self.Second_Quarter
        elif (self.Sin_Theta(x, y, x1, y1) <= 0) and (self.Cos_Theta(x, y, x1, y1) <= 0):
            return self.Third_Quarter
        elif (self.Sin_Theta(x, y, x1, y1) <= 0) and (self.Cos_Theta(x, y, x1, y1) >= 0):
            return self.Fourth_Quarter
        return 0
    #Determining Speed of Two Players
    def Speed(self, Player):
        sqrt1 = (Player.x - Player.x_prev) ** 2
        sqrt2 = (Player.y - Player.y_prev) ** 2
        dist = sqrt(sqrt1 + sqrt2)
        if dist <= 0.05:
            return 0.05
        return dist
    #Initialization for positioning Game
    def Again(self):
        self.Ball.x = self.Center_Ball_x
        self.Ball.y = self.Center_Ball_y
        self.Ball.x_prev = self.Center_Ball_x
        self.Ball.y_prev = self.Center_Ball_y
        self.Player_Bottom.x = self.Center_Player_Bottom_x
        self.Player_Bottom.y = self.Center_Player_Bottom_y
        self.Player_Bottom.x_prev = self.Center_Player_Bottom_x
        self.Player_Bottom.y_prev = self.Center_Player_Bottom_y
        self.Player_Top.x = self.Center_Player_Top_x
        self.Player_Top.y = self.Center_Player_Top_y
        self.Player_Top.x_prev = self.Center_Player_Top_x
        self.Player_Top.y_prev = self.Center_Player_Top_y
        self.Flag_Collision_Bottom_Player = True
        self.Flag_Collision_Top_Player = True
        self.time = 11
        self.step_y_ball = 0
        self.step_x_ball = 0
    #Controlling for Top_Player
    def MouseMotion(self, x, y):
        self.Player_Top.x_prev = self.Player_Top.x
        self.Player_Top.y_prev = self.Player_Top.y
        self.Player_Top.x = x / 125 - self.WINDOW_WIDTH / 2
        self.Player_Top.y = y / -130 + self.WINDOW_HEIGHT / 2
        if not(self.Player_Top.y >= self.Center_Line + self.Player_Top.re + self.Player_Top.ri):
            self.Player_Top.y = self.Center_Line + self.Player_Top.re + self.Player_Top.ri
        if self.Test_Wall(self.Player_Top) == self.From_Right:
            self.Player_Top.x = self.Right_Wall.left - self.Player_Top.re - self.Player_Top.ri
        elif self.Test_Wall(self.Player_Top) == self.From_Left:
            self.Player_Top.x = self.Left_Wall.right + self.Player_Top.re + self.Player_Top.ri
        if self.Test_Wall(self.Player_Top) == self.From_Top:
            self.Player_Top.y = self.Top_Wall.bottom - self.Player_Top.re - self.Player_Top.ri
        elif self.Test_Wall(self.Player_Top) == self.From_Bottom:
            self.Player_Top.y = self.Top_Wall.top + self.Player_Top.re + self.Player_Top.ri
    #to know how to determin how b
    def Contorol_For_Handling_Ball(self):
        if self.Player_Bottom.x > self.Ball.x + self.dist_radius:
            self.Player_Bottom.x -= self.step_x_Bottom_Player
        elif self.Player_Bottom.x < self.Ball.x - self.dist_radius:
            self.Player_Bottom.x += self.step_x_Bottom_Player
        if self.Player_Bottom.y >= self.Ball.y + self.dist_radius:
            self.Player_Bottom.y -= self.step_x_Bottom_Player
        elif self.Player_Bottom.y < self.Ball.y:
            self.Player_Bottom.y += self.step_x_Bottom_Player
    #Controlling for Bottom_Player
    def keyboard(self):
        self.Player_Bottom.x_prev = self.Player_Bottom.x
        self.Player_Bottom.y_prev = self.Player_Bottom.y
        self.Player_Top.x_prev = self.Player_Top.x
        self.Player_Top.y_prev = self.Player_Top.y
        if self.keystrokes[ord('a')] == True:
            self.Player_Bottom.x = self.Player_Bottom.x - self.step_x_Bottom_Player
        elif self.keystrokes[ord('d')] == True:
            self.Player_Bottom.x = self.Player_Bottom.x + self.step_x_Bottom_Player
        elif self.keystrokes[ord('w')] == True:
            self.Player_Bottom.y = self.Player_Bottom.y + self.step_y_Bottom_Player
        elif self.keystrokes[ord('x')] == True:
            self.Player_Bottom.y = self.Player_Bottom.y - self.step_y_Bottom_Player
        elif self.keystrokes[ord('e')] == True:
            self.Player_Bottom.x = self.Player_Bottom.x + self.step_x_Bottom_Player
            self.Player_Bottom.y = self.Player_Bottom.y + self.step_y_Bottom_Player
        elif self.keystrokes[ord('c')] == True:
             self.Player_Bottom.x = self.Player_Bottom.x + self.step_x_Bottom_Player
             self.Player_Bottom.y = self.Player_Bottom.y - self.step_y_Bottom_Player
        elif self.keystrokes[ord('q')] == True:
             self.Player_Bottom.x = self.Player_Bottom.x - self.step_x_Bottom_Player
             self.Player_Bottom.y = self.Player_Bottom.y + self.step_y_Bottom_Player
        elif self.keystrokes[ord('z')] == True:
             self.Player_Bottom.x = self.Player_Bottom.x - self.step_x_Bottom_Player
             self.Player_Bottom.y = self.Player_Bottom.y - self.step_y_Bottom_Player
        if not(self.Player_Bottom.y <= self.Center_Line - self.Player_Bottom.re -  self.Player_Bottom.ri):
            self.Player_Bottom.y = self.Center_Line - self.Player_Bottom.re - self.Player_Bottom.ri
        if self.Test_Wall(self.Player_Bottom) == self.From_Right:
            self.Player_Bottom.x = self.Right_Wall.left - self.Player_Bottom.re - self.Player_Bottom.ri
        elif self.Test_Wall(self.Player_Bottom) == self.From_Left:
            self.Player_Bottom.x = self.Left_Wall.right + self.Player_Bottom.re + self.Player_Bottom.ri
        if self.Test_Wall(self.Player_Bottom) == self.From_Top:
            self.Player_Bottom.y = self.Bottom_Wall.bottom - self.Player_Bottom.re - self.Player_Bottom.ri
        elif self.Test_Wall(self.Player_Bottom) == self.From_Bottom:
            self.Player_Bottom.y = self.Bottom_Wall.top + self.Player_Bottom.re + self.Player_Bottom.ri
        """if self.Test_Collision_Ball_Player(self.Player_Bottom) == self.Collision_Ball_Bottom_Player:"""

        """
        if self.keystrokes['g']:
            self.Player_Top.x = self.Player_Top.x - self.step_x_Top_Player
        elif self.keystrokes['j']:
            self.Player_Top.x = self.Player_Top.x + self.step_x_Top_Player
        elif self.keystrokes['y']:
            self.Player_Top.y = self.Player_Top.y + self.step_y_Top_Player
        elif self.keystrokes['n']:
            self.Player_Top.y = self.Player_Top.y - self.step_y_Top_Player
        elif self.keystrokes['u']:
            self.Player_Top.x = self.Player_Top.x + self.step_x_Top_Player
            self.Player_Top.y = self.Player_Top.y + self.step_y_Top_Player
        elif self.keystrokes['m']:
             self.Player_Top.x = self.Player_Top.x + self.step_x_Top_Player
             self.Player_Top.y = self.Player_Top.y - self.step_y_Top_Player
        elif self.keystrokes['r']:
             self.Player_Top.x = self.Player_Top.x - self.step_x_Top_Player
             self.Player_Top.y = self.Player_Top.y + self.step_y_Top_Player
        elif self.keystrokes['b']:
             self.Player_Top.x = self.Player_Top.x - self.step_x_Top_Player
             self.Player_Top.y = self.Player_Top.y - self.step_y_Top_Player
        if not(self.Player_Top.y >= self.Center_Line + self.Player_Top.re + self.Player_Top.ri):
            self.Player_Top.y = self.Center_Line + self.Player_Top.re + self.Player_Top.ri
        if Test_Wall(self.Player_Top) == From_Right:
            self.Player_Top.x = self.Right_Wall.left - self.Player_Top.re - self.Player_Top.ri
        elif Test_Wall(self.Player_Top) == From_Left:
            self.Player_Top.x = self.Left_Wall.right + self.Player_Top.re + self.Player_Top.ri
        if Test_Wall(self.Player_Top) == From_Top:
            self.Player_Top.y = Top_Wall.bottom - self.Player_Top.re - self.Player_Top.ri
        elif Test_Wall(self.Player_Top) == From_Bottom:
            self.Player_Top.y = Top_Wall.top + self.Player_Top.re + self.Player_Top.ri"""
    #fn for determing the collision between ball and wall
    def Test_Wall(self, obj):
        if self.Right_Wall.left - obj.x <= obj.re + obj.ri or obj.x > self.Right_Wall.left:
            return self.From_Right
        if obj.x - self.Left_Wall.right <= obj.re + obj.ri or obj.x < self.Left_Wall.right:
            return self.From_Left
        if obj.y - self.Bottom_Wall.top <= obj.re + obj.ri or obj.y < self.Bottom_Wall.top:
            return self.From_Bottom
        if self.Top_Wall.bottom - obj.y <= obj.re + obj.ri or obj.y > self.Top_Wall.top:
            return self.From_Top
        return 0
    #fn for determing the collision has happened or no between player and ball
    def Test_Collision_Ball_Player(self):
        sqrt1 = (self.Ball.x - self.Player_Bottom.x) ** 2
        sqrt2 = (self.Ball.y - self.Player_Bottom.y) ** 2
        sqrt3 = (self.Ball.x - self.Player_Top.x) ** 2
        sqrt4 = (self.Ball.y - self.Player_Top.y) ** 2
        dist1 = sqrt(sqrt1 + sqrt2)
        dist2 = sqrt(sqrt3 + sqrt4)
        if dist1 <= self.dist_radius:
            return self.Collision_Ball_Bottom_Player
        if dist2 <= self.dist_radius:
            return self.Collision_Ball_Top_Player
        return 0
    #
    def music_fn(self):
        winsound.PlaySound('sound.wav', winsound.SND_FILENAME)
        mixer.init(frequency=48000)
        self.sound = mixer.Sound("elaabyala.wav")
        self.sound.play(loops =10000)
    #fn for drawing scene
    def Display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        #glColor4f(0.1, 0.1, 0.1, 1)
        self.Draw_Background()
        self.keyboard()
        self.Ball.x_prev = self.Ball.x
        self.Ball.y_prev = self.Ball.y
        self.Ball.y += self.step_y_ball
        self.Ball.x += self.step_x_ball
        if self.Flag_For_Computer:
            self.Computer_Player(self.Computer_Step)
        """if self.Ball.x > self.Right_Wall.left:
            self.Ball.x = self.Right_Wall.left - Ball.re
            self.step_x_ball = -self.step_x_ball
        if self.Ball.x < self.Left_Wall.right:
            self.Ball.x = self.Left_Wall.right + Ball.re
            self.step_x_ball = -self.step_x_ball
        if self.Ball.y > Top_Wall.bottom:
            self.Ball.y = Top_Wall.bottom - Ball.re
            self.step_y_ball = -self.step_y_ball
        if self.Ball.y < Bottom_Wall.top:
            self.Ball.y = Bottom_Wall.top + Ball.re"""
        self.time += 1
        if self.time == 10:
            self.Flag_Collision_Bottom_Player = True
            self.Flag_Collision_Top_Player = True
        if self.Ball_Goal() == self.Goal_For_Top_Player:
            self.Player_Top_Score += 1
            self.Again()
        if self.Ball_Goal() == self.Goal_For_Bottom_Player:
            self.Player_Bottom_Score += 1
            self.Again()
        if self.Test_Wall(self.Ball) == self.From_Right:
            self.Flag_Collision_Bottom_Player = True
            self.Flag_Collision_Top_Player = True
            self.Ball.x -= (self.width_wall - 0.25)/3
            self.step_x_ball = -self.step_x_ball
        if self.Test_Wall(self.Ball) == self.From_Left:
            self.Flag_Collision_Bottom_Player = True
            self.Flag_Collision_Top_Player = True
            self.Ball.x += (self.width_wall - 0.25)/3
            self.step_x_ball = -self.step_x_ball
        if self.Test_Wall(self.Ball) == self.From_Top:
            self.Flag_Collision_Bottom_Player = True
            self.Flag_Collision_Top_Player = True
            self.Ball.y -= (self.width_wall - 0.25)/3
            self.step_y_ball = -self.step_y_ball
        if self.Test_Wall(self.Ball) == self.From_Bottom:
            self.Flag_Collision_Bottom_Player = True
            self.Flag_Collision_Top_Player = True
            self.Ball.y += (self.width_wall - .025)/3
            self.step_y_ball = -self.step_y_ball
        if self.Test_Collision_Ball_Player() == self.Collision_Ball_Top_Player:
            self.Flag_Collision_Top_Player = False
            self.Flag_Collision_Bottom_Player = True
            self.time = 0
            if (not(self.Player_Top.x == self.Player_Top.x_prev and self.Player_Top.y == self.Player_Top.y_prev)) and self.Test_Quarter(self.Player_Top.x_prev, self.Player_Top.y_prev, self.Player_Top.x , self.Player_Top.y) == self.Test_Quarter(self.Player_Top.x, self.Player_Top.y, self.Ball.x, self.Ball.y):
                self.step_x_ball = (self.Speed(self.Player_Top) / 6) * self.Cos_Theta(self.Player_Top.x, self.Player_Top.y, self.Ball.x, self.Ball.y)
                self.step_y_ball = (self.Speed(self.Player_Top) / 6) * self.Sin_Theta(self.Player_Top.x, self.Player_Top.y, self.Ball.x, self.Ball.y)
            else:
                self.step_x_ball = 0.01 * self.Cos_Theta(self.Player_Top.x, self.Player_Top.y, self.Ball.x, self.Ball.y)
                self.step_y_ball = 0.01 * self.Sin_Theta(self.Player_Top.x, self.Player_Top.y, self.Ball.x, self.Ball.y)
        if self.Test_Collision_Ball_Player() == self.Collision_Ball_Bottom_Player:
            self.Flag_Collision_Top_Player = True
            self.Flag_Collision_Bottom_Player = False
            self.time = 0
            if(not(self.Player_Bottom.x == self.Player_Bottom.x_prev and self.Player_Bottom.y == self.Player_Bottom.y_prev)) and  self.Test_Quarter(self.Player_Bottom.x_prev, self.Player_Bottom.y_prev, self.Player_Bottom.x , self.Player_Bottom.y) == self.Test_Quarter(self.Player_Bottom.x, self.Player_Bottom.y, self.Ball.x, self.Ball.y):
                self.step_x_ball = (self.Speed(self.Player_Bottom) / 6) * self.Cos_Theta(self.Player_Bottom.x, self.Player_Bottom.y, self.Ball.x, self.Ball.y)
                self.step_y_ball = (self.Speed(self.Player_Bottom) / 6) * self.Sin_Theta(self.Player_Bottom.x, self.Player_Bottom.y, self.Ball.x, self.Ball.y) + (self.Ball.re/100)
            else:
                self.step_x_ball = 0.01 * self.Cos_Theta(self.Player_Bottom.x, self.Player_Bottom.y, self.Ball.x, self.Ball.y)
                self.step_y_ball = 0.01 * self.Sin_Theta(self.Player_Bottom.x, self.Player_Bottom.y, self.Ball.x, self.Ball.y)
            if self.Player_Bottom.x > self.Ball.x:
                self.Player_Bottom.x += self.Ball.re/12
            if self.Player_Bottom.x < self.Ball.x:
                self.Player_Bottom.x -= self.Ball.re/12
            if self.Player_Bottom.y > self.Ball.y:
                self.Player_Bottom.y += self.Ball.re/12
            if self.Player_Bottom.y < self.Ball.y:
                self.Player_Bottom.y -= self.Ball.re/6
        glDisable(GL_TEXTURE_2D)
        self.string = "player Top : " + str(self.Player_Top_Score)
        self.drawText(self.string, -1.5, 2)
        self.string = "player Bottom :  " + str(self.Player_Bottom_Score)
        self.drawText(self.string, -1.5, 1.8)
        """label = pyglet.text.Label(
        "Hello, World", font_name='Times New Roman', font_size=36,
        x=self.Width_Size/2, y= self.Height_Size/2, anchor_x='center', anchor_y='center')
        label.draw()"""
        glColor3f(0.86, 0.08, 0.23)
        self.Draw_Player(self.Player_Bottom)
        glColor3f(1, 1, 0)
        self.Draw_Player(self.Player_Top)
        glColor3f(0.75, 0.75, 0.75)
        self.Draw_Ball(self.Ball)
        glutSwapBuffers()


    def Timer(self, v):
        self.Display()
        glutTimerFunc(self.time_interval, self.Timer, 1)
    def main(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(self.Width_Size, self.Height_Size)
        glutInitWindowPosition(0, 0)
        glutCreateWindow(b"Glow Hockey")
        self.LoadTextures()
        glutDisplayFunc(self.Display)
        glutIdleFunc(self.Display)
        glutTimerFunc(self.time_interval, self.Timer, 1)
        glutKeyboardFunc(self.Key_Pressed)
        glutKeyboardUpFunc(self.Key_Up)
        glutSpecialFunc(self.arrow_press)
        if not self.Flag_For_Computer:
            glutPassiveMotionFunc(self.MouseMotion)
        self.InitGL(self.Width_Size, self.Height_Size)
        glutMainLoop()

game = Game(True, True, 0.004)
game.main()
