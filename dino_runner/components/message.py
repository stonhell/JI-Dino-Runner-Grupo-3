from email import message
import pygame
from dino_runner.utils.constants import FONT_STYLE, SCREEN_HEIGHT, SCREEN_WIDTH

FONT_COLOR = (0, 0, 0)
FONT_SIZE = 30
FONT_STYLE = "freesansbold.ttf"

def draw_message(
    message,
    screen,
    font_color=FONT_COLOR,
    font_zise=FONT_SIZE,
    pos_y_center=SCREEN_HEIGHT // 2,
    pos_x_center=SCREEN_WIDTH // 2
):
    font = pygame.font.Font(FONT_STYLE, font_zise)
    text = font.render(message, True, font_color)
    text_rect = text.get_rect()
    text_rect.center = (pos_x_center, pos_y_center)
    screen.blit(text, text_rect)
