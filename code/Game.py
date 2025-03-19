import pygame
from pygame.font import Font
from pygame.rect import Rect
from pygame.surface import Surface

from code.Const import WIN_WIDTH, WIN_HEIGHT, C_RED, C_BLUE, C_WHITE
from code.Menu import Menu


class Game:

    def __init__(self):
        pygame.init()
        self.janela = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))  # Configura tamanho da tela
        self.imagem = pygame.image.load('./asset/BackgroundGameOver.png').convert_alpha()  # carrega a imagem
        self.dimensaoImagem = self.imagem.get_rect(left=0, top=0)  # seta o retangulo para ele

        self.imagemVitoria = pygame.image.load('./asset/BackgroundWin.png').convert_alpha()
        self.dimensaoImagemVitoria = self.imagem.get_rect(left=0, top=0)

        self.imagemTutorial = pygame.image.load('./asset/BackgroundGameOver.png').convert_alpha()
        self.dimensaoImagemTutorial = self.imagem.get_rect(left=0, top=0)

    def run(self):
        from code.Menu import Menu  # Importação local para evitar a importação circular
        menu = Menu(self.janela)
        menu.run()


    def screen_game_over(self):
        self.janela.blit(source=self.imagem, dest=self.dimensaoImagem)  # Atribui a imagem para a janela
        self.menu_text(50, "Game Over", C_RED, ((WIN_WIDTH / 2), 60))  # Textos do menu
        self.menu_text(25, "A Floresta foi dominada pelos Lobisomens", C_RED, ((WIN_WIDTH / 2), 100))

        self.menu_text(25, "Pressione Enter para Voltar ao Menu", C_RED, ((WIN_WIDTH / 2), 150))

        pygame.mixer_music.load('./asset/Menu.mp3')
        pygame.mixer_music.play(-1)

        pygame.display.flip()  # Atualiza a tela para mostrar as mudanças

        # Espera o jogador pressionar Enter para voltar ao menu
        waiting_for_input = True

        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Habilitando a possibilidade de fechar o programa
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Só sai do loop quando Enter é pressionado
                        waiting_for_input = False  # Sai do loop e volta ao menu

    def screen_victory(self):

        pygame.mixer_music.load('./asset/Menu.mp3')
        pygame.mixer_music.play(-1)

        self.janela.blit(source=self.imagemVitoria, dest=self.dimensaoImagemVitoria)  # Atribui a imagem para a janela
        self.menu_text(50, "VOCÊ VENCEU!!", C_WHITE, ((WIN_WIDTH / 2), 60))  # Textos do menu

        self.menu_text(25, "Parabéns, você concluiu o jogo!", C_BLUE, ((WIN_WIDTH / 2), 150))
        self.menu_text(25, "A floresta agora está pacífica e livre de Lobisomens!", C_BLUE, ((WIN_WIDTH / 2), 180))
        self.menu_text(20, "Pressione Enter para jogar novamente!", C_BLUE, ((WIN_WIDTH / 2), 250))


        pygame.display.flip()  # Atualiza a tela para mostrar as mudanças

        # Espera o jogador pressionar Enter para voltar ao menu
        waiting_for_input = True

        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Habilitando a possibilidade de fechar o programa
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Só sai do loop quando Enter é pressionado
                        waiting_for_input = False  # Sai do loop e volta ao menu


    def screen_tutorial(self):

        self.janela.blit(source=self.imagemTutorial, dest=self.dimensaoImagemTutorial)  # Atribui a imagem para a janela
        self.menu_text(50, "Aprenda a jogar:", C_RED, ((WIN_WIDTH / 2), 60))  # Textos do menu

        self.menu_text(25, "Aperte X para Atacar", C_RED, ((WIN_WIDTH / 2), 130))
        self.menu_text(25, "Controle o Personagem usando as setas direcionais do teclado", C_RED, ((WIN_WIDTH / 2), 150))

        self.menu_text(25, "Seu objetivo é pacificar uma antiga floresta", C_RED,
                       ((WIN_WIDTH / 2), 190))

        self.menu_text(25, "Mate 10 Lobisomens para Vencer!!", C_RED,
                       ((WIN_WIDTH / 2), 210))


        self.menu_text(20, "Pressione Enter para voltar ao menu!", C_RED, ((WIN_WIDTH / 2), 250))




        pygame.display.flip()  # Atualiza a tela para mostrar as mudanças

        # Espera o jogador pressionar Enter para voltar ao menu
        waiting_for_input = True

        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Habilitando a possibilidade de fechar o programa
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Só sai do loop quando Enter é pressionado
                        waiting_for_input = False  # Sai do loop e volta ao menu




    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont('Gothic', text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.janela.blit(text_surf, text_rect)


