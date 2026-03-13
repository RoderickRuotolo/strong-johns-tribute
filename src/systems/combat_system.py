def player_attack(players, enemies, boss):
    hit_events = []

    for player in players:
        if player.attack and player.attack_profile:
            profile = player.attack_profile

            for enemy in enemies:
                enemy_id = id(enemy)
                if enemy_id in player.current_attack_hits:
                    continue

                if player.attack_rect.colliderect(enemy.rect):
                    hit_landed = enemy.take_hit(
                        damage=profile["damage"],
                        attacker_x=player.rect.centerx,
                        hit_stun=profile["hit_stun"],
                        knockback=profile["knockback"],
                    )
                    if hit_landed:
                        player.current_attack_hits.add(enemy_id)
                        hit_events.append(
                            {
                                "x": enemy.rect.centerx,
                                "y": enemy.rect.centery,
                                "heavy": profile["name"] == "heavy",
                            }
                        )

            if boss and player.attack_rect.colliderect(boss.rect):
                boss_id = id(boss)
                if boss_id not in player.current_attack_hits:
                    hit_landed = boss.take_hit(
                        damage=profile["damage"],
                        attacker_x=player.rect.centerx,
                        hit_stun=max(5, int(profile["hit_stun"] * 0.6)),
                        knockback=max(3.0, profile["knockback"] * 0.5),
                    )
                    if hit_landed:
                        player.current_attack_hits.add(boss_id)
                        hit_events.append(
                            {
                                "x": boss.rect.centerx,
                                "y": boss.rect.centery,
                                "heavy": profile["name"] == "heavy",
                            }
                        )

    enemies[:] = [enemy for enemy in enemies if enemy.alive]
    return hit_events
