# -*- coding: utf-8 -*-


class GameStatus:


	def __init__(self, board_state, turn_O):

		self.board_state = board_state
		self.turn_O = turn_O
		self.oldScores = 0

		self.winner = ""


	def is_terminal(self):
		"""
        YOUR CODE HERE TO CHECK IF ANY CELL IS EMPTY WITH THE VALUE 0. IF THERE IS NO EMPTY
        THEN YOU SHOULD ALSO RETURN THE WINNER OF THE GAME BY CHECKING THE SCORES FOR EACH PLAYER 
        """
		rows = len(self.board_state)
		cols = len(self.board_state[0])
		for r in range(rows):
			for c in range(cols):
				if self.board_state[r][c] == 0:
					return False
		scores = self.get_scores(True)
		if scores > 0:
			self.winner = "HUMAN"
		elif scores < 0:
			self.winner = "AI"
		else:
			self.winner = "DRAW"
		return True	

	def get_scores(self, terminal):
		"""
        YOUR CODE HERE TO CALCULATE THE SCORES. MAKE SURE YOU ADD THE SCORE FOR EACH PLAYER BY CHECKING 
        EACH TRIPLET IN THE BOARD IN EACH DIRECTION (HORIZONAL, VERTICAL, AND ANY DIAGONAL DIRECTION)
        
        YOU SHOULD THEN RETURN THE CALCULATED SCORE WHICH CAN BE POSITIVE (HUMAN PLAYER WINS),
        NEGATIVE (AI PLAYER WINS), OR 0 (DRAW)
        """        
		rows = len(self.board_state)
		cols = len(self.board_state[0])
		scores = 0
		check_point = 3 if terminal else 2

		for r in range(rows):
			for c in range(cols):
				if self.board_state[r][c] != 0:
					# Check horizontal
					if c + check_point < cols and all(self.board_state[r][k] == self.board_state[r][c] for k in range(c, c + check_point + 1)):
						scores += self.board_state[r][c]
					# Check vertical
					if r + check_point < rows and all(self.board_state[k][c] == self.board_state[r][c] for k in range(r, r + check_point + 1)):
						scores += self.board_state[r][c]
					# Check diagonal (top-left to bottom-right)
					if r + check_point < rows and c + check_point < cols and all(self.board_state[r + k][c + k] == self.board_state[r][c] for k in range(check_point + 1)):
						scores += self.board_state[r][c]
					# Check diagonal (top-right to bottom-left)
					if r + check_point < rows and c - check_point >= 0 and all(self.board_state[r + k][c - k] == self.board_state[r][c] for k in range(check_point + 1)):
						scores += self.board_state[r][c]
		return scores
	
	def get_negamax_scores(self, terminal):
		"""
        YOUR CODE HERE TO CALCULATE NEGAMAX SCORES. THIS FUNCTION SHOULD EXACTLY BE THE SAME OF GET_SCORES UNLESS
        YOU SET THE SCORE FOR NEGAMX TO A VALUE THAT IS NOT AN INCREMENT OF 1 (E.G., YOU CAN DO SCORES = SCORES + 100 
                                                                               FOR HUMAN PLAYER INSTEAD OF 
                                                                               SCORES = SCORES + 1)
        """
		rows = len(self.board_state)
		cols = len(self.board_state[0])
		scores = 0
		check_point = 3 if terminal else 2

		for r in range(rows):
			for c in range(cols):
				if self.board_state[r][c] != 0:
					# Check horizontal
					if c + check_point < cols and all(self.board_state[r][k] == self.board_state[r][c] for k in range(c, c + check_point + 1)):
						scores += 100 * self.board_state[r][c]
					# Check vertical
					if r + check_point < rows and all(self.board_state[k][c] == self.board_state[r][c] for k in range(r, r + check_point + 1)):
						scores += 100 * self.board_state[r][c]
					# Check diagonal (top-left to bottom-right)
					if r + check_point < rows and c + check_point < cols and all(self.board_state[r + k][c + k] == self.board_state[r][c] for k in range(check_point + 1)):
						scores += 100 * self.board_state[r][c]
					# Check diagonal (top-right to bottom-left)
					if r + check_point < rows and c - check_point >= 0 and all(self.board_state[r + k][c - k] == self.board_state[r][c] for k in range(check_point + 1)):
						scores += 100 * self.board_state[r][c]
		return scores

	def get_moves(self):
		moves = []
		"""
        YOUR CODE HERE TO ADD ALL THE NON EMPTY CELLS TO MOVES VARIABLES AND RETURN IT TO BE USE BY YOUR
        MINIMAX OR NEGAMAX FUNCTIONS
        """
		# Get the dimensions of your board
		rows = len(self.board_state)
		cols = len(self.board_state[0])	
		# Iterate through every cell in the board
		for r in range(rows):
			for c in range(cols):
				# Check if the cell is empty (value is 0)
				if self.board_state[r][c] == 0:
					# If empty, add this (row, column) coordinate to the list
					moves.append((r, c))

		return moves

	def get_new_state(self, move):
		new_board_state = self.board_state.copy()
		x, y = move[0], move[1]
		new_board_state[x,y] = 1 if self.turn_O else -1
		return GameStatus(new_board_state, not self.turn_O)
