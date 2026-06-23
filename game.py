import pygame
import random
import sys

# --- GAME CONFIGURATION ---
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (150, 0, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🛸 Fighter Jet vs Aliens: Level 1-10 🚀")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Impact", 28)
large_font = pygame.font.SysFont("Impact", 60)

# --- GAME OBJECT CLASSES ---

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Creating a custom geometric vector shape for the Fighter Jet
        self.image = pygame.Surface((50, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, CYAN, [(25, 0), (50, 40), (25, 30), (0, 40)])
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed = 7
        self.weapon_level = 1

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def shoot(self):
        if self.weapon_level == 1:
            # Single straight laser shot
            laser = Laser(self.rect.centerx, self.rect.top, 0)
            all_sprites.add(laser)
            lasers.add(laser)
        elif self.weapon_level == 2:
            # Double dual straight laser shots
            l1 = Laser(self.rect.left + 5, self.rect.top, 0)
            l2 = Laser(self.rect.right - 5, self.rect.top, 0)
            all_sprites.add(l1, l2)
            lasers.add(l1, l2)
        else:
            # Weapon level 3+: Triple spread laser shot
            l1 = Laser(self.rect.centerx, self.rect.top, 0)
            l2 = Laser(self.rect.left, self.rect.top, -2) # Angled left
            l3 = Laser(self.rect.right, self.rect.top, 2)  # Angled right
            all_sprites.add(l1, l2, l3)
            lasers.add(l1, l2, l3)

class Alien(pygame.sprite.Sprite):
    def __init__(self, current_level):
        super().__init__()
        self.image = pygame.Surface((40, 30), pygame.SRCALPHA)
        # Dynamic colored variants based on incoming threat difficulty
        color = PURPLE if current_level > 5 else RED
        pygame.draw.ellipse(self.image, color, [0, 5, 40, 20])
        pygame.draw.circle(self.image, GREEN, (20, 15), 6) # Alien core eye
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 40)
        self.rect.y = random.randint(-100, -40)
        # Speed increases progressively with level scaling
        self.speed_y = random.randint(2, 4 + current_level)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - 40)
            self.rect.y = random.randint(-100, -40)

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x):
        super().__init__()
        self.image = pygame.Surface((4, 15))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10
        self.speed_x = speed_x

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if self.rect.bottom < 0 or self.rect.left < 0 or self.rect.right > WIDTH:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (12, 12), 12)
        # Draw a little white cross to show it's a structural weapon upgrade
        pygame.draw.rect(self.image, WHITE, [10, 4, 4, 16])
        pygame.draw.rect(self.image, WHITE, [4, 10, 16, 4])
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed_y = 3

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.kill()

# --- INITIALIZE ENTITY GROUPS ---
all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
lasers = pygame.sprite.Group()
powerups = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Game state track counters
score = 0
level = 1
kills_for_next_level = 15
aliens_killed_this_level = 0
game_over = False
victory = False

def spawn_aliens(count):
    for _ in range(count):
        alien = Alien(level)
        all_sprites.add(alien)
        aliens.add(alien)

# Initial population wave spawn
spawn_aliens(6)

# --- CORE GAME LOOP ENGINE ---
running = True
while running:
    clock.tick(FPS)

    # 1. Event Input Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over and not victory:
                player.shoot()
            if event.key == pygame.K_r and (game_over or victory):
                # Reset game states completely
                all_sprites.empty()
                aliens.empty()
                lasers.empty()
                powerups.empty()
                player = Player()
                all_sprites.add(player)
                score = 0
                level = 1
                aliens_killed_this_level = 0
                game_over = False
                victory = False
                spawn_aliens(6)

    # 2. Update Engine Positions
    if not game_over and not victory:
        all_sprites.update()

        # Check collision: Lasers hitting Alien targets
        hits = pygame.sprite.groupcollide(aliens, lasers, True, True)
        for hit in hits:
            score += 10
            aliens_killed_this_level += 1
            
            # Chance to drop an upgrade item on destruction (25% rate)
            if random.random() < 0.25:
                p_up = PowerUp(hit.rect.centerx, hit.rect.centery)
                all_sprites.add(p_up)
                powerups.add(p_up)
            
            # Replace destroyed alien ship instantly
            spawn_aliens(1)

            # Check level progress thresholds
            if aliens_killed_this_level >= kills_for_next_level:
                level += 1
                aliens_killed_this_level = 0
                if level > 10:
                    victory = True
                else:
                    # Scale up enemy volume for added level trickiness
                    spawn_aliens(2) 

        # Check collision: Player collecting Power-Up drops
        power_hits = pygame.sprite.spritecollide(player, powerups, True)
        for p in power_hits:
            player.weapon_level += 1

        # Check collision: Alien colliding with Player Jet
        if pygame.sprite.spritecollide(player, aliens, False):
            game_over = True

    # 3. Canvas Frame Rendering
    screen.fill(BLACK)
    
    # Draw random scrolling star particles to create space movement depth effect
    for _ in range(3):
        pygame.draw.circle(screen, WHITE, (random.randint(0, WIDTH), random.randint(0, HEIGHT)), 1)

    all_sprites.draw(screen)

    # Draw HUD text elements
    score_txt = font.render(f"SCORE: {score}", True, WHITE)
    level_txt = font.render(f"LEVEL: {level}/10", True, GREEN)
    weapon_txt = font.render(f"WEAPON POWER: LVL {player.weapon_level}", True, YELLOW)
    progress_txt = font.render(f"NEXT LEVEL BAR: {aliens_killed_this_level}/{kills_for_next_level}", True, CYAN)

    screen.blit(score_txt, (10, 10))
    screen.blit(level_txt, (10, 45))
    screen.blit(progress_txt, (10, 80))
    screen.blit(weapon_txt, (WIDTH - weapon_txt.get_width() - 10, 10))

    # Handle Overlay screens
    if game_over:
        go_txt = large_font.render("GAME OVER", True, RED)
        r_txt = font.render("Press 'R' key to Restart your Jet", True, WHITE)
        screen.blit(go_txt, (WIDTH // 2 - go_txt.get_width() // 2, HEIGHT // 3))
        screen.blit(r_txt, (WIDTH // 2 - r_txt.get_width() // 2, HEIGHT // 2))

    if victory:
        vic_txt = large_font.render("VICTORY! GALAXY SAVED!", True, GREEN)
        r_txt = font.render("Press 'R' key to Play Again", True, WHITE)
        screen.blit(vic_txt, (WIDTH // 2 - vic_txt.get_width() // 2, HEIGHT // 3))
        screen.blit(r_txt, (WIDTH // 2 - r_txt.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()




##to run this game run (python game.py) in your terminal after installing pygame library using (pip install pygame)