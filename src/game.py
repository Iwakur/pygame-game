import pygame
from map import MapManager
from player import Player

class Game:

    def __init__(self):
        # Démarrage
        self.running = True
        self.screen = pygame.display.set_mode((600,400))
        pygame.display.set_caption("Intro-PyGame")

        # Générer un joueur
        self.player = Player(0, 0)
        self.map_manager = MapManager(self.screen, self.player)
        self.joystick = None

    def update(self):

        self.map_manager.update()

    def input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LSHIFT]:
            self.player.run()
        else:
            self.player.walk()

        # handle joypad and joystick events

        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            self.player.move_up()
        elif pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.player.move_down()
        elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.player.move_right()
        elif pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            self.player.move_left()

        if pressed[pygame.K_SPACE]:
            map_list = []
            for i,map in enumerate(self.map_manager.maps, 1):
                print(i, map)
                map_list.append(map)

            self.map_manager.set_current_map(self.map_manager.maps[map_list[int(input("Choisissez un map : "))-1]].name)

        # player movement with analog stick
        if self.joystick:
            if self.joystick.get_axis(0) > 0.75:
                self.player.move_right()
            elif self.joystick.get_axis(0) < -0.75:
                self.player.move_left()
            elif self.joystick.get_axis(1) > 0.75:
                self.player.move_down()
            elif self.joystick.get_axis(1) < -0.75:
                self.player.move_up()


    def run(self):
        print("Starting")
        clock = pygame.time.Clock()
        self.running = True

        # pygame.mixer.music.load('../assets/music/8 Bit Game.mp3')
        # pygame.mixer.music.play(-1)

        # Boucle de jeu
        while self.running:

            self.input()
            self.update()
            self.map_manager.draw()
            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == pygame.JOYDEVICEADDED:
                    self.joystick = pygame.joystick.Joystick(0)
                    self.joystick.init()
                    print("Joystick connected")

                if self.joystick:
                    if event.type == pygame.JOYBUTTONDOWN:
                        print("Joystick button pressed.")
                    if event.type == pygame.JOYBUTTONUP:
                        print("Joystick button released.")

                if event.type == pygame.QUIT:
                    self.running = False

            clock.tick(60)

        pygame.quit()