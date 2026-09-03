def update_particles(particles):
    for p in particles:
        p.update()

    # Check every pair once
    num_particles = len(particles)
    for i in range(num_particles):
        for j in range(i + 1, num_particles):
            particles[i].resolve_collision(particles[j])
