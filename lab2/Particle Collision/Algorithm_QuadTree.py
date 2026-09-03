# ====== Configuration ======
CAPACITY = 30

def update_particles(particles):
    for p in particles:
        p.update()

    Quadtree.particles = particles
    p0 = particles[0]
    r_max = p0.radius
    x_min = x_max = p0.x
    y_min = y_max = p0.y
    for p in particles:
        if p.x < x_min: x_min = p.x
        elif p.x > x_max: x_max = p.x
        if p.y < y_min: y_min = p.y
        elif p.y > y_max: y_max = p.y
        if p.radius > r_max: r_max = p.radius
    Quadtree.radius = r_max
    Quadtree(x_min, y_min,x_max - x_min,y_max - y_min, 0, len(particles), None).update()

# ====== Quadtree ======
class Quadtree:
    __slots__ = ('x', 'y', 'u', 'v', 'i', 'j', 'root', 'children')
    particles = []
    radius = 1

    def __init__(self, x, y, u, v, i, j,root):
        self.x = x # left edge
        self.y = y # top edge
        self.u = u # right edge
        self.v = v # bottom edge
        self.i = i # idx of first particle
        self.j = j # idx after last particle
        self.root = root or self
        self.children = None

        margin = 4 * Quadtree.radius
        if (j - i > CAPACITY and u - x > margin and v - y > margin):
            self.split()
            return

    def split(self):
        particles = Quadtree.particles
        x_mid = (self.x + self.u) / 2
        y_mid = (self.y + self.v) / 2

        # partition the particles top-bottom
        i,j = self.i, self.j - 1
        while True:
            while i < self.j and particles[i].y < y_mid:
                i += 1
            while j >= self.i and particles[j].y >= y_mid:
                j -= 1
            if i > j:
                break
            particles[i], particles[j] = particles[j], particles[i]

        # partition the top particles left-right
        b,i,j = i,self.i,j
        while True:
            while i < b and particles[i].x < x_mid:
                i += 1
            while j >= self.i and particles[j].x >= x_mid:
                j -= 1
            if i > j:
                break
            particles[i], particles[j] = particles[j], particles[i]

        # partition the bottom particles left-right
        a,i,j = i,b,self.j - 1
        while True:
            while i < self.j and particles[i].x < x_mid:
                i += 1
            while j >= b and particles[j].x >= x_mid:
                j -= 1
            if i > j:
                break
            particles[i], particles[j] = particles[j], particles[i]

        # recursively build children following Z-order
        # https://en.wikipedia.org/wiki/Z-order_curve
        c,i,j = i,self.i,self.j
        self.children = (
            Quadtree(self.x,self.y,x_mid,y_mid,i,a,self.root),
            Quadtree(x_mid,self.y,self.u,y_mid,a,b,self.root),
            Quadtree(self.x,y_mid,x_mid,self.v,b,c,self.root),
            Quadtree(x_mid,y_mid,self.u,self.v,c,j,self.root))

    # get neighbor particles earlier in the Z-order (others will include us later)
    def get_neighbors(self):
        particles = Quadtree.particles

        # get bounding box
        margin = 2 * Quadtree.radius
        x_min, y_min = self.x - margin, self.y - margin
        x_max, y_max = self.u + margin, self.v + margin
        limit = self.i
        neighbors = []

        def walk(node):
            if (node.i == node.j    # skip empty nodes
                or node.i >= limit  # skip later nodes
                or node.u < x_min   # skip nodes too far to the left
                or node.x > x_max   # skip nodes too far to the right
                or node.v < y_min   # skip nodes too far above
                or node.y > y_max): # skip nodes too far below
                return
            if node.children:
                for c in node.children:
                    walk(c)
                return
            for i in range(node.i, node.j):
                p = particles[i]
                if (x_min <= p.x <= x_max and y_min <= p.y <= y_max):
                    neighbors.append(p)

        walk(self.root)
        return neighbors

    def update(self):
        if self.children:
            for c in self.children:
                c.update()
            return
        particles = Quadtree.particles
        neighbors = self.get_neighbors()
        for i in range(self.i,self.j):
            resolve = particles[i].resolve_collision
            for j in range(self.i,i):
                resolve(particles[j])
            for p2 in neighbors:
                resolve(p2)
