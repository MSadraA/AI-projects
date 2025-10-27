from copy import deepcopy
from .ghost import Ghost
from .snack import Snack

class PacmanGame:
    def __init__(self, player : tuple[int, int], ghosts : list[Ghost], snacks : list[Snack], is_wall, move_direction = None):
        self.player = player
        self.ghosts = deepcopy(ghosts)
        self.snacks = deepcopy(snacks)
        self.is_wall = is_wall
        self.move_direction = move_direction
        self.height = len(is_wall)
        self.width = len(is_wall[0])

    """
        It returns a pair of move_direction and information for dynamic objects of the game.
        Store this information and return it in solvers. It's used on the GUI feature.
    """    
    def get_info(self):
        return (self.move_direction, [self.player] + [ghost.get_info() for ghost in self.ghosts] + [snack.get_info() for snack in self.snacks])

    """
        It returns the snack which is supposed to get eaten to on current state of the game.
    """
    def determine_goal(self):
        remaining_snacks = [s.type for s in self.snacks if s.exists]
        if len(remaining_snacks) == 0:
            return None
        return min(remaining_snacks)

    """
        Determines if (x, y) is in bounds of map or not.
    """
    def in_bounds(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width

    """
        Determines if player/ghost can go to (x, y) without hitting a wall or getting out of bounds
    """
    def is_valid(self, x, y):
        return self.in_bounds(x, y) and not self.is_wall[x][y]

    """
        It determines if the game is finished or not.
    """
    def is_goal(self):
        return all(not b for b in [snack.exists for snack in self.snacks])
    
    """
        It returns a string form of the map at current state.
    """    
    def get_map(self) -> str:
        height = len(self.is_wall)
        width = len(self.is_wall[0])
        display_grid = [[' ' for _ in range(width)] for _ in range(height)]

        for x in range(height):
            for y in range(width):
                if self.is_wall[x][y]:
                    display_grid[x][y] = 'W'

        for snack in self.snacks:
            if snack.exists:
                display_grid[snack.x][snack.y] = f'{snack.type}'

        for g in self.ghosts:
            gx, gy = g.x, g.y
            display_grid[gx][gy] = f'{g.axis}'

        px, py = self.player
        display_grid[px][py] = 'P'

        map_string = "╔" + "═" * width + "╗" + "\n"
        for row in display_grid:
            map_string += "║" + "".join(row) + "║" + "\n"
        return map_string + "╚" + "═" * width + "╝" + "\n"
    

    """
        Use this method (or any defined method by yourself) to explore next possible states of the game.
    """
    def move_ghost(self, ghost):
        next_x, next_y = ghost.get_next_position() 
        new_direction = ghost.direction
        
        is_move_valid = True
        
        if ghost.is_horizontal():
            if abs(next_y - ghost.center[1]) > ghost.radius:
                is_move_valid = False
        else:
            if abs(next_x - ghost.center[0]) > ghost.radius:
                is_move_valid = False
        
        if not self.is_valid(next_x, next_y):
             is_move_valid = False

        if not is_move_valid:
            new_direction = ghost.direction * -1
            
            if ghost.is_horizontal():
                next_x, next_y = ghost.x, ghost.y + new_direction
            else:
                next_x, next_y = ghost.x + new_direction, ghost.y

        ghost.set_state(next_x, next_y, new_direction)

    def get_next_states(self):
        next_states = []

        moves = {
            "U": (-1, 0),
            "L": (0, -1),
            "D": (1, 0),
            "R": (0, 1)
        }

        current_goal_snack = self.determine_goal()
        
        (py, px) = self.player

        for dir, (dy, dx) in moves.items():
            
            new_py, new_px = py + dy, px + dx
            
            if not self.is_valid(new_py, new_px):
                continue
            
            collision = False
            new_ghosts = deepcopy(self.ghosts)
            for ghost in new_ghosts:
                prev_gy, prev_gx = ghost.x, ghost.y
                self.move_ghost(ghost)
                new_gy, new_gx = ghost.x, ghost.y

                if (new_py, new_px) == (new_gy, new_gx):
                    collision = True
                    break
                
                if (new_py, new_px) == (prev_gy, prev_gx) and (new_gy, new_gx) == (py, px):
                    collision = True
                    break

            if collision:
                continue
            
            new_snacks = deepcopy(self.snacks)
            for snack in new_snacks:
                
                if snack.exists and (snack.x, snack.y) == (new_py, new_px) and snack.type == current_goal_snack:
                    snack.exists = False
   
            new_state_game = PacmanGame(
                player=(new_py, new_px),
                ghosts=new_ghosts,
                snacks=new_snacks,
                is_wall=self.is_wall,
                move_direction=dir
            )
            
            next_states.append(new_state_game)                    

        return next_states
    
    """
        Use this method (or any defined method by yourself) to represent current state of the game.
    """
    def get_state(self):
        player_pos = self.player
        snack_status = tuple(s.exists for s in self.snacks)
        ghost_states = tuple(sorted((g.x, g.y, g.direction) for g in self.ghosts))
        return (player_pos, snack_status, ghost_states)
    