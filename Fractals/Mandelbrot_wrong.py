import pygame, sys
import numpy as np
from pygame.locals import *

def Mandelbrot(Z, C, result, i):
    if i == iter_max or result.all():
        return result
    if False:
        check = [ x for x in enumerate(np.abs(Z) > 10.0) if x[1] ]
        for x, _ in check:
            Z[x] = complex_NaN
            result[x] = i
    else:
        while np.abs(np.nanmax(Z)) > 10.0:
            x = np.nanargmax(Z)
            Z[x] = complex_NaN
            result[x] = i
    return Mandelbrot(Z**d + C, C, result, i + 1)

def z_comp(a, b):
    x = (a - WIDTH // 2) / scale
    y = (b - HEIGHT // 2) / scale
    return x + y * 1j + CENTER

def color(i):
    if not i:
        return BLACK
    ratio_pur = i / iter_max
    ratio_whi = 1 - ratio_pur
    result = []
    for j in range(3):
        result.append(int(PURPLE[j] * ratio_pur + WHITE[j] * ratio_whi))
    return tuple(result)

PURPLE = (200, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 600
CENTER = -0.5 + 0j
scale = 200 #scale pixels = 1 unit length
iter_max = 50
d = 2

complex_NaN = np.NaN * 1j

def main():
    pygame.init() #Initialize pygame

    FPS = 60 #Frames per second
    fpsClock = pygame.time.Clock() #Clock initialization

    #Prepare the display
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    pygame.display.set_caption('Mandelbrot set')
    DISPLAYSURF.fill(WHITE) #Clear the surface

    a = 0 #Current worked column indicator

    #Draw the simulation
    while True:
        if a < WIDTH:
            for p in range(WIDTH // WIDTH):
                result = Mandelbrot(np.zeros(HEIGHT, complex),
                    np.array([ z_comp(a, i) for i in range(HEIGHT) ]),
                    np.zeros(HEIGHT, int), 0)

                for i, k in enumerate(result):
                    DISPLAYSURF.set_at((a, i), color(k))
                a += 1

        if __name__ != "__main__": #Exit it you just want to timeit
            pygame.quit()
            return None

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == "__main__":
    main()
