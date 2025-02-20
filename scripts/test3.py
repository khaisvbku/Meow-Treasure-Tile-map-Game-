from utilities import *
import pygame as pg

class game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([1536, 800])
        self.clock = pg.time.Clock()
        self.level = 1
        self.running = True
        
        self.assets = {
            # UI emojis:
            "emoji" : {
                "idle": Animation(load_images("UI/emoji/idle"), 15),
                "angry": Animation(load_images("UI/emoji/angry"), 20),
                "love": Animation(load_images("UI/emoji/love"), 20),
                "courage": Animation(load_images("UI/emoji/courage"), 20),
                "sleep": Animation(load_images("UI/emoji/sleep"), 20),
                "glasses": Animation(load_images("UI/emoji/glasses"), 20),
                "normal": Animation(load_images("UI/emoji/normal"), 15),
            },
            "Dialog Box": load_image("UI/dialog box big.png"),

            # Fonts:
            "CO - Regular": "data/fonts/ChangaOne-Regular.ttf",
            "Bungee": "data/fonts/Bungee-Regular.ttf",
            "basic_font": "data/fonts/basic_font.ttf"
        }
        self.dialog = Ingame_Dialog(self, "level 1", 15, 30, (1000, 120))

    def handle_event(self):
        self.screen.fill("black")
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.dialog.save_script()
                self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and self.dialog.is_done:
                    self.dialog.next_dialog()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_TAB:
                    self.level += 1
                    if self.dialog_detect():
                        self.dialog_create()
                if event.key == pg.K_SPACE and self.dialog.is_done:
                    self.dialog.next_dialog()
                    

    def dialog_detect(self) -> bool:
        return f"level {self.level}" in self.dialog.whole_script and not self.dialog.whole_script[f"level {self.level}"]["state"]

    def dialog_create(self):
        self.dialog = Ingame_Dialog(self, f"level {self.level}", 15, 30, (1000, 120))

    def dialog_update(self):
        if self.dialog_detect():
            self.dialog.render(self.screen)

    def system_update(self):
        self.clock.tick(60)
        pg.display.flip()

    def run(self):
        while self.running:
            self.handle_event()
            self.dialog_update()
            self.system_update()
        pg.quit()

if __name__ == "__main__":
    whole_game = game()
    whole_game.run()