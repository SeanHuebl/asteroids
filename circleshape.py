import pygame

# Base class for circular game objects, such as asteroids and the player.
class CircleShape(pygame.sprite.Sprite):
    """
    A base class for game objects with a circular shape, providing shared
    behavior like position, velocity, and collision detection.
    
    This class is designed to be extended by more specific game objects.
    """

    def __init__(self, x, y, radius):
        """
        Initialize a circular game object at the given position with a radius.

        Parameters:
            x (float): The x-coordinate of the object's position.
            y (float): The y-coordinate of the object's position.
            radius (float): The radius of the object, used for both size and collision.
        """
        # If containers are set in a subclass, the object is automatically added to sprite groups.
        if hasattr(self, "containers"):
            super().__init__(self.containers)  # Inherits container groups if set
        else:
            super().__init__()  # Call the base initializer without containers

        # Position and velocity vectors for object movement and positioning.
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)  # Velocity starts at zero
        self.radius = radius  # Radius used for drawing and collision detection

    def draw(self, screen):
        """
        Draw the object on the screen.

        This method must be overridden in subclasses to define the specific
        way the circular object is rendered.
        """
        pass

    def update(self, dt):
        """
        Update the object's state based on time passed (dt).

        This method is a placeholder and must be implemented in subclasses 
        to update position, movement, or other state changes.
        """
        pass

    def collision(self, other):
        """
        Check for collision with another circular object.

        The method calculates the distance between this object and another
        object and returns True if they are close enough to collide.

        Parameters:
            other (CircleShape): The other circular object to check for collision.

        Returns:
            bool: True if the objects collide, False otherwise.
        """
        # Calculate the distance between this object and the other object.
        distance_between = self.position.distance_to(other.position)

        # A collision occurs if the distance is less than the sum of their radii.
        if distance_between < self.radius + other.radius:
            return True
        
        return False
