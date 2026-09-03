def update_particles(particles):
    for p in particles:
        p.update()

    # Sort the particles by their left edge
    particles.sort(key=lambda e: e.x - e.radius)

    num_particles = len(particles)
    for i in range(num_particles):
        p1 = particles[i]
        # The farthest this particle can reach toward the right
        p1_max_x = p1.x + p1.radius

        for j in range(i + 1, num_particles):
            p2 = particles[j]
            # The farthest this particle can reach toward the left
            p2_min_x = p2.x - p2.radius
            # If this particle can't possibly reach it, then no particle after it can reach either
            if p2_min_x > p1_max_x:
                break
            p1.resolve_collision(p2)
