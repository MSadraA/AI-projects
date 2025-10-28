from ..environment.game import PacmanGame

"""
    Place your heuristic functions here.
"""

def manhattan_distance(pos1, pos2):
    y1, x1 = pos1
    y2, x2 = pos2
    return abs(y1 - y2) + abs(x1 - x2)

def get_target_snacks(game: PacmanGame):
    target_snacks_pos = [ (snack.x, snack.y) for snack in game.snacks if snack.type == 'A' and snack.exists ]
    
    if not target_snacks_pos:
        target_snacks_pos = [ (snack.x, snack.y) for snack in game.snacks if snack.type == 'B' and snack.exists ]
        
    return target_snacks_pos

def heuristic_1(game: PacmanGame):
    pacman_pos = game.player
    target_snacks = get_target_snacks(game)
    
    if not target_snacks:
        return 0
    
    distances = [ manhattan_distance(pacman_pos, snack_pos) for snack_pos in target_snacks ]
    
    return min(distances)

def heuristic_2(game: PacmanGame):
    pacman_pos = game.player
    target_snacks = get_target_snacks(game)
    
    if not target_snacks:
        return 0
    
    distances = [ manhattan_distance(pacman_pos, snack_pos) for snack_pos in target_snacks ]
    
    return max(distances)