import pygame as pg
from particle import Particle

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

pg.init()
pg.display.set_caption("Coloumb's Law Simulation")

window = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
font = pg.font.SysFont("Arial", 30)

particles = []

charge_index = 0
default_radius = 15

charges = [-1, 0, 1]
classes = ["Electron", "Neutron", "Proton"]

simulating = False

running = True
while running:
    dt = clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed()[0]:
                mouse_pos = pg.mouse.get_pos()
                particles.append(Particle(pg.Vector2(mouse_pos[0], mouse_pos[1]), default_radius, charges[charge_index]))
            elif pg.mouse.get_pressed()[2]:
                charge_index = (charge_index + 1) % 3
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                simulating = not simulating
            elif event.key == pg.K_r:
                particles = []
    
    window.fill((0, 0, 0))

    # Draw text to show selected particle
    text = font.render(classes[charge_index], False, (255, 255, 255))
    window.blit(text, (0, 0))

    # Draw text to show status of simulation
    if not simulating:
        text = font.render("Paused", False, (255, 255, 255))
        window.blit(text, (SCREEN_WIDTH - 100, 0))

    if simulating:
        for i, particle in enumerate(particles):
            # Stops rendering particles that are far off screen
            if particle.active:
                particle.update_velocity(particles, dt)
            else:
                particles.pop(i)

    for particle in particles:
        particle.draw(window)


    pg.display.flip()

pg.quit()