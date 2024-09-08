import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50
BULLET_WIDTH = 5
BULLET_HEIGHT = 10
FPS = 60
SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 3

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Galaga-like Game")

# Load images (you can replace these with your own)
player_img = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
player_img.fill(GREEN)

enemy_img = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
enemy_img.fill(RED)

bullet_img = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
bullet_img.fill(BLACK)

# Player class
class Player:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.dx = 0
        self.bullets = []

    def move(self, keys):
        self.dx = 0
        if keys[pygame.K_LEFT]:
            self.dx = -SPEED
        if keys[pygame.K_RIGHT]:
            self.dx = SPEED
        self.rect.x += self.dx
        self.rect.x = max(0, min(SCREEN_WIDTH - PLAYER_WIDTH, self.rect.x))

    def shoot(self):
        bullet = pygame.Rect(self.rect.centerx - BULLET_WIDTH // 2, self.rect.top, BULLET_WIDTH, BULLET_HEIGHT)
        self.bullets.append(bullet)

    def draw(self):
        screen.blit(player_img, self.rect)
        for bullet in self.bullets:
            pygame.draw.rect(screen, BLACK, bullet)

# Enemy class
class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH), random.randint(-100, -ENEMY_HEIGHT), ENEMY_WIDTH, ENEMY_HEIGHT)

    def move(self):
        self.rect.y += ENEMY_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = random.randint(-100, -ENEMY_HEIGHT)
            self.rect.x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)

    def draw(self):
        screen.blit(enemy_img, self.rect)

# Main game loop
def main():
    clock = pygame.time.Clock()
    player = Player()
    enemies = [Enemy() for _ in range(5)]
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    player.shoot()

        keys = pygame.key.get_pressed()
        if not game_over:
            player.move(keys)

            # Move bullets and enemies
            for bullet in player.bullets[:]:
                bullet.y -= BULLET_SPEED
                if bullet.bottom < 0:
                    player.bullets.remove(bullet)

            for enemy in enemies:
                enemy.move()

                # Check for collisions between bullets and enemies
                for bullet in player.bullets[:]:
                    if enemy.rect.colliderect(bullet):
                        enemies.remove(enemy)
                        player.bullets.remove(bullet)
                        enemies.append(Enemy())  # Respawn enemy

                # Check for collision between player and enemies
                if player.rect.colliderect(enemy.rect):
                    game_over = True

        # Fill the screen with white
        screen.fill(WHITE)

        # Draw the player and enemies
        player.draw()
        for enemy in enemies:
            enemy.draw()

        # If game over, show game over text
        if game_over:
            font = pygame.font.Font(None, 74)
            game_over_text = font.render("GAME OVER", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()