import pygame as pg
from scripts.utilities import load_image, load_images, Animation, Button, Word
from scripts.entities import player, chest
from scripts.tilemap import Tilemap

PLAYER_FRAME_DURATION = 15
CHEST_FRAME_DURATION = 12
SCREEN_COEFFICIENT = 0.5

class game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1536, 800))
        self.screen_size = self.screen.get_size()
        self.display = pg.surface.Surface((self.screen_size[0] * SCREEN_COEFFICIENT, 
                                           self.screen_size[1] * SCREEN_COEFFICIENT))
        self.clock = pg.time.Clock()
        pg.display.set_caption("ESCAPE THE ISLAND")

        self.running = True
        self.maximum_level = 5
        self.level = 1

        self.assets = {
            # Button image:
            "next_level": load_image("button/next_level.png"),
            "pause" : load_image("button/pause.png"),
            "home" : load_image("button/home.png"),
            "levels" : load_image("button/levels.png"),
            "play" : load_image("button/play.png"),
            "replay" : load_image("button/replay.png"),
            "sign" : load_image("button/sign.png"),

            # Player: Syntax: assets["player/" + "direcition"]["state"]
            "player/front": {"idle": Animation(load_images("player/front", "idle"), PLAYER_FRAME_DURATION), "run" : Animation(load_images("player/front", "run"), PLAYER_FRAME_DURATION)},
            "player/back": {"idle": Animation(load_images("player/back", "idle"), PLAYER_FRAME_DURATION), "run" : Animation(load_images("player/back", "run"), PLAYER_FRAME_DURATION)},
            "player/left": {"idle": Animation(load_images("player/left", "idle"), PLAYER_FRAME_DURATION), "run" : Animation(load_images("player/left", "run"), PLAYER_FRAME_DURATION)},
            "player/right": {"idle": Animation(load_images("player/right", "idle"), PLAYER_FRAME_DURATION), "run" : Animation(load_images("player/right", "run"), PLAYER_FRAME_DURATION)},

            # Chest:            
            "chest/front": {"close": Animation(load_images("chest/front", "close"), CHEST_FRAME_DURATION), "open": Animation(load_images("chest/front", "open"), CHEST_FRAME_DURATION)},
            "chest/left": {"close": Animation(load_images("chest/left", "close"), CHEST_FRAME_DURATION), "open": Animation(load_images("chest/left", "open"), CHEST_FRAME_DURATION)},
            
            # Map & others:
            "grass" : load_images("grass"),
            "fence" : load_images("fence"),
            "water" : load_images("water"),
            "object": load_images("objects"),
            "chest": load_images("chests"),

            # Fonts:
            "CO - Regular": "data/fonts/ChangaOne-Regular.ttf",
            "Bungee": "data/fonts/Bungee-Regular.ttf"
        }

        self.tilemap = Tilemap(self)

        self.tilemap.load_map(f"level/level_{self.level}.json")

        self.chest = chest(self, self.tilemap, self.tilemap.end_point()[0], self.tilemap.end_point()[1])

        self.player = player(self, self.tilemap, self.tilemap.start_point())

        # Ingame buttons
        self.replay_button = Button(self.assets["replay"], (42, 42), [324, 210], (242, 208, 169), 1)
        self.home = Button(self.assets["home"], (42, 42), [384, 210], (242, 208, 169), 1)
        self.next_level_button = Button(self.assets["next_level"], (42, 42), [444, 210], (242, 208, 169), 1)
        self.buttons = [self.replay_button, self.home, self.next_level_button]
        
        # Ingame Words
        self.word = Word(26, (255, 255, 255), (384, -100), f"LEVEL {self.level} COMPLETE", self.assets["Bungee"])

    def button_function(self, name:str):
        self.level = self.level = min(self.level+1, self.maximum_level) if name == "level up" else self.level

        for button in self.buttons:
            button.reset()

        self.word.update(f"LEVEL {self.level} COMPLETE")

        self.word.reset()

        self.tilemap.load_map(f"level/level_{self.level}.json")

        self.chest = chest(self, self.tilemap, self.tilemap.end_point()[0], self.tilemap.end_point()[1])

        self.player = player(self, self.tilemap, self.tilemap.start_point())

    def win(self):
        self.word.render(self.display, "fly", [384, 170], 5)
        if self.word.done:
            for num, button in enumerate(self.buttons):
                button.animation([338 + num*60, 210], "appear", 5)
                button.render(self.display)
                button.detect_mouse_inside(self.display, self.mouse_pos)

    def handle_event(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if (event.key == pg.K_a or event.key == pg.K_LEFT) and not (self.player.is_moving or self.player.found_chest()):
                        self.player.is_moving = True
                        self.player.set_state("run")
                        self.player.set_direction("left")
                        
                    elif (event.key == pg.K_d or event.key == pg.K_RIGHT) and not (self.player.is_moving or self.player.found_chest()):
                        self.player.is_moving = True
                        self.player.set_state("run")
                        self.player.set_direction("right")
                        
                    elif (event.key == pg.K_s or event.key == pg.K_DOWN) and not (self.player.is_moving or self.player.found_chest()):
                        self.player.is_moving = True
                        self.player.set_state("run")
                        self.player.set_direction("front")
                        
                    elif (event.key == pg.K_w or event.key == pg.K_UP) and not (self.player.is_moving or self.player.found_chest()):
                        self.player.is_moving = True
                        self.player.set_state("run")
                        self.player.set_direction("back")
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.next_level_button.detect_mouse_inside(self.display, self.mouse_pos):
                            self.button_function("level up")
                        elif self.replay_button.detect_mouse_inside(self.display, self.mouse_pos):
                            self.button_function("replay")
    
    def render(self):
        self.tilemap.render(self.display)
        self.player.render(self.display)
        self.chest.render(self.display)

    def update(self):
        self.player.update()
        self.player.move()
        self.chest.update()
        if self.player.found_chest():
            self.chest.founded()
        if self.chest.animation.done:
            self.win()

        self.screen.blit((pg.transform.scale(self.display, self.screen.get_size())), (0, 0))
        self.clock.tick(60)
        pg.display.flip()

    def run(self):
        while self.running:
            self.keys = pg.key.get_pressed()
            self.mouse_pos = (pg.mouse.get_pos()[0] * SCREEN_COEFFICIENT, pg.mouse.get_pos()[1] * SCREEN_COEFFICIENT)
            
            self.handle_event()
            self.render()
            self.update()
        pg.quit()

if __name__ == "__main__":
    whole_game = game()
    whole_game.run()