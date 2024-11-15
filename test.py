from puzzleSolver import puzzleSolver

solver = puzzleSolver()

# Define a sample 2D board
board = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 15, 14, 0]
]

# Call the calculate_path method
solver.calculate_path(board)
print("Optimal Moves: ", solver.optimal_moves)
