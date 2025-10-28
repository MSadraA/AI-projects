from ..environment.game import PacmanGame
import time

def dfs_solver(game: PacmanGame, timeout=10):
    start_time = time.time()
    
    initial_path = [game.get_info()]
    # Use list as a stack
    stack_to_visit = [ (game, initial_path) ]

    # Keep track of states visited during the entire search
    visited_hashes = set()
    visited_hashes.add(game.get_state())

    while stack_to_visit:
        if time.time() - start_time > timeout:
            print("DFS Timeout!")
            return [game.get_info()] 

        current_node, path = stack_to_visit.pop()

        if current_node.is_goal():
            print("DFS Goal Found!")
            return path 

        # Explore neighbors
        for child_node in current_node.get_next_states():
            child_hash = child_node.get_state()
            if child_hash not in visited_hashes:
                visited_hashes.add(child_hash)
                new_path = path + [child_node.get_info()]
                stack_to_visit.append( (child_node, new_path) )

    print("DFS No Solution Found.")
    return None