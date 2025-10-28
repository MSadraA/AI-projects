from ..environment.game import PacmanGame
from copy import deepcopy
import time

"""
    Use this method (or any defined method by yourself) to run IDS algorithm on a given 'game' with a given 'max_limit'.
    At the end, you must return the walked path represented as a list of moves by using use PacmanGame.get_info()
    It's recommended to use the earlier defined DFS function here.
"""

def dls(game: PacmanGame, depth_limit: int , start_time , timeout):
    init_path = [game.get_info()]
    depth = 0
    
    visited = {game.get_state()}
    
    stack = [(depth, game, init_path , visited)]

    while stack:
        if(time.time() - start_time > timeout):
            return "timeout"
        
        cur_depth, cur_node , cur_path , cur_visited = stack.pop()

        if cur_node.is_goal():
            return cur_path 

        for child in cur_node.get_next_states():
            child_hash = child.get_state()
            if child_hash not in cur_visited:
                child_depth = cur_depth + 1
                if child_depth <= depth_limit:
                    cur_visited = cur_visited.union({child_hash})
                    child_path = cur_path + [child.get_info()]
                    stack.append( ( child_depth, child, child_path , cur_visited) )
    return None 
    
def ids_solver(game: PacmanGame, max_limit: int = 1000, timeout=10):
    start_time = time.time()
    
    for i in range(max_limit):
        if time.time() - start_time > timeout:
            print("IDS Timeout")
            return [game.get_info()]
        
        result = dls(game, i, start_time, timeout)
        
        if result == "timeout":
            print("IDS Timeout")
            return [game.get_info()]

        if result is not None:
            print(f"IDS Goal Found at depth {i}!")
            return result

    print("IDS No Solution Found (reached max_limit).")
    return None