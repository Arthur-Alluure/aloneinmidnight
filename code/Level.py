import sys
import time

import pygame.mixer_music
from pygame.font import Font
from pygame.rect import Rect
from pygame.surface import Surface

from code.Background import Background
from code.Const import ENTITY_SPEED, WIN_HEIGHT, C_RED
from code.Player import Player
from code.Enemy import Enemy


class Level:

    def __init__(self, janela, name):
        self.name = name
        self.janela = janela
        self.backgrounds = [
            Background(name, (0, 0), ENTITY_SPEED[name] * 0.8)  # Ajustando a velocidade para suavidade
            for name in ENTITY_SPEED
        ]

        self.player = Player("PlayerParado", (10, WIN_HEIGHT))  # Posição inicial do player

        self.enemies = []
        self.spawn_enemy()  # Spawna um inimigo no início
        self.enemies_killed = 0

    def spawn_enemy(self):
        """Cria um novo inimigo e adiciona na lista"""
        enemy = Enemy("EnemyParado", (400, WIN_HEIGHT - 130))  # Posição inicial do inimigo
        self.enemies.append(enemy)


    def run(self):

        pygame.mixer_music.load(f'./asset/Level.mp3')
        pygame.mixer_music.play(-1)

        clock = pygame.time.Clock()  # Garantir que o fps seja constante


        while True:
            clock.tick(60)

            keys = pygame.key.get_pressed()  # Captura os inputs do teclado



            # Atualiza e desenha os backgrounds
            for bg in self.backgrounds:
                bg.move()
                bg.draw(self.janela)

            # Atualiza e desenha o player
            self.player.update(keys, self.backgrounds)
            self.player.draw(self.janela)

            # Atualiza os inimigos
            for enemy in self.enemies[:]:
                if enemy.alive:  # Apenas desenha se ele estiver vivo
                    enemy.update(self.player, self.backgrounds)
                    enemy.draw(self.janela)

                # Se o inimigo morreu e já passaram 6 segundos, remove ele e spawna um novo
                if not enemy.alive and (time.time() - enemy.death_time) > 5:
                    self.enemies.remove(enemy)
                    self.enemies_killed += 1
                    self.spawn_enemy()  # Spawna um novo inimigo após 5 segundos


            if not self.player.alive: #se meu player morrer retorna o level como false
                return False

            if  self.enemies_killed == 10: #Se o Player matar 10 inimigos ele ganha o level
                return True

            self.level_text(25, f'Player 1 - Health: {self.player.health}', C_RED, (10, 25))
            self.level_text(25, f'Lobisomens Mortos: {self.enemies_killed}', C_RED, (350, 25))
            self.level_text(20, f' fps: {clock.get_fps() :.0f}', C_RED, (10, 45))

            pygame.display.flip()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont('Gothic', text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.janela.blit(text_surf, text_rect)