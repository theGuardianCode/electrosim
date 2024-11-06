import pygame as pg
from particle import Particle

pg.init()

window = pg.display.set_mode((800, 800))
clock = pg.time.Clock()
font = pg.font.SysFont("Arial", 30)

particles = []

charge_index = 0
default_radius = 15

charges = [-1, 0, 1]
classes = ["electron", "neutron", "proton"]

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

    # Draw text
    text = font.render(classes[charge_index], False, (255, 255, 255))
    window.blit(text, (0, 0))

    if simulating:
        for particle in particles:
            particle.update_velocity(particles, dt)

    for particle in particles:
        particle.draw(window)


    pg.display.flip()

pg.quit()