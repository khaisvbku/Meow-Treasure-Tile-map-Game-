import pygame as pg
import os
BASE_IMAGE_PATH = "data/images/"

def folder_len(path_to_folder):
    return len(os.listdir(path_to_folder))

def load_image(path_to_image):
    image = pg.image.load(BASE_IMAGE_PATH + path_to_image).convert_alpha()
    image.set_colorkey((0, 0, 0))
    return image

def load_images(path_to_folder, state=None):
    images = []
    image_files = []
    for image_path in sorted(os.listdir(BASE_IMAGE_PATH + path_to_folder)):
        if os.path.isfile(os.path.join(BASE_IMAGE_PATH + path_to_folder, image_path)):
            image_files.append(image_path)
    
    if state is None:
        for image_name in image_files:
           images.append(load_image(path_to_folder + "/" + image_name))
    
    else:
        # chest
        if state == "close":
            images.append(load_image(path_to_folder + "/" + image_files[0]))
        elif state == "open":
            for i in range(1, 5):
                images.append(load_image(path_to_folder + "/" + image_files[i]))
        
        # player
        if state == "idle":
            for i in range(2):
                images.append(load_image(path_to_folder + "/" + image_files[i]))
        elif state == "run":
            for i in range(2, 4):
                images.append(load_image(path_to_folder + "/" + image_files[i]))
    return images

class Animation:
    def __init__(self, images, duration):
        self.images = images
        self.duration = duration
        self.loop = True
        self.done = False
        self.frame = 0
    
    def copy(self):
        return Animation(self.images, self.duration)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.duration * len(self.images) - 1)
            if self.frame >= self.duration * len(self.images) - 1:
                self.done = True

    def image(self):
        return self.images[int(self.frame / self.duration)]

class Button:
    def __init__(self, image, size: tuple, pos: tuple, border_color: tuple, border_width: int, animation_type=None):
        self.image = pg.transform.scale(image, size).convert_alpha()
        self.INITIAL_POS = pos
        self.pos = list(pos)
        self.mask = pg.mask.from_surface(self.image)
        self.outline = self.mask.outline()
        self.border_color = border_color
        self.border_width = border_width
        self.rect = self.image.get_rect(center=self.pos)
        self.alpha = 255 if animation_type == None else 0
        self.done = False
        self.animation_type = animation_type

    def draw_border(self, surface):
        offset = self.rect.topleft
        adjusted_outline = [(p[0] + offset[0], p[1] + offset[1]) for p in self.outline]
        pg.draw.lines(surface, self.border_color, True, adjusted_outline, self.border_width)

    def animation(self, end_pos: tuple, speed=None):
        if self.animation_type == "fly":
            dx = min(speed, abs(end_pos[0] - self.rect.centerx))
            dy = min(speed, abs(end_pos[1] - self.rect.centery))
            new_x = self.rect.centerx + dx if self.rect.centerx < end_pos[0] else self.rect.centerx - dx
            new_y = self.rect.centery + dy if self.rect.centery < end_pos[1] else self.rect.centery - dy
            self.rect.center = (new_x, new_y)
            if dx == dy == 0:
                self.done = True

        elif self.animation_type == "appear":
            self.alpha = min(self.alpha + speed, 255)
            self.image.set_alpha(self.alpha)
            self.done = True if self.alpha == 255 else False

    def render(self, surface):
        surface.blit(self.image, self.rect)

    def detect_mouse_inside(self, surface, mouse_pos) -> bool:
        if self.rect.collidepoint(mouse_pos) and self.alpha >= 255:
            self.draw_border(surface)
            return True
        return False

    def reset(self):
        self.rect.center = self.INITIAL_POS
        self.alpha = 0
        self.done = False

    def reset(self):
        self.alpha = 0
        self.pos = self.INITIAL_POS

class Word:
    def __init__(self, size, color : tuple, pos, content, font=None):
        self.INITIAL_POS = list(pos)
        self.pos = self.INITIAL_POS
        self.font = pg.font.SysFont("timesnewroman", size) if font is None else pg.font.Font(font, size)
        self.color = color
        self.word = self.font.render(content, False, self.color).convert_alpha()
        self.rect = self.word.get_rect(center = self.pos)
        self.done = False
    
    def update(self, content):
        self.word = self.font.render(content, True, self.color)
    
    def render(self, surface, animation=None, end_pos = None, speed = None):
        if animation == "fly" and end_pos is not None:
            dx = min(speed, abs(end_pos[0] - self.rect.centerx))
            dy = min(speed, abs(end_pos[1] - self.rect.centery))
            new_x = self.rect.centerx + dx if self.rect.centerx < end_pos[0] else self.rect.centerx - dx
            new_y = self.rect.centery + dy if self.rect.centery < end_pos[1] else self.rect.centery - dy
            self.rect.center = (new_x, new_y)
            if dx == dy == 0:
                self.done = True
        surface.blit(self.word, self.rect)

    def reset(self):
        self.pos = self.INITIAL_POS
        self.rect.center = self.pos
        self.done = False

class Ingame_Dialog:
    def __init__(self, text, font, size, speed, max_width):
        self.text = text
        self.speed = speed
        self.max_width = max_width
        self.font = pg.font.Font(font, size)

    def wrap_text(self):
        lines = []
        self.text = self.text.split(" ")
        current_line = ""

        for word in self.text:
            test_line = f"{current_line} {word}".strip()
            if self.font.size(test_line)[0] <= self.max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    def update(self, elapsed_time):
        chars_to_show = int(elapsed_time * self.speed)
        return self.text[:chars_to_show]

    def render(self):
        pass