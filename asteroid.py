import pygame
import random
from pygame.surface import Surface
from pygame.math import Vector2

from circleshape import CircleShape
from constants import *

class Asteroid(CircleShape):
    """
    Class representing an asteroid object in the game. Inherits from CircleShape.
    
    Asteroids are circular objects that move, can be drawn on the screen, 
    and can split into smaller pieces when destroyed.
    """
    
    def __init__(self, x: float, y: float, radius: float) -> None:
        """
        Initialize an asteroid at the given position with a specified radius.

        Parameters:
            x (float): The x-coordinate of the asteroid's position.
            y (float): The y-coordinate of the asteroid's position.
            radius (float): The radius of the asteroid, which determines its size.
        """
        super().__init__(x, y, radius)

    def draw(self, screen: Surface) -> None:
        """
        Draw the asteroid as a white circle on the screen.

        Parameters:
            screen (Surface): The Pygame surface to draw the asteroid on.
        """
        pygame.draw.circle(screen, 'white', self.position, self.radius, 2)

    def update(self, dt: float) -> None:
        """
        Update the asteroid's position based on its velocity and the time delta.

        This ensures smooth motion by adjusting the position relative to
        the time that has passed since the last frame.

        Parameters:
            dt (float): Time delta since the last frame, used to adjust movement.
        """
        self.position += self.velocity * dt

    def split(self) -> None:
        """
        Split the asteroid into two smaller asteroids upon destruction.

        If the asteroid is larger than the minimum allowed radius, it will split
        into two smaller asteroids, each with randomized directions based on the
        current velocity. If the asteroid is too small, it will simply be destroyed.
        """
        self.kill()  # Remove the current asteroid from the game

        # If the asteroid is already at the minimum size, don't split it further.
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        # Randomly determine the angle by which the asteroid's velocity will split.
        angle: float = random.uniform(20, 50)

        # Create two new velocity vectors for the split asteroids, deviating by the angle.
        asteroid_vector_1: Vector2 = self.velocity.rotate(angle)
        asteroid_vector_2: Vector2 = self.velocity.rotate(-angle)

        # Set the radius of the split asteroids to be smaller than the original.
        new_radius: float = self.radius - ASTEROID_MIN_RADIUS

        # Create the two smaller asteroids at the same position as the original.
        asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)

        # Give the new asteroids slightly increased speed to make the gameplay more dynamic.
        asteroid_1.velocity = asteroid_vector_1 * 1.2
        asteroid_2.velocity = asteroid_vector_2 * 1.2
