import pygame as pg

class physical_entities:
    def __init__(self, type, game, tile_map, pos):
        self.type = type
        self.game = game
        self.tile_map = tile_map
        self.tile_size = self.tile_map.tile_size 
        self.pos = pos
        self.tile_pos = [(self.pos[0]) // self.tile_size + 1, self.pos[1] // self.tile_size + 1]
        self.animation = self.game.assets[f"{self.type}/" + self.direction][self.state].copy()
        
    def set_state(self, state):
        if state != self.state:
            self.state = state
            self.animation = self.game.assets[f"{self.type}/" + self.direction][self.state].copy()

    def set_direction(self, direction):
        if direction != self.direction:
            self.direction = direction
            self.animation = self.game.assets[f"{self.type}/" + self.direction][self.state].copy()
    
    def render(self, surface):
        surface.blit(self.animation.image(), (self.pos))

    def update(self):
        self.animation.update()
        self.tile_pos = [(self.pos[0]) // self.tile_size + 1, self.pos[1] // self.tile_size + 1]
        
class player(physical_entities):
    def __init__(self, game, tile_map, pos):        

        self.state = "idle"

        self.direction = "front"
        
        self.is_moving = False
        
        self.collision = {"front": False, "back": False, "left": False, "right": False}
        
        self.movement = {
            "front": [0, 1], "back": [0, -1], 
            "left": [-1, 0], "right": [1, 0]
            }
        
        self.speed = 1

        super().__init__("player", game, tile_map, pos)

    def update(self):
        super().update()
        # Check for collision    
        self.tile_pos = [(self.pos[0]) // self.tile_size + 1, self.pos[1] // self.tile_size + 1]
        self.next_pos = {
            "front": str(self.tile_pos[0]) + ", " + str(self.tile_pos[1] + 1),
            "back": str(self.tile_pos[0]) + ", " + str(self.tile_pos[1] - 1),
            "left": str(self.tile_pos[0] - 1) + ", " + str(self.tile_pos[1]),
            "right": str(self.tile_pos[0] + 1) + ", " + str(self.tile_pos[1])
        }

        for direction, pos in self.next_pos.items():
            if direction == "left" or direction == "right":
                if (pos in self.tile_map.tile_map["fence_layer"] or pos in self.tile_map.tile_map["object_layer"] or pos in self.tile_map.tile_map["chest"]) and self.pos[0] % self.tile_size == 0:
                    self.collision[direction] = True
                else:
                    self.collision[direction] = False
            elif direction == "front" or direction == "back":
                if (pos in self.tile_map.tile_map["fence_layer"] or pos in self.tile_map.tile_map["object_layer"] or pos in self.tile_map.tile_map["chest"]) and self.pos[1] % self.tile_size == 0:
                    self.collision[direction] = True
                else:
                    self.collision[direction] = False

    def found_chest(self) -> bool:
        if self.next_pos[self.direction] in self.tile_map.tile_map["chest"] and self.is_moving == False:
            return True
        else: return False

    def move(self):
        # Movements
        if self.is_moving and not self.collision[self.direction]:
            self.pos[0] += self.movement[self.direction][0]*self.speed
            self.pos[1] += self.movement[self.direction][1]*self.speed
        else: 
            self.is_moving = False
            self.set_state("idle")

class chest(physical_entities):
    def __init__(self, game, tile_map, direction, pos):
        self.state = "close"
        self.direction = direction
        
        super().__init__("chest", game, tile_map, pos)
        self.open_sound = self.game.assets["chest_open"]
    
    def update(self):
        if not self.animation.done:
            super().update()

    def founded(self):
        if self.state != "open":
            self.set_state("open")
            self.open_sound.play()
            self.animation.loop = False