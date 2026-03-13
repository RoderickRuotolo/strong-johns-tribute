import random
import pygame

from src.core.config import ENEMY_ARCHETYPES, ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_Y, KNOCKBACK_FRICTION, WIDTH


class Enemy:
    def __init__(self, archetype="rush"):
        if archetype not in ENEMY_ARCHETYPES:
            archetype = "rush"
        self.archetype = archetype
        self.profile = ENEMY_ARCHETYPES[archetype]
        self.rect = pygame.Rect(random.randint(700, 1000), ENEMY_Y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.speed = random.randint(self.profile["speed_min"], self.profile["speed_max"])
        self.attack_timer = 0
        self.health = self.profile["health"]
        self.facing = -1
        self.stun_timer = 0
        self.knockback_velocity = 0.0
        self.invulnerability_timer = 0

    @property
    def alive(self):
        return self.health > 0

    def move(self, player):
        if self.stun_timer > 0:
            return
        if player.health <= 0:
            return

        distance_x = player.rect.centerx - self.rect.centerx
        stop_distance = self.profile["contact_range"]

        if abs(distance_x) <= stop_distance:
            return

        if distance_x < 0:
            self.rect.x -= self.speed
            self.facing = -1
        else:
            self.rect.x += self.speed
            self.facing = 1

    def attack(self, player):
        if player.health <= 0:
            return

        distance_x = abs(player.rect.centerx - self.rect.centerx)
        in_contact = self.rect.colliderect(player.rect)
        in_range = distance_x <= self.profile["contact_range"]
        can_attack = in_contact or (self.profile["contact_range"] > 0 and in_range)

        if can_attack and self.attack_timer == 0:
            player.damage(self.profile["damage"], source_x=self.rect.centerx)
            self.attack_timer = self.profile["attack_cooldown"]

        if self.attack_timer > 0:
            self.attack_timer -= 1

    def update(self):
        if self.stun_timer > 0:
            self.stun_timer -= 1
        if self.invulnerability_timer > 0:
            self.invulnerability_timer -= 1

        if abs(self.knockback_velocity) > 0.05:
            self.rect.x += int(self.knockback_velocity)
            self.knockback_velocity *= KNOCKBACK_FRICTION
        else:
            self.knockback_velocity = 0.0

        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))

    def take_hit(self, damage, attacker_x, hit_stun=10, knockback=9.0):
        if self.invulnerability_timer > 0:
            return False

        self.health -= damage
        self.invulnerability_timer = 6
        adjusted_stun = max(4, int(hit_stun / self.profile["stun_resistance"]))
        self.stun_timer = max(self.stun_timer, adjusted_stun)
        if self.rect.centerx >= attacker_x:
            self.knockback_velocity = knockback
            self.facing = -1
        else:
            self.knockback_velocity = -knockback
            self.facing = 1
        return True

    def draw(self, surface):
        x = self.rect.x
        y = self.rect.y
        pygame.draw.circle(surface, (210, 180, 150), (x + 30, y - 5), 15)
        pygame.draw.rect(surface, self.profile["color"], (x, y, 60, 65))
