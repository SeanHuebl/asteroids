import pygame

from circleshape import CircleShape
from constants import *

class Shot(CircleShape):
    """
    Class representing a projectile (shot) fired by the player. Inherits from CircleShape.
    
    Shots are small circular objects that move in a straight line based on the direction
    and speed set when they are fired.
    """
    
    def __init__(self, x, y):
        """
        Initialize a shot at the given position with a predefined radius.

        Shots have a smaller radius compared to other game objects and start 
        from the player's position when fired.

        Parameters:
            x (float): The x-coordinate of the shot's initial position.
            y (float): The y-coordinate of the shot's initial position.
        """
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
        """
        Draw the shot as a white circle on the screen.

        Parameters:
            screen (Surface): The Pygame surface to draw the shot on.
        """
        pygame.draw.circle(screen, 'white', self.position, self.radius, 2)

    def update(self, dt):
        """
        Update the shot's position based on its velocity and the time delta.

        This function moves the shot in the direction it was fired, with the 
        velocity being set when the shot is created.

        Parameters:
            dt (float): Time delta since the last frame, used to adjust the shot's movement.
        """
        self.position += self.velocity * dt
