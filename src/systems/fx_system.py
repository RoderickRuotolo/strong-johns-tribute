import random

import pygame


class FXSystem:
    def __init__(self):
        self.sparks = []
        self.screen_shake_timer = 0
        self.screen_shake_intensity = 0
        self.hit_stop_frames = 0

    def on_hit(self, x, y, heavy=False):
        spark_count = 10 if heavy else 6
        for _ in range(spark_count):
            self.sparks.append(
                {
                    "x": float(x),
                    "y": float(y),
                    "vx": random.uniform(-4.2, 4.2),
                    "vy": random.uniform(-3.2, -0.6),
                    "life": random.randint(10, 16),
                    "size": random.randint(2, 4),
                    "color": (255, random.randint(170, 230), 80),
                }
            )

        self.screen_shake_timer = max(self.screen_shake_timer, 7 if heavy else 4)
        self.screen_shake_intensity = max(self.screen_shake_intensity, 8 if heavy else 4)
        self.hit_stop_frames = max(self.hit_stop_frames, 4 if heavy else 2)

    def update(self):
        if self.screen_shake_timer > 0:
            self.screen_shake_timer -= 1
            if self.screen_shake_timer == 0:
                self.screen_shake_intensity = 0

        updated = []
        for spark in self.sparks:
            spark["x"] += spark["vx"]
            spark["y"] += spark["vy"]
            spark["vy"] += 0.35
            spark["life"] -= 1
            if spark["life"] > 0:
                updated.append(spark)
        self.sparks = updated

    def consume_hit_stop(self):
        if self.hit_stop_frames > 0:
            self.hit_stop_frames -= 1
            return True
        return False

    def camera_offset(self):
        if self.screen_shake_timer <= 0:
            return (0, 0)
        return (
            random.randint(-self.screen_shake_intensity, self.screen_shake_intensity),
            random.randint(-self.screen_shake_intensity, self.screen_shake_intensity),
        )

    def draw(self, surface):
        for spark in self.sparks:
            pygame.draw.circle(
                surface,
                spark["color"],
                (int(spark["x"]), int(spark["y"])),
                spark["size"],
            )
