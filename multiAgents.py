from GameStatus_5120 import GameStatus


def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):
	# Checks if game is over 
    terminal = game_state.is_terminal()
	# if the game is not over it gets new scores
    if (depth==0) or (terminal):
        newScores = game_state.get_scores(terminal)
        return newScores, None

	# initalizing moves with the current moves on the board 
	# Gets what actions are avilable on the current state of the board
    moves = game_state.get_moves()
	# Set best_moves to None Always before a new turn 
    best_moves = None 
		
 

    if (maximizingPlayer == True):
		# Pick the Highest Value 
        value = float('-inf')
        for move in moves: 
			# Updates Child state with the new move from the game_state 
            child_state = game_state.get_new_state(move)
			# Recusively Call minimax 
            child_value, child_move = minimax(child_state, depth -1, False, alpha, beta)
			# if the child value is greater than the value then we must update the values
            if child_value > value: 
                value = child_value
                best_moves = move
				
            # Update alpha with the max alpha from the tree
            alpha = max(alpha, value) 
			# prune the rest of the tree if alpha is greater than beta
            if alpha >= beta:
                break
		# return the values for the maximizing player 
        return value, best_moves

    else: 
        value = float('inf')
        for move in moves: 
            child_state = game_state.get_new_state(move)
            child_value, child_move = minimax(child_state, depth - 1, True, alpha, beta)
			# MAIN diff minimize if value is greater than child_value then updated value, best_moves
            if child_value < value: 
                value = child_value
                best_moves = move 
			# Update beta with the mini value
            beta = min(beta, value) 
			# Prune the rest of the branch
            if alpha >= beta:
                break
			
        return value, best_moves
	



        # Pick lowest Value 
		# Updated Beta 

    # This will get the values from max_value, mini_value then 
    # minimax will determine which move is the best. Based on the value returned 

	

def negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
	# Checking if game is over
    terminal = game_status.is_terminal()

    # If game is over or depth is reached then return score at node
    if (depth==0) or (terminal):
		# Get score of node
        scores = game_status.get_negamax_scores(terminal)
        # Convert to current  player's perspective i.e either human or opponent
        scores = scores * turn_multiplier
        # Return score of node, no move needed it is leaf node
        return scores, None

    # Get a list of legal moves available
    moves = game_status.get_moves()
    # Set best value seen so far as -inf
    value = float('-inf')
    # Initialize best_move variable for correct node path can be stored back to root
    best_move = None

    # Beginning loop through available moves
    for move in moves:
        # Get child avaiable moves
        child_status = game_status.get_new_state(move)
        # Switch the turn for the child node (alternate player)
        child_multiplier = -turn_multiplier
        # Recursively call negamax to explore all child paths
        child_value, child_move = negamax(child_status, depth-1, child_multiplier, -beta, -alpha)
        # Flip current value to reflect current player perspective
        child_value = -child_value
        # Check if the best value found so far is less than current child value
        if (value < child_value):
            value = child_value
            best_move = move
        # Raise alpha if we found a better value
        alpha = max(alpha, value)
        # If condition is true prune all other children nodes on this path and return to parent node
        if (alpha >= beta):
            return (value, best_move)
            
    # Return the best score and move found      
    return value, best_move