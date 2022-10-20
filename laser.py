import pygame

class laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed = 8, height = 800) -> None:
        super().__init__()
        self.image = pygame.Surface((4,20))
        self.image.fill('red')
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.y_constraint = height

    def update(self):
        self.rect.y -= self.speed
        self.destroy()

    def destroy(self):
        if self.rect.y <= 0 or self.rect.y >= self.y_constraint:
            self.kill()
        