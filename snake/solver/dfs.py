from collections import deque
import random

from snake.base.direc import Direc
from snake.base.pos import Pos
from snake.solver.base import BaseSolver


class DFSSolver(BaseSolver):
    
    def __init__(self, snake):
        super().__init__(snake)
        self._max_depth = 50  

    def next_direc(self):
        start = self.snake.head()
        
        stack = deque()
        stack.append((start, [])) 
        visited = set([start])
        
        while stack:
            current, path = stack.pop()
            
            if current == self.map.food:
                if path:  
                    return path[0]
                break
            
            if len(path) >= self._max_depth:
                continue
                
            directions = [Direc.LEFT, Direc.UP, Direc.RIGHT, Direc.DOWN]
            random.shuffle(directions)
            
            for direc in directions:
                next_pos = current.adj(direc)
                
                if (self._is_valid_position(next_pos) and 
                    next_pos not in visited):
                    
                    visited.add(next_pos)
                    new_path = path + [direc]
                    stack.append((next_pos, new_path))
        
        return self._find_safe_direction()

    def _is_valid_position(self, pos):
        return self.map.is_safe(pos)

    def _find_safe_direction(self):
        head = self.snake.head()
        safe_directions = []
        
        for direc in [Direc.LEFT, Direc.UP, Direc.RIGHT, Direc.DOWN]:
            next_pos = head.adj(direc)
            if self._is_valid_position(next_pos):
                safe_directions.append(direc)
        
        if self.snake.direc in safe_directions:
            return self.snake.direc
        
        if safe_directions:
            return random.choice(safe_directions)
        
        return self.snake.direc
