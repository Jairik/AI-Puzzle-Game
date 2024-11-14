''' Class that uses A* Search to calculate the best overall path - JJ McCauley - 11/13/24 '''

from random import randint, shuffle
import heapq

class puzzleSolver:
    
    ''' Initialize variables and final optimal path on create '''
    def __init__(self):
        self.move_counter = 0
        self.visited = set()
        self.lastmove = None
        self.optimal_moves = []
        self.movement_cost = 1  # Hardcoded movement cost (will always be 1)
        
    '''Calculates the scaled Manhattan Distance of the provided board, also considering linear conflicts'''
    def heuristic(self, board):
        total_distance = 0
        for i in range(4):
            for j in range(4):
                tile = board[i][j]
                if tile != 0:
                    target_i, target_j = divmod(tile - 1, 4)  # Get target i, j
                    total_distance += abs(target_i - i) + abs(target_j - j)  # Add the distance of each
                    # Checking for and penalizing any linear conflicts
                    if target_i == i:  # Linear conflicts in row
                        for k in range(j+1, 4):  # Checking all tiles to the right
                            other_tile = board[i][k]
                            if other_tile != 0:  # Skipping blank space
                                target_i_other = (other_tile-1) // 4  # Calculating target row of other tile
                                # Check if other tile belongs in same row and is above it when it should be below, 
                                # Essentially blocking the other tile
                                if target_i_other == i and other_tile < tile:
                                    total_distance += 2  # Minimum 2 moves to swap
                    if target_j == j:  # Linear conflicts in column
                        for k in range(i+1, 4):  # Checking all tiles below
                            other_tile = board[k][j]
                            if other_tile != 0:
                                target_j_other = (other_tile-1) % 4  # Calculating target column of other tile
                                # Check if other tile is 'blocking' current tile
                                if target_j_other == j and other_tile < tile:
                                    total_distance += 2  # Minimum 2 moves to swap
        return total_distance * 2  # Scaling heuristic
    
    
    '''Gets Adjancent from provided blankspace
    Helper for A* Search, return a list of tuples of adjacent tiles'''
    def get_adjacent_tiles(self, cords: tuple):
        adjacent_cords = []
        if cords[0] < 3: adjacent_cords.append((cords[0]+1, cords[1]))  # Move down
        if cords[0] > 0: adjacent_cords.append((cords[0]-1, cords[1]))  # Move up
        if cords[1] < 3: adjacent_cords.append((cords[0], cords[1]+1))  # Move right
        if cords[1] > 0: adjacent_cords.append((cords[0], cords[1]-1))  # Move left
        return adjacent_cords
    
    '''Returns a list of board configurations when swapping each adjacent tile (simulating board)'''
    def get_adjacent_board_configs(board):
        pass
    
    
    '''Helper function that checks if the board is solved
    Returns: Whether the board was solved (True if solved, False if not)'''
    def is_solved(board):
        return board == [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
    
    
    '''Calculates the optimal tree using A* Search
    Parameters: current board (2d list) and coordinates of blank space '''
    def calculate_path(self, board):
        open_list = []
        heapq.heappush(open_list, (0, board))  # Add starting board configuration with cost (0)
        parent = {}
        g_score = {board: 0}  # Cost from start to current board configuration
        f_score = {board: self.heuristic(board)}
        
        while open_list:
            open_list, current_board_config = heapq.heappop(open_list)  # Pop node with lowest code
           
            # Check if current state is the goal state
            if self.is_solved(current_board_config):
                # Return reconstructed optimal path
                return self.determine_optimal_path(parent, current_board_config)
                    
            # Get board configurations for adjacent tiles
            adjacent_board_configs = self.get_adjacent_board_configs(board)
            
            for adjacent_board_config in adjacent_board_configs:  # Long variable names because I am evil >:)
                temp_score = g_score[current_board_config] + self.movement_cost
                if adjacent_board_config not in g_score or temp_score < g_score[adjacent_board_config]:
                    parent[adjacent_board_config] = current_board_config
                    g_score[adjacent_board_config] = temp_score
                    f_score[adjacent_board_config] = temp_score + self.heuristic(adjacent_board_config)
                    # Push possible board configuration onto heap
                    heapq.heappush(open_list)
            
    
    ''' Finds the optimal path, given the parent dictionary and current board configuration '''
    def determine_optimal_path(self, parent, current_config):
        while current_config in parent:
            self.optimal_moves.append(current_config)
            current_config = parent[current_config]
        self.optimal_moves.reverse()