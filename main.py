import pygame
import sys

# Import custom game objects and constants
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import *
from player import Player
from shot import Shot


def main():
    """
    Run the Asteroids game.

    Initializes the game, sets up the screen, and manages the game loop.
    """
    # Initialize Pygame and set up the display screen.
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Create a clock to manage the game frame rate.
    clock = pygame.time.Clock()
    dt = 0  # Time delta to keep movements consistent across different frame rates.

    # Create sprite groups for updateable and drawable objects.
    # The distinction allows us to update game logic separately from what we draw.
    updateable = pygame.sprite.Group()  # Objects that require updating each frame.
    drawable = pygame.sprite.Group()    # Objects that need to be drawn to the screen.
    asteroids = pygame.sprite.Group()   # Store all asteroids for collision detection.
    shots = pygame.sprite.Group()       # Store player shots for collision detection.

    # Assign sprite groups to each game object type, enabling automatic updates/drawing.
    Player.containers = (updateable, drawable)
    Asteroid.containers = (updateable, drawable, asteroids)
    AsteroidField.containers = updateable
    Shot.containers = (shots, updateable, drawable)

    # Instantiate the player at the center of the screen and create an asteroid field.
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()  # Automatically populates the screen with asteroids.

    # Main game loop.
    while True:
        # Event handling for user input or window closure.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # Exit the game loop if the user closes the window.
        
        # Fill the screen with black before drawing the next frame.
        # This prevents "ghosting" of previous frames.
        screen.fill(color='black')

        # Update all objects that need logic calculations (e.g., movement, physics).
        # The time delta (dt) ensures smooth movement by adjusting changes based on elapsed time.
        for obj in updateable:
            obj.update(dt)

        # Collision detection between asteroids and the player or bullets.
        # Checking for collisions here reduces complexity by separating concerns.
        for asteroid in asteroids:
            if asteroid.collision(player):  # If the player hits an asteroid.
                print("Game over!")
                sys.exit()  # End the game; this could later trigger a game-over screen.
            
            # Check if any player shots have hit an asteroid.
            for bullet in shots:
                if asteroid.collision(bullet):
                    asteroid.split()  # Asteroids split into smaller ones on hit.
                    bullet.kill()  # Remove the shot after it hits an asteroid.

        # Draw all drawable objects (player, asteroids, shots, etc.) onto the screen.
        # Separating drawing logic ensures that visual updates are clear and independent.
        for obj in drawable:
            obj.draw(screen)

        # Update the screen display after drawing all objects.
        pygame.display.flip()

        # Maintain a consistent frame rate of 60 FPS and calculate time delta for movement updates.
        dt = clock.tick(60) / 1000  # Dividing by 1000 converts milliseconds to seconds for dt.


# Run the game when the script is executed directly.
if __name__ == "__main__":
    main()
