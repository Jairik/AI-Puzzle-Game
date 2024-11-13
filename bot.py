''' Class that holds AI functionality - JJ McCauley - 11/7/24 '''

import numpy as np  # Board calculations
from random import randint, shuffle
import heapq

class bot:
    
    ''' Initialize variables on create '''
    def __init__(self):
        self.total_cost = 0
        self.visited = set()
        self.lastmove = None
        
        
    '''Calculates and returns the distance to the nearest misplaced tile.
    Acts almost as a second heuristic function, enticing the selection of 
    tiles that closer to misplaced tiles.'''
    def get_min_dist_to_misplaced(self, board, pos: tuple):
        min_distance = 999  # Signal value
        for i in range(4):
            for j in range(4):
                tile = board[i][j]
                if tile != 0:  # Skip blank tile
                    target_i, target_j = divmod(tile-1, 4)  # Getting target i, j
                    # Check if tile is misplaced
                    if(i, j) != (target_i, target_j):
                        # Calculate manhattan distance from pos 
                        distance_from_current = abs(pos[0] - i) + abs(pos[1] - j)
                        # Update the minimum distance if current distance is smaller
                        if(distance_from_current < min_distance):
                            min_distance = distance_from_current 
        if min_distance == 999: min_distance = 0  # Winning move
        return min_distance
        
        
    '''Calculates heuristic function based on Manhattan Distance'''
    def heuristic(self, board):
        total_distance = 0
        for i in range(4):
            for j in range(4):
                tile = board[i][j]
                if tile != 0:
                    target_i, target_j = divmod(tile - 1, 4)  # Get target i, j
                    total_distance += abs(target_i - i) + abs(target_j - j)  # Add the distance of each
                    
                    # Adding forward weight penalty to tiles not at goal state
                    if i != target_i and j != target_j:
                        total_distance += 1  # Adding forward weight as penalty
                    
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
                    
        return total_distance
    
    
    '''Gets Adjancent from provided blankspace
    Helper for A* Search, return a list of tuples of adjacent tiles'''
    def get_adjacent(self, cords: tuple):
        adjacent_cords = []
        if cords[0] < 3: adjacent_cords.append((cords[0]+1, cords[1]))  # Move down
        if cords[0] > 0: adjacent_cords.append((cords[0]-1, cords[1]))  # Move up
        if cords[1] < 3: adjacent_cords.append((cords[0], cords[1]+1))  # Move right
        if cords[1] > 0: adjacent_cords.append((cords[0], cords[1]-1))  # Move left
        return adjacent_cords
    
    
    '''Calculates next move using A* Search, returning the new blank space and the updated board
    Parameters: current board (2d list) and coordinates of blank space '''
    def make_next_move(self, board, cords: tuple):
        
        adjacent_cords = self.get_adjacent(cords)  # Get list of tuples of adjacent tiles
        print("Blank Position: ", cords)
        print("Adjacent Tiles: ", adjacent_cords)
        self.total_cost+= 1
        moves = []  # Store the avaialble moves that have not yet been visited
        board_tuple = None  # Initialize to avoid comparison errors
        
        # Simulate the cost of each movement
        for pos in adjacent_cords:
            if(pos == self.lastmove):  # Avoid revisiting the direct last move
                continue  # Move onto next iteration
            
            simulated_board = [row[:] for row in board]  # Deep copy
            x_blank, y_blank = cords
                        
            # Swap given indexes on temporary board
            simulated_board[x_blank][y_blank], simulated_board[pos[0]][pos[1]] = \
            simulated_board[pos[0]][pos[1]], simulated_board[x_blank][y_blank]
            
            # Check to see if state has already been visited
            simulated_board_tuple = tuple(tuple(row) for row in simulated_board)  # Convert to hashable object
            if simulated_board_tuple in self.visited: 
                continue  # Skip and move onto next iteration
            
            # Calculate costs and add to adjacent_cord_costs
            hCost = self.heuristic(simulated_board)# Get heuristic cost
            cur_cost = (hCost + 1)
            moves.append((cur_cost, pos, simulated_board, simulated_board_tuple))

        # If moves is not empty, choose the best one
        if moves != []:
            # Get minimum cost
            shuffle(moves)  # Avoid algorithm picking the first one in list, if all costs are same
            min_cost = min(moves, key=lambda x: x[0])[0]
            best_moves = [move for move in moves if move[0] == min_cost]
            
            # If same costs, select move that won't go back to last state
            for move in best_moves:
                if move[1] != self.lastmove:
                    selected_move = move
                    break
                else:
                    selected_move = best_moves[0]
            cost, (min_i, min_j), new_board, board_tuple = selected_move 
        # If moves is empty, select a random adjacent tile to swap with
        else:
            print("SELECTING RANDOM TILE")
            random_tile_index = randint(0, len(adjacent_cords)-1)
            random_tile = adjacent_cords[random_tile_index]
            # Calculate cost of tile
            simulated_board = [row[:] for row in board]  # Deep copy of board
            x_blank, y_blank = cords 
            simulated_board[x_blank][y_blank], simulated_board[random_tile[0]][random_tile[1]] = \
            simulated_board[random_tile[0]][random_tile[1]], simulated_board[x_blank][y_blank]
            hCost = self.heuristic(simulated_board)  # Get heuristic cost
            cost = (hCost + 1)
            min_i, min_j, new_board = random_tile[0], random_tile[1], simulated_board
        
        # Swap coordinates on the actual board
        board[:] = new_board[:]  # Deep copy board

        # Add current board to visited set, if new configuration
        if board_tuple:
            self.visited.add(board_tuple)
        
        # Return swapped indexes and updated board
        print("Min i,j: ", min_i, ",", min_j, "  -  WITH COST OF: ", cost)
        print("Moves: ", moves)
        print("Visited: ", self.visited)
        self.lastmove = (x_blank, y_blank)
        return (min_i, min_j), board