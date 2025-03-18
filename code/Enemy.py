import pygame
from code.Const import WIN_WIDTH, WIN_HEIGHT, ENTITY_SPEED
from code.Entity import Entity
import time

from code.Const import GAME_HEALTH


class Enemy(Entity):
    FRAME_RATES = {
        "idle": 5,
        "attack": 6,
        "walk": 10
    }

    FRAME_COUNTS = {
        "idle": 8,
        "attack": 6,
        "walk": 11
    }

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

        self.spritesheets = {
            "idle": pygame.transform.flip(pygame.image.load("./asset/EnemyParado.png"), True, False),
            "attack": pygame.transform.flip(pygame.image.load("./asset/EnemyAttack.png"), True, False),
            "walk": pygame.transform.flip(pygame.image.load("./asset/EnemyAnda.png"), True, False)
        }

        self.current_action = "idle"
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.image = self.get_frame()
        self.rect = self.image.get_rect(topleft=position)

        self.attack_range = 90
        self.last_attack_time = time.time()
        self.attack_cooldown = 1 #Tempo entre os ataques
        self.speed = 2  # Velocidade reduzida para se aproximar devagar
        self.collided = False  # Para saber se colidiu com o player
        self.alive = True #vivo?
        self.death_time = None #Tempo da morte
        self.already_damaged = False  # Para evitar múltiplos danos por ataque
        self.health = GAME_HEALTH['Enemy1']  # vida

    def get_frame(self):
        sheet = self.spritesheets[self.current_action]
        frame_count = self.FRAME_COUNTS[self.current_action]
        frame_width = sheet.get_width() // frame_count
        frame_height = sheet.get_height()
        frame = sheet.subsurface(pygame.Rect(self.frame_index * frame_width, 0, frame_width, frame_height))
        return pygame.transform.scale(frame, (frame_width, frame_height))

    def animate(self):
        now = pygame.time.get_ticks()
        frame_rate = 1000 // self.FRAME_RATES[self.current_action]

        if now - self.last_update > frame_rate:
            self.last_update = now
            self.frame_index += 1

            if self.frame_index >= self.FRAME_COUNTS[self.current_action]:
                self.frame_index = 0
                if self.current_action == "attack":
                    self.current_action = "idle"

            self.image = self.get_frame()

    def check_collision(self, player, backgrounds):
        """Verifica colisão e aplica dano corretamente"""
        if self.rect.colliderect(player.rect):
            self.collided = True

            # Para o background
            for bg in backgrounds:
                bg.speed = 0

                # Ajusta a posição do player para encostar no inimigo
            player.rect.x = self.rect.left - player.rect.width + 40

            # Player ataca inimigo
            if player.attacking and self.alive:
                self.take_damage(10, backgrounds)  # Passando backgrounds para restaurar a velocidade

            # O inimigo ataca o player apenas se o cooldown passou
            if time.time() - self.last_attack_time >= self.attack_cooldown:
                self.current_action = "attack"
                self.last_attack_time = time.time()
                player.take_damage(5)  # Dano inimigo

            # Garante que o Player continue animando
            if not player.attacking:
                player.current_action = "idle"

    def detect_player(self, player):
        """Se o player estiver dentro do alcance, ataca"""
        distance = abs(self.rect.x - player.rect.x)
        if distance < self.attack_range:
            self.current_action = "attack"

    def move_with_background(self, backgrounds):
        """ Move o inimigo devagar conforme o deslocamento do background """
        if self.collided or any(bg.collided for bg in backgrounds):  # Se colidiu, não se move mais
            return

        moving = False

        for bg in backgrounds:
            if bg.offset_x != 0:
                self.rect.x -= bg.speed // 2  # Move devagar, metade da velocidade do fundo
                moving = True

        if moving:
            self.current_action = "walk"
        else:
            self.current_action = "idle"

    def update(self, player, backgrounds):
        """Atualiza o inimigo apenas se ele estiver vivo"""
        if not self.alive:
            return  # Se morreu, para tudo

        self.move_with_background(backgrounds)
        self.detect_player(player)
        self.check_collision(player, backgrounds)
        self.animate()

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def take_damage(self, amount, backgrounds):
        """Reduz a vida do inimigo quando atingido."""
        if not self.alive:
            return  #  Se já morreu, ignora qualquer dano

        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.death_time = time.time()  # Marca o tempo que morreu
            print("Inimigo morreu!")

            for bg in backgrounds:
                bg.speed = ENTITY_SPEED[bg.name] * 0.8  # Background voltando a se mover apos matar inimigo

    def move(self):
        pass