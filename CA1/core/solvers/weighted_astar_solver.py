import heapq
from ..environment.game import PacmanGame
from .heuristics import * # Assuming heuristics like heuristic_1, heuristic_2 are here
import time

def weighted_astar_calculator(initial_game: PacmanGame, heuristic_func, weight: int = 1, time_limit=10):
    start_time = time.time()
    
    # Priority queue: (f_score, g_score, tie_break, state, path)
    priority_queue = [] 
    
    # Track min g_score found for each state hash
    min_costs = {} 
    
    node_counter = 0 # Tie-breaker

    start_node = initial_game
    start_hash = start_node.get_state()
    g_val = 0
    h_val = heuristic_func(start_node)
    f_val = g_val + (weight * h_val)
    start_path = [start_node.get_info()]
    
    heapq.heappush(priority_queue, (f_val, g_val, node_counter, start_node, start_path))
    node_counter += 1
    
    min_costs[start_hash] = g_val

    while priority_queue:
        if time.time() - start_time > time_limit:
            print("A* Timeout!")
            return [initial_game.get_info()]

        f_current, g_current, _, current_node, path_taken = heapq.heappop(priority_queue)
        
        current_hash = current_node.get_state()

        if current_node.is_goal():
            print("A* Goal Found!")
            return path_taken

        # Skip if we found a better path already
        if g_current > min_costs.get(current_hash, float('inf')):
            continue

        for successor_node in current_node.get_next_states():
            successor_hash = successor_node.get_state()
            
            step_cost = 1 
            g_successor = g_current + step_cost

            # Check if this path is better
            if g_successor < min_costs.get(successor_hash, float('inf')):
                min_costs[successor_hash] = g_successor
                h_successor = heuristic_func(successor_node)
                f_successor = g_successor + (weight * h_successor)
                new_path_history = path_taken + [successor_node.get_info()]
                
                heapq.heappush(priority_queue, (f_successor, g_successor, node_counter, successor_node, new_path_history))
                node_counter += 1

    print("A* No Solution Found.")
    return None

def weighted_astar_solver(game: PacmanGame, weight: int = 2, timeout=10):
    # heuristic_choice = heuristic_1
    heuristic_choice = heuristic_2 
    return weighted_astar_calculator(game, heuristic_choice, weight, timeout)