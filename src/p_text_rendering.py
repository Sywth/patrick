import pygame
pygame.font.init()
def get_rendered_font(string :str, font_size :int = 14, color : tuple[int]= (0,255,0)):
    """
    Returns rendered font surface instance (pygame.Surface instance) of 'string' provided 
    using default 'Courier' font size 14 color green
    """
    pg_font = pygame.font.SysFont("Courier", font_size)
    str_out = pg_font.render(string, 1, color)
    return str_out
