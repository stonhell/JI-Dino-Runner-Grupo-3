from email.mime import image
from unittest.mock import DEFAULT
import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.message import draw_message
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.utils.constants import (BG, DEFAULT_TYPE, FONT_STYLE, FPS, ICON, ICONM, SCREEN_HEIGHT,
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
        self.power_up_manager = PowerUpManager()

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
        self.power_up_manager.reset_power_ups()
        self.game_speed = 12
        self.score = 0
        self.playing = True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False            

    def update(self):
        self.update_score()
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacles_manager.update(self)
        self.power_up_manager.update(self.score, self.game_speed, self.player)

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 5 

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.draw_score()
        self.draw_power_up_time()
        self.player.draw(self.screen)
        self.obstacles_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
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
        draw_message(
            f"Points: {self.score}",
            font_zise=22,
            pos_x_center=1000,
            pos_y_center=50
        )

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.has_power_up_time_up - pygame.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                draw_message(
                f"{self.player.type.capitalize()} enable for{time_to_show} seconds. ",
                self.screen,
                font_zise=18,
                pos_x_center=500,
                pos_y_center=40
            )
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                self.score = 0
            elif event.type == pygame.KEYDOWN:
                self.run()
                self.score = 0
                self.game_speed = 12
            else:
                break

    def show_menu(self):
        self.screen.fill((40, 180, 99)) # 40, 180, 99   / 53, 205, 173
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            draw_message("Press any key to start", self.screen)
        else:
            draw_message("Pess any key to restart", self.screen)
            draw_message(
                f"Your score: {self.score}",
                self.scree,
                pos_y_center=half_screen_height + 50
            )
            draw_message(
                f"Death count: {self.death_count}",
                self.screen,
                pos_y_center=half_screen_height + 100
            )
        self.screen.blit(ICON, (half_screen_height +48, half_screen_width -310))
        self.screen.blit(ICON, (half_screen_height +411, half_screen_width -310))
        self.screen.blit(ICONM, (half_screen_height +145, half_screen_width -310))
        self.screen.blit(ICONM, (half_screen_height +280, half_screen_width -310))

        pygame.display.update()
        self.handle_events_on_menu()