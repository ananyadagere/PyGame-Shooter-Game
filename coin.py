import pygame
import math

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.bounce_counter = 0

    def update(self, player, score):
        self.bounce_counter += 1
        self.rect.y += int(3 * math.sin(self.bounce_counter * 0.1))
        if pygame.sprite.collide_rect(self, player):
            score += 1
            self.kill()
        return score
