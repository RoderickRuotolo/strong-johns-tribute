import sys

import pygame

from src.core.config import BLUE, FPS, HEIGHT, WIDTH, WINDOW_TITLE
from src.entities.player import Player
from src.systems.ai_system import select_target_by_threat
from src.systems.audio_system import AudioSystem
from src.systems.combat_system import player_attack
from src.systems.fx_system import FXSystem
from src.systems.input_system import default_bindings, key_name
from src.systems.render_system import (
    draw_bar,
    draw_boss,
    draw_boss_text,
    draw_enemy,
    draw_game_over,
    draw_health,
    draw_options_menu,
    draw_pause_menu,
    draw_player_feedback,
    draw_players,
    draw_restart_hint,
    draw_controls_menu,
    draw_stage_clear,
    draw_victory,
    draw_wave_info,
    get_main_font,
)
from src.systems.spawn_system import init_wave_state, update_spawning


def reset_match():
    player1 = Player(150, (250, 250, 250))
    player2 = Player(260, BLUE)
    players = [player1, player2]
    enemies = []
    boss = None
    spawn_timer = 0
    wave_state = init_wave_state()
    game_state = "playing"
    clear_timer = 0
    return players, enemies, boss, spawn_timer, wave_state, game_state, clear_timer


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    frame_surface = pygame.Surface((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = get_main_font()
    fx = FXSystem()
    audio = AudioSystem()
    audio.start_music()
    bindings = default_bindings()
    settings = {
        "master_volume": 0.35,
        "screen_shake": True,
        "fullscreen": False,
    }
    audio.set_volume(settings["master_volume"])

    players, enemies, boss, spawn_timer, wave_state, game_state, clear_timer = reset_match()
    running = True
    frame_count = 0
    defeat_sfx_played = False
    victory_sfx_played = False
    ui_mode = "none"
    pause_index = 0
    options_index = 0
    controls_index = 0
    waiting_rebind_action = None

    control_actions = [
        "p1_left",
        "p1_right",
        "p1_jump",
        "p2_left",
        "p2_right",
        "p2_jump",
        "light_attack",
        "heavy_attack",
        "pause",
        "restart",
    ]

    while running:
        frame_count += 1
        active_play = game_state == "playing" and ui_mode == "none"
        freeze_frame = active_play and fx.consume_hit_stop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if ui_mode == "controls" and waiting_rebind_action is not None:
                    bindings[waiting_rebind_action] = event.key
                    waiting_rebind_action = None
                    audio.play_sfx("ui")
                    continue

                if event.key == bindings["pause"] and game_state == "playing":
                    if ui_mode == "none":
                        ui_mode = "pause"
                    elif ui_mode == "pause":
                        ui_mode = "none"
                    elif ui_mode == "options":
                        ui_mode = "pause"
                    elif ui_mode == "controls":
                        waiting_rebind_action = None
                        ui_mode = "options"
                    audio.play_sfx("ui")
                    continue

                if ui_mode == "pause":
                    if event.key in (pygame.K_UP, pygame.K_w):
                        pause_index = (pause_index - 1) % 4
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        pause_index = (pause_index + 1) % 4
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if pause_index == 0:
                            ui_mode = "none"
                        elif pause_index == 1:
                            players, enemies, boss, spawn_timer, wave_state, game_state, clear_timer = reset_match()
                            defeat_sfx_played = False
                            victory_sfx_played = False
                            ui_mode = "none"
                        elif pause_index == 2:
                            ui_mode = "options"
                        elif pause_index == 3:
                            running = False
                        audio.play_sfx("ui")
                    continue

                if ui_mode == "options":
                    if event.key in (pygame.K_UP, pygame.K_w):
                        options_index = (options_index - 1) % 5
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        options_index = (options_index + 1) % 5
                    elif event.key in (pygame.K_LEFT, pygame.K_a) and options_index == 0:
                        settings["master_volume"] = max(0.0, settings["master_volume"] - 0.05)
                        audio.set_volume(settings["master_volume"])
                        audio.play_sfx("ui")
                    elif event.key in (pygame.K_RIGHT, pygame.K_d) and options_index == 0:
                        settings["master_volume"] = min(1.0, settings["master_volume"] + 0.05)
                        audio.set_volume(settings["master_volume"])
                        audio.play_sfx("ui")
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if options_index == 1:
                            settings["screen_shake"] = not settings["screen_shake"]
                            audio.play_sfx("ui")
                        elif options_index == 2:
                            settings["fullscreen"] = not settings["fullscreen"]
                            if settings["fullscreen"]:
                                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                            else:
                                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                            frame_surface = pygame.Surface((WIDTH, HEIGHT))
                            audio.play_sfx("ui")
                        elif options_index == 3:
                            ui_mode = "controls"
                            waiting_rebind_action = None
                            audio.play_sfx("ui")
                        elif options_index == 4:
                            ui_mode = "pause"
                            audio.play_sfx("ui")
                    elif event.key == pygame.K_BACKSPACE:
                        ui_mode = "pause"
                        audio.play_sfx("ui")
                    continue

                if ui_mode == "controls":
                    max_idx = len(control_actions)
                    if event.key in (pygame.K_UP, pygame.K_w):
                        controls_index = (controls_index - 1) % (max_idx + 1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        controls_index = (controls_index + 1) % (max_idx + 1)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if controls_index == max_idx:
                            ui_mode = "options"
                            waiting_rebind_action = None
                        else:
                            waiting_rebind_action = control_actions[controls_index]
                        audio.play_sfx("ui")
                    elif event.key == pygame.K_BACKSPACE:
                        ui_mode = "options"
                        waiting_rebind_action = None
                        audio.play_sfx("ui")
                    continue

                if event.key == bindings["restart"] and game_state in ("victory", "defeat"):
                    players, enemies, boss, spawn_timer, wave_state, game_state, clear_timer = reset_match()
                    defeat_sfx_played = False
                    victory_sfx_played = False
                    audio.play_sfx("ui")

                if active_play and event.key == bindings["light_attack"]:
                    for player in players:
                        if player.health > 0:
                            player.queue_light_attack()

                if active_play and event.key == bindings["heavy_attack"]:
                    for player in players:
                        if player.health > 0:
                            player.queue_heavy_attack()

        player1, player2 = players
        prev_health = (player1.health, player2.health)

        if active_play and not freeze_frame:
            if player1.health > 0:
                player1.move(bindings["p1_left"], bindings["p1_right"], bindings["p1_jump"])
            if player2.health > 0:
                player2.move(bindings["p2_left"], bindings["p2_right"], bindings["p2_jump"])

        for player in players:
            player.update()

        if active_play and not freeze_frame:
            spawn_timer, boss, wave_state = update_spawning(spawn_timer, enemies, boss, wave_state)

        draw_bar(frame_surface, frame_count)
        draw_players(frame_surface, player1, player2)

        for enemy in enemies:
            if active_play and not freeze_frame:
                target = select_target_by_threat(players, enemy.rect.centerx)
                enemy.move(target)
                if player1.health > 0:
                    enemy.attack(player1)
                if player2.health > 0:
                    enemy.attack(player2)
            enemy.update()
            draw_enemy(frame_surface, enemy)

        if boss:
            if active_play and not freeze_frame:
                target = select_target_by_threat(players, boss.rect.centerx)
                boss.move(target)
                if player1.health > 0:
                    boss.attack(player1)
                if player2.health > 0:
                    boss.attack(player2)
            boss.update()
            draw_boss(frame_surface, boss)
            if boss.alive:
                draw_boss_text(frame_surface, font, boss)

        if active_play and not freeze_frame:
            hit_events = player_attack(players, enemies, boss)
            for hit in hit_events:
                fx.on_hit(hit["x"], hit["y"], heavy=hit["heavy"])
                audio.play_sfx("heavy" if hit["heavy"] else "punch")

        if player1.health < prev_health[0] or player2.health < prev_health[1]:
            hit_x = player1.rect.centerx if player1.health < prev_health[0] else player2.rect.centerx
            hit_y = player1.rect.centery if player1.health < prev_health[0] else player2.rect.centery
            fx.on_hit(hit_x, hit_y, heavy=False)
            audio.play_sfx("hurt")

        draw_health(frame_surface, player1, 40, 40)
        draw_health(frame_surface, player2, 40, 70)
        draw_wave_info(frame_surface, font, wave_state, len(enemies))
        draw_player_feedback(frame_surface, font, player1, 40, 130, "P1")
        draw_player_feedback(frame_surface, font, player2, 40, 160, "P2")

        if active_play and player1.health <= 0 and player2.health <= 0:
            game_state = "defeat"

        if active_play and boss and not boss.alive and not enemies:
            game_state = "stage_clear"
            clear_timer = 120

        if game_state == "stage_clear":
            draw_stage_clear(frame_surface, font)
            clear_timer -= 1
            if clear_timer <= 0:
                game_state = "victory"

        if game_state == "defeat":
            draw_game_over(frame_surface, font)
            draw_restart_hint(frame_surface, font, key_name(bindings["restart"]))
            if not defeat_sfx_played:
                audio.play_sfx("ko")
                defeat_sfx_played = True

        if game_state == "victory":
            draw_victory(frame_surface, font)
            draw_restart_hint(frame_surface, font, key_name(bindings["restart"]))
            if not victory_sfx_played:
                audio.play_sfx("ui")
                victory_sfx_played = True

        fx.update()
        fx.draw(frame_surface)
        if settings["screen_shake"]:
            shake_x, shake_y = fx.camera_offset()
        else:
            shake_x, shake_y = (0, 0)
        screen.fill((0, 0, 0))
        screen.blit(frame_surface, (shake_x, shake_y))

        if ui_mode == "pause":
            draw_pause_menu(screen, font, pause_index)
        elif ui_mode == "options":
            draw_options_menu(screen, font, options_index, settings)
        elif ui_mode == "controls":
            draw_controls_menu(screen, font, controls_index, bindings, waiting_rebind_action)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
