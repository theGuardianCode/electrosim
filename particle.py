import pygame as pg

class Particle:
    def __init__(self, pos, rad, charge, moveable):
        self.pos = pos
        self.rad = rad
        self.charge = charge
        self.moveable = moveable

        # Colour particles based on their charge
        if charge > 0:
            self.colour = (255, 0, 0)
        elif charge < 0:
            self.colour = (0, 0, 255)
        else:
            self.colour = (211, 211, 211)

        self.vel = pg.Vector2(0, 0)
        self.prev_pos = self.pos

        self.active = True
    
    def will_collide(self, pos, particles):
        for particle in particles:
            if particle != self:
                if (particle.pos - pos).magnitude() < self.rad + particle.rad:
                    return True
        
        return False
    
    def draw(self, surface):
        pg.draw.circle(surface, self.colour, self.pos, self.rad)

        # If particle is fixed draw green circle inside
        if self.moveable == False:
            pg.draw.circle(surface, (0, 200, 0), self.pos, self.rad / 4)

    def update_velocity(self, particles, time_step):
        for particle in particles:
            if particle != self and self.charge != 0:
                factor = 1
                if (particle.charge > 0 and self.charge > 0) or (particle.charge < 0 and self.charge < 0):
                    # this is true if both particles are positive or both negative. Therefore they repel each other = opposite directions
                    factor = -1


                force_dir = (particle.pos - self.pos).normalize() * factor

                dst_sqr = (particle.pos - self.pos).magnitude_squared() - self.rad * 2
                force = 5 * abs(self.charge * particle.charge) / dst_sqr

                acceleration = force_dir * force / abs(self.charge)

                # Verlet integration: x(t + dt) = 2x - x(t-dt) + a(t)(dt^2)
                new_pos = 2 * self.pos - self.prev_pos + (acceleration * time_step * time_step)

                if not self.will_collide(new_pos, particles):
                    self.prev_pos = self.pos
                    self.pos = new_pos
                
        # Check if particle is far from screen center
        if (self.pos - pg.Vector2(400, 400)).magnitude() > 1000:
            self.active = False