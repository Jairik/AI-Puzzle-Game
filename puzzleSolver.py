''' Class that uses A* Search to calculate the best overall path - JJ McCauley - 11/13/24 '''

from random import randint, shuffle
from time import sleep

import heapq

class puzzleSolver:
    
    ''' Initialize variables and final optimal path on create '''
    def __init__(self, m_cost = 1):
        self.move_counter = 0
        self.target_board: tuple[tuple] = ((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 0))
        self.visited = set()
        self.lastmove = None
        self.optimal_moves = []  # List of 
        self.movement_cost = m_cost  # Hardcoded movement cost (will always be 1 more than parent)
        
    '''Calculates the scaled Manhattan Distance of the provided board, also considering linear conflicts'''
    def heuristic(self, board) -> float:
        total_distance = 0
        for i in range(4):
            for j in range(4):
                tile = board[i][j]
                target_i, target_j = divmod(tile - 1, 4)  # Get target i, j
                total_distance += abs(target_i - i) + abs(target_j - j)  # Add the distance of each
                # Checking for and penalizing any linear conflicts (Removed to improve computational efficiency)
                # if target_i == i:  # Linear conflicts in row
                #     for k in range(j+1, 4):  # Checking all tiles to the right
                #         other_tile = board[i][k]
                #         if other_tile != 0:  # Skipping blank space
                #             target_i_other = (other_tile-1) // 4  # Calculating target row of other tile
                #             # Check if other tile belongs in same row and is above it when it should be below, 
                #             # Essentially blocking the other tile
                #             if target_i_other == i and other_tile < tile:
                #                 total_distance += 1  # Small penalty
                # if target_j == j:  # Linear conflicts in column
                #     for k in range(i+1, 4):  # Checking all tiles below
                #         other_tile = board[k][j]
                #         if other_tile != 0:
                #             target_j_other = (other_tile-1) % 4  # Calculating target column of other tile
                #             # Check if other tile is 'blocking' current tile
                #             if target_j_other == j and other_tile < tile:
                #                 total_distance += 1  # Small penalty
        return total_distance #* 1.5 # Scaling heuristic
    
    
    '''Gets Adjancent from provided blankspace
    Helper for A* Search, return a list of tuples of adjacent tiles'''
    def get_adjacent_tiles(self, cords: tuple) -> list[tuple]:
        adjacent_cords = []
        if cords[0] < 3: adjacent_cords.append((cords[0]+1, cords[1]))  # Move down
        if cords[0] > 0: adjacent_cords.append((cords[0]-1, cords[1]))  # Move up
        if cords[1] < 3: adjacent_cords.append((cords[0], cords[1]+1))  # Move right
        if cords[1] > 0: adjacent_cords.append((cords[0], cords[1]-1))  # Move left
        return adjacent_cords
    
    
    '''Returns a list of board configurations when swapping each adjacent tile (simulating board)'''
    def get_adjacent_board_configs(self, board_t: tuple[tuple]) -> tuple[tuple]:
        adjacent_boards = []  # Hold the board configurations of adjacent boards
        blank_pos = self.find_blank(board_t)
        adjacent_tile_coordinates: list[tuple] = self.get_adjacent_tiles(blank_pos)
        # Simulate each board shift
        for pos in adjacent_tile_coordinates:
            board_l = [list(row) for row in board_t]  # Convert tuple to list
            simulated_board = [row[:] for row in board_l]  # Deep copy of board list
             # Swap given indexes on temporary board
            simulated_board[blank_pos[0]][blank_pos[1]], simulated_board[pos[0]][pos[1]] = \
            simulated_board[pos[0]][pos[1]], simulated_board[blank_pos[0]][blank_pos[1]]
            simulated_board_t = tuple(tuple(row) for row in simulated_board)  # Convert back to hashable tuple of tuples
            adjacent_boards.append(simulated_board_t)
        return adjacent_boards
    
    
    '''Helper function that checks if the board is solved
    Returns: Whether the board was solved (True if solved, False if not)'''
    def is_solved(self, board) -> bool:
        goal_state = ((1, 2, 3, 4),
                  (5, 6, 7, 8),
                  (9, 10, 11, 12),
                  (13, 14, 15, 0))
        return board == goal_state
    
    
    '''Helper function that returns the index position of the blank'''
    def find_blank(self, board: tuple[tuple]) -> tuple:
        for i in range(4):
            for j in range(4):
                if board[i][j] == 0:
                    return (i, j)
        return None  # Should never happen
    
    
    '''Calculates the optimal tree using A* Search
    Parameters: current board (2d list) and coordinates of blank space '''
    def calculate_path(self, board: list[list]) -> None:
        iteration = 0 ##DEBUGGING
        board_t = tuple(tuple(row) for row in board)  # Convert to tuple of tuples
        open_list = []
        parent = {}
        g_score = {board_t: 0}  # Cost of start configuration
        f_score = {board_t: self.heuristic(board)}
        visited = set()
        #open_set = {board_t}
        heapq.heappush(open_list, (f_score[board_t], g_score[board_t], board_t))  # Add starting board configuration
        
        while open_list:
            #sleep(5)
            iteration += 1
            cur_f_score, cur_g_score, current_board_config = heapq.heappop(open_list)  # Pop node with lowest code (tuple of tuples)
        
            # Check is current configuration has already been visited
            if current_board_config in visited:
                continue  # Skip if already processed
            visited.add(current_board_config)
            print("Board config visited, iteration ", iteration, ": ", current_board_config, " cost: ", cur_f_score)
        
            # Check if current state is the goal state
            if self.is_solved(current_board_config):
                print("-------------BOARD IS SOLVED!!!!!!!---------------------")
                # Return reconstructed optimal path
                self.determine_optimal_path(parent, current_board_config)  
                return
                    
            # Get board configurations for adjacent tiles
            adjacent_board_configs = self.get_adjacent_board_configs(current_board_config)
            for adjacent_board_config in adjacent_board_configs:  # Long variable names because I am evil >:)
                # Check is the configuration has already been visited
                if adjacent_board_config in visited:
                    continue
                # Calculate the g(n) and f(n) for current board configuration
                temp_g_score = g_score[current_board_config] + self.movement_cost
                temp_f_score = temp_g_score + self.heuristic(adjacent_board_config)
                # Record this movement if lower cost than 
                if temp_g_score < g_score.get(adjacent_board_config, float('inf')):
                    parent[adjacent_board_config] = current_board_config
                    g_score[adjacent_board_config] = temp_g_score
                    f_score[adjacent_board_config] = temp_f_score
                    print(f"\tConfig pushed onto heap with {temp_f_score} cost")
                    heapq.heappush(open_list, (temp_f_score, temp_g_score, adjacent_board_config))
                
        print("Done calculating path")
            
    
    ''' Assigns the optimal path, given the parent dictionary and current board configuration '''
    def determine_optimal_path(self, parent, current_config) -> None:
        while current_config in parent:
            self.optimal_moves.append(current_config)
            current_config = parent[current_config]
        self.optimal_moves.reverse()
        
    
    ''' Chooses the next best move from the optimal path '''
    def get_move(self, board) -> tuple[int, int]:
        # Ensure that the board has not changed since last iteration (expandable)
        if not self.optimal_moves:
            if self.is_solved(board):
                return (-1, -1)  # Signal values indicating won board
                
        last_board_config = self.optimal_moves.pop(0)
        board = tuple(tuple(row) for row in board)  # Convert to hashable object
        if(board != last_board_config):
            # Calculate path for the next best working board
            self.move_counter = 0
            self.optimal_moves = []
            self.calculate_path(board)
        else:
            self.move_counter += 1
        # Get and return the index of the tile to swap with in next move
        next_swap_pos = self.find_blank(self.optimal_moves[0])
        return next_swap_pos[0], next_swap_pos[1]
    