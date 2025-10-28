import sys
from ..environment.game import PacmanGame
from copy import deepcopy # This import is not used
import time

# Increase recursion depth limit for potentially deep paths
sys.setrecursionlimit(20000)

def depth_limited_search(current_state, history, depth_remaining, nodes_in_path, start_timestamp, timeout_seconds):
    if time.time() - start_timestamp > timeout_seconds:
        return "timeout" # Signal timeout

    if current_state.is_goal():
        return history # Goal found

    if depth_remaining == 0:
        return None # Depth limit reached

    for next_node in current_state.get_next_states():
        next_node_hash = next_node.get_state()

        # Avoid cycles within the current path
        if next_node_hash not in nodes_in_path:
            
            nodes_in_path.add(next_node_hash) # Add to current path
            
            new_history = history + [next_node.get_info()]
            
            # Recursive call for the child node
            search_result = depth_limited_search(
                next_node,
                new_history,
                depth_remaining - 1, # Decrease remaining depth
                nodes_in_path,
                start_timestamp,
                timeout_seconds
            )
            
            nodes_in_path.remove(next_node_hash) # Backtrack: remove from current path

            # Propagate results up
            if search_result == "timeout":
                return "timeout"
            if search_result is not None:
                return search_result # Goal found in this branch

    return None # No goal found in this branch within the depth limit

def ids_solver(game: PacmanGame, max_depth: int = 1000, timeout: int = 10):
    start_time = time.time()
    
    # Iterate through increasing depth limits
    for depth_limit in range(max_depth):
        if time.time() - start_time > timeout:
            print("IDS Timeout")
            return [game.get_info()] # Signal timeout
        
        # Prepare for DLS at the current depth
        start_node_hash = game.get_state()
        nodes_on_path = {start_node_hash} # Set for nodes currently in the recursion path
        start_history = [game.get_info()]
        
        # Call the recursive DLS helper
        outcome = depth_limited_search(
            game,
            start_history,
            depth_limit, # Current depth limit
            nodes_on_path,
            start_time,
            timeout
        )
        
        if outcome == "timeout":
            print("IDS Timeout")
            return [game.get_info()]

        if outcome is not None:
            # Found a solution at this depth (which is guaranteed to be optimal)
            print(f"IDS Goal Found at depth {depth_limit}!")
            return outcome
        
        # If outcome is None, continue to the next depth limit
        
    print("IDS No Solution Found (reached max_limit).")
    return None