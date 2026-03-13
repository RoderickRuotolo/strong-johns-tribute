import pygame

from src.core.config import BLUE, BOSS_HEIGHT, BOSS_SKIN, BOSS_WIDTH, BOSS_Y, GRAY, KNOCKBACK_FRICTION, WIDTH


class Boss:
    def __init__(self):
        self.rect = pygame.Rect(850, BOSS_Y, BOSS_WIDTH, BOSS_HEIGHT)
        self.health = 200
        self.max_health = 200
        self.speed = 2
        self.attack_timer = 0
        self.stun_timer = 0
        self.knockback_velocity = 0.0
        self.facing = -1
        self.invulnerability_timer = 0
        self.state = "intro"
        self.state_timer = 0

    @property
    def alive(self):
        return self.health > 0

    def _state_profile(self):
        if self.state == "intro":
            return {"speed": 0, "damage": 0, "attack_cooldown": 120}
        if self.state == "phase_1":
            return {"speed": 2, "damage": 12, "attack_cooldown": 50}
        if self.state == "phase_2":
            return {"speed": 3, "damage": 15, "attack_cooldown": 40}
        if self.state == "enraged":
            return {"speed": 4, "damage": 19, "attack_cooldown": 30}
        return {"speed": 0, "damage": 0, "attack_cooldown": 120}

    def _update_state_machine(self):
        if not self.alive:
            self.state = "defeated"
            return

        self.state_timer += 1
        health_pct = self.health / self.max_health

        if self.state == "intro":
            if self.state_timer >= 120:
                self.state = "phase_1"
                self.state_timer = 0
            return

        if health_pct <= 0.25:
            if self.state != "enraged":
                self.state = "enraged"
                self.state_timer = 0
            return

        if health_pct <= 0.6:
            if self.state != "phase_2":
                self.state = "phase_2"
                self.state_timer = 0
            return

        if self.state not in ("phase_1", "phase_2", "enraged"):
            self.state = "phase_1"
            self.state_timer = 0

    def move(self, player):
        if self.stun_timer > 0 or not self.alive:
            return
        if self.state == "intro":
            return

        state_profile = self._state_profile()
        speed = state_profile["speed"]

        if self.rect.x > player.rect.x:
            self.rect.x -= speed
            self.facing = -1
        else:
            self.rect.x += speed
            self.facing = 1

    def attack(self, player):
        if not self.alive:
            return
        if self.state == "intro":
            return

        state_profile = self._state_profile()

        if self.rect.colliderect(player.rect):
            if self.attack_timer == 0:
                player.damage(state_profile["damage"], source_x=self.rect.centerx)
                self.attack_timer = state_profile["attack_cooldown"]

        if self.attack_timer > 0:
            self.attack_timer -= 1

    def update(self):
        self._update_state_machine()

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

    def take_hit(self, damage, attacker_x, hit_stun=8, knockback=5.0):
        if not self.alive:
            return False
        if self.invulnerability_timer > 0:
            return False

        self.health -= damage
        self.invulnerability_timer = 4
        self.stun_timer = max(self.stun_timer, hit_stun)
        if self.rect.centerx >= attacker_x:
            self.knockback_velocity = knockback
            self.facing = -1
        else:
            self.knockback_velocity = -knockback
            self.facing = 1
        return True

    def draw(self, surface):
        if not self.alive:
            return

        x = self.rect.x
        y = self.rect.y

        pygame.draw.circle(surface, BOSS_SKIN, (x + 55, y - 10), 22)
        hair_color = BLUE
        if self.state == "phase_2":
            hair_color = (220, 120, 40)
        if self.state == "enraged":
            hair_color = (220, 40, 40)
        pygame.draw.rect(surface, hair_color, (x + 30, y - 30, 50, 15))
        pygame.draw.rect(surface, GRAY, (x, y, 110, 60))
        pygame.draw.rect(surface, hair_color, (x, y + 60, 110, 30))
        pygame.draw.circle(surface, GRAY, (x - 10, y + 30), 20)
        pygame.draw.circle(surface, GRAY, (x + 120, y + 30), 20)
