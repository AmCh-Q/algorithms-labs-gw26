# ====== Configuration ======
WIDTH, HEIGHT = 800, 800

# ====== Particle ======
class Particle:
    __slots__ = ('x', 'y', 'vx', 'vy', 'radius', 'color')

    def __init__(self, x, y, vx, vy, radius):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius

    def update(self):
        # Motion
        self.x += self.vx
        self.y += self.vy

        # Wall collision
        if (self.vx < 0 and self.x - self.radius < 0) or (self.vx > 0 and self.x + self.radius > WIDTH):
            self.vx = -self.vx
        if (self.vy < 0 and self.y - self.radius < 0) or (self.vy > 0 and self.y + self.radius > HEIGHT):
            self.vy = -self.vy

    def resolve_collision(self, other):
        # Skip if they are not touching
        dx = other.x - self.x
        dy = other.y - self.y
        ds = dx * dx + dy * dy
        r = other.radius + self.radius
        if ds > r * r or ds == 0:
            return

        # Skip if they are moving apart
        dvx = other.vx - self.vx
        dvy = other.vy - self.vy
        if dvx * dx + dvy * dy >= 0:
            return

        # Swap velocities
        self.vx, other.vx = other.vx, self.vx
        self.vy, other.vy = other.vy, self.vy
