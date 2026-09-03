import sys
import time
import math
import random
import pygame
import colorsys

from Particle import Particle
#from Algorithm_Simple import update_particles
#from Algorithm_SortAndSweep import update_particles
from Algorithm_QuadTree import update_particles

# ====== Configuration ======
WIDTH, HEIGHT = 800, 800
SPEED = 1.0

# ====== Main application ======
def main():
    if len(sys.argv) < 2:
        print("Usage: python particles.py <num_particles>")
        sys.exit(1)

    num_particles = int(sys.argv[1])
    random.seed(num_particles)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Particle Collision")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Consolas", 24, bold=True)

    # Initialize Particles class
    radius = max(1,min(WIDTH // 20, HEIGHT // 20, 5 * math.sqrt((WIDTH + HEIGHT) / num_particles)))
    Particle.width = WIDTH
    Particle.height = HEIGHT

    # Create particles with random positions and directions
    particles = []
    for _ in range(num_particles):
        x = random.uniform(WIDTH // 4, 3 * WIDTH // 4)
        y = random.uniform(WIDTH // 4, 3 * HEIGHT // 4)
        angle = random.uniform(0, 2 * math.pi)
        vx = random.gauss(0, SPEED)
        vy = random.gauss(0, SPEED)
        particles.append(Particle(x, y, vx, vy, radius))

    # a simple exponential moving average of the time
    time_average = math.nan

    paused = False
    running = True
    while running:
        time_start = time.perf_counter()

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

        # Physics
        if not paused:
            update_particles(particles)

        # Drawing
        screen.fill((0, 0, 0))
        for i in range(num_particles):
            hue = (0.9 * i / num_particles) % 1
            r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            pygame.draw.circle(
                screen,
                (int(r * 255), int(g * 255), int(b * 255)),
                (int(particles[i].x), int(particles[i].y)),
                radius
            )

        # Status
        status = "Paused  (press space to pause)" if paused else "Running (press space to pause)"
        info = f"{status}\nParticles: {num_particles}\nFrame time: {time_average * 1000:.2f} ms\nFPS: {1.0 / time_average:.2f} (Limit: 60)"
        text = font.render(info, True, (255, 255, 255))
        screen.blit(text, (10, 10))

        # Hover tooltip
        if paused:
            mx, my = pygame.mouse.get_pos()
            hovered = None
            for i,p in enumerate(particles):
                if (mx - p.x) ** 2 + (my - p.y) ** 2 <= radius ** 2:
                    hovered = (i,p)
                    break
            if hovered:
                pos_text = font.render(
                    f"Pos: ({hovered[1].x:.2f}, {hovered[1].y:.2f})\ni: {hovered[0]}",
                    True, (0, 255, 0)
                )
                screen.blit(pos_text, (mx + 10, my - 10))

        # Display
        pygame.display.flip()

        # Wait till next frame
        time_end = time.perf_counter()
        if math.isnan(time_average):
            time_average = time_end - time_start
        else:
            time_average = (time_end - time_start) * 0.01 + time_average * 0.99
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
