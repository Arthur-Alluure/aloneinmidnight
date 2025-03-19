import pygame
import pygame.image
from pygame.font import Font
from pygame.rect import Rect
from pygame.surface import Surface


from code.Const import WIN_WIDTH, C_ORANGE, MENU_OPTION, C_WHITE, C_YELLOW, C_RED, C_DARK_RED, C_BLACK, C_BLUE
from code.Level import Level


class Menu:
    def __init__(self, janela):
        self.janela = janela
        self.imagem = pygame.image.load('./asset/MenuBg.png').convert_alpha() # carrega a imagem
        self.dimensaoImagem = self.imagem.get_rect(left=0, top=0) # seta o retangulo para ele
        self.opcao_atual = 0  # Indica a opção selecionada (começa com o primeiro item)


    def run(self):

        pygame.mixer_music.load('./asset/Menu.mp3')  # carregando a musica
        pygame.mixer_music.play(-1)  # tocando com -1 para deixar infinito


        while True:
            self.janela.blit(source=self.imagem, dest=self.dimensaoImagem)
            self.menu_text(50, "ALONE", C_WHITE, ((WIN_WIDTH / 2), 40))
            self.menu_text(50, "IN", C_WHITE, ((WIN_WIDTH / 2), 80))
            self.menu_text(50, "MIDNIGHT", C_WHITE, ((WIN_WIDTH / 2), 120))

            self.exibir_menu_opcoes()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:  # Setas para baixo
                        self.opcao_atual = (self.opcao_atual + 1) % len(MENU_OPTION)
                    if event.key == pygame.K_UP:  # Setas para cima
                        self.opcao_atual = (self.opcao_atual - 1) % len(MENU_OPTION)
                    # Seleção de uma opção com Enter
                    if event.key == pygame.K_RETURN:
                        self.selecionar_opcao()


    def exibir_menu_opcoes(self):
        # Desenha cada opção no menu, destacando a opção atual
        for i, opcao in enumerate(MENU_OPTION):
            y_pos = 200 + i * 30  # Define a posição das opções (espacamento entre elas)
            cor = C_WHITE

            # Destacar a opção selecionada
            if i == self.opcao_atual:
                cor = C_RED  # Muda a cor se a opção for selecionada

            # Desenha a opção no menu
            self.menu_text(30, opcao, cor, (WIN_WIDTH / 2, y_pos))


    def selecionar_opcao(self):
        if MENU_OPTION[self.opcao_atual] == 'NOVO JOGO':
            level = Level(self.janela, 'Background')  # Passando o background para o parallax
            level_return = level.run()

            if not level_return: #Game Over
                from code.Game import Game  # Para Evitar importação circular
                game = Game()  # Cria a instância da classe Game
                game.screen_game_over()  # Chama a tela de game over

            if level_return: #Ganhei o jogo
                from code.Game import Game
                game = Game()
                game.screen_victory()


        if MENU_OPTION[self.opcao_atual] == 'TUTORIAL':
            from code.Game import Game
            game = Game()
            game.screen_tutorial()


        elif MENU_OPTION[self.opcao_atual] == 'SAIR':
            pygame.quit()
            quit()



    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont('Gothic', text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.janela.blit(text_surf, text_rect)
