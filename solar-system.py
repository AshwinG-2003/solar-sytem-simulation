import pygame
import numpy as np
import random
from scipy.integrate import ode

# initialize Pygame
pygame.init()

# set window dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulation")

# Define colors for planets
WHITE = (255, 255, 255)
MERCURY_COLOR = (169, 169, 169)
VENUS_COLOR = (255, 223, 0)
EARTH_COLOR = (70, 130, 180)
MARS_COLOR = (255, 69, 0)
JUPITER_COLOR = (255, 140, 0)
SATURN_COLOR = (218, 165, 32)
URANUS_COLOR = (173, 216, 230)
NEPTUNE_COLOR = (0, 0, 255)
SUN_COLOR = (255, 255, 0)

# gravitational constant
G = 6.67428e-11  
# one day per step
TIMESTEP = 60 * 60 * 24

# define an AU (astronomical unit) in meters
AU = 149.6e6 * 1000

class HeavenlyBody:
    def __init__(self, x, y, mass, color, radius, vel_x=0, vel_y=0):
        self.x = x
        self.y = y
        self.mass = mass
        self.color = color
        self.radius = radius
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.orbit = []
        self.sun = False
        self.name = None

    def draw(self, screen, scale_factor):
        x_screen = int(self.x * scale_factor + WIDTH / 2)
        y_screen = int(self.y * scale_factor + HEIGHT / 2)
        pygame.draw.circle(screen, self.color, (x_screen, y_screen), self.radius)

        font = pygame.font.Font(None, 12)
        text = font.render(self.name, True, (255, 255, 255))
        screen.blit(text, (x_screen - 15, y_screen + self.radius + 5))

# function defining the ODE system
def ode_system(t, state, bodies):
    num_bodies = len(bodies)
    dydt = np.zeros_like(state)
    
    for i in range(num_bodies):
        index = i * 4
        x, y, vx, vy = state[index:index+4]

        ax, ay = 0, 0
        for j in range(num_bodies):
            if i == j:
                continue

            j_index = j * 4
            xj, yj, _, _ = state[j_index:j_index+4]
            dx, dy = xj - x, yj - y
            distance = np.sqrt(dx**2 + dy**2)

            if distance == 0:
                continue

            # gravitational force equation: F = G * m1 * m2 / r^2
            m1 = bodies[i].mass
            m2 = bodies[j].mass  
            force = G * m1 * m2 / distance**2

            # acceleration due to the force: a = F / m
            ax += force * dx / (m1 * distance)  
            ay += force * dy / (m1 * distance)

        dydt[index] = vx
        dydt[index+1] = vy
        dydt[index+2] = ax
        dydt[index+3] = ay

    return dydt


def add_random_body(planetBodies, solver):
    x = random.uniform(-20, 20) * AU
    y = random.uniform(-20, 20) * AU
    mass = random.uniform(1e23, 1e28)
    radius = random.randint(2, 7)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    distance_from_sun = np.sqrt(x**2 + y**2)
    if distance_from_sun == 0:
        return

    vel_magnitude = np.sqrt(G * planetBodies[0].mass / distance_from_sun)
    vel_angle = np.arctan2(y, x) + np.pi / 2
    vel_x = vel_magnitude * np.cos(vel_angle)
    vel_y = vel_magnitude * np.sin(vel_angle)

    new_body = HeavenlyBody(x, y, mass, color, radius, vel_x, vel_y)
    new_body.name = "Body " + str(len(planetBodies))

    planetBodies.append(new_body)

    new_state = np.array([new_body.x, new_body.y, new_body.vel_x, new_body.vel_y])
    solver.set_initial_value(np.append(solver.y, new_state), solver.t)
    solver.set_f_params(planetBodies)

# main function to run the simulation
def main():
    global G, TIMESTEP

    clock = pygame.time.Clock()
    frame_rate = 60
    simulation_speed = 1
    game_on = False

    # Define planets
    sun = HeavenlyBody(0, 0, 1.98892e30, SUN_COLOR, 9)
    sun.sun = True
    sun.name = "Sun"

    mercury = HeavenlyBody(-0.387 * AU, 0, 3.30e23, MERCURY_COLOR, 1, vel_y=-47.4e3)
    mercury.name = "Mercury"

    venus = HeavenlyBody(-0.723 * AU, 0, 4.8685e24, VENUS_COLOR, 3, vel_y=-35.02e3)
    venus.name = "Venus"

    earth = HeavenlyBody(-1 * AU, 0, 5.9722e24, EARTH_COLOR, 3, vel_y=-29.783e3)
    earth.name = "Earth"

    mars = HeavenlyBody(-1.524 * AU, 0, 6.39e23, MARS_COLOR, 2, vel_y=-24.077e3)
    mars.name = "Mars"

    jupiter = HeavenlyBody(-5.204 * AU, 0, 1.898e27, JUPITER_COLOR, 7, vel_y=-13.06e3)
    jupiter.name = "Jupiter"

    saturn = HeavenlyBody(-9.573 * AU, 0, 5.683e26, SATURN_COLOR, 6, vel_y=-9.68e3)
    saturn.name = "Saturn"

    uranus = HeavenlyBody(-19.165 * AU, 0, 8.681e25, URANUS_COLOR, 5, vel_y=-6.80e3)
    uranus.name = "Uranus"

    neptune = HeavenlyBody(-30.178 * AU, 0, 1.024e26, NEPTUNE_COLOR, 5, vel_y=-5.43e3)
    neptune.name = "Neptune"

    planetBodies = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    # Initial state: [x, y, vx, vy] for each planet
    state = []
    for body in planetBodies:
        state.extend([body.x, body.y, body.vel_x, body.vel_y])

    state = np.array(state)

    # Set up ODE solver
    solver = ode(ode_system).set_integrator("dop853")
    solver.set_initial_value(state, 0)
    solver.set_f_params(planetBodies)

    zoom_scale = 0.5
    run = True

    while run:
        clock.tick(frame_rate * simulation_speed)
        screen.fill((0, 0, 0))

        font = pygame.font.Font(None, 22)

        instructions = [
            "Instructions:",
            "Press SPACE to start the simulation",
            "Press 'A' to increase simulation speed",
            "Press 'D' to decrease simulation speed",
            "Press 'W' to increase gravitational constant",
            "Press 'S' to decrease gravitational constant",
            "Press 'N' to add a random new celestial body",
            "Press '+/-' to zoom in or out",
            "Press ESC to exit"
        ]

        for i, line in enumerate(instructions):
            text = font.render(line, True, WHITE)
            screen.blit(text, (10, (HEIGHT // 3 + i * 20) - 190))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if not game_on:
                    if event.key == pygame.K_SPACE:
                        game_on = True
                else:
                    if event.key == pygame.K_a:
                        simulation_speed += 0.1
                    elif event.key == pygame.K_d:
                        simulation_speed = max(0.1, simulation_speed - 0.1)
                    elif event.key == pygame.K_w:
                        G *= 1.1 
                    elif event.key == pygame.K_s:
                        G /= 1.1
                    elif event.key == pygame.K_n:
                        add_random_body(planetBodies, solver)
                    elif event.key in (pygame.K_EQUALS, pygame.K_KP_PLUS):
                        zoom_scale /= 0.5
                    elif event.key == pygame.K_MINUS:
                        zoom_scale *= 0.5
                    elif event.key == pygame.K_ESCAPE:
                        run = False

        # solve ODE for the next time step
        if solver.successful():
            solver.integrate(solver.t + TIMESTEP)
            state = solver.y

            # update planet positions
            for i, body in enumerate(planetBodies):
                index = i * 4
                body.x = state[index]
                body.y = state[index+1]

        if game_on:
            SCALE_FACTOR = 1e-9 * zoom_scale
            for body in planetBodies:
                body.draw(screen, SCALE_FACTOR)

        pygame.display.update()

    pygame.quit()

main()

