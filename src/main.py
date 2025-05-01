# main.py

from game import Game
from ui import main_menu

if __name__ == "__main__":
    if main_menu():
        game = Game()
        game.run()
