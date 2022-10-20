import pygame
import os
from laser import laser
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed):
        super().__init__()
        self.image = pygame.image.load(os.path.join("graphics", "player.png")).convert_alpha() 
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.max_constraint = constraint
        self.laser_time = 0
        self.laser_cooldown = 600
        self.ready = True
        self.lasers = pygame.sprite.Group()
    

    def get_input(self): # Player movement 
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True
    
    
    def constraint(self): # at 0 it should stop and at max width 
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_constraint:
            self.rect.right = self.max_constraint
    
    def shoot_laser(self):
        self.lasers.add(laser(self.rect.center))

    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()
