import pygame
import random
import sys

# ---------------------------
#  Config & Constants
# ---------------------------
WIDTH, HEIGHT = 480, 640
FPS = 60
PLAYER_SPEED = 5
BULLET_SPEED = -10
ENEMY_SPEED = 3
SPAWN_INTERVAL = 1000  # ms between enemy spawns
SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1

# ---------------------------
#  Init
# ---------------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Shmup")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)

# ---------------------------
#  Sprites
# ---------------------------
class Player(pygame.sprite.Sprite):
    """Green rectangle the player moves left↔right and shoots."""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))

    def update(self):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * PLAYER_SPEED
        self.rect.x += dx
        self.rect.clamp_ip(screen.get_rect())  # keep on‑screen

    def shoot(self):
        bullet = Bullet(self.rect.midtop)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Bullet(pygame.sprite.Sprite):
    """Yellow shot that travels upward and despawns off‑screen."""

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(midbottom=pos)

    def update(self):
        self.rect.y += BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    """Red rectangle that spawns at random x and falls downward."""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(midbottom=(random.randint(20, WIDTH - 20), -10))

    def update(self):
        self.rect.y += ENEMY_SPEED
        if self.rect.top > HEIGHT:
            self.kill()


# ---------------------------
#  Helpers
# ---------------------------

def draw_text(surf, text, pos):
    img = font.render(text, True, (255, 255, 255))
    surf.blit(img, pos)


# ---------------------------
#  Main game loop
# ---------------------------

def main():
    global all_sprites, bullets, enemies
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    # schedule enemy spawns
    pygame.time.set_timer(SPAWN_ENEMY_EVENT, SPAWN_INTERVAL)

    score = 0
    running = True
    game_over = False

    while running:
        clock.tick(FPS)

        # --- events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SPAWN_ENEMY_EVENT and not game_over:
                enemy = Enemy()
                all_sprites.add(enemy)
                enemies.add(enemy)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    player.shoot()
                elif event.key == pygame.K_r and game_over:
                    return main()  # quick restart

        # --- update ---
        if not game_over:
            all_sprites.update()
            # bullet ↔ enemy collisions
            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
            score += len(hits)
            # enemy ↔ player collision → game over
            if pygame.sprite.spritecollideany(player, enemies):
                game_over = True

        # --- draw ---
        screen.fill((20, 20, 40))
        all_sprites.draw(screen)
        draw_text(screen, f"Score: {score}", (10, 10))
        if game_over:
            draw_text(screen, "GAME OVER – press R to restart", (WIDTH // 2 - 150, HEIGHT // 2))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
