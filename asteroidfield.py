import pygame
import random
from pygame.math import Vector2
from asteroid import Asteroid
from constants import *

class AsteroidField(pygame.sprite.Sprite):
    """
    A class to manage spawning and updating asteroids in the game.

    Asteroids spawn randomly at the edges of the screen and move inward, 
    increasing the challenge for the player.
    """
    
    # Define possible asteroid spawn edges with associated directions.
    # This creates asteroids that start outside the screen and move inward.
    edges: list[list[Vector2, callable]] = [
        [
            Vector2(1, 0),
            lambda y: Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            Vector2(-1, 0),
            lambda y: Vector2(SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            Vector2(0, 1),
            lambda x: Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            Vector2(0, -1),
            lambda x: Vector2(x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS),
        ],
    ]

    def __init__(self) -> None:
        """
        Initialize an AsteroidField with a spawn timer.

        The spawn timer controls when new asteroids are generated.
        """
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer: float = 0.0

    def spawn(self, radius: float, position: Vector2, velocity: Vector2) -> None:
        """
        Create a new asteroid at the specified position with a given velocity.

        Parameters:
            radius (float): The radius of the asteroid.
            position (Vector2): The spawn location of the asteroid.
            velocity (Vector2): The asteroid's initial velocity.
        """
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt: float) -> None:
        """
        Update the asteroid field, spawning new asteroids at intervals.

        Asteroids spawn randomly from screen edges and move toward the center.

        Parameters:
            dt (float): Time delta since the last frame, ensuring 
                        frame-rate-independent timing.
        """
        self.spawn_timer += dt

        # Spawn new asteroids when enough time has passed.
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0

            # Randomly choose one of the edges to spawn an asteroid.
            edge: list[Vector2, callable] = random.choice(self.edges)

            # Randomize asteroid speed and adjust its initial trajectory 
            # to avoid predictable straight-line motion.
            speed: int = random.randint(40, 100)
            velocity: Vector2 = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))

            # Spawn the asteroid at a random position along the chosen edge.
            position: Vector2 = edge[1](random.uniform(0, 1))

            # Randomize asteroid size to introduce variation in difficulty.
            kind: int = random.randint(1, ASTEROID_KINDS)

            # Spawn the asteroid with the appropriate size and velocity.
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
