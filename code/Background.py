import pygame
from code.Const import ENTITY_SPEED, WIN_WIDTH
from code.Entity import Entity

class Background(Entity):
    def __init__(self, name: str, position: tuple, speed: float):
        super().__init__(name, position)
        self.speed = speed
        self.offset_x = 0
        self.collided = False  # Adiciona flag para controle de colisão

    def move(self):
        if self.collided:
            return  # Se houver colisão, não move o background

        self.offset_x -= self.speed  # Move o background de acordo com a velocidade

        # Se a imagem inteira saiu da tela, reposiciona suavemente
        if self.offset_x <= -WIN_WIDTH:
            self.offset_x += WIN_WIDTH

    def draw(self, screen):
        screen_width, screen_height = screen.get_size()

        # Redimensiona a imagem para ocupar a tela inteira
        scaled_surf = pygame.transform.scale(self.surf, (screen_width, screen_height))

        # Corrige o deslocamento para evitar travamentos
        offset_x = int(self.offset_x) % screen_width

        # Desenha duas cópias da imagem para garantir continuidade
        screen.blit(scaled_surf, (offset_x - screen_width, 0))  # Primeira cópia
        screen.blit(scaled_surf, (offset_x, 0))  # Segunda cópia
