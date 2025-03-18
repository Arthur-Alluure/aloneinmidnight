#C
import pygame.constants

C_ORANGE = (255, 128, 0)
C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_YELLOW = (255, 255, 0)
C_GREEN = (0, 255, 0)
C_CYAN = (0, 255, 255)
C_BLUE = (0, 0, 255)
C_PURPLE = (128, 0, 128)
C_RED = (255, 0, 0)
C_GRAY = (128, 128, 128)
C_DARK_RED =(139,0,0)


#E
ENTITY_SPEED = {
    'Background01': 0,
    'Background02': 1,
    'Background03': 2,
    'Background04': 3,
    'Background05': 4,

}


#G

GAME_HEALTH = {
    'Player1': 100,
    'Enemy1' : 650
}


#M
MENU_OPTION = ('NOVO JOGO',
               'SAIR')



#P
PLAYER_KEY_UP = {
    'Player1': pygame.K_w,
}

PLAYER_KEY_DOWN = {
    'Player1': pygame.K_s,
}

PLAYER_KEY_LEFT = {
    'Player1': pygame.K_a,
}

PLAYER_KEY_RIGHT = {
    'Player1': pygame.K_d,
}



#W
WIN_WIDTH = 576
WIN_HEIGHT = 324