# Nematic.py
#
# Script modeling nematic material using Monte Carlo method.
#
# Changelog:
# 16.12.2016 - Script created
# 13.01.2017 - Script rewritten

# Scientific libraries
import numpy as np
import numpy.random

# Graphical libraries
import pygame
import sys
import pygame.gfxdraw
from pygame.locals import *

import functools

WIDTH, HEIGHT = 600, 600  # Size of the window

@functools.lru_cache()
def exp_coeff(dU, T):
    return np.exp(- dU / T)

def draw_FPS(screen):
    textSurfaceObj = fontObj.render("FPS: " + str(round(fpsClock.get_fps(), 1)),
                                    True, (0, 0, 0))
    textRectObj.topright = (WIDTH - 101, 0)
    screen.blit(textSurfaceObj, textRectObj)

P2 = {x: 0.5 * (3 * np.cos(np.pi * x / 180) ** 2 - 1)
      for x in range(-190, 191)}
sin_deg = {x: np.sin(np.pi / 180 * x) for x in range(-10, 190)}
cos_deg = {x: np.cos(np.pi / 180 * x) for x in range(-10, 190)}


class Nematic:
    possible_orientations = [i for i in range(180)]
    range_phi = [i for i in range(-10, 11) if i != 0]

    def __init__(self, L=20, T=1e-6, E=0.0, is_ordered = True):
        """Initialize grid method

        x - list of possible site values,
        L - integer, length of the side of the grid.
        """
        if is_ordered:
            self.grid = np.zeros((L, L))
        else:
            self.grid = np.random.choice(self.possible_orientations, size=(L, L))
        self.L = L
        self.Lm1 = L - 1
        self.T = T
        self.E = E
        self.ksi = -25

        self.grid[..., 0] *= 0
        self.grid[..., -1] *= 0

    def draw(self, screen):
        for x, column in enumerate(self.grid):
            for y, point in enumerate(column):
                x1 = 100 + 20 * x - 9 * cos_deg[point]
                y1 = 100 + 20 * y - 9 * sin_deg[point]
                x2 = 100 + 20 * x + 9 * cos_deg[point]
                y2 = 100 + 20 * y + 9 * sin_deg[point]
                pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2))

        # Print temperature
        textSurfaceObj = fontObj.render("T = " + str(round(self.T, 2)),
                                        True, (0, 0, 0))
        textRectObj.topright = (WIDTH - 101, 25)
        screen.blit(textSurfaceObj, textRectObj)
        # Print electric field
        textSurfaceObj = fontObj.render("E = " + str(round(self.E, 2)),
                                        True, (0, 0, 0))
        textRectObj.topright = (WIDTH - 101, 50)
        screen.blit(textSurfaceObj, textRectObj)

    def local_energy(self, x, y, point):
        result = P2[point - self.grid[x, y - 1]]
        result += P2[point - self.grid[x, y + 1]]
        result += P2[point - self.grid[(x - 1) % self.L, y]]
        result += P2[point - self.grid[(x + 1) % self.L, y]]
        result += self.E**2 * sin_deg[point]
        return self.ksi * result

    def MonteCarloStep(self):
        delta_phis = np.random.choice(
            self.range_phi, size=(self.L, self.L - 2))
        for x, column in enumerate(self.grid):
            for y, point in enumerate(column):
                if y != 0 and y != self.Lm1:
                    delta_phi = delta_phis[x, y - 1]
                    delta_U = self.local_energy(
                        x, y, point + delta_phi) - self.local_energy(x, y, point)
                    if delta_U <= 0 or np.random.rand() < exp_coeff(delta_U, self.T):
                        self.grid[x, y] = (point + delta_phi) % 180

    def cos2(self):
        x = np.power(np.cos( np.pi / 180 *self.grid[:, 1:-1]),2)
        return np.sum(x / self.L / (self.L-2))


if __name__ == "__main__":
    nematic = Nematic(L=20)

    f = open("output.txt", 'w')

    pygame.init()  # Initialize pygame

    FPS = 60  # Frames per second
    N = 10  # Number of evolution steps per frame
    fpsClock = pygame.time.Clock()  # Clock initialization

    fontsize = 18

    # Prepare the display
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    pygame.display.set_caption('Brownian motion')

    # Prepare print of the text
    fontObj = pygame.font.Font('freesansbold.ttf', fontsize)
    textSurfaceObj = fontObj.render('', True, (0, 0, 0))
    textRectObj = textSurfaceObj.get_rect()

    ksi = 1

    # Draw the simulation
    while True:
        DISPLAYSURF.fill((255, 255, 255))  # Clear the surface

        draw_FPS(DISPLAYSURF)  # Write the FPS text

        nematic.draw(DISPLAYSURF)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                f.close()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[K_4]:
            nematic.T = max(nematic.T - 0.01, 0.01)
        if keys[K_6]:
            nematic.T = min(nematic.T + 0.01, 50)
        if keys[K_7]:
            nematic.E = max(0, nematic.E - 0.01)
        if keys[K_9]:
            nematic.E += 0.01


        x = 0
        for i in range(N):
            nematic.MonteCarloStep()
            x += nematic.cos2()

        f.write("{}\t{}\n".format(nematic.E, x/N))
        nematic.E += 0.001

        pygame.display.update()
        fpsClock.tick(FPS)
