from collections import deque
from ..environment.game import PacmanGame
import time

"""
    Use this method (or any defined method by yourself) to run BFS algorithm on a given 'game'.
    At the end, you must return the walked path represented as a list of moves by using use PacmanGame.get_info()
"""
def bfs_solver(game: PacmanGame, timeout=10):
    start_time = time.time()

    init_path = [game.get_info()]
    node_queue = deque( [(game, init_path)] )

    visited = set()
    visited.add(game.get_state())

    while node_queue:
        if time.time() - start_time > timeout:
            print("BFS Timeout!")
            return [game.get_info()] 

        cur_node, cur_path = node_queue.popleft()

        if cur_node.is_goal():
            print("BFS Goal Found!")
            return cur_path

        for child in cur_node.get_next_states():
            
            child_hash = child.get_state()
            if child_hash not in visited:
                visited.add(child_hash)
                child_path = cur_path + [child.get_info()]
                node_queue.append( (child, child_path) )

    print("BFS No Solution Found.")
    return None
    