import pygame as pg
import json
from scripts.utilities import load_image, load_images, folder_len, Animation, Button, Word, Ingame_Dialog
from scripts.entities import player, chest, Item
from scripts.tilemap import Tilemap

# Conventional constants
PLAYER_RUN_DURATION = 10
PLAYER_IDLE_DURATION = 18
UI_EMOJI_DURATION = 18
CHEST_FRAME_DURATION = 10
SCREEN_COEFFICIENT = 0.5

class game:
    def __init__(self):
        # Fundamentals for game display
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((1800, 938), pg.FULLSCREEN)
        self.screen_size = self.screen.get_size()
        self.display = pg.surface.Surface((self.screen_size[0] * SCREEN_COEFFICIENT, self.screen_size[1] * SCREEN_COEFFICIENT))
        self.width = self.display.get_width()
        self.height = self.display.get_height()
        self.clock = pg.time.Clock()
        pg.display.set_caption("~ MEOW AHEAD GET TREASURE ~")

        # Ingame background music & sounds
        pg.mixer.music.load("data/sound/background_music.mp3")
        pg.mixer.music.play(loops = -1)
        pg.mixer.music.set_volume(0.3)
        self.click_sound = pg.mixer.Sound("data/sound/click_sound.wav")

        self.running = True
        self.transition_done = True
        self.pause = False
        self.maximum_level = folder_len("level") - 2
        self.level = 1
        self.load_level()
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
            "chest/right": {"close": Animation(load_images("chest/right", "close"), CHEST_FRAME_DURATION), "open": Animation(load_images("chest/right", "open"), CHEST_FRAME_DURATION)},
            "chest_open": pg.mixer.Sound("data/sound/chest_open.wav"),
            
            # Map & others:
            "grass" : load_images("grass"),
            "dirt": load_images("dirt"),
            "fence" : load_images("fence"),
            "water" : load_images("water"),
            "object": load_images("objects"),
            "chest": load_images("chests"),
            "item": load_images("item"),

            # UI emojis:
            "emoji" : {
                "idle": Animation(load_images("UI/emoji/idle"), UI_EMOJI_DURATION),
                "angry": Animation(load_images("UI/emoji/angry"), UI_EMOJI_DURATION),
                "love": Animation(load_images("UI/emoji/love"), UI_EMOJI_DURATION),
                "courage": Animation(load_images("UI/emoji/courage"), UI_EMOJI_DURATION),
                "sleep": Animation(load_images("UI/emoji/sleep"), UI_EMOJI_DURATION),
                "glasses": Animation(load_images("UI/emoji/glasses"), UI_EMOJI_DURATION),
                "normal": Animation(load_images("UI/emoji/normal"), UI_EMOJI_DURATION),
            },
            "Dialog Box": load_image("UI/dialog box big.png"),

            # Fonts:
            "changaone": "data/fonts/changaone.ttf",
            "bungee": "data/fonts/bungee.ttf",
            "basic": "data/fonts/basic.ttf",
            "pixel" : "data/fonts/pixel.ttf",
            "pixellari" : "data/fonts/pixellari.ttf",
            "absender": "data/fonts/absender.ttf",
            "consolamono": "data/fonts/consolamono.ttf",
            "downtown": "data/fonts/downtown.otf",
            "caviardream": "data/fonts/caviardream.ttf",
            "caviardream_bold": "data/fonts/caviardream_bold.ttf"
        }

        # Ingame dialog:
        self.dialog = Ingame_Dialog(self, f"level {self.level}", self.assets["bungee"], 12 , 30, (500, 85), (self.width // 2 + 40, self.height - 60))

        # Menu display resources
        self.menu_item_list = {}

        self.first_word = Word(55, (252, 245, 199), (self.width/2, 60), "MEOW AHEAD", self.assets["pixel"])
        self.second_word = Word(70, (255, 238, 147), (self.width/2, 130), "GET TREASURE", self.assets["pixel"])
        self.third_word = Word(24, (255, 238, 147), (135, self.height - 15), "Beta version ", self.assets["pixel"])
        self.words = [self.first_word, self.second_word, self.third_word]
        
        self.menu_map = Tilemap(self)   
        
        self.menu_map.load_map("level/menu_map.json")
        
        self.menu_chest = chest(self, self.menu_map, self.menu_map.end_point()[0], self.menu_map.end_point()[1])
        
        self.menu_player = player(self, self.menu_map, self.menu_map.start_point())
        
        self.play_button = Button(self.assets["menu_play"], (128, 60), (self.width/2, 240), (252, 245, 199), 2)
        self.continue_button = Button(self.assets["menu_continue"], (128, 60), (self.width/2, 240), (252, 245, 199), 2)
        self.new_game_button = Button(self.assets["menu_newgame"], (128, 60), (self.width/2, 320), (252, 245, 199), 2)
        self.exit_button = Button(self.assets["menu_exit"], (128, 60), (self.width/2, 400), (252, 245, 199), 2)

        for loc in self.menu_map.item_pos():
            item = self.menu_map.item_pos()[loc]
            self.menu_item_list[loc] = Item(self, item["pos"], item["variant"])

        # Pause resources:
        self.pause_button = Button(self.assets["pause_icon"], (36, 36), (24, 24), (252, 245, 199), 2)
        self.pause_resume = Button(self.assets["pause_resume"], (112, 52), (self.width/2 - 60, 270), (252, 245, 199), 2)
        self.pause_restart = Button(self.assets["pause_restart"], (112, 52), (self.width/2 + 60, 270), (252, 245, 199), 2)
        self.pause_home = Button(self.assets["pause_home"], (112, 52), (self.width/2, 330), (252, 245, 199), 2)
        self.pause_word = Word(36, (252, 245, 199), (self.width/2, 210), "PAUSE", self.assets["basic"])
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
        self.replay_button = Button(self.assets["replay"], (50, 50), [self.width/2 - 70, self.height/2], (252, 245, 199), 2, "appear")
        self.home = Button(self.assets["home"], (50, 50), [self.width/2, self.height/2], (252, 245, 199), 2, "appear")
        self.next_level_button = Button(self.assets["next_level"], (50, 50), [self.width/2 + 70, self.height/2], (252, 245, 199), 2, "appear")
        self.ingame_buttons = [self.replay_button, self.home, self.next_level_button]
        
        # Ingame Words
        self.word = Word(26, (255, 238, 147), (self.width/2, -100), f"LEVEL {self.level} COMPLETED", self.assets["bungee"])
        self.lose_word = Word(26, (255, 238, 147), (self.width/2, -100), f"YOU LOSE", self.assets["bungee"])

    def set_state(self, state):
        if state != self.state:
            self.state = state

    def UI_function(self, name:str):
        if name == "home": # Go back to menu display
            self.set_state("menu")
        
        elif name == "new game":
            self.set_state("play")
            self.level = 1
            for button in self.ingame_buttons:
                button.reset()
            self.word.update(f"LEVEL {self.level} COMPLETED")
            self.word.reset()
            self.tilemap.load_map(f"level/level_{self.level}.json")
            self.chest = chest(self, self.tilemap, self.tilemap.end_point()[0], self.tilemap.end_point()[1])
            self.player = player(self, self.tilemap, self.tilemap.start_point())
            self.item_list = {}
            for loc in self.tilemap.item_pos():
                item = self.tilemap.item_pos()[loc]
                self.item_list[loc] = Item(self, item["pos"], item["variant"])
            
        elif name == "level up":
            self.set_state("play")
            self.level = min(self.level + 1, self.maximum_level)
            if self.dialog_detect():
                self.dialog.reset_dialog(f"level {self.level}")

            for button in self.ingame_buttons:
                button.reset()
            self.word.update(f"LEVEL {self.level} COMPLETED")
            self.word.reset()
            self.tilemap.load_map(f"level/level_{self.level}.json")
            self.chest = chest(self, self.tilemap, self.tilemap.end_point()[0], self.tilemap.end_point()[1])
            self.player = player(self, self.tilemap, self.tilemap.start_point())
            self.item_list = {}
            for loc in self.tilemap.item_pos():
                item = self.tilemap.item_pos()[loc]
                self.item_list[loc] = Item(self, item["pos"], item["variant"])

        elif name == "replay":
            self.set_state("play")
            for button in self.ingame_buttons:
                button.reset()
            self.word.update(f"LEVEL {self.level} COMPLETED")
            self.word.reset()
            self.tilemap.load_map(f"level/level_{self.level}.json")
            self.chest = chest(self, self.tilemap, self.tilemap.end_point()[0], self.tilemap.end_point()[1])
            self.player = player(self, self.tilemap, self.tilemap.start_point())
            for loc in self.tilemap.item_pos():
                item = self.tilemap.item_pos()[loc]
                self.item_list[loc] = Item(self, item["pos"], item["variant"])

    def transition_effect(self, name):
        if self.transition == -3.75:
            self.UI_function(name)

        if self.transition < 30:
            self.transition += 1.25
        radius = abs(self.transition) * 15

        if self.transition >= 30:
            self.transition = -30  
            self.transition_done = True

        if self.transition:
            transition_surf = pg.Surface(self.display.get_size())
            pg.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), radius)
            transition_surf.set_colorkey((255, 255, 255))
            self.display.blit(transition_surf, (0, 0))

    def win(self):
        self.word.render(self.display, "fly", [self.width/2, self.height/2 - 50], 5)
        if self.word.done and self.level == self.maximum_level: # Reach the highest level
            for num, button in enumerate(self.ingame_buttons):
                if button != self.next_level_button:
                    button.animation([338 + num*60, 210], 5)
                    button.render(self.display)
                    button.detect_mouse_inside(self.display, self.mouse_pos)
        elif self.word.done:
            for num, button in enumerate(self.ingame_buttons):
                button.animation([338 + num*60, 210], 5)
                button.render(self.display)
                button.detect_mouse_inside(self.display, self.mouse_pos)

    def lose(self):
        if self.player.fall_off():
            self.running = False

    def dialog_detect(self) -> bool:
        return f"level {self.level}" in self.dialog.whole_script and not self.dialog.whole_script[f"level {self.level}"]["state"]

    def menu_render(self):
        self.menu_buttons = [self.play_button, self.new_game_button, self.exit_button] if self.level == 1 else [self.continue_button, self.new_game_button, self.exit_button]
        self.menu_map.render(self.display)
        self.menu_chest.render(self.display)
        self.menu_player.render(self.display)
        
        for word in self.words:
            word.render(self.display)
        
        for button in self.menu_buttons:
            button.render(self.display) 
            button.detect_mouse_inside(self.display, self.mouse_pos)

        for loc in self.menu_item_list:
            item = self.menu_item_list[loc]
            item.render(self.display)

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
                    self.dialog.save_script()
                    pg.mixer.music.stop()
                    self.save_level()
                    self.running = False

                if event.type == pg.KEYDOWN:
                    # Character movements
                    if not self.dialog_detect() or (self.dialog_detect() and self.dialog.whole_script[f"level {self.level}"]["state"]):
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
                        
                        if event.key == pg.K_ESCAPE and self.state == "play" and not self.chest.animation.done:
                            self.pause = not self.pause
                            self.click_sound.play()
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1: 
                        if self.dialog.is_done:
                            self.dialog.next_dialog()
                            self.click_sound.play()

                        if self.state == "menu": # MENU
                            if self.exit_button.detect_mouse_inside(self.display, self.mouse_pos):
                                self.save_level()
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

    def save_level(self):
        with open("game_level", "w") as json_file:
            json.dump(self.level, json_file, indent=4)

    def load_level(self):
        with open("game_level", "r") as json_file:
            self.level = json.load(json_file)

    def game_render(self):
        self.tilemap.render(self.display)
        for loc in self.item_list:
            item = self.item_list[loc]
            item.render(self.display)
        self.player.render(self.display)
        self.chest.render(self.display)
        self.pause_button.render(self.display)

    def game_update(self):
        self.lose()
        self.player.update()
        self.player.move()
        self.chest.update()
        if self.player.collected_item() and str(self.player.tile_pos[0]) + ", " + str(self.player.tile_pos[1]) in self.item_list:
            del self.item_list[str(self.player.tile_pos[0]) + ", " + str(self.player.tile_pos[1])]
        if self.player.found_chest() and not len(self.item_list):
            self.chest.founded()
        if self.chest.animation.done:
            self.win()
        else:
            self.pause_button.detect_mouse_inside(self.display, self.mouse_pos)
        if self.dialog_detect():
            self.dialog.render(self.display)

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