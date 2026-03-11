"""
PLEASE READ THE COMMENTS BELOW AND THE HOMEWORK DESCRIPTION VERY CAREFULLY BEFORE YOU START CODING

 The file where you will need to create the GUI which should include (i) drawing the grid, (ii) call your Minimax/Negamax functions
 at each step of the game, (iii) allowing the controls on the GUI to be managed (e.g., setting board size, using 
                                                                                 Minimax or Negamax, and other options)
 In the example below, grid creation is supported using pygame which you can use. You are free to use any other 
 library to create better looking GUI with more control. In the __init__ function, GRID_SIZE (Line number 36) is the variable that
 sets the size of the grid. Once you have the Minimax code written in multiAgents.py file, it is recommended to test
 your algorithm (with alpha-beta pruning) on a 3x3 GRID_SIZE to see if the computer always tries for a draw and does 
 not let you win the game. Here is a video tutorial for using pygame to create grids http://youtu.be/mdTeqiWyFnc
 
 
 PLEASE CAREFULLY SEE THE PORTIONS OF THE CODE/FUNCTIONS WHERE IT INDICATES "YOUR CODE BELOW" TO COMPLETE THE SECTIONS
 
"""
import pygame
import numpy as np
from GameStatus_5120 import GameStatus
from multiAgents import minimax, negamax
import sys, random

mode = "player_vs_ai" # default mode for playing the game (player vs AI)

# Layout constants
PANEL_HEIGHT = 180
BOARD_SIZE = 600

class RandomBoardTicTacToe:
    def __init__(self, size = (600, 600)):

        self.size = self.width, self.height = size
        # Define some colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        # Extra colors for symbols
        self.CIRCLE_COLOR = (140, 146, 172)
        self.CROSS_COLOR = (140, 146, 172)

        # Grid Size
        self.GRID_SIZE = 4
        self.GRID_ROWS = 4
        self.GRID_COLS = 4
        self.OFFSET = 5
    

        # This sets the width and height of each grid location
        self.WIDTH = self.size[0]/self.GRID_COLS - self.OFFSET
        self.HEIGHT = self.size[1]/self.GRID_ROWS - self.OFFSET

        # This sets the margin between each cell
        self.MARGIN = 5

        # Game settings
        self.human_symbol = "X"
        self.ai_symbol = "O"
        self.use_negamax = False
        self.game_mode = "player_vs_ai"
        self.winner_text = ""
        self.human_score = 0
        self.ai_score = 0
        self.game_started = False

        # Settings input state
        self.size_text = "3"
        self.active_input = None

        # Initialize pygame
        pygame.init()
        self.font = pygame.font.SysFont("Inter", 16)
        self.font_small = pygame.font.SysFont("Inter", 14)
        self.font_large = pygame.font.SysFont("Inter", 20, bold=True)

        # Define clickable button areas for settings panel
        self.nought_btn = pygame.Rect(15, 60, 130, 22)
        self.cross_btn = pygame.Rect(15, 88, 120, 22)
        self.hvh_btn = pygame.Rect(15, 123, 160, 22)
        self.hvc_btn = pygame.Rect(15, 151, 170, 22)
        self.minimax_btn = pygame.Rect(200, 123, 110, 22)
        self.negamax_btn = pygame.Rect(200, 151, 110, 22)
        self.size_box = pygame.Rect(420, 68, 45, 24)
        self.start_btn = pygame.Rect(380, 135, 140, 35)

        self.game_reset()

    def recalculate_sizes(self):
        self.WIDTH = BOARD_SIZE / self.GRID_SIZE - self.OFFSET
        self.HEIGHT = BOARD_SIZE / self.GRID_SIZE - self.OFFSET
        total_height = PANEL_HEIGHT + BOARD_SIZE
        self.size = self.width, self.height = (BOARD_SIZE, total_height)

    def draw_panel(self):
        # Draw white settings panel at top of window
        pygame.draw.rect(self.screen, self.WHITE, (0, 0, BOARD_SIZE, PANEL_HEIGHT))
        pygame.draw.rect(self.screen, self.BLACK, (0, 0, BOARD_SIZE, PANEL_HEIGHT), 2)

        # Title
        self.screen.blit(self.font_large.render("Tic-Tac-Toe", True, self.BLACK), (10, 8))
        pygame.draw.line(self.screen, self.WHITE, (5, 30), (BOARD_SIZE - 5, 30), 1)

        # Symbol selection label
        p1_label = "human player" if self.game_mode == "player_vs_ai" else "Player 1"
        self.screen.blit(self.font.render("Select " + p1_label + " symbol", True, self.BLACK), (15, 40))

        # Radius of the radio buttons
        radio_r = 7

        # Nought (O) radio
        pygame.draw.circle(self.screen, self.BLACK, (self.nought_btn.x + radio_r, self.nought_btn.centery), radio_r)
        if self.human_symbol == "O":
            pygame.draw.circle(self.screen, self.GREEN, (self.nought_btn.x + radio_r, self.nought_btn.centery), 3)
        self.screen.blit(self.font_small.render("Nought (O)", True, self.BLACK), (self.nought_btn.x + 20, self.nought_btn.y + 2))

        # Cross (X) radio
        pygame.draw.circle(self.screen, self.BLACK, (self.cross_btn.x + radio_r, self.cross_btn.centery), radio_r)
        if self.human_symbol == "X":
            pygame.draw.circle(self.screen, self.GREEN, (self.cross_btn.x + radio_r, self.cross_btn.centery), 3)
        self.screen.blit(self.font_small.render("Cross (X)", True, self.BLACK), (self.cross_btn.x + 20, self.cross_btn.y + 2))

        # Board size input (single square dimension, min 3)
        self.screen.blit(self.font.render("Board size:", True, self.BLACK), (330, 45))
        self.screen.blit(self.font_small.render("Size (NxN):", True, self.BLACK), (340, 72))
        pygame.draw.rect(self.screen, self.GREEN if self.active_input == "size" else self.BLACK, self.size_box, 2)
        self.screen.blit(self.font_small.render(self.size_text, True, self.BLACK), (self.size_box.x + 5, self.size_box.y + 4))
        self.screen.blit(self.font_small.render("(min 3, max 10)", True, self.BLACK), (475, 72))

        # Scores
        p1_label = "P1" if self.game_mode == "player_vs_player" else "You"
        p2_label = "P2" if self.game_mode == "player_vs_player" else "AI"
        self.screen.blit(self.font_small.render(p1_label + ": " + str(self.human_score) + "  |  " + p2_label + ": " + str(self.ai_score), True, self.BLACK), (310, 118))

        # Human vs human radio
        pygame.draw.circle(self.screen, self.BLACK, (self.hvh_btn.x + radio_r, self.hvh_btn.centery), radio_r)
        if self.game_mode == "player_vs_player":
            pygame.draw.circle(self.screen, self.GREEN, (self.hvh_btn.x + radio_r, self.hvh_btn.centery), 3)
        self.screen.blit(self.font_small.render("Human vs human", True, self.BLACK), (self.hvh_btn.x + 20, self.hvh_btn.y + 2))

        # Human vs computer radio
        pygame.draw.circle(self.screen, self.BLACK, (self.hvc_btn.x + radio_r, self.hvc_btn.centery), radio_r)
        if self.game_mode == "player_vs_ai":
            pygame.draw.circle(self.screen, self.GREEN, (self.hvc_btn.x + radio_r, self.hvc_btn.centery), 3)
        self.screen.blit(self.font_small.render("Human vs computer", True, self.BLACK), (self.hvc_btn.x + 20, self.hvc_btn.y + 2))

        # Minimax radio
        pygame.draw.circle(self.screen, self.BLACK, (self.minimax_btn.x + radio_r, self.minimax_btn.centery), radio_r)
        if not self.use_negamax:
            pygame.draw.circle(self.screen, self.GREEN, (self.minimax_btn.x + radio_r, self.minimax_btn.centery), 3)
        self.screen.blit(self.font_small.render("Minimax", True, self.BLACK), (self.minimax_btn.x + 20, self.minimax_btn.y + 2))

        # Negamax radio
        pygame.draw.circle(self.screen, self.BLACK, (self.negamax_btn.x + radio_r, self.negamax_btn.centery), radio_r)
        if self.use_negamax:
            pygame.draw.circle(self.screen, self.GREEN, (self.negamax_btn.x + radio_r, self.negamax_btn.centery), 3)
        self.screen.blit(self.font_small.render("Negamax", True, self.BLACK), (self.negamax_btn.x + 20, self.negamax_btn.y + 2))

        # Start / Reset button
        btn_label = "Start game" if not self.game_started else "Reset"
        pygame.draw.rect(self.screen, self.BLACK, self.start_btn)
        text_surf = self.font.render(btn_label, True, self.WHITE)
        text_x = self.start_btn.x + (self.start_btn.width - text_surf.get_width()) // 2
        self.screen.blit(text_surf, (text_x, self.start_btn.y + 7))

    def handle_panel_click(self, mx, my):
        # Only allow settings changes before game starts
        if not self.game_started:
            if self.nought_btn.collidepoint(mx, my):
                self.human_symbol = "O"
                self.ai_symbol = "X"
            elif self.cross_btn.collidepoint(mx, my):
                self.human_symbol = "X"
                self.ai_symbol = "O"
            elif self.hvh_btn.collidepoint(mx, my):
                self.game_mode = "player_vs_player"
            elif self.hvc_btn.collidepoint(mx, my):
                self.game_mode = "player_vs_ai"
            elif self.minimax_btn.collidepoint(mx, my):
                self.use_negamax = False
            elif self.negamax_btn.collidepoint(mx, my):
                self.use_negamax = True
            elif self.size_box.collidepoint(mx, my):
                self.active_input = "size"
            elif self.start_btn.collidepoint(mx, my):
                self.apply_settings_and_start()
        else:
            # Game already started, button acts as reset
            if self.start_btn.collidepoint(mx, my):
                self.game_started = False
                self.game_over = False
                self.winner_text = ""

    def handle_panel_key(self, event):
        if self.game_started or self.active_input is None:
            return
        if event.key == pygame.K_BACKSPACE:
            self.size_text = self.size_text[:-1]
        elif event.unicode.isdigit() and len(self.size_text) < 2:
            self.size_text += event.unicode
        # Redraw panel immediately so the input box updates in real time
        self.draw_panel()
        pygame.display.update()

    def apply_settings_and_start(self):

        # Restrict board size to >=3 and <=10
        try:
            n = int(self.size_text) if self.size_text else 3
            n = max(3, min(n, 10))
        except ValueError:
            n = 3
        self.GRID_SIZE = n
        self.GRID_ROWS = n
        self.GRID_COLS = n
        self.size_text = str(n)
        self.recalculate_sizes()
        self.game_started = True
        self.game_reset()

    def draw_game(self):
        # Create a 2 dimensional array using the column and row variables
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Tic Tac Toe Random Grid")
        self.screen.fill(self.BLACK)
        # Draw the grid
        
        """
        YOUR CODE HERE TO DRAW THE GRID OTHER CONTROLS AS PART OF THE GUI
        """

        # Draw rects per row, then by column based on variable dimensions
        # Grid is offset by PANEL_HEIGHT so it draws below the settings panel
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                x = (self.MARGIN + self.WIDTH) * col + self.MARGIN
                y = PANEL_HEIGHT + (self.MARGIN + self.HEIGHT) * row + self.MARGIN
                pygame.draw.rect(self.screen, self.WHITE, [x, y, self.WIDTH, self.HEIGHT])

        # Draw settings panel on top
        self.draw_panel()
        
        pygame.display.update()

    def change_turn(self):

        if(self.game_state.turn_O):
            pygame.display.set_caption(f"Tic Tac Toe - {self.human_symbol}'s turn")
        else:
            pygame.display.set_caption(f"Tic Tac Toe - {self.ai_symbol}'s turn")


    def draw_circle(self, x, y):
        """
        YOUR CODE HERE TO DRAW THE CIRCLE FOR THE NOUGHTS PLAYER
        """

        # Draw circle at center of cell, offset by PANEL_HEIGHT
        cx = int((self.MARGIN + self.WIDTH) * y + self.MARGIN + self.WIDTH // 2)
        cy = int(PANEL_HEIGHT + (self.MARGIN + self.HEIGHT) * x + self.MARGIN + self.HEIGHT // 2)
        radius = int(min(self.WIDTH, self.HEIGHT) // 2 - 10)
        pygame.draw.circle(self.screen, self.CIRCLE_COLOR, (cx, cy), radius, 4)
        pygame.display.update()
        

    def draw_cross(self, x, y):
        """
        YOUR CODE HERE TO DRAW THE CROSS FOR THE CROSS PLAYER AT THE CELL THAT IS SELECTED VIA THE gui
        """

        # Draw cross at center of cell, offset by PANEL_HEIGHT and with padding
        padding = 10

        x0 = int((self.MARGIN + self.WIDTH) * y + self.MARGIN + padding)
        x1 = int((self.MARGIN + self.WIDTH) * y + self.MARGIN + self.WIDTH - padding)

        y0 = int(PANEL_HEIGHT + (self.MARGIN + self.HEIGHT) * x + self.MARGIN + padding)
        y1 = int(PANEL_HEIGHT + (self.MARGIN + self.HEIGHT) * x + self.MARGIN + self.HEIGHT - padding)

        pygame.draw.line(self.screen, self.CROSS_COLOR, (x0, y0), (x1, y1), 4)
        pygame.draw.line(self.screen, self.CROSS_COLOR, (x1, y0), (x0, y1), 4)
        pygame.display.update()
        

    def is_game_over(self):

        """
        YOUR CODE HERE TO SEE IF THE GAME HAS TERMINATED AFTER MAKING A MOVE. YOU SHOULD USE THE IS_TERMINAL()
        FUNCTION FROM GAMESTATUS_5120.PY FILE (YOU WILL FIRST NEED TO COMPLETE IS_TERMINAL() FUNCTION)
        
        YOUR RETURN VALUE SHOULD BE TRUE OR FALSE TO BE USED IN OTHER PARTS OF THE GAME
        """
        return self.game_state.is_terminal()

    # Score update and overlay helper functions for UI behavior, added for functionality outside of defined requirements 
    def update_scores(self):
        """Recalculate live triplet scores from the current board state."""
        scores = self.game_state.get_scores(True)
        # Positive score = P1/human triplets dominate, negative = P2/AI
        # Count individual triplets for each side
        self.human_score = max(0, int(scores))
        self.ai_score = max(0, int(-scores))

    def draw_overlay(self, message):
        """Draw a semi-transparent overlay with a message over the board."""
        overlay = pygame.Surface((BOARD_SIZE, BOARD_SIZE), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, PANEL_HEIGHT))

        font_overlay = pygame.font.SysFont("Inter", 48, bold=True)
        text_surf = font_overlay.render(message, True, self.WHITE)
        text_x = (BOARD_SIZE - text_surf.get_width()) // 2
        text_y = PANEL_HEIGHT + (BOARD_SIZE - text_surf.get_height()) // 2
        self.screen.blit(text_surf, (text_x, text_y))

        hint_surf = self.font_small.render("Press Reset to play again", True, (200, 200, 200))
        hint_x = (BOARD_SIZE - hint_surf.get_width()) // 2
        self.screen.blit(hint_surf, (hint_x, text_y + 60))

        pygame.display.update()
    

    def move(self, move):
        self.game_state = self.game_state.get_new_state(move)


    def play_ai(self):
        """
        YOUR CODE HERE TO CALL MINIMAX OR NEGAMAX DEPENDEING ON WHICH ALGORITHM SELECTED FROM THE GUI
        ONCE THE ALGORITHM RETURNS THE BEST MOVE TO BE SELECTED, YOU SHOULD DRAW THE NOUGHT (OR CIRCLE DEPENDING
        ON WHICH SYMBOL YOU SELECTED FOR THE AI PLAYER)
        
        THE RETURN VALUES FROM YOUR MINIMAX/NEGAMAX ALGORITHM SHOULD BE THE SCORE, MOVE WHERE SCORE IS AN INTEGER
        NUMBER AND MOVE IS AN X,Y LOCATION RETURNED BY THE AGENT
        """
        # Full-depth search for 3x3; cap depth for larger boards to avoid freezing
        if self.GRID_SIZE <= 3:
            depth = self.GRID_SIZE * self.GRID_SIZE
        else:
            depth = 4

        if self.use_negamax:
            turn_multiplier = 1 if self.game_state.turn_O else -1
            score, best_move = negamax(self.game_state, depth, turn_multiplier)
        else:
            score, best_move = minimax(self.game_state, depth, False)

        if best_move is not None:
            self.move(best_move)
            if self.ai_symbol == "O":
                self.draw_circle(best_move[0], best_move[1])
            else:
                self.draw_cross(best_move[0], best_move[1])

        # Update live triplet scores after AI move
        self.update_scores()
        self.draw_panel()
        self.change_turn()

        pygame.display.update()
        terminal = self.game_state.is_terminal()
        """ USE self.game_state.get_scores(terminal) HERE TO COMPUTE AND DISPLAY THE FINAL SCORES """
        if terminal:
            scores = self.game_state.get_scores(terminal)

            if scores > 0:
                self.winner_text = "Human wins! Score:" + str(scores)
            elif scores < 0:
                self.winner_text = "AI wins! Score:" + str(scores)
            else:
                self.winner_text = "Draw! Score:" + str(scores)
            print(self.winner_text)

            self.draw_overlay(self.winner_text)



    def game_reset(self):
        self.draw_game()
        """
        YOUR CODE HERE TO RESET THE BOARD TO VALUE 0 FOR ALL CELLS AND CREATE A NEW GAME STATE WITH NEWLY INITIALIZED
        BOARD STATE
        """
        board = np.zeros((self.GRID_ROWS, self.GRID_COLS))
        self.game_state = GameStatus(board, True)
        self.game_over = False
        self.human_score = 0
        self.ai_score = 0
        self.winner_text = ""
        
        pygame.display.update()

    def draw_symbol_for_current_player(self, row, col):
        # Player 1 (turn_O=True) uses human_symbol, Player 2/AI (turn_O=False) uses ai_symbol
        if self.game_state.turn_O:
            symbol = self.human_symbol
        else:
            symbol = self.ai_symbol
        if symbol == "O":
            self.draw_circle(row, col)
        else:
            self.draw_cross(row, col)

    def play_game(self, mode = "player_vs_ai"):
        done = False

        clock = pygame.time.Clock()


        while not done:
            for event in pygame.event.get():  # User did something
                """
                YOUR CODE HERE TO CHECK IF THE USER CLICKED ON A GRID ITEM. EXIT THE GAME IF THE USER CLICKED EXIT
                """
                if event.type == pygame.QUIT:
                    done = True

                """
                YOUR CODE HERE TO HANDLE THE SITUATION IF THE GAME IS OVER. IF THE GAME IS OVER THEN DISPLAY THE SCORE,
                THE WINNER, AND POSSIBLY WAIT FOR THE USER TO CLEAR THE BOARD AND START THE GAME AGAIN (OR CLICK EXIT)
                """

                # Handle keyboard input for settings text boxes
                if event.type == pygame.KEYDOWN:
                    if self.game_over and event.key == pygame.K_r:
                        self.game_reset()
                    else:
                        self.handle_panel_key(event)

                if event.type == pygame.MOUSEBUTTONUP:
                    mx, my = event.pos

                    # Clicks in the panel area go to settings handler
                    if my < PANEL_HEIGHT:
                        self.handle_panel_click(mx, my)
                        # Redraw panel to reflect changes
                        self.draw_panel()
                        pygame.display.update()
                        continue

                    # Ignore board clicks if game hasn't started or is over
                    if not self.game_started or self.game_over:
                        continue

                    """
                    YOUR CODE HERE TO NOW CHECK WHAT TO DO IF THE GAME IS NOT OVER AND THE USER SELECTED A NON EMPTY CELL
                    IF CLICKED A NON EMPTY CELL, THEN GET THE X,Y POSITION, SET ITS VALUE TO 1 (SELECTED BY HUMAN PLAYER),
                    DRAW CROSS (OR NOUGHT DEPENDING ON WHICH SYMBOL YOU CHOSE FOR YOURSELF FROM THE gui) AND CALL YOUR 
                    PLAY_AI FUNCTION TO LET THE AGENT PLAY AGAINST YOU
                    """
                
                    # Get the position
                    pos = (mx, my - PANEL_HEIGHT)
                    
                    # Change the x/y screen coordinates to grid coordinates
                    col = int(pos[0] // (self.WIDTH + self.MARGIN))
                    row = int(pos[1] // (self.HEIGHT + self.MARGIN))

                    if row < self.GRID_ROWS and col < self.GRID_COLS and self.game_state.board_state[row][col] == 0:
                        # Draw symbol based on whose turn it is before moving
                        self.draw_symbol_for_current_player(row, col)
                        self.move((row, col))
                        self.change_turn()

                        # Update live triplet scores after every move
                        self.update_scores()
                        self.draw_panel()

                        if self.is_game_over():
                            self.game_over = True
                            scores = self.game_state.get_scores(True)
                            if scores > 0:
                                self.winner_text = f"{"Player 1" if self.game_mode == "player_vs_player" else "Human"} wins! Score:" + str(scores) + "!" 
                            elif scores < 0:
                                self.winner_text = f"{"Player 2" if self.game_mode == "player_vs_player" else "AI"} wins! Score:" + str(scores) + "!"
                            else:
                                self.winner_text = "Draw! Score:" + str(scores) + "!"
                            print(self.winner_text)
                            self.draw_overlay(self.winner_text)
                        else:
                            # Check if the game is human vs human or human vs AI player from the GUI. 
                            # If it is human vs human then your opponent should have the value of the selected cell set to -1
                            # Then draw the symbol for your opponent in the selected cell
                            # Within this code portion, continue checking if the game has ended by using is_terminal function
                            if self.game_mode == "player_vs_ai":
                                self.play_ai()
                    
            # Update the screen with what was drawn.
            pygame.display.update()

        pygame.quit()

tictactoegame = RandomBoardTicTacToe()
"""
YOUR CODE HERE TO SELECT THE OPTIONS VIA THE GUI CALLED FROM THE ABOVE LINE
AFTER THE ABOVE LINE, THE USER SHOULD SELECT THE OPTIONS AND START THE GAME. 
YOUR FUNCTION PLAY_GAME SHOULD THEN BE CALLED WITH THE RIGHT OPTIONS AS SOON
AS THE USER STARTS THE GAME
"""

tictactoegame.play_game(tictactoegame.game_mode)