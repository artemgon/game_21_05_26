import pygame
import sys
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, GREEN, BLUE, RED, TILE_SIZE, SHOOT_COOLDOWN, YELLOW
from sprites import Tank, EnemyTank, Wall

def show_game_over_screen(screen):
    font = pygame.font.SysFont("Arial", 64, bold=True)
    text = font.render("GAME OVER", True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    screen.fill(BLACK)
    screen.blit(text, text_rect)
    pygame.display.flip()
    
    # Чекаємо 3 секунди перед виходом
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Battle Village - Fixed Controls")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()

    player = Tank(SCREEN_WIDTH // 2 - TILE_SIZE // 2, SCREEN_HEIGHT - TILE_SIZE * 2, GREEN)
    all_sprites.add(player)

    wall_positions = [
        (120, 160), (160, 160), (200, 160), (240, 160), 
        (520, 160), (560, 160), (600, 160), (640, 160),
        (80, 280), (120, 280), (320, 280), (360, 280), 
        (400, 280), (440, 280), (640, 280), (680, 280),
        (200, 320), (200, 360), (560, 320), (560, 360),
        (160, 440), (200, 440), (240, 440), (360, 440), 
        (400, 440), (440, 440), (520, 440), (560, 440), (600, 440)
    ]
    for pos in wall_positions:
        wall = Wall(pos[0], pos[1])
        all_sprites.add(wall)
        walls_group.add(wall)

    enemy_spawn_positions = [(80, 60), (380, 60), (680, 60)]
    for pos in enemy_spawn_positions:
        enemy = EnemyTank(pos[0], pos[1])
        all_sprites.add(enemy)
        enemies_group.add(enemy)

    while True:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.shoot(bullets_group, SHOOT_COOLDOWN, "UP", is_enemy=False, color=YELLOW)
                elif event.key == pygame.K_DOWN:
                    player.shoot(bullets_group, SHOOT_COOLDOWN, "DOWN", is_enemy=False, color=YELLOW)
                elif event.key == pygame.K_LEFT:
                    player.shoot(bullets_group, SHOOT_COOLDOWN, "LEFT", is_enemy=False, color=YELLOW)
                elif event.key == pygame.K_RIGHT:
                    player.shoot(bullets_group, SHOOT_COOLDOWN, "RIGHT", is_enemy=False, color=YELLOW)

        for enemy in enemies_group:
            if random.randint(1, 80) == 1:
                enemy.shoot(bullets_group, cooldown=1200, direction=enemy.direction, is_enemy=True, color=BLUE)

        player.update(walls_group)
        enemies_group.update(walls_group)
        bullets_group.update()

        for bullet in list(bullets_group):
            hit_walls = pygame.sprite.spritecollide(bullet, walls_group, False)
            if hit_walls:
                bullet.kill()
                for wall in hit_walls:
                    wall.take_damage()

        for bullet in list(bullets_group):
            if not bullet.is_enemy:
                hit_enemies = pygame.sprite.spritecollide(bullet, enemies_group, True)
                if hit_enemies:
                    bullet.kill()
            else:
                if pygame.sprite.collide_rect(bullet, player):
                    bullet.kill()
                    player.hp -= 1
                    print(f"Влучання! Залишилось: {player.hp} HP")
                    if player.hp <= 0:
                        show_game_over_screen(screen)

        screen.fill(BLACK)
        all_sprites.draw(screen)
        bullets_group.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()