import pygame as pg
from scripts.utilities import load_images, Word
from scripts.tilemap import Tilemap

SCREEN_COEFFICIENT = 0.5
water = "water_layer"
save_name = "level_1"
based_level =  water

class Editor:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1800, 938), pg.FULLSCREEN)
        self.display = pg.surface.Surface((self.screen.get_width()*SCREEN_COEFFICIENT, self.screen.get_height()*SCREEN_COEFFICIENT))
        self.clock = pg.time.Clock()
        pg.display.set_caption("Mini game")
        self.running = True

        self.assets = {
            "water" : load_images("water"),
            "grass" : load_images("grass"),
            "dirt": load_images("dirt"),
            "fence" : load_images("fence"),
            "object": load_images("objects"),
            "chest": load_images("chests"),
            "item": load_images("item")
        }
        self.clicking = False
        self.shift = False
        self.delete = False

        self.tilemap = Tilemap(self)
        
        self.tile_list = list(self.assets)
        self.tile_layer_name = list(self.tilemap.tile_map)
        self.tile_group = 0
        self.tile_variant = 0
        self.tile_layer = 0

        self.show_layer = Word(15, "yellow", (60, 10), f"layer: {self.tile_layer_name[self.tile_layer]}")
        self.show_variant = Word(15, "yellow", (32, 30), f"variant: {self.tile_variant}")
    
    def handle_event(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                # KEY CHECK
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LSHIFT:
                        self.shift = True
                    
                    if event.key == pg.K_SPACE:
                        self.tile_layer = (self.tile_layer + 1) % len(self.tile_layer_name)
                        self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                        self.tile_variant = 0
                    
                    elif event.key == pg.K_TAB:
                        self.tile_layer = 6
                        self.tile_group = 6
                        self.tile_variant = 0

                    elif event.key == pg.K_1:
                        self.tile_layer = 0
                        self.tile_group = 0
                        self.tile_variant = 0

                    elif event.key == pg.K_2:
                        self.tile_layer = 1
                        self.tile_group = 1
                        self.tile_variant = 0
                    
                    elif event.key == pg.K_3:
                        self.tile_layer = 2
                        self.tile_group = 2
                        self.tile_variant = 0

                    elif event.key == pg.K_4:
                        self.tile_layer = 3
                        self.tile_group = 3
                        self.tile_variant = 0

                    elif event.key == pg.K_5:
                        self.tile_layer = 4
                        self.tile_group = 4
                        self.tile_variant = 0

                    elif event.key == pg.K_6:
                        self.tile_layer = 5
                        self.tile_group = 5
                        self.tile_variant = 0

                    if self.shift and event.key == pg.K_o:
                        self.tilemap.save_map(f"level/{save_name}.json")
                    elif self.shift and event.key == pg.K_l:
                        self.tilemap.load_map(f"level/{based_level}.json")
                        self.tile_layer = 0
                        self.tile_group = 0
                        self.tile_variant = 0
                
                if event.type == pg.KEYUP:
                    if event.key == pg.K_LSHIFT:
                        self.shift = False
                
                # MOUSEBUTTON CHECK
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                    if event.button == 3: 
                        self.delete = True
                    
                    else: # change tile variant in a group
                        if event.button == 4: 
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.delete = False

    def run(self):
        while self.running:
            self.handle_event()
            self.display.fill("black")
            self.tilemap.render(self.display, "edit")
            mouse_pos = (pg.mouse.get_pos()[0] * SCREEN_COEFFICIENT, pg.mouse.get_pos()[1] * SCREEN_COEFFICIENT)
            
            self.keys = pg.key.get_pressed()

            tile_pos = (mouse_pos[0]//self.tilemap.tile_size, mouse_pos[1]//self.tilemap.tile_size)

            if self.clicking:
                self.tilemap.tile_map[self.tile_layer_name[self.tile_layer]][str(tile_pos[0]) + ", " + str(tile_pos[1])] = {
                    "group": self.tile_list[self.tile_group],
                    "variant": self.tile_variant,
                    "pos": tile_pos
                }

            if self.delete:
                tile_loc = str(tile_pos[0]) + ", " + str(tile_pos[1])
                if tile_loc in self.tilemap.tile_map[self.tile_layer_name[self.tile_layer]]:
                    del self.tilemap.tile_map[self.tile_layer_name[self.tile_layer]][tile_loc]

            current_tile = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile.set_alpha(150)
            
            self.display.blit(current_tile, (tile_pos[0] * self.tilemap.tile_size, tile_pos[1] * self.tilemap.tile_size))
            
            self.show_layer.update(f"layer: {self.tile_layer_name[self.tile_layer]}")
            self.show_layer.render(self.display)

            self.show_variant.update(f"variant: {self.tile_variant}")
            self.show_variant.render(self.display)

            self.screen.blit(pg.transform.scale(self.display, self.screen.get_size()), (0, 0))
            self.clock.tick(60)
            pg.display.flip() 
        pg.quit()

if __name__ == "__main__":
    Editor_mode = Editor()
    Editor_mode.run()