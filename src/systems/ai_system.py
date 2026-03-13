def select_target_by_threat(players, attacker_x):
    alive_players = [player for player in players if player.health > 0]
    if not alive_players:
        return players[0]

    def score(player):
        distance = abs(player.rect.centerx - attacker_x)
        threat = 0
        if player.current_attack is not None:
            threat += 90
        if player.combo_index >= 0:
            threat += player.combo_index * 20
        if not player.on_ground:
            threat += 10
        threat += min(50, int((100 - max(0, player.health)) * 0.3))
        return distance - threat

    return min(alive_players, key=score)

