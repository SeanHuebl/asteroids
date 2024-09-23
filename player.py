import pygame
from pygame.surface import Surface
from pygame.math import Vector2

from constants import *
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    """
    A class representing the player-controlled spaceship. Inherits from CircleShape
    and provides additional functionality for player movement, rotation, and shooting.
    """

    def __init__(self, x: float, y: float) -> None:
        """
        Initialize the player at the given position with a predefined radius.

        Parameters:
            x (float): The x-coordinate of the player's initial position.
            y (float): The y-coordinate of the player's initial position.
        """
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation: float = 0  # Player starts facing up (rotation 0)
        self.timer: float = 0     # Timer for managing shooting cooldown

    def triangle(self) -> list[Vector2]:
        """
        Calculate the vertices of the triangle representing the player on the screen.

        The player's shape is a triangle that points in the direction of its rotation.
        This function calculates the positions of the three vertices based on the player's
        current position, rotation, and size.

        Returns:
            list[Vector2]: A list of three points representing the triangle's vertices.
        """
        forward: Vector2 = pygame.Vector2(0, 1).rotate(self.rotation)  # Forward direction based on rotation
        right: Vector2 = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5  # Right-side direction
        a: Vector2 = self.position + forward * self.radius  # Front vertex
        b: Vector2 = self.position - forward * self.radius - right  # Bottom-left vertex
        c: Vector2 = self.position - forward * self.radius + right  # Bottom-right vertex
        return [a, b, c]

    def draw(self, screen: Surface) -> None:
        """
        Draw the player as a white triangle on the screen.

        Parameters:
            screen (Surface): The Pygame surface to draw the player on.
        """
        pygame.draw.polygon(screen, 'white', self.triangle(), 2)

    def rotate(self, dt: float) -> None:
        """
        Rotate the player based on time delta and turning speed.

        This function adjusts the player's rotation over time, allowing the player
        to rotate left or right based on user input.

        Parameters:
            dt (float): Time delta since the last frame, used to adjust rotation speed.
        """
        self.rotation += dt * PLAYER_TURN_SPEED

    def update(self, dt: float) -> None:
        """
        Update the player's state, including handling movement, rotation, and shooting.

        This method processes user input, such as turning, moving forward/backward,
        and shooting, and updates the player's state accordingly.

        Parameters:
            dt (float): Time delta since the last frame, used for frame-rate-independent updates.
        """
        self.timer -= dt  # Decrease the shot cooldown timer

        keys = pygame.key.get_pressed()

        # Handle rotation (left: A, right: D)
        if keys[pygame.K_a]:
            self.rotate(-dt)  # Rotate counterclockwise
        if keys[pygame.K_d]:
            self.rotate(dt)  # Rotate clockwise

        # Handle movement (forward: W, backward: S)
        if keys[pygame.K_w]:
            self.move(dt)  # Move forward
        if keys[pygame.K_s]:
            self.move(-dt)  # Move backward

        # Handle shooting (Spacebar)
        if keys[pygame.K_SPACE]:
            self.shoot(dt)

    def move(self, dt: float) -> None:
        """
        Move the player in the direction it's facing based on player speed.

        This method moves the player forward or backward, depending on the user's input.

        Parameters:
            dt (float): Time delta since the last frame, used to adjust movement speed.
        """
        forward: Vector2 = pygame.Vector2(0, 1).rotate(self.rotation)  # Calculate forward direction based on rotation
        self.position += forward * PLAYER_SPEED * dt  # Update the player's position

    def shoot(self, dt: float) -> None:
        """
        Shoot a projectile from the player's current position in the direction it's facing.

        The function ensures that the player can only shoot when the cooldown timer
        has expired, preventing rapid fire.

        Parameters:
            dt (float): Time delta since the last frame, used for frame-rate-independent shooting.
        """
        if self.timer > 0:
            return  # If the cooldown timer is still active, prevent shooting

        # Create a new shot at the player's current position
        shot: Shot = Shot(self.position.x, self.position.y)
        
        # Set the shot's velocity to match the player's current direction
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity *= PLAYER_SHOOT_SPEED  # Set the shot's speed

        # Reset the cooldown timer after shooting
        self.timer = PLAYER_SHOOT_COOLDOWN
