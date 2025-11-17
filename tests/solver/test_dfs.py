from snake.base import Direc, Map, PointType, Pos, Snake
from snake.solver.dfs import DFSSolver

def main():
    print("=== DFS Solver Simple Test ===")
    
    game_map = Map(8, 8)
    snake = Snake(game_map)
    
    food_pos = Pos(4, 4)
    game_map.create_food(food_pos)
    
    print(f"Initial state:")
    print(f"Snake head position: {snake.head()}")
    print(f"Food position: {food_pos}")
    print(f"Snake direction: {snake.direc}")
    
    dfs_solver = DFSSolver(snake)
    
    for step in range(10):
        next_direc = dfs_solver.next_direc()
        print(f"\nStep {step + 1}:")
        print(f"Selected direction: {next_direc}")
        
        snake.move(next_direc)
        
        print(f"New snake head position: {snake.head()}")
        print(f"Snake length: {snake.len()}")
        
        if snake.head() == food_pos:
            print("*** Food eaten! ***")
            new_food = game_map.create_rand_food()
            if new_food:
                print(f"New food position: {new_food}")
                food_pos = new_food
            else:
                print("Map is full!")
                break
        
        if snake.dead:
            print("*** Snake died! ***")
            break
    
    print(f"\nTest finished:")
    print(f"Final snake length: {snake.len()}")
    print(f"Total steps: {snake.steps}")

if __name__ == "__main__":
    main()
