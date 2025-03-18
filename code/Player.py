import pygame

from code.Const import WIN_WIDTH, WIN_HEIGHT
from code.Entity import Entity
from code.Const import GAME_HEALTH

class Player(Entity):


    #variaveis para os frames

    FRAME_RATES = { #velocidade de cada animação + frames mais rapida a troca de quadros
        "idle": 5,
        "walk": 8,
        "run": 8,
        "jump": 12,
        "attack": 6
    }

    FRAME_COUNTS = {  #quantidade de frames disponivel para cada ação do spritesheet (walk tem 8 imagens, logo 8 frames)
        "idle": 6,
        "walk": 8,
        "run": 8,
        "jump": 12,
        "attack": 5
    }

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

        self.spritesheets = {
            "walk": pygame.image.load("./asset/PlayerAnda.png"),
            "idle": pygame.image.load("./asset/PlayerParado.png"),
            "run": pygame.image.load("./asset/PlayerCorre.png"),
            "jump": pygame.image.load("./asset/PlayerPulo.png"),
            "attack": pygame.image.load("./asset/PlayerAttack.png")
        }

        self.health = GAME_HEALTH['Player1'] #vida do player

        self.current_action = "walk" #começa com ele andando
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.image = self.get_frame()  # Primeiro frame
        self.rect = self.image.get_rect(topleft=position)
        self.speed = 2
        self.gravity = 1
        self.velocity_y = 0
        self.on_ground = False
        self.attacking = False
        self.alive = True


    def get_frame(self):
        """Pega o frame atual da animação para exibir na tela"""

        sheet = self.spritesheets[self.current_action] #pega a ação atual
        frame_count = self.FRAME_COUNTS[self.current_action]
        frame_width = sheet.get_width() // frame_count
        frame_height = sheet.get_height()

        frame = sheet.subsurface(pygame.Rect(self.frame_index * frame_width, 0, frame_width, frame_height)) #corta o spritesheet corretamente
        return pygame.transform.scale(frame, (frame_width * 1, frame_height * 1))  # Aumenta o tamanho da escala do player

    def animate(self):
        """Atualiza a animação com base no tempo"""
        now = pygame.time.get_ticks()
        frame_rate = 1000 // self.FRAME_RATES[self.current_action] #quanto cada frame vai durar

        if now - self.last_update > frame_rate: #atualiza o frame
            self.last_update = now
            self.frame_index += 1

            if self.frame_index >= self.FRAME_COUNTS[self.current_action]:
                if self.current_action == "attack": #ataca e reseta
                    self.attacking = False
                    self.current_action = "idle" #volta a andar e reseta o frame
                self.frame_index = 0

            self.image = self.get_frame() #atualiza

    def apply_gravity(self):
        """Aplica gravidade ao Player"""
        if not self.on_ground:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y
        if self.rect.bottom >= WIN_HEIGHT:  # Chão correspondente a altura da imagem (pe do player)
            self.rect.bottom = WIN_HEIGHT
            self.on_ground = True
            self.velocity_y = 0 #se atingir o chao para

    def move(self, keys, backgrounds):
        """Movimentação do player e ajuste do background"""
        if self.attacking or any(bg.collided for bg in backgrounds): # Se atacando ou colidiu, não mexe o fundo
            return

        moving = False

        if keys[pygame.K_LEFT]:
            for bg in backgrounds:
                bg.offset_x += bg.speed  # Se esquerda, pausa o background e ele fica parado
            self.current_action = "idle"
            moving = True
        elif keys[pygame.K_RIGHT]:
            for bg in backgrounds:
                bg.offset_x -= bg.speed  # Move o background para a esquerda
            self.current_action = "run"
            moving = True

        else:
            self.current_action = "walk"

        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -15
            self.on_ground = False
            self.current_action = "jump"

        if keys[pygame.K_x] and not self.attacking:  # Ataque com a tecla 'X'
            self.current_action = "attack"
            self.attacking = True
            self.frame_index = 0  # Reinicia a animação do ataque

    def update(self, keys, backgrounds): #atualiza tudo a cada frame
        self.move(keys, backgrounds)
        self.apply_gravity()
        self.animate()

    def draw(self, screen):  #desenha o player
        screen.blit(self.image, self.rect.topleft)

    def take_damage(self, amount):
        """Reduz a vida do inimigo quando atingido."""
        if not self.alive:
            return  # Se já morreu, ignora qualquer dano

        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.alive = False
            print("Player morreu!")






