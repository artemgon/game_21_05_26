import pygame
import random
from config import TILE_SIZE, TANK_SPEED, ENEMY_SPEED, BULLET_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, BLUE, YELLOW, WALL_CRISP, WALL_DAMAGED, WALL_BROKEN

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.hp = 10  
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE)).convert()
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.direction = "UP"
        self.last_shot = pygame.time.get_ticks()

    def update(self, walls):
        keys = pygame.key.get_pressed()
        old_x, old_y = self.rect.x, self.rect.y
        
        if keys[pygame.K_a]:
            self.rect.x -= TANK_SPEED
            self.direction = "LEFT"
            if pygame.sprite.spritecollideany(self, walls): self.rect.x = old_x
        elif keys[pygame.K_d]:
            self.rect.x += TANK_SPEED
            self.direction = "RIGHT"
            if pygame.sprite.spritecollideany(self, walls): self.rect.x = old_x
        elif keys[pygame.K_w]:
            self.rect.y -= TANK_SPEED
            self.direction = "UP"
            if pygame.sprite.spritecollideany(self, walls): self.rect.y = old_y
        elif keys[pygame.K_s]:
            self.rect.y += TANK_SPEED
            self.direction = "DOWN"
            if pygame.sprite.spritecollideany(self, walls): self.rect.y = old_y

        self.clamp_to_screen()

    def clamp_to_screen(self):
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT: self.rect.bottom = SCREEN_HEIGHT

    def shoot(self, bullet_group, cooldown, direction, is_enemy=False, color=YELLOW):
        now = pygame.time.get_ticks()
        if now - self.last_shot > cooldown:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.centery, direction, color, is_enemy)
            bullet_group.add(bullet)


class EnemyTank(Tank):
    def __init__(self, x, y):
        super().__init__(x, y, BLUE)  
        self.direction = "DOWN"
        self.last_move_change = pygame.time.get_ticks()

    def update(self, walls):
        now = pygame.time.get_ticks()
        old_x, old_y = self.rect.x, self.rect.y

        if now - self.last_move_change > random.randint(1500, 3000):
            self.direction = random.choices(["DOWN", "LEFT", "RIGHT", "UP"], weights=[60, 15, 15, 10])[0]
            self.last_move_change = now

        if self.direction == "LEFT":
            self.rect.x -= ENEMY_SPEED
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.x = old_x
                self.direction = random.choice(["DOWN", "RIGHT"])
        elif self.direction == "RIGHT":
            self.rect.x += ENEMY_SPEED
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.x = old_x
                self.direction = random.choice(["DOWN", "LEFT"])
        elif self.direction == "UP":
            self.rect.y -= ENEMY_SPEED
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.y = old_y
                self.direction = random.choice(["DOWN", "LEFT", "RIGHT"])
        elif self.direction == "DOWN":
            self.rect.y += ENEMY_SPEED
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.y = old_y
                self.direction = random.choice(["LEFT", "RIGHT", "UP"])

        self.clamp_to_screen()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, color, is_enemy):
        super().__init__()
        self.image = pygame.Surface((8, 8)).convert()
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.is_enemy = is_enemy

    def update(self):
        if self.direction == "LEFT": self.rect.x -= BULLET_SPEED
        elif self.direction == "RIGHT": self.rect.x += BULLET_SPEED
        elif self.direction == "UP": self.rect.y -= BULLET_SPEED
        elif self.direction == "DOWN": self.rect.y += BULLET_SPEED

        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.hp = 3
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE)).convert()
        self.image.fill(WALL_CRISP)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def take_damage(self):
        self.hp -= 1
        if self.hp == 2: self.image.fill(WALL_DAMAGED)
        elif self.hp == 1: self.image.fill(WALL_BROKEN)
        elif self.hp <= 0: self.kill()