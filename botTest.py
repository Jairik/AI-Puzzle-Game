from bot import bot

b_pos = (2, 2)  # Hardcoded for test case
bot = bot()  # Make a new bot object

def run_bot(board, moves_label):    
    global b_pos
    
    # Define a function for each iteration of the bot's movement
    def bot_iteration(board):
        global b_pos
        #print("\n\nExecuting Bot Iteration #", move_count)
        print("Original Board: ", board, "\n")
        # Get the optimal move from the bot. Will update board within function (by reference)
        b_pos, board = bot.make_next_move(board, b_pos)
        print("Blank position After Make_Next_Move function: ", b_pos)
        print("New board: ", board, "\n")
        
        # Check if board is solved for easier testing
        if(board == [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]):
            print("--- BOARD IS SOLVED!!! ---")
            return
        
        # Increment move counter and update the GUI
        #move_count += 1
        #moves_label.setText(f"Moves Made: {move_count}")
        temp = input("\nEnter any character to continue...")
        print()  # Empty line
        bot_iteration(board)
        
    # Start the bot iteration
    bot_iteration(board)
    
    
'''Testing logic'''
board = [[4, 2, 3, 1], 
         [5, 6, 7, 8], 
         [9, 10, 0, 12], 
         [13, 14, 11, 15]]  # Hardcoded test case
run_bot(board, None)