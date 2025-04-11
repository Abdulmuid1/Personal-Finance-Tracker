# ID - 3143047
# Icebreaker project

# imports all the public names defined in the graphics module into the current namespace
from graphics import *

def pixel_to_board_coord(x, y, square_size, margin):
    """
    Convert pixel coordinates to board coordinates.

    Parameters:
        x (int): The x-coordinate of the pixel.
        y (int): The y-coordinate of the pixel.
        square_size (int): The size of each square on the board.
        margin (int): The margin around each square.

    Returns:
        int, int: The row and column corresponding to the pixel coordinates.
    """    
    current_row = int((y - margin) // (square_size + margin))
    current_col = int((x - margin) // (square_size + margin))
    return current_row, current_col

# Create class Icebreaker
class Icebreaker:    
    
    # Initialize player scores
    player1_score = 0
    player2_score = 0    
    
    def __init__(self):
        """
            Initialize the Icebreaker game.
    
            Parameters:
                win (GraphWin): The GraphWin object representing the game window.
                board (Board): The Board object representing the game board.
                players (Player): The Player object representing the players.
        """        
        # Create a GraphWin object
        self.win = GraphWin("Abdulmuid's Icebreaker", 650, 720)
        
        # Create a Board object
        self.game_board = Board(self.win, 90)
        self.win.setBackground(color_rgb(192, 192, 192))
        self.width = self.game_board.square_size
        self.current_task = "MOVE"  # Initialize current task
        # Create players
        self.create_players()        
        self.current_player = 0 # Starting player        
        self.create_buttons()
        self.status_msg = Text(Point(100, 590), "")  # Initialize status_msg attribute with an empty string
        self.status_msg.setSize(16)
        self.status_msg.draw(self.win)
        self.move_made = False  # Flag to track whether a move has been made by the current player        
        self.create_status_messages()  
               
        
        
    def current_player_can_move(self):
        """
        Checks if the current player can make a move.
        
        Returns:
            bool: True if the current player can make a move, False otherwise.
        """
        if self.current_player == 0:
            player = self.player1
        else:
            player = self.player2
    
        return player.can_move()         
        
    def create_players(self):
        """
        Create player 1 and player 2 objects.
        """
        # Create Player 1
        self.player1 = Player(self.win, self.game_board, 'black', 0, 0)

        # Create Player 2
        self.player2 = Player(self.win, self.game_board, 'white', 5, 6)
                
                
    def create_buttons(self):
        """
        Create the quit and reset buttons for the game.
        
        """        
        self.quit_button = Rectangle(Point(540, 550), Point(620, 600))
        self.quit_button.setOutline('black')
        self.quit_button.setWidth(3)
        self.quit_button.draw(self.win)
        quit_text = Text(Point(580, 575), 'QUIT')
        quit_text.setSize(16)
        quit_text.draw(self.win)

        self.reset_button = Rectangle(Point(540, 640), Point(620, 690))
        self.reset_button.setOutline('black')
        self.reset_button.setWidth(3)
        self.reset_button.draw(self.win)
        reset_text = Text(Point(580, 665), 'RESET')
        reset_text.setSize(16)
        reset_text.draw(self.win)
        
        # Create title messages i.e. bye bye and reset
        self.title_msg = Text(Point(100, 660), '')
        self.title_msg.setSize(16)
        self.title_msg.draw(self.win)        
        

    def create_status_messages(self):
        """
        Create and update the status messages for the game.
        """
        player_name = "PLAYER 0" if self.current_player == 0 else "PLAYER 1"
        task_message = "MOVE" if self.current_task == "MOVE" else "BREAK ICE"
    
        if self.current_task == "MOVE" and self.move_made:
            player_position = f"[{self.player1.current_col if self.current_player == 0 else self.player2.current_col},\
            {self.player1.current_row if self.current_player == 0 else self.player2.current_row}]"
        else:
            # Determine the current player
            if self.current_player == 0:
                current_player = self.player1
            else:
                current_player = self.player2
    
            player_position = f"[{current_player.current_col},{current_player.current_row}]"
    
        # Construct the status message based on the current state of the game
        status_text = f"{player_name}: {player_position}\n\n{task_message}"
        
        # Check for winner if the current player cannot make a move
        if not self.current_player_can_move():
            winner = "Player " + str(1 - self.current_player)
            status_text = f"GAME OVER !!\n{winner} HAS WON"
    
        # Set the text of the status message
        self.status_msg.setText(status_text)
       
        # Clear the title message if a move has been made
        if self.move_made:
            self.title_msg.setText("")               


        
    def reset_game(self):
        # Move player 1 to its initial position [0, 0]
        self.player1.move_player(0 - self.player1.current_col, 0 - self.player1.current_row)
        
        # Move player 2 to its initial position [5, 6]
        self.player2.move_player(6 - self.player2.current_col, 5 - self.player2.current_row)
         
        # Reset all non-ice squares on the board to their initial state
        for row in range(self.game_board.rows):
            for col in range(self.game_board.cols):
                if not self.game_board.is_ice(row, col):
                    self.game_board.reset_square(row, col)  # Reset the square
                    
        # Reset current player and task
        self.current_player = 0
        self.current_task = "MOVE"  # Reset current task
        self.move_made = False  # Reset move_made flag
        self.create_status_messages()  # Update status message
       


    def switch_players(self):
        """
        Switch the current player and update the current task.
        """        
        # Switch current player
        self.current_player = 1 - self.current_player
    
        # Update current task
        self.current_task = "MOVE" if self.current_task == "BREAK ICE" else "BREAK ICE"
        self.move_made = False
    
        # Update status message
        self.create_status_messages()

    def play(self):
        """
        Starts the Icebreaker game.
        """
        self.current_player = 0
        self.create_status_messages()  # Call this method to initialize status messages
        
        while True:
            point = self.win.getMouse()
            row, col = pixel_to_board_coord(int(point.getX()), int(point.getY()), self.game_board.square_size, self.game_board.margin)
    
            if self.game_board.in_rectangle(point, self.quit_button):
                self.title_msg.setText("BYE BYE !!")
                break
    
            elif self.game_board.in_rectangle(point, self.reset_button):
                self.title_msg.setText("RESET")
                self.reset_game()  # Call reset_game method when reset button is clicked
                continue  # Continue to the next iteration of the loop
            
            
            # Check if the current player can make a move
            if not self.current_player_can_move():
                # If the current player cannot move, the opponent wins
                if self.current_player == 0:
                    Icebreaker.player2_score += 1
                else:
                    Icebreaker.player1_score += 1       
                self.create_status_messages()  # Update status message to display winner
                break
    
            if self.current_player == 0:
                player = self.player1
            else:
                player = self.player2
    
            if self.current_task == "MOVE":
                current_row, current_col = player.get_player_position()
                dx, dy = player.get_direction_from_click(point, (current_row, current_col))
                new_row, new_col = current_row + dy, current_col + dx  # Calculate new position
    
                # Check if the absolute difference between row and column is equal to 1
                if abs(new_row - current_row) <= 1 and abs(new_col - current_col) <= 1:
                    if self.game_board.is_valid_move(new_row, new_col):  # Check if move is valid
                        new_row, new_col = player.move_player(dx, dy)  # Move the piece
                        self.move_made = True
                        self.current_task = "BREAK ICE"
                        self.create_status_messages()  # Update status message
                    else:
                        if not self.move_made:
                            self.create_status_messages()  # Update status message
                else:
                    self.title_msg.setText("NOT VALID")  # Display "NOT VALID" if move is invalid
    
            elif self.current_task == "BREAK ICE":
                if self.move_made:
                    if self.game_board.is_valid_break(row, col):
                        self.game_board.break_ice(row, col)  # Break the ice at the selected position
                        self.move_made = False
                        self.switch_players()
                        
                        # Check if the opponent can make a move after the current player's move
                        if not self.current_player_can_move():
                            # If the opponent cannot move, the current player wins
                            if self.current_player == 1:
                                Icebreaker.player1_score += 1
                            else:
                                
                                Icebreaker.player2_score += 1                            
                            self.create_status_messages()  # Update status message to display winner
                            break
                    else:
                        self.title_msg.setText("NOT VALID")
                else:
                    self.create_status_messages()  # Update status message
                    self.status_msg.setText(self.create_status_messages())  
    
        self.win.getMouse()
        self.win.close()    

    

# Create the board class
class Board:
    def __init__(self, win, width):
        """
        Initialize the game board.
        
        Parameters:
        win (GraphWin): The GraphWin object representing the game window.
        width (int): The width of each square on the board.
        """        
        self.win = win
        self.width = width
        self.margin = 8
        self.rows = 6  # Number of rows on the board
        self.cols = 7  # Number of columns on the board        
        self.square_size = 80
        self.game_board = None
        self.state_board = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.create_board()

    def create_board(self):
        """
        Draw the game board.
        """        
        self.game_board = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                x1 = j * self.width + self.margin
                y1 = i * self.width + self.margin
                x2 = (j + 1) * self.width
                y2 = (i + 1) * self.width
                r = Rectangle(Point(x1, y1), Point(x2, y2))
                r.setFill("darkgrey")
                r.draw(self.win)
                row.append(r)
            self.game_board.append(row)
             
    def reset_square(self, row, col):
        """
        Reset a square to its initial state.
        
        Parameters:
            row (int): The row index of the square.
            col (int): The column index of the square.
        """
        square = self.game_board[row][col]
        square.setFill("darkgrey")  # Reset square to its initial state                
                
                
    def is_occupied(self, row, col):
            # Check if the square at the given row and column is occupied
            # For now, let's assume the square is occupied if it's not an empty square (Broken ice or player's piece)
        return self.is_player_piece(row, col)
    
    def is_empty(self, row, col):
        # Check if the square at the given row and column is empty (not broken ice and not occupied by a player's piece)
        return not self.is_broken_ice(row, col) and not self.is_player_piece(row, col)
    
    def is_ice(self, row, col):
        try:
            square = self.game_board[row][col]
            return square.config['fill'] == 'darkgrey'  # Check square's fill color
        except IndexError:
            return False
        
    def is_broken_ice(self, row, col):
        """
        Check if the specified position contains broken ice.
    
        Parameters:
            row (int): The row index of the position to check.
            col (int): The column index of the position to check.
    
        Returns:
            bool: True if the square contains broken ice, False otherwise.
        """
        try:
            square = self.game_board[row][col]
            return square.config['fill'] == 'lightblue'  # Check if the square contains broken ice
        except IndexError:
            return False
        
    

    def get_center_player(self, player_number, row, col):
        """
        Get the center coordinates of the square at the given row and column for the specified player.
        
        Parameters:
            player_number (int): The player number (1 or 2).
            row (int): The row of the square.
            col (int): The column of the square.
        
        Returns:
            Point: The center coordinates of the square for the specified player.
        """
        if player_number == 1:
            x = col * (self.square_size + self.margin) + self.square_size / 2 + self.margin
            y = row * (self.square_size + self.margin) + self.square_size / 2 + self.margin 
        elif player_number == 2:
            x = col * (self.square_size + self.margin) + self.square_size / 1.5 + self.margin
            y = row * (self.square_size + self.margin) + self.square_size / 1.6 + self.margin
        
        return Point(x, y)
    
    def get_square(self, row, col):
            # Return the square object at the specified row and column
        return self.game_board[row][col]
    
    def set_square_state(self, row, col, state):
        # Update the logical state of the square
        self.state_board[row][col] = state
            
    
    def set_square_fill(self, row, col, color):
           # Update the square object at the specified row and column with the new color
        square = self.get_square(row, col)
        square.setFill(color)    


    def is_player_piece(self, row, col):
        # Check the state_board to determine if the square is occupied by a player piece
        return self.state_board[row][col] == 'player1' or self.state_board[row][col] == 'player2'


    def is_valid_move(self, row, col):
        """
        Check if the position (row, col) is a valid move for a piece.
    
        Parameters:
            row (int): The row index of the position.
            col (int): The column index of the position.
    
        Returns:
            bool: True if the move is valid, False otherwise.
        """
        # Check if the position (row, col) is within the boundaries of the board
        # and is not already occupied by another player's piece or broken ice
        return 0 <= row < self.rows and 0 <= col < self.cols \
           and not self.is_occupied(row, col) \
           and not self.is_broken_ice(row, col) 
    
    def print_board_state(self):
        for row in range(self.rows):
            for col in range(self.cols):
                state = self.state_board[row][col]

    def is_valid_break(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            
            # Check if there is ice at the specified position and if it's not occupied by a player's piece
            valid_break = self.is_ice(row, col) and not self.is_player_piece(row, col) and not self.is_broken_ice(row, col)
            return valid_break
        else:
            return False


                
    def break_ice(self, row, col):
        # Check if breaking the ice at the specified position is a valid move
        if self.is_valid_break(row, col):
            square = self.game_board[row][col]  # Access the square
            square.setFill("lightblue")
        else:
            # Here you can handle the invalid move, for example, by showing an error message
            return False
            
    def in_rectangle(self, click_point, rect):
        # Function in_rectangle was adapted from code written by [Phillip Mees] for the Icebreaker project.
        
        """
        Purpose: Determines whether the mouse is clicked inside a rectangle
        Parameters: click_point - Point object at which the mouse was clicked
                    rect - Rectangle object to be checked for mouse click
        Returns: bool - True if click-point is inside rect, False otherwise
        """        
        if int(rect.getP1().getX()) < int(rect.getP2().getX()):
            x_check = int(rect.getP1().getX()) < click_point.getX() < int(rect.getP2().getX())
        else:
            x_check = int(rect.getP2().getX()) < click_point.getX() < int(rect.getP1().getX())

        if int(rect.getP1().getY()) < int(rect.getP2().getY()):
            y_check = int(rect.getP1().getY()) < click_point.getY() < int(rect.getP2().getY())
        else:
            y_check = int(rect.getP2().getY()) < click_point.getY() < int(rect.getP1().getY())

        return x_check and y_check
    
    
# Define the Player class
class Player:
    def __init__(self, win, game_board, color, initial_row, initial_col):
        self.win = win
        self.game_board = game_board
        self.color = color  # Color of the player's piece
        self.current_row = initial_row  # Initial row for the player
        self.current_col = initial_col  # Initial column for the player
        self.create_piece()
        
    def create_piece(self):  # Adjusted method name
        """
        Create the player's piece.
        """
        # Choose the appropriate method for creating the player's piece based on the player's color
        if self.color == 'black':
            self.create_piece1()  # Adjusted method name
        elif self.color == 'white':
            self.create_piece2()  # Adjusted method name      

    def create_piece1(self):
        """
        Create Player 1 (red piece).
        """
        center = self.game_board.get_center_player(1, self.current_row, self.current_col)  # Pass player number 1
        self.piece = Circle(center, self.game_board.square_size // 2.5)
        self.piece.setFill(self.color)
        # Update the logical state of the square to indicate it's occupied by player 1
        self.game_board.set_square_state(self.current_row, self.current_col, 'player1')                
        self.piece.setWidth(3)
        self.piece.draw(self.win)

    def create_piece2(self):
        """
        Create Player 2 (blue piece).
        """
        center = self.game_board.get_center_player(2, self.current_row, self.current_col)  # Pass player number 2
        self.piece = Circle(center, self.game_board.square_size // 2.5)
        self.piece.setFill(self.color)
        # Update the logical state of the square to indicate it's occupied by player 1
        self.game_board.set_square_state(self.current_row, self.current_col, 'player2')        
        self.piece.setWidth(3)
        self.piece.draw(self.win)
        
    def can_move(self):
        """
        Check if the player can make a move to an adjacent square after being bombarded by broken ice.
        
        Returns:
            bool: True if the player can make a move, False otherwise.
        """
        # Check if any adjacent square to the player's current position is valid for a move
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                # Exclude the case where both dx and dy are 0 (no movement)
                if dx != 0 or dy != 0:
                    # Check if the move is within the bounds of the board and is valid
                    if self.game_board.is_valid_move(self.current_row + dy, self.current_col + dx):
                        return True
        return False   
    
    def move_player(self, dx, dy):
        """
        Move the player piece by the specified displacement.

        Parameters:
            dx (int): The change in the x-coordinate.
            dy (int): The change in the y-coordinate.

        Returns:
            tuple: The new row and column positions of the player.
        """
        # Get the current row and column positions
        current_row, current_col = self.get_player_position()

        # Calculate the new row and column positions
        new_row = current_row + dy
        new_col = current_col + dx
        
        # Update the logical state of the square to indicate it's now empty
        self.game_board.set_square_state(current_row, current_col, None)        

        # Move the player's piece
        self.piece.move(dx * (self.game_board.square_size + self.game_board.margin*1.25),
                        dy * (self.game_board.square_size + self.game_board.margin*1.22))

        # Update the player's current position
        self.current_row = new_row
        self.current_col = new_col
        
        # Update the logical state of the new square to indicate it's occupied by the player        
        if self.color == 'black':
            self.game_board.set_square_state(new_row, new_col, 'player1')
        elif self.color == 'white':
            self.game_board.set_square_state(new_row, new_col, 'player2')        
        
        # After the move is made, print the board state to debug
        self.game_board.print_board_state()  
        
        return new_row, new_col

    def move_player_to_position(self, row, col):
        """
        Move the player piece to the specified position.
    
        Parameters:
            row (int): The row coordinate of the position.
            col (int): The column coordinate of the position.
        """
        # Calculate the center of the specified position
        center = self.game_board.get_center_player1(row, col)
        center = self.game_board.get_center_player2(row, col)
        
        # Move the player's piece to the center of the specified position
        self.piece.move(center.getX() - self.piece.getCenter().getX(), center.getY() - self.piece.getCenter().getY())
        # Update the player's current position
        self.current_row = row
        self.current_col = col



    
    def move_player1(self, dx, dy):
            """
            Move Player 2 (blue piece) by the specified displacement.
    
            Parameters:
                dx (int): The change in the x-coordinate.
                dy (int): The change in the y-coordinate.
            """
            # Calculate the new row and column positions for Player 2
            current_row, current_col = self.player1.get_player_position()
            new_row = current_row + dy
            new_col = current_col + dx
    
            # Move Player 2's piece
            self.player1.move_player(dx, dy)    
    
    def move_player2(self, dx, dy):
            """
            Move Player 2 (blue piece) by the specified displacement.
    
            Parameters:
                dx (int): The change in the x-coordinate.
                dy (int): The change in the y-coordinate.
            """
            # Calculate the new row and column positions for Player 2
            current_row, current_col = self.player2.get_player_position()
            new_row = current_row + dy 
            new_col = current_col + dx 
    
            # Move Player 2's piece
            self.player2.move_player(dx, dy)    





     
    def get_direction_from_click(self, click_point, current_position):
        """
        Determine the direction of the click relative to the player's current position.
    
        Parameters:
            click_point (Point): The Point object representing the location of the click.
            current_position (tuple): A tuple containing the current row and column of the player.
    
        Returns:
            tuple: The difference in row and column (dx, dy).
        """
        # Determine the row and column of the click
        click_row, click_col = pixel_to_board_coord(click_point.getX(), click_point.getY(), self.game_board.square_size, self.game_board.margin)
    
        # Calculate the difference in row and column
        dx = click_col - current_position[1]
        dy = click_row - current_position[0] 
        
        return dx, dy

            
            
    def get_player_position(self):
            return self.current_row, self.current_col        
            
            
    def player_clicked(self, point):
        # Check if the click occurs on an empty square
        row, col = pixel_to_board_coord(int(point.getX()), int(point.getY()), self.game_board.square_size, self.game_board.margin)
        return not (self.game_board.is_occupied(row, col) or self.game_board.is_ice(row, col))
    
        
def create_splash_screen():
    # Create a GraphWin object for the splash screen
    splash_win = GraphWin("Icebreaker Splash Screen", 600, 600)
    splash_win.setBackground(color_rgb(192, 192, 192))
    
    title = Text(Point(300, 50), "Icebreaker Game")
    title.setSize(20)
    title.draw(splash_win)
        
    info = Text(Point(300, 150), "Welcome to the Icebreaker game\n This game was written by Abdulmuid Olaniyan\n for CMPT 103, Winter session 2024")
    info.setSize(14)
    info2 = Text(Point(300, 230), "Do you want to play?")
    info2.setSize(20)
    info2.setStyle('bold')
    info.draw(splash_win)
    info2.draw(splash_win)
        
    # Play Game button
    play_button = Rectangle(Point(190, 300), Point(390, 350))
    play_button.setFill("darkgrey")
    play_button.draw(splash_win)
    play_text = Text(Point(290, 330), "Play Game")
    play_text.setSize(20)
    play_button.setOutline('black')    
    play_text.setStyle('bold')    
    play_text.draw(splash_win)
    
    # Terminate game button
    cancel_button = Rectangle(Point(190, 400), Point(390, 450))
    cancel_button.setFill("darkgrey")
    cancel_button.draw(splash_win)
    cancel_text = Text(Point(290, 430), "No Thanks")
    cancel_text.setSize(20)
    cancel_button.setOutline('black')    
    cancel_text.setStyle('bold')     
    cancel_text.draw(splash_win)    
    
    return splash_win, play_button, cancel_button
    
def create_score_screen(player1_score, player2_score):
    # Create a GraphWin object for the score screen
    score_win = GraphWin("Icebreaker Score Screen", 600, 600)
    score_win.setBackground(color_rgb(192, 192, 192))
        
    game_text = Text(Point(290, 90), "Game Score") 
    game_text.setSize(15)
    game_text.setStyle("bold")  
    # player scores container
    player_shed = Rectangle(Point(200, 100), Point(380, 250))
    player_shed.setFill("darkgrey")
    player_shed.draw(score_win)  
    player_shed.setOutline('black')
    # Player 1 score    
    player1_text = Text(Point(290, 150), "Player 0: " + str(player1_score))
    player1_text.setSize(15)
    player1_text.draw(score_win)
    game_text.draw(score_win)
            
    # Player 2 score
    player2_text = Text(Point(290, 200), "Player 1: " + str(player2_score))
    player2_text.setSize(15)
    player2_text.draw(score_win)
        
    # Replay Game button
    start_button = Rectangle(Point(190, 300), Point(390, 350))
    start_button.setFill("darkgrey")
    start_button.draw(score_win)
    start_text = Text(Point(290, 330), "Next Round")
    start_text.setSize(20)
    start_button.setOutline('black')    
    start_text.setStyle('bold')    
    start_text.draw(score_win)

        # Terminate game button
    quit_button = Rectangle(Point(190, 400), Point(390, 450))
    quit_button.setFill("darkgrey")
    quit_button.draw(score_win)
    quit_text = Text(Point(290, 430), "No Thanks")
    quit_text.setSize(20)
    quit_button.setOutline('black')    
    quit_text.setStyle('bold')     
    quit_text.draw(score_win)    

        
    return score_win, start_button, quit_button, player_shed, player1_text, player2_text
    
def main():
    # Create splash screen
    splash_win, play_button, cancel_button = create_splash_screen()
    click_point = splash_win.getMouse()
    
    # Check if Play Game button is clicked
    if click_point.getX() >= 190 and click_point.getX() <= 390 and \
        click_point.getY() >= 300 and click_point.getY() <= 350:
        # Close splash screen
        splash_win.close()
        
        exit_game = False  # Control flag for the outer loop
        score_win = None  # Initialize score_win to None
        
        while not exit_game:
            # Initialize Icebreaker game
            icebreaker = Icebreaker()
            
            # Play the game
            icebreaker.play()
            
            # Close the previous score screen if it's open
            if score_win is not None:
                score_win.close()            
            
            # After the game ends, display score screen
            player1_score = icebreaker.player1_score
            player2_score = icebreaker.player2_score
            
            score_win, start_button, quit_button, player_shed, player1_text, player2_text = create_score_screen(Icebreaker.player1_score, Icebreaker.player2_score)
            
                       
            
            # Wait for user interaction on the score screen
            while True:
                click_point = score_win.getMouse()
                # Check if the user wants to start another round
                if start_button.getP1().getX() <= click_point.getX() <= start_button.getP2().getX() and \
                   start_button.getP1().getY() <= click_point.getY() <= start_button.getP2().getY():
                    # Next Round button clicked
                    score_win.close()
                    score_win = None  # Reset score_win to None
                    break  # Exit the loop to start a new round
                elif quit_button.getP1().getX() <= click_point.getX() <= quit_button.getP2().getX() and \
                     quit_button.getP1().getY() <= click_point.getY() <= quit_button.getP2().getY():
                    # No thanks button clicked
                    score_win.close()
                    exit_game = True  # Set flag to exit the outer loop
                    break  # Exit the loop to end the game
    else:
        splash_win.close()

if __name__ == "__main__":
    main()
