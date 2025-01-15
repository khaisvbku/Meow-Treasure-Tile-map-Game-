      pg.mixer.music.load("data/sound/background_music.mp3")
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(loops = -1)
        self.click_sound = pg.mixer.Sound("data/sound/click_sound.wav")