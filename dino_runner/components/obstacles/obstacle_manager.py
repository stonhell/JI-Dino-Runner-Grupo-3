from dino_runner.components.obstacles.cactus import Cactus
import random
import pygame
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.constants import SHIELD_TYPE, SMALL_CACTUS, LARGE_CACTUS

class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            cactus_type = "SMALL" if random.randint(0, 1) == 0 else "LARGE"
            self.obstacles.append(Cactus(cactus_type))
    
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if game.player.type != SHIELD_TYPE:
                    pygame.time.delay(500)
                    game.playing = False
                    game.death_count =+ 1
                    break
                

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacle(self):
        self.obstacles = []

    

   # def reset_obstacle