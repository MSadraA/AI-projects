import heapq
from ..environment.game import PacmanGame
from .heuristics import * 
from .weighted_astar_solver import weighted_astar_calculator

def astar_solver(game: PacmanGame, timeout=10):
    
    # default_heuristic = heuristic_1
    default_heuristic = heuristic_2
    
    return weighted_astar_calculator( game,  heuristic_func=default_heuristic,  weight=1, time_limit=timeout)