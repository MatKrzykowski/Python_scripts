# common.py
#
# Common file for Pendulums project
#
# Changelog:
# 18.03.2017 - script created

# Scientific libraries
import numpy as np
from scipy.integrate import ode

# Graphical libraries
import pygame, sys
from pygame.locals import *
import pygame.gfxdraw

##########
# Pygame #
##########

# Colors
PURPLE = (200, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init() #Initialize pygame

#Prepare object for printing text into the screen
fontObj = pygame.font.SysFont('Comic Sans MS', 20)
textRectObj = fontObj.render('', True, BLACK).get_rect()

WIDTH, HEIGHT = 600, 600 #Dimentions of the screen
FPS = 30 #Frames per second

def draw_FPS(screen, fps):
    """Draw FPS counter onto the screen function.

    screen - screen to print onto,
    fps - pygame's fps object."""
    textSurfaceObj = fontObj.render("FPS: " + str(round(fps.get_fps(), 1)),
                                    True, BLACK) #Text
    textRectObj.topright = (WIDTH - 141, 0) #Move the field
    screen.blit(textSurfaceObj, textRectObj) #Blit onto the screen

#######################
# Physical parameters #
#######################
dt = 1 / FPS #Time step
g = 9.8 #Gravitational accelaration
d = 1.0 #Lenght of the pendulum arm
m = 1.0 #Mass at the end of the pendulum (arm is weightless)

class Pendulum():
    """Pendulum class."""

    def __init__(self, theta, ni=0.0):
        """Initialize Pendulum object.

        theta - angles in radians,
        ni - dissipation force coeficient (F = -ni * omega)."""

        #Physical properties
        self.n = len(theta) #Number of part in the pendulum
        self.theta = np.array(theta) #Angle
        self.omega = np.zeros(self.n) #Angular velocity
        self.ni = ni #dissipation force coeficient

        #ODE object definition
        self.r = ode(self.derivative).set_integrator('dop853', rtol = 1e-7)
        self.r.set_initial_value([*self.theta, *self.omega], 0.0)
        self.r.set_f_params(self.ni, self.n)

        #Parameters for drawing
        self.beg = (300, 300) #Start point of the pendulum
        self.scale = 200 // self.n #Scale of the pendulum, 1m -> scale px
        self.radius = 10 #Radius of the mass of the pendulum

    @staticmethod
    def derivative(t, y, ni, n):
        """Derivative function as per scipy specifications."""
        #return [y[1], - m * g * d * np.sin(y[0]) - ni * y[1]]
        return list(y[n:]) + [float(-m*d*y[2]**2*np.sin(y[0]-y[1])*np.cos(y[0]-y[1])+g*m*np.sin(y[1])*np.cos(y[0]-y[1])-m*d*y[3]**2*np.sin(y[0]-y[1])-2*m*g*np.sin(y[0]))/float(2*d*m-m*d*np.cos(y[0]-y[1])**2)-ni*y[2],
            float(m*d*y[3]**2*np.sin(y[0]-y[1])*np.cos(y[0]-y[1])+g*2*m*np.sin(y[0])*np.cos(y[0]-y[1])+2*m*d*y[2]**2*np.sin(y[0]-y[1])-2*m*g*np.sin(y[1]))/float(2*d*m-m*d*np.cos(y[0]-y[1])**2)-ni*y[3]]

    @property
    def x(self):
        """x position of the end of the pendulum."""
        return d * np.sin(self.theta)

    @property
    def y(self):
        """y position of the end of the pendulum."""
        return -d * np.cos(self.theta)

    @property
    def energy(self):
        """Total energy of the pendulum."""
        return sum([-m * g * float(d * np.cos(self.theta[i])) * (2-i) for i in range(self.n)]) + 0.5 * m * g * d * (self.n + self.n**2) + \
            0.5 * d**2 * m * float(2*self.omega[0] ** 2 + self.omega[1] ** 2 + 2 * self.omega[0] * self.omega[1] * np.cos(self.theta[0]-self.theta[1]))

    @property
    def end(self):
        """Endpoint of the pendulum."""
        points = [self.beg]
        for i in range(self.n):
            points.append((int(round(float(points[i][0] + self.scale * self.x[i]))), #x coordinate
                           int(round(float(points[i][1] - self.scale * self.y[i]))))) #y coordinate

        return points

    def draw(self, screen):
        """Draw the pendulum."""
        points = self.end
        for i in range(self.n):
            pygame.draw.line(screen , BLACK, points[i], points[i+1], 2)
            pygame.draw.circle(screen, PURPLE, points[i+1], self.radius)
            pygame.gfxdraw.aacircle(screen, *points[i+1], self.radius, PURPLE)

    def draw_energy(self, screen):
        """Print total energy onto screen."""
        textSurfaceObj = fontObj.render("Energy: " + str(round(self.energy, 3)),
                                        True, (0, 0, 0))
        textRectObj.topright = (WIDTH - 141, 20)
        screen.blit(textSurfaceObj, textRectObj)

    def integrate(self):
        """Perform ODE integration step from T to T+dt."""
        self.r.integrate(self.r.t + dt)
        self.theta, self.omega = self.r.y[:self.n], self.r.y[self.n:]

#Print a message if file run as a script
if __name__ == "__main__":
    print("You were not supposed to do that!")
