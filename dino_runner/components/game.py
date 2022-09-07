from email.mime import image
import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.constants import (BG, FONT_STYLE, FPS, ICON, ICONM, SCREEN_HEIGHT,
                                         SCREEN_WIDTH, TITLE)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 12
        self.x_pos_bg = 0
        self.y_pos_bg = 350

        self.player = Dinosaur()
        self.obstacles_manager = ObstacleManager()

        self.running = False
        self.score = 0
        self.death_count = 0

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.obstacles_manager.reset_obstacle()
        while self.playing:
            self.events()
            self.update()
            self.draw()
       
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False            

    def update(self):
        self.update_score()
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacles_manager.update(self)

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 5 


    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.draw_score()
        self.player.draw(self.screen)
        self.obstacles_manager.draw(self.screen)
        pygame.display.update()
        

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 50)
        self.screen.blit(text, text_rect)

    def habdle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                self.score = 0
            elif event.type == pygame.KEYDOWN:
                self.run()

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render("Press any key to start", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (half_screen_width, half_screen_height)
        self.screen.blit(text, text_rect)
                    #DESING MENU
        self.screen.blit(ICON, (half_screen_height +48, half_screen_width -310))
        self.screen.blit(ICON, (half_screen_height +411, half_screen_width -310))
        self.screen.blit(ICONM, (half_screen_height +150, half_screen_width -310))
        self.screen.blit(ICONM, (half_screen_height +280, half_screen_width -310))
        
        pygame.display.update()
        self.habdle_events_on_menu()