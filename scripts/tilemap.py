import pygame as pg
import json

class Tilemap:
    def __init__(self, game, tile_size = 16):
        self.game = game
        self.tile_size = tile_size
        self.tile_map = {   
            "water_layer": {}, 
            "ground_layer": {},
            "dirt": {},
            "fence_layer": {},
            "object_layer": {},
            "chest" : {},
            "item": {}
            }

    def render(self, surface):
        for layer in self.tile_map:
            # if layer != "item":
            for loc in self.tile_map[layer]:
                tile = self.tile_map[layer][loc]
                surface.blit(pg.transform.scale(self.game.assets[tile["group"]][tile["variant"]], (self.tile_size, self.tile_size)), 
                            (tile["pos"][0] * self.tile_size, tile["pos"][1] * self.tile_size))

    def item_pos(self):
        return self.tile_map["item"]

    def save_map(self, file_name):
        with open(file_name, "w") as json_file:
            json.dump(self.tile_map, json_file, indent=4)
    
    def load_map(self, file_name):
        with open(file_name, "r") as json_file:
            self.tile_map = json.load(json_file)
    
    def start_point(self):
        for loc in self.tile_map["ground_layer"]:
            tile = self.tile_map["ground_layer"][loc]
            if tile["variant"] == 1 or tile["variant"] == 13:
                return [(tile["pos"][0] - 1)*self.tile_size, (tile["pos"][1] - 1)*self.tile_size]
            
    def end_point(self):
        for loc in self.tile_map["chest"]:
            tile = self.tile_map["chest"][loc]
            if tile["variant"] == 0:
                return ("front", [(tile["pos"][0] - 1)*self.tile_size, (tile["pos"][1] - 1)*self.tile_size])
            elif tile["variant"] == 1:
                return ("left", [(tile["pos"][0] - 1)*self.tile_size, (tile["pos"][1] - 1)*self.tile_size])