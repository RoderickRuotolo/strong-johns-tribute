import math
from array import array

import pygame


class AudioSystem:
    def __init__(self):
        self.enabled = False
        self.sfx = {}
        self._music_sound = None

        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            self.enabled = True
            self._build_sfx()
            self.set_volume(0.35)
        except pygame.error:
            self.enabled = False

    def _tone(self, frequency, ms, volume=0.5):
        sample_rate = 22050
        count = int(sample_rate * ms / 1000.0)
        data = array("h")
        amplitude = int(32767 * max(0.0, min(1.0, volume)))
        for i in range(count):
            sample = int(amplitude * math.sin(2.0 * math.pi * frequency * (i / sample_rate)))
            data.append(sample)
        return pygame.mixer.Sound(buffer=data.tobytes())

    def _build_sfx(self):
        self.sfx["punch"] = self._tone(180, 70, 0.45)
        self.sfx["heavy"] = self._tone(110, 120, 0.6)
        self.sfx["hurt"] = self._tone(240, 80, 0.35)
        self.sfx["ko"] = self._tone(90, 200, 0.55)
        self.sfx["ui"] = self._tone(520, 70, 0.2)
        self._music_sound = self._tone(130, 1800, 0.08)

    def set_volume(self, master):
        if not self.enabled:
            return
        for sound in self.sfx.values():
            sound.set_volume(master)
        if self._music_sound:
            self._music_sound.set_volume(master * 0.8)

    def play_sfx(self, name):
        if not self.enabled:
            return
        sound = self.sfx.get(name)
        if sound:
            sound.play()

    def start_music(self):
        if not self.enabled or not self._music_sound:
            return
        self._music_sound.play(loops=-1)
