from collections import deque
from ..environment.game import PacmanGame
from copy import deepcopy
import time

"""
    Use this method (or any defined method by yourself) to run DFS algorithm on a given 'game' with a given 'heuristic.
    At the end, you must return the walked path represented as a list of moves by using use PacmanGame.get_info()
"""

def dfs_recursive_helper(cur_node, cur_path, visited, start_time, timeout):
        if time.time() - start_time > timeout:
            return "timeout"

        if cur_node.is_goal():
            return cur_path

        for child in cur_node.get_next_states():
            child_hash = child.get_state()

            if child_hash not in visited:

                visited.add(child_hash)

                child_path = cur_path + [child.get_info()]

                result = dfs_recursive_helper(child, child_path, visited, start_time, timeout)

                if result == "timeout":
                    return "timeout"
                if result is not None:
                    return result

        return None

def dfs_solver(game: PacmanGame, timeout=10):
    start_time = time.time()
    init_path = [game.get_info()]
    visited = set()
    result = dfs_recursive_helper( game, init_path, visited, start_time, timeout )

    if result == "timeout":
        print("DFS Timeout!")
        return [game.get_info()]
    elif result is None:
        print("DFS No Solution Found (or hit recursion limit).")
    else:
        print("DFS Goal Found!")
        return result
    

    