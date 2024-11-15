''' Class that uses A* Search to calculate the best overall path - JJ McCauley - 11/13/24 '''

from random import randint, shuffle
from time import sleep

import heapq

class puzzleSolver:
    
    ''' Initialize variables and final optimal path on create '''
    def __init__(self, m_cost = 1):
        self.move_counter = 0
        self.pop_counter = 0
        self.initial_board_config = None
        self.target_board: tuple[tuple] = ((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 0))
        self.visited = set()
        self.optimal_moves: list[int] = []  # List of 1-d representations for optimal moves
        self.movement_cost = m_cost  # Hardcoded movement cost (will always be 1 more than parent)
        self.moves = {
            0: [1, 4], 1: [0, 2, 5], 2: [1, 3, 6], 3: [2, 7],
            4: [0, 5, 8], 5: [1, 4, 6, 9], 6: [2, 5, 7, 10], 7: [3, 6, 11],
            8: [4, 9, 12], 9: [5, 8, 10, 13], 10: [6, 9, 11, 14], 11: [7, 10, 15],
            12: [8, 13], 13: [9, 12, 14], 14: [10, 13, 15], 15: [11, 14]
        }

        
    '''Calculates the Manhattan Distance of the provided board, also considering linear conflicts'''
    def heuristic(self, board: tuple) -> float:
        total_distance = 0
        conflicts = 0
        num_misplaced = 0
        for index, tile in enumerate(board):
            if tile == 0:
                continue
            target_i, target_j = divmod(tile - 1, 4)  # Get target i, j
            i, j = divmod(index, 4)
            total_distance += abs(target_i - i) + abs(target_j - j)  # Add the distance of each
            # Get the total number of misplacements
            if index != (target_i * 4 + target_j):
                num_misplaced += 1
            # Checking for and penalizing any linear conflicts (Removed to improve computational efficiency)
            # for row in range(4):
            #     tiles_in_cur_row = []
            #     for col in range(4):
            #         index = row * 4 + col
            #         tile = board[index]
            #         if tile == 0:
            #             continue
            #         target_i, target_j = divmod(tile - 1, 4)
            #         if target_i == row:
            #             tiles_in_cur_row.append((col, target_j))
            #     # Count linear conflicts in list
            #     for i in range(len(tiles_in_cur_row)):
            #         for j in range(i + 1, len(tiles_in_cur_row)):
            #             pos_i, target_i = tiles_in_cur_row[i]
            #             pos_j, target_j = tiles_in_cur_row[j]
            #             if target_i > target_j and pos_i < pos_j:
            #                 conflicts += 2
                    
        return (total_distance * 1.5) #+ (num_misplaced * .5)) #+ (conflicts * .5) 
    
    
    '''Returns a list of board configurations when swapping each adjacent tile (simulating board)'''
    def get_adjacent_board_config(self, board_t: tuple, move: int) -> tuple:
        b = board_t.index(0)  # Index of blank position
        new_board_config = list(board_t)
        new_board_config[b], new_board_config[move] = new_board_config[move], new_board_config[b]  # Swap blank & move
        return tuple(new_board_config)  # Return tuple of swapped indecies (hashable)
    
    '''Helper function that checks if the board is solved
    Returns: Whether the board was solved (True if solved, False if not)'''
    def is_solved(self, board: tuple) -> bool:
        return board == tuple(range(1, 16)) + (0,)
    
    
    '''Calculates the optimal tree using A* Search
    Parameters: current board (2d list) and coordinates of blank space '''
    def calculate_path(self, board: list[list]) -> None:
        iteration = 0 ##DEBUGGING
        board_t = tuple(board[i][j] for i in range(4) for j in range(4))  # Convert to flat, hashable tuple board
        self.initial_board_config = board_t
        open_list = []
        path = []
        visited = {board_t: 0}
        start_h = self.heuristic(board_t)
        heapq.heappush(open_list, (start_h, 0, start_h, board_t, path))  # Add starting board configuration
        
        while open_list:
            #sleep(.1)
            iteration += 1
            cur_f_cost, cur_g_cost, _, current_board_config, cur_path = heapq.heappop(open_list)  # Pop node with lowest code (tuple of tuples)
            blank_pos = current_board_config.index(0)
            print(f"Popping Iteration {iteration}, Cost: {cur_f_cost}, Board: {current_board_config}, Heap Size: {len(open_list)}")
        
            # Check is current configuration has already been visited
            if current_board_config in visited and cur_g_cost > visited[current_board_config]:
                continue  # Skip if already processed
        
            # Check if current state is the goal state
            if self.is_solved(current_board_config):
                print("-------------BOARD IS SOLVED!!!!!!!---------------------")
                self.optimal_moves = cur_path  # Assigning optimal path
                sleep(5000) ##TESTING PURPOSES PLEASE REMEMBER TO DELETE ELSE I WILL BE REALLY MAD LATER
                return
                    
            # Get board configurations for adjacent tiles
            for possible_move in self.moves[blank_pos]:
                new_board_config: tuple = self.get_adjacent_board_config(current_board_config, possible_move)
                new_g_cost = cur_g_cost + self.movement_cost  # Increment by 1
                new_h_cost = self.heuristic(new_board_config)
                new_f_cost = new_g_cost + new_h_cost  # F(n)=g(n)+h(n)
                
                # Record this movement if lower cost than previous
                if new_board_config not in visited or new_g_cost < visited[new_board_config]:
                    visited[new_board_config] = new_g_cost
                    heapq.heappush(open_list, (new_f_cost, new_g_cost, new_h_cost, new_board_config, path + [possible_move]))       
                             
        print("Done calculating path")
        
    
    ''' Chooses the next best move from the optimal path '''
    def get_move(self, board: list[list]) -> tuple[int, int]:
        # Ensure that the board has not changed since last iteration (expandable)
        board_t = tuple(board[i][j] for i in range(4) for j in range(4))
        if not self.optimal_moves:
            if self.is_solved(board):
                return (-1, -1)  # Signal values indicating won board
                
        last_board_config = self.optimal_moves.pop(0)
        if(board_t != last_board_config):
            # Calculate path for the next best working board
            self.move_counter = 0
            self.optimal_moves = []
            self.calculate_path(board)
        else:
            self.move_counter += 1
        # Get and return the index of the tile to swap with in next move
        next_board_config = self.optimal_moves.pop(0)
        blank_pos = next_board_config.index(0)
        next_move_i, next_move_j = divmod(blank_pos, 4)
        return next_move_i, next_move_j
    