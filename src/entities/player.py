import pygame

from src.core.config import (
    ATTACK_CHAIN,
    AIR_ATTACK,
    GRAVITY,
    HEAVY_ATTACK,
    HEIGHT,
    JUMP_VELOCITY,
    KNOCKBACK_FRICTION,
    MAX_FALL_SPEED,
    PLAYER_HEIGHT,
    PLAYER_WIDTH,
    PLAYER_Y,
    WIDTH,
)


class Player:
    def __init__(self, x, color):
        self.rect = pygame.Rect(x, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.color = color
        self.speed = 5
        self.health = 100
        self.attack = False
        self.attack_rect = pygame.Rect(0, 0, 0, 0)
        self.damage_cooldown = 0
        self.facing = 1
        self.stun_timer = 0
        self.hurt_flash_timer = 0
        self.knockback_velocity = 0.0
        self.attack_elapsed = 0
        self.current_attack = None
        self.combo_index = -1
        self.combo_timer = 0
        self.current_attack_hits = set()
        self.velocity_y = 0.0
        self.pos_y = float(self.rect.y)
        self.invulnerability_timer = 0
        self.air_attack_used = False
        self.light_buffer_timer = 0
        self.heavy_buffer_timer = 0

    def move(self, left, right, jump):
        keys = pygame.key.get_pressed()
        if self.stun_timer > 0 or self.current_attack is not None:
            return

        if keys[left]:
            self.rect.x -= self.speed
            self.facing = -1
        if keys[right]:
            self.rect.x += self.speed
            self.facing = 1

        if keys[jump] and self.on_ground:
            self.velocity_y = JUMP_VELOCITY
            self.air_attack_used = False

    def start_attack(self):
        if self.stun_timer > 0 or self.current_attack is not None:
            return

        if not self.on_ground:
            if self.air_attack_used:
                return
            self._begin_attack(profile=AIR_ATTACK, combo_index=-1)
            self.air_attack_used = True
            return

        if self.combo_timer > 0 and self.combo_index < len(ATTACK_CHAIN) - 1:
            next_index = self.combo_index + 1
        else:
            next_index = 0

        self._begin_attack(profile=ATTACK_CHAIN[next_index], combo_index=next_index)

    def start_heavy_attack(self):
        if self.stun_timer > 0 or self.current_attack is not None or not self.on_ground:
            return

        self.combo_index = -1
        self.combo_timer = 0
        self._begin_attack(profile=HEAVY_ATTACK, combo_index=-1)

    def queue_light_attack(self):
        self.light_buffer_timer = 8

    def queue_heavy_attack(self):
        self.heavy_buffer_timer = 8

    def update(self):
        if self.stun_timer > 0:
            self.stun_timer -= 1

        if self.invulnerability_timer > 0:
            self.invulnerability_timer -= 1

        if self.light_buffer_timer > 0:
            self.light_buffer_timer -= 1

        if self.heavy_buffer_timer > 0:
            self.heavy_buffer_timer -= 1

        if self.current_attack is not None:
            self.attack_elapsed += 1
            active_start = self.current_attack["active_start"]
            active_end = self.current_attack["active_end"]
            self.attack = active_start <= self.attack_elapsed <= active_end

            if self.attack_elapsed >= self.current_attack["total_frames"]:
                self.current_attack = None
                self.attack_elapsed = 0
                self.attack = False
                self.current_attack_hits.clear()
        else:
            self.attack = False
            if self.combo_timer > 0:
                self.combo_timer -= 1
            else:
                self.combo_index = -1

        if self.current_attack is None and self.stun_timer == 0:
            if self.heavy_buffer_timer > 0:
                self.start_heavy_attack()
                if self.current_attack is not None:
                    self.heavy_buffer_timer = 0
                    self.light_buffer_timer = 0
            elif self.light_buffer_timer > 0:
                self.start_attack()
                if self.current_attack is not None:
                    self.light_buffer_timer = 0

        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        if self.hurt_flash_timer > 0:
            self.hurt_flash_timer -= 1

        if not self.on_ground or self.velocity_y < 0:
            self.velocity_y = min(self.velocity_y + GRAVITY, MAX_FALL_SPEED)
            self.pos_y += self.velocity_y

            if self.pos_y >= PLAYER_Y:
                self.pos_y = float(PLAYER_Y)
                self.velocity_y = 0.0
                self.air_attack_used = False

        self.rect.y = int(self.pos_y)

        if abs(self.knockback_velocity) > 0.05:
            self.rect.x += int(self.knockback_velocity)
            self.knockback_velocity *= KNOCKBACK_FRICTION
        else:
            self.knockback_velocity = 0.0

        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))
        self.pos_y = float(self.rect.y)

        if self.attack and self.current_attack is not None:
            if self.facing >= 0:
                attack_x = self.rect.x + self.rect.width + self.current_attack["hitbox_offset_x"]
            else:
                attack_x = self.rect.x - self.current_attack["hitbox_width"] - self.current_attack["hitbox_offset_x"]
            self.attack_rect = pygame.Rect(
                attack_x,
                self.rect.y + self.current_attack["hitbox_offset_y"],
                self.current_attack["hitbox_width"],
                self.current_attack["hitbox_height"],
            )
        else:
            self.attack_rect = pygame.Rect(0, 0, 0, 0)

    def damage(self, amount, source_x=None):
        if self.damage_cooldown == 0 and self.invulnerability_timer == 0:
            self.health -= amount
            self.damage_cooldown = 30
            self.invulnerability_timer = 20
            self.hurt_flash_timer = 10
            self.stun_timer = max(self.stun_timer, 8)
            if source_x is not None:
                if self.rect.centerx >= source_x:
                    self.knockback_velocity = 6.0
                else:
                    self.knockback_velocity = -6.0

    @property
    def attack_profile(self):
        return self.current_attack

    @property
    def on_ground(self):
        return self.rect.y >= PLAYER_Y and self.velocity_y == 0.0

    def _begin_attack(self, profile, combo_index):
        self.current_attack = profile
        self.combo_index = combo_index
        self.combo_timer = self.current_attack["combo_link_window"]
        self.attack_elapsed = 0
        self.attack = False
        self.current_attack_hits.clear()
