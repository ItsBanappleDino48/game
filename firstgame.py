import pygame
import random

# Game setup
pygame.init()
WIDTH, HEIGHT = 800, 600
WHITE, RED, GREEN = (255, 255, 255), (255, 0, 0), (0, 255, 0)
PLAYER_SIZE, ENEMY_SIZE, COIN_SIZE = 50, 30, 25

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Easter Coin Hunt")

player_x, player_y = WIDTH // 2, HEIGHT - PLAYER_SIZE - 10
player_speed = 5
score = 0

enemies = [[random.randint(0, WIDTH - ENEMY_SIZE), random.randint(-HEIGHT, 0), random.randint(3, 6)] for _ in range(5)]
coins = [[random.randint(0, WIDTH - COIN_SIZE), random.randint(-HEIGHT, 0)] for _ in range(5)]

# Game loop
running = True
clock = pygame.time.Clock()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - PLAYER_SIZE:
        player_x += player_speed

    # Move enemies
    for enemy in enemies:
        enemy[1] += enemy[2]
        if enemy[1] > HEIGHT:
            enemy[1] = random.randint(-HEIGHT, -ENEMY_SIZE)
            enemy[0] = random.randint(0, WIDTH - ENEMY_SIZE)
        if player_x < enemy[0] + ENEMY_SIZE and player_x + PLAYER_SIZE > enemy[0] and \
           player_y < enemy[1] + ENEMY_SIZE and player_y + PLAYER_SIZE > enemy[1]:
            running = False  # collision

    # Move coins
    for coin in coins:
        coin[1] += 5
        if coin[1] > HEIGHT:
            coin[1] = random.randint(-HEIGHT, -COIN_SIZE)
            coin[0] = random.randint(0, WIDTH - COIN_SIZE)
        if player_x < coin[0] + COIN_SIZE and player_x + PLAYER_SIZE > coin[0] and \
           player_y < coin[1] + COIN_SIZE and player_y + PLAYER_SIZE > coin[1]:
            score += 1
            player_speed += 0.2  # Slight speed boost
            coin[1] = random.randint(-HEIGHT, -COIN_SIZE)
            coin[0] = random.randint(0, WIDTH - COIN_SIZE)

    # Draw player, enemies, and coins
    pygame.draw.rect(screen, GREEN, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], ENEMY_SIZE, ENEMY_SIZE))
    for coin in coins:
        pygame.draw.circle(screen, (255, 223, 0), (coin[0] + COIN_SIZE // 2, coin[1] + COIN_SIZE // 2), COIN_SIZE // 2)

    # Score display
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

# Game over
pygame.quit()
print("\n🎮 Game Over!")
print(f"Final Score: {score}")
