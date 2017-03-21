import pygame, sys
from pygame.locals import *

def Mandelbrot(z, c, i):
    if i == iter_max:
        return 0
    if abs(z) > 10.:
        return i
    return Mandelbrot(z**d + c, c, i + 1)

def z_comp(a, b):
    x = (a - WIDTH // 2) / scale
    y = (b - HEIGHT // 2) / scale
    return x + y * 1j + CENTER

def color(i):
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
iter_max = 100
d = 2.01

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
            for b in range(HEIGHT):
                result = Mandelbrot(0j, z_comp(a,b), 0)
                if result == 0:
                    DISPLAYSURF.set_at((a, b), BLACK)
                else:
                    DISPLAYSURF.set_at((a, b), color(result))
            a += 1
            #print(round(a * 100 / WIDTH, 1),"%")
        elif __name__ != "__main__":
            #pygame.event.post(pygame.event.Event(pygame.QUIT))
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
