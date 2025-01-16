import pygame as pg
from scripts.utilities import folder_len, load_image, load_images, Animation, Button, Word
from scripts.entities import player, chest, Item
from scripts.tilemap import Tilemap

PLAYER_RUN_DURATION = 10
PLAYER_IDLE_DURATION = 18
CHEST_FRAME_DURATION = 10
SCREEN_COEFFICIENT = 0.5

class game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((1536, 800))
        self.screen_size = self.screen.get_size()
        self.display = pg.surface.Surface((self.screen_size[0] * SCREEN_COEFFICIENT, self.screen_size[1] * SCREEN_COEFFICIENT))
        self.clock = pg.time.Clock()
        pg.display.set_caption("ESCAPE THE ISLAND")

        # Ingame background music % sounds
        pg.mixer.music.load("data/sound/background_music.mp3")
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(loops = -1)
        self.click_sound = pg.mixer.Sound("data/sound/click_sound.wav")

        self.running = True
        self.transition_done = True
        self.pause = False
        self.maximum_level = folder_len("level") - 2
        self.level = 1
        self.transition = -30
        self.state = "menu"
        self.next_display = ""

        self.assets = {
            # Ingame buttons:
            "next_level": load_image("button/next_level.png"),
            "pause" : load_image("button/pause.png"),
            "home" : load_image("button/home.png"),
            "levels" : load_image("button/levels.png"),
            "play" : load_image("button/play.png"),
            "replay" : load_image("button/replay.png"),

            # Menu buttons
            "menu_play": load_image("button/menu_play.png"),
            "menu_newgame": load_image("button/menu_newgame.png"),
            "menu_continue": load_image("button/menu_continue.png"),
            "menu_exit": load_image("button/menu_exit.png"), 

            # Pause buttons
            "pause_icon": load_image("button/pause.png"),
            "pause_resume": load_image("button/pause_resume.png"),
            "pause_restart": load_image("button/pause_restart.png"),
            "pause_home": load_image("button/pause_home.png"),
            "pause_table": load_image("button/pause_table.png"),

            # Player: Syntax: assets["player/" + "direcition"]["state"]
            "player/front": {"idle": Animation(load_images("player/front", "idle"), PLAYER_IDLE_DURATION), "run" : Animation(load_images("player/front", "run"), PLAYER_RUN_DURATION )},
            "player/back": {"idle": Animation(load_images("player/back", "idle"), PLAYER_IDLE_DURATION), "run" : Animation(load_images("player/back", "run"), PLAYER_RUN_DURATION )},
            "player/left": {"idle": Animation(load_images("player/left", "idle"), PLAYER_IDLE_DURATION), "run" : Animation(load_images("player/left", "run"), PLAYER_RUN_DURATION )},
            "player/right": {"idle": Animation(load_images("player/right", "idle"), PLAYER_IDLE_DURATION), "run" : Animation(load_images("player/right", "run"), PLAYER_RUN_DURATION )},

            # Chest: Syntax: assets["chest/" + "direcition"]["state"]         
            "chest/front": {"close": Animation(load_images("chest/front", "close"), CHEST_FRAME_DURATION), "open": Animation(load_images("chest/front", "open"), CHEST_FRAME_DURATION)},
            "chest/left": {"close": Animation(load_images("chest/left", "close"), CHEST_FRAME_DURATION), "open": Animation(load_images("chest/left", "open"), CHEST_FRAME_DURATION)},
            "chest_open": pg.mixer.Sound("data/sound/chest_open.wav"),
            
            # Map & others:
            "grass" : load_images("grass"),
            "dirt": load_images("dirt"),
            "fence" : load_images("fence"),
            "water" : load_images("water"),
            "object": load_images("objects"),
            "chest": load_images("chests"),
            "item": load_images("item"),

            # Fonts:
            "CO - Regular": "data/fonts/ChangaOne-Regular.ttf",
            "Bungee": "data/fonts/Bungee-Regular.ttf"
        }

        # Menu display resources
        self.first_word = Word(32, (252, 245, 199), (384, 40), "MEOW AHEAD", self.assets["Bungee"])
        self.second_word = Word(55, (255, 238, 147), (384, 85), "GET TREASURE", self.assets["CO - Regular"])
        self.words = [self.first_word, self.second_word]
        self.tile_map = Tilemap(self)
        self.tile_map.load_map("level/menu_map.json")
        self.menu_chest = chest(self, self.tile_map, self.tile_map.end_point()[0], self.tile_map.end_point()[1])
        self.menu_player = player(self, self.tile_map, self.tile_map.start_point())
        self.play_button = Button(self.assets["menu_play"], (112, 52), (384, 165), (252, 245, 199), 2)
        self.continue_button = Button(self.assets["menu_continue"], (112, 52), (384, 165), (252, 245, 199), 2)
        self.new_game_button = Button(self.assets["menu_newgame"], (112, 52), (384, 225), (252, 245, 199), 2)
        self.exit_button = Button(self.assets["menu_exit"], (112, 52), (384, 285), (252, 245, 199), 2)

        # Pause resources:
        self.pause_button = Button(self.assets["pause_icon"], (32, 32), (20, 20), (252, 245, 199), 2)
        self.pause_word = Word(36, (252, 245, 199), (384, 130), "PAUSE", self.assets["Bungee"])
        self.pause_resume = Button(self.assets["pause_resume"], (86, 42), (334, 180), (252, 245, 199), 2)
        self.pause_restart = Button(self.assets["pause_restart"], (86, 42), (434, 180), (252, 245, 199), 2)
        self.pause_home = Button(self.assets["pause_home"], (86, 42), (384, 230), (252, 245, 199), 2)
        self.pause_buttons = [self.pause_resume, self.pause_restart, self.pause_home]

        # Ingame resources
        self.tilemap = Tilemap(self)
        self.tilemap.load_map(f"level/level_{self.level}.json")
        self.chest = chest(self, self.tilemap, self.tilemap.end_point()[0], self.tilemap.end_point()[1])
        self.player = player(self, self.tilemap, self.tilemap.start_point())
        self.item_list = {}
        for loc in self.tilemap.item_pos():
            item = self.tilemap.item_pos()[loc]
            self.item_list[loc] = Item(self, item["pos"], item["variant"])

        # Ingame buttons
        self.replay_button = Button(self.assets["replay"], (42, 42), [324, 210], (252, 245, 199), 2, "appear")
        self.home = Button(self.assets["home"], (42, 42), [384, 210], (252, 245, 199), 2, "appear")
        self.next_level_button = Button(self.assets["next_level"], (42, 42), [444, 210], (252, 245, 199), 2, "appear")
        self.ingame_buttons = [self.replay_button, self.home, self.next_level_button]
        
        # Ingame Words
        self.word = Word(26, (252, 245, 199), (384, -100), f"LEVEL {self.level} COMPLETE", self.assets["Bungee"])

    def set_state(self, state):
        if state != self.state:
            self.state = state

    def button_function(self, name:str):
        if name == "home": # Go back to menu display
            self.set_state("menu")
        
        elif name == "new game":
            self.set_state("play")
            self.level = 1
            for button in self.ingame_buttons:
                button.reset()
            self.word.update(f"LEVEL {self.level} COMPLETE")
            self.word.reset()
            self.tilemap.load_map(f"level/level_{self.level}.json")
            self.chest = chest(self, self.tilemap, self.tilemap.end_point()[0], self.tilemap.end_point()[1])
            self.player = player(self, self.tilemap, self.tilemap.start_point())
            for loc in self.tilemap.item_pos():
                item = self.tilemap.item_pos()[loc]
                self.item_list[loc] = Item(self, item["pos"], item["variant"])
            
        elif name == "level up":
            self.set_state("play")
            self.level = min(self.level + 1, self.maximum_level)

            for button in self.ingame_buttons:
                button.reset()
            self.word.update(f"LEVEL {self.level} COMPLETE")
            self.word.reset()
            self.tilemap.load_map(f"level/level_{self.level}.json")
            self.chest = chest(self, self.tilemap, self.tilemap.end_point()[0], self.tilemap.end_point()[1])
            self.player = player(self, self.tilemap, self.tilemap.start_point())
            for loc in self.tilemap.item_pos():
                item = self.tilemap.item_pos()[loc]
                self.item_list[loc] = Item(self, item["pos"], item["variant"])

        elif name == "replay":
            self.set_state("play")
            for button in self.ingame_buttons:
                button.reset()
            self.word.update(f"LEVEL {self.level} COMPLETE")
            self.word.reset()
            self.tilemap.load_map(f"level/level_{self.level}.json")
            self.chest = chest(self, self.tilemap, self.tilemap.end_point()[0], self.tilemap.end_point()[1])
            self.player = player(self, self.tilemap, self.tilemap.start_point())
            for loc in self.tilemap.item_pos():
                item = self.tilemap.item_pos()[loc]
                self.item_list[loc] = Item(self, item["pos"], item["variant"])

    def transition_effect(self, name):
        if self.transition == -3:
            self.button_function(name)

        if self.transition < 30:
            self.transition += 1.5
        radius = abs(self.transition) * 12

        if self.transition >= 30:
            self.transition = -30  
            self.transition_done = True

        if self.transition:
            transition_surf = pg.Surface(self.display.get_size())
            pg.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), radius)
            transition_surf.set_colorkey((255, 255, 255))
            self.display.blit(transition_surf, (0, 0))

    def win(self):
        self.word.render(self.display, "fly", [384, 155], 5)
        if self.word.done:
            for num, button in enumerate(self.ingame_buttons):
                button.animation([338 + num*60, 210], 5)
                button.render(self.display)
                button.detect_mouse_inside(self.display, self.mouse_pos)

    def menu_render(self):
        self.menu_buttons = [self.play_button, self.new_game_button, self.exit_button] if self.level == 1 else [self.continue_button, self.new_game_button, self.exit_button]
        self.tile_map.render(self.display)
        self.menu_chest.render(self.display)
        self.menu_player.render(self.display)
        
        for word in self.words:
            word.render(self.display)
        
        for button in self.menu_buttons:
            button.render(self.display) 
            button.detect_mouse_inside(self.display, self.mouse_pos)

    def menu_update(self):
        self.menu_player.update()
        self.menu_chest.update()

    def pause_render(self):
        self.pause_word.render(self.display)
        for button in self.pause_buttons:
            button.render(self.display)
            button.detect_mouse_inside(self.display, self.mouse_pos)

    def handle_event(self):
        self.mouse_pos = (pg.mouse.get_pos()[0] * SCREEN_COEFFICIENT, pg.mouse.get_pos()[1] * SCREEN_COEFFICIENT)
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.mixer.music.stop()
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if (event.key == pg.K_a or event.key == pg.K_LEFT) and not (self.player.is_moving or self.pause or (not len(self.item_list) and self.player.found_chest())):
                        self.player.is_moving = True
                        self.player.set_state("run")
                        self.player.set_direction("left")
                        
                    elif (event.key == pg.K_d or event.key == pg.K_RIGHT) and not (self.player.is_moving or self.pause or (not len(self.item_list) and self.player.found_chest())):
                        self.player.is_moving = True
                        self.player.set_state("run")
                        self.player.set_direction("right")
                        
                    elif (event.key == pg.K_s or event.key == pg.K_DOWN) and not (self.player.is_moving or self.pause or (not len(self.item_list) and self.player.found_chest())):
                        self.player.is_moving = True
                        self.player.set_state("run")
                        self.player.set_direction("front")
                        
                    elif (event.key == pg.K_w or event.key == pg.K_UP) and not (self.player.is_moving or self.pause or (not len(self.item_list) and self.player.found_chest())):
                        self.player.is_moving = True
                        self.player.set_state("run")
                        self.player.set_direction("back")
                    elif event.key == pg.K_ESCAPE and self.state == "play" and not self.chest.animation.done:
                        self.pause = not self.pause
                        self.click_sound.play()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1: # Left button clicked
                        if self.state == "menu": # MENU
                            if self.exit_button.detect_mouse_inside(self.display, self.mouse_pos):
                                self.running = False
                            elif self.continue_button.detect_mouse_inside(self.display, self.mouse_pos) or self.play_button.detect_mouse_inside(self.display, self.mouse_pos):
                                self.transition_done = False
                                self.next_display = "replay"
                                self.click_sound.play()
                            elif self.new_game_button.detect_mouse_inside(self.display, self.mouse_pos):
                                self.transition_done = False
                                self.next_display = "new game"
                                self.click_sound.play()
                        
                        elif self.state == "play": # PLAYING SCREEN
                            if self.next_level_button.detect_mouse_inside(self.display, self.mouse_pos):
                                self.transition_done = False
                                self.next_display = "level up"
                                self.click_sound.play()
                            elif self.replay_button.detect_mouse_inside(self.display, self.mouse_pos):
                                self.transition_done = False
                                self.next_display = "replay"
                                self.click_sound.play()
                            elif self.home.detect_mouse_inside(self.display, self.mouse_pos):
                                self.transition_done = False
                                self.next_display = "home"
                                self.click_sound.play()
                            elif self.pause_button.detect_mouse_inside(self.display, self.mouse_pos) and not self.pause and not self.chest.animation.done:
                                self.pause = True
                                self.click_sound.play()
                            
                            if self.pause: # PAUSE
                                if self.pause_home.detect_mouse_inside(self.display, self.mouse_pos):
                                    self.transition_done = False
                                    self.next_display = "home"
                                    self.pause = False
                                    self.click_sound.play()
                                elif self.pause_restart.detect_mouse_inside(self.display, self.mouse_pos):
                                    self.transition_done = False
                                    self.next_display = "replay"
                                    self.pause = False
                                    self.click_sound.play()
                                elif self.pause_resume.detect_mouse_inside(self.display, self.mouse_pos):
                                    self.pause = False
                                    self.click_sound.play()

    def game_render(self):
        self.tilemap.render(self.display)
        for loc in self.item_list:
            item = self.item_list[loc]
            item.render(self.display)
        self.player.render(self.display)
        self.chest.render(self.display)
        self.pause_button.render(self.display)

    def game_update(self):
        self.player.update()
        self.player.move()
        self.chest.update()
        if self.player.found_chest() and not len(self.item_list):
            self.chest.founded()
        if self.chest.animation.done:
            self.win()
        else:
            self.pause_button.detect_mouse_inside(self.display, self.mouse_pos)

    def system_update(self):
        self.screen.blit((pg.transform.scale(self.display, self.screen.get_size())), (0, 0))
        self.clock.tick(60)
        pg.display.flip()

    def run(self):
        while self.running:
            self.handle_event()

            if self.state == "menu":
                self.menu_render()
                self.menu_update()

            elif self.state == "play":
                self.game_render()
                if self.pause:
                    self.pause_render()
                else:
                    self.game_update()
            
            if not self.transition_done:
                self.transition_effect(self.next_display)
            self.system_update()
        pg.quit()

if __name__ == "__main__":
    whole_game = game()
    whole_game.run()