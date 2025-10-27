from collections import deque
from ..environment.game import PacmanGame
from copy import deepcopy
import time

"""
    Use this method (or any defined method by yourself) to run DFS algorithm on a given 'game' with a given 'heuristic.
    At the end, you must return the walked path represented as a list of moves by using use PacmanGame.get_info()
"""

def dfs_solver(game: PacmanGame, timeout=10):
    start_time = time.time()
    initial_history = [game.get_info()]
    stack = [ (game, initial_history) ]

    visited = set()
    visited.add(game.get_state())

    while stack:
        if time.time() - start_time > timeout:
            print("DFS Timeout!")
            return [game.get_info()] 

        cur_node , cur_path = stack.pop()

        if cur_node .is_goal():
            print("DFS Goal Found!")
            return cur_path 

        for child in cur_node .get_next_states():
            child_hash = child.get_state()
            if child_hash not in visited:
                visited.add(child_hash)
                child_path = cur_path + [child.get_info()]
                stack.append( (child, child_path) )

    print("DFS No Solution Found.")
    return None
    

    