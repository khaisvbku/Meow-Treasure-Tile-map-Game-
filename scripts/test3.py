from utilities import *
import pygame as pg

class game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([1536, 800])
        self.clock = pg.time.Clock()
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

        self.dialog_text = Ingame_Dialog(self, "level 1", 15, 30, (1000, 120))

    def handle_event(self):
        self.screen.fill("white")
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and self.dialog_text.is_done:
                    self.dialog_text.next_dialog()

    def system_update(self):
        self.clock.tick(60)
        pg.display.flip()

    def run(self):
        while self.running:
            self.handle_event()
            self.dialog_text.render(self.screen, (800, 700))
            self.system_update()
        pg.quit()

if __name__ == "__main__":
    whole_game = game()
    whole_game.run()