import sys
from ..environment.game import PacmanGame
from copy import deepcopy
import time

"""
    Use this method (or any defined method by yourself) to run IDS algorithm on a given 'game' with a given 'max_limit'.
    At the end, you must return the walked path represented as a list of moves by using use PacmanGame.get_info()
    It's recommended to use the earlier defined DFS function here.
"""

sys.setrecursionlimit(20000) # set recursion limit

def dls_recursive(current_game, current_history, limit, path_visited_hashes, start_time, timeout):
    if time.time() - start_time > timeout:
        return "timeout"

    if current_game.is_goal():
        return current_history

    if limit == 0:
        return None

    for next_game_state in current_game.get_next_states():
        next_state_hash = next_game_state.get_state()

        if next_state_hash not in path_visited_hashes:
            
            path_visited_hashes.add(next_state_hash)

            new_history = current_history + [next_game_state.get_info()]
            
            result = dls_recursive( next_game_state, new_history, limit - 1, path_visited_hashes, start_time, timeout)
            
            path_visited_hashes.remove(next_state_hash)

            if result == "timeout":
                return "timeout"
            if result is not None:
                return result

    return None

def ids_solver(game: PacmanGame, max_limit: int = 1000, timeout=10):
    start_time = time.time()
    
    for i in range(max_limit):
        if time.time() - start_time > timeout:
            print("IDS Timeout")
            return [game.get_info()]
        
        
        initial_state_hash = game.get_state()
        path_visited_hashes = {initial_state_hash} 
        initial_history = [game.get_info()]
        
        result = dls_recursive(game ,initial_history ,i ,path_visited_hashes ,start_time ,timeout )
        
        if result == "timeout":
            print("IDS Timeout")
            return [game.get_info()]

        if result is not None:
            print(f"IDS Goal Found at depth {i}!")
            return result
        
    print("IDS No Solution Found (reached max_limit).")
    return None