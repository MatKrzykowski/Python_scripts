from common import *

pendulum = Pendulum([np.pi / 1.00001])

fpsClock = pygame.time.Clock() #Clock initialization

#Prepare the display
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Single pendulum')

#Draw the simulation
while True:
    DISPLAYSURF.fill(WHITE) #Clear the surface
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pendulum.draw(DISPLAYSURF)
    draw_FPS(DISPLAYSURF, fpsClock)
    pendulum.draw_energy(DISPLAYSURF)

    pendulum.integrate()

    pygame.display.update()
    fpsClock.tick(FPS)
