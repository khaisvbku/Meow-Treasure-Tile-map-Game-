import pygame as pg
from scripts.utilities import load_image, load_images, Animation, Button, Word
from scripts.entities import player, chest
from scripts.tilemap import Tilemap

PLAYER_FRAME_DURATION = 15
CHEST_FRAME_DURATION = 12
SCREEN_COEFFICIENT = 0.5

class menu:
    def __init__(self, game):
        self.game = game

        self.first_word = Word(32, (252, 245, 199), (384, 35), "MEOW MEOW", self.game.assets["Bungee"])
        
        self.second_word = Word(55, (255, 238, 147), (384, 85), "TREASURE GAME", self.game.assets["Bungee"])

        self.words = [self.first_word, self.second_word]

        self.tile_map = Tilemap(self.game)

        self.tile_map.load_map("level/menu_map.json")

        self.chest = chest(self.game, self.tile_map, self.tile_map.end_point()[0], self.tile_map.end_point()[1])

        self.player = player(self.game, self.tile_map, self.tile_map.start_point())

        self.play_button = Button(self.game.assets["menu_play"], (98, 42), (384, 180), (252, 245, 199), 2)

        self.continue_button = Button(self.game.assets["menu_continue"], (98, 42), (384, 180), (252, 245, 199), 2)
    
        self.new_game_button = Button(self.game.assets["menu_newgame"], (98, 42), (384, 230), (252, 245, 199), 2)

        self.exit_button = Button(self.game.assets["menu_exit"], (98, 42), (384, 280), (252, 245, 199), 2)

    def render(self, surface, level, mouse_pos):
        self.buttons = [self.play_button, self.new_game_button, self.exit_button] if level == 1 else [self.continue_button, self.new_game_button, self.exit_button]
        self.tile_map.render(surface)
        self.chest.render(surface)
        self.player.render(surface)
        for word in self.words:
            word.render(surface)
        for button in self.buttons:
            button.render(surface) 
            button.detect_mouse_inside(surface, mouse_pos)
    
    def update(self):
        self.player.update()
        self.chest.update()
        
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
        self.maximum_level = 6
        self.level = 1
        self.state = "play"
        self.transition = -50
        self.transition_done = True

        self.assets = {
            # Button image:
            "next_level": load_image("button/next_level.png"),
            "pause" : load_image("button/pause.png"),
            "home" : load_image("button/home.png"),
            "levels" : load_image("button/levels.png"),
            "play" : load_image("button/play.png"),
            "replay" : load_image("button/replay.png"),

            "menu_play": load_image("button/menu_play.png"),
            "menu_newgame": load_image("button/menu_newgame.png"),
            "menu_continue": load_image("button/menu_continue.png"),
            "menu_exit": load_image("button/menu_exit.png"), 

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

        self.menu = menu(self)

        self.tilemap = Tilemap(self)

        self.tilemap.load_map(f"level/level_{self.level}.json")

        self.chest = chest(self, self.tilemap, self.tilemap.end_point()[0], self.tilemap.end_point()[1])

        self.player = player(self, self.tilemap, self.tilemap.start_point())

        # Ingame buttons
        self.replay_button = Button(self.assets["replay"], (42, 42), [324, 210], (252, 245, 199), 2)
        self.home = Button(self.assets["home"], (42, 42), [384, 210], (252, 245, 199), 2)
        self.next_level_button = Button(self.assets["next_level"], (42, 42), [444, 210], (252, 245, 199), 2)
        self.buttons = [self.replay_button, self.home, self.next_level_button]
        
        # Ingame Words
        self.word = Word(26, (252, 245, 199), (384, -100), f"LEVEL {self.level} COMPLETE", self.assets["Bungee"])

    def set_state(self, state):
        if state != self.state:
            self.state = state

    def button_function(self, name:str):
        if name == "home": # Go back to menu display
            self.set_state("menu")
        else: # start or restart the level
            if name == "new game":
                self.level = 1
            elif name == "level up":
                self.level = min(self.level + 1, self.maximum_level)

            for button in self.buttons:
                button.reset()

            self.word.update(f"LEVEL {self.level} COMPLETE")

            self.word.reset()

            self.tilemap.load_map(f"level/level_{self.level}.json")

            self.chest = chest(self, self.tilemap, self.tilemap.end_point()[0], self.tilemap.end_point()[1])

            self.player = player(self, self.tilemap, self.tilemap.start_point())

    def transition_effect(self):
        if self.transition < 0:
            self.transition += 1
        radius = (50 - abs(self.transition)) * 10

        if self.transition == 0:
            self.transition = -50  
            self.transition_done = True  

        if self.transition:
            transition_surf = pg.Surface(self.display.get_size())
            pg.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), radius)
            transition_surf.set_colorkey((255, 255, 255))
            self.display.blit(transition_surf, (0, 0))

    def win(self):
        self.word.render(self.display, "fly", [384, 155], 5)
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
                        if self.state == "menu":
                            if self.menu.exit_button.detect_mouse_inside(self.display, self.mouse_pos):
                                self.running = False
                            elif self.menu.continue_button.detect_mouse_inside(self.display, self.mouse_pos) or self.menu.play_button.detect_mouse_inside(self.display, self.mouse_pos):
                                self.transition_done = False
                                self.button_function("replay")
                            elif self.menu.new_game_button.detect_mouse_inside(self.display, self.mouse_pos):
                                self.transition_done = False
                                self.button_function("new game")
                        elif self.state == "play":
                            if self.next_level_button.detect_mouse_inside(self.display, self.mouse_pos):
                                self.transition_done = False
                                self.button_function("level up")
                            elif self.replay_button.detect_mouse_inside(self.display, self.mouse_pos):
                                self.transition_done = False
                                self.button_function("replay")
                            elif self.home.detect_mouse_inside(self.display, self.mouse_pos):
                                self.transition_done = False
                                self.button_function("home")
    
    def game_render(self):
        self.tilemap.render(self.display)
        self.player.render(self.display)
        self.chest.render(self.display)

    def game_update(self):
        self.player.update()
        self.player.move()
        self.chest.update()
        if self.player.found_chest():
            self.chest.founded()
        if self.chest.animation.done:
            self.win()

    def run(self):
        while self.running:
            self.keys = pg.key.get_pressed()
            self.mouse_pos = (pg.mouse.get_pos()[0] * SCREEN_COEFFICIENT, pg.mouse.get_pos()[1] * SCREEN_COEFFICIENT)
            self.handle_event()

            if self.state == "menu":
                self.menu.render(self.display, self.level, self.mouse_pos)
                self.menu.update()

            elif self.state == "play":
                self.game_render()
                self.game_update()
            
            if not self.transition_done:
                self.transition_effect()

            self.screen.blit((pg.transform.scale(self.display, self.screen.get_size())), (0, 0))
            self.clock.tick(60)
            pg.display.flip()
        pg.quit()

if __name__ == "__main__":
    whole_game = game()
    whole_game.run()