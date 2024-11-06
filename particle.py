import pygame as pg

class Particle:
    def __init__(self, pos, rad, charge):
        self.pos = pos
        self.rad = rad
        self.charge = charge

        # Colour particles based on their charge
        if charge > 0:
            self.colour = (255, 0, 0)
        elif charge < 0:
            self.colour = (0, 0, 255)
        else:
            self.colour = (211, 211, 211)

        self.vel = pg.Vector2(0, 0)
    
    def will_collide(self, pos, particles):
        for particle in particles:
            if particle != self:
                if (particle.pos - pos).magnitude() < self.rad + particle.rad:
                    return True
        
        return False
    
    def draw(self, surface):
        pg.draw.circle(surface, self.colour, self.pos, self.rad)

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
                self.vel += acceleration * time_step

    def update_position(self, particles, time_step):
        new_pos = self.pos + (self.vel * time_step)
        if not self.will_collide(new_pos, particles):
            self.pos = new_pos