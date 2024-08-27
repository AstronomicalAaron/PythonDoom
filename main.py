import sys
from settings import *
from map import *


class Game:
    def __init__(self):
        pg.init()  # Create the pygame modules
        self.screen = pg.display.set_mode(RES)  # Create a screen using the resolution set in settings.py
        self.clock = pg.time.Clock()  # set the frame rate
        self.new_game()

    def new_game(self):
        self.map = Map(self)

    def update(self):  # Updates the screen and display current FPS in a window caption
        pg.display.flip()  # update screen
        self.clock.tick(FPS)  # updates the clock
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')  # display FPS in the window

    def draw(self):
        self.screen.fill('black')  # for each clock cycle fill the screen black
        self.map.draw()

    def check_events(self):
        for event in pg.event.get():  # loop through all of the events
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit(1)

    def run(self):  # main loop of the game
        while True:  # indefinitely run the game
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
