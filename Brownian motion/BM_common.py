# Based on program I've written in AngularJS in 2014
# https://www.khanacademy.org/computer-programming/elastic-collisionsbrownian-movement/5114294751461376

import numpy as np  # Import math modules

dt = 0.002  # Time differential
n = 200  # Number of particles
inf_diag = np.diag(np.inf * np.ones(n))
min_r, max_r = 3, 5  # Maximum and minimum radius of generated particle
max_dist = []

WIDTH, HEIGHT = 800, 600  # Size of the window


def sqlength(A):
    """Find square length of a 2-element vector"""
    return np.sum(A**2)


def length(A):
    """Find length of a 2-element vector"""
    return np.linalg.norm(A)


def generate_particles(items, n):
    """Generate n particles, some in random locations"""
    # Add 2 large particles in specified locations
    items.append(particle(100, 100, 80, 200, 100))
    items.append(particle(500, 100, 80, 200, 99))
    items[0].color = (255, 0, 0)
    items[1].color = (0, 128, 255)

    # Generate the rest of the particles
    while len(items) < n:  # How many particles are being generated
        r = np.random.randint(3, max_r + 1)  # Radius of generated particles
        pos = (r + np.random.randint(WIDTH - 2 * r),
               r + np.random.randint(HEIGHT - 2 * r))
        for item in items:
            # Check if there are no particle overlap
            if length(pos - item.position) <= r + item.radius:
                break
        else:
            items.append(particle(*pos, 0, 0, r))

    return items, np.array([i.radius for i in items]) + max_r


def total_energy(items):
    """Calculate sum of all particles' energy"""
    result = 0.0
    for item in items:
        result += item.kinetic()
    return result


def simulation_step(i, j, dist):
    if dist <= i.radius + j.radius:
        scalar = np.sum((i.position - j.position) * (i.velocity - j.velocity))
        if scalar < 0.0:
            A = 2 * scalar / (i.mass + j.mass) / dist**2
            i.velocity, j.velocity = \
                i.velocity - j.mass * A * (i.position - j.position), \
                j.velocity - i.mass * A * (j.position - i.position)


def time_evolution(items, max_dist):
    # Move particles
    for item in items:
        item.increment()  # Integrate position using velocity

    # Prepare distance array
    dist_arr = np.array([i.position for i in items])  # Array of dist_arr
    # 2D array of distance vectors
    dist_arr = dist_arr.reshape(n, 1, 2) - dist_arr
    dist_arr = np.sqrt((dist_arr**2).sum(2))  # 2D array of distances
    dist_arr += inf_diag  # Make diagonal elements infinite

    # First step, interaction of two unique particles
    simulation_step(items[0], items[1], dist_arr[0, 1])

    # Remaining interactions
    dist_arr = dist_arr[2:, :]  # Remove unnecessary elements
    while True:
        min_arg = np.argmin(dist_arr, 0)  # Calculate arguments for minima
        # Assign pairs i,j so that they point to the minima
        for i, j in enumerate(min_arg):
            # Simulation step for found pair of particles
            simulation_step(items[i], items[j + 2], dist_arr[j, i])
            # Make visited values infinite
            if i < len(min_arg) - 2:
                dist_arr[i, j] = np.inf
            dist_arr[j, i] = np.inf

        # Break loop is all remaining distance larger than max interaction dist
        min_val = np.min(dist_arr, 0)
        if (min_val >= max_dist[0:len(min_val)]).all():
            break

        # Otherwise remove as much right hand side elements as possible
        i = len(min_val) - 1  # Index to be removed
        while True:
            # If element is safe to be removed, continue
            if min_val[i] > max_dist[i]:
                i -= 1
            # If not slice the distance array and break from the loop
            else:
                dist_arr = dist_arr[:i + 1, :i + 1]
                break

        # Reflect from walls and other effects
        for item in items:
            item.reflect()  # Reflect particle from walls
            # item.velocity[1] += 10 * dt #Gravity, unimplemented
            # item.velocity *= np.exp(-0.03 * dt) #Damping, unimplemented

##########################################################################


class particle:
    """Class describing particle"""
    rho = 1.0  # Density

    def __init__(self, x, y, vx, vy, radius, color=(200, 0, 255)):
        """Instantiation operation"""
        self.position = np.array(
            [float(x), float(y)])  # Cartesian coordinates tuple
        # Velocity vector tuple
        self.velocity = np.array([float(vx), float(vy)])
        self.mass = self.rho * np.pi * radius**2  # Particle mass
        self.radius = radius  # Particle radius
        self.color = color  # Particle color

    def kinetic(self):
        """Kinetic energy of the particle"""
        return self.mass * sqlength(self.velocity) / 2.0

    def momentum(self):
        """Momentum value of the particle"""
        return self.mass * length(self.velocity)

    def increment(self):
        """Change position due to velocity"""
        self.position += self.velocity * dt

    def reflect(self):
        """Bouncing off the walls by the particle"""
        # Along the x axis
        if self.position[0] > 800 - self.radius and self.velocity[0] > 0:
            self.velocity[0] *= -1
        elif self.position[0] < self.radius and self.velocity[0] < 0:
            self.velocity[0] *= -1
        # Along the y axis
        if self.position[1] > 600 - self.radius and self.velocity[1] > 0:
            self.velocity[1] *= -1
        elif self.position[1] < self.radius and self.velocity[1] < 0:
            self.velocity[1] *= -1

    def intpos(self):
        """Return position tuple cast onto int"""
        return (int(self.position[0]), int(self.position[1]))
