from collections import deque
from ..environment.game import PacmanGame
import time

def bfs_solver(game: PacmanGame, timeout=10):
    start_time = time.time()

    # Path starts with the initial state info
    initial_path = [game.get_info()]
    # Use deque as a queue (FIFO)
    frontier = deque( [(game, initial_path)] )

    # Keep track of visited states
    explored_states = set()
    explored_states.add(game.get_state())

    while frontier:
        if time.time() - start_time > timeout:
            print("BFS Timeout!")
            return [game.get_info()] # Signal timeout

        current_state, path_so_far = frontier.popleft()

        if current_state.is_goal():
            print("BFS Goal Found!")
            return path_so_far

        for next_state in current_state.get_next_states():
            state_hash = next_state.get_state()
            if state_hash not in explored_states:
                explored_states.add(state_hash)
                new_path = path_so_far + [next_state.get_info()]
                frontier.append( (next_state, new_path) )

    print("BFS No Solution Found.")
    return None