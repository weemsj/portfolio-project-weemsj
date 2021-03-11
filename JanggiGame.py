# Name: Jacqueline Weems
# Date: 02/27/2021
# Description: This program is an abstract board game called Jangi. It doesn't implement the rules regarding perpetual
# check, position repetition, any kind of draw or any miscellaneous rules. However this program does handle checkmate
# situations and piece specific rules.
# PIECE RULES:
# soldier: can move forward and sideways one step per turn. can move diagonal only in fortress.
# General: can move forward, sideways, backwards, and diagonal one step within the the fortress.
# Guard: as like the General, moves one step within the fortress.
# Elephant: can move one step forward then two diagonal or one step sideways and two diagonal. Elephants can be blocked
# Horse: cna move one step forward then one step diagonal per turn or one step sideways then one diagonal per turn.
# like Elephant Horse can be blocked.
# Chariot: can move unlimited spaces horizontal or vertical.
# Cannon: can only move by jumping another piece horizontal or vertically unless in the fortress the jum can be any
# length provided their is exactly one piece any where between the original position and the target. Cannons can not
# capture other cannons or jump over another cannon @ start there are no valid moves for cannon.
# CHECK MATE: happens if your General can not move or sit still without avoiding capture.


class JanggiGame:

    def __init__(self):
        """
        represents a Janggi game
        """

        self._game_state = 'UNFINISHED'
        self._whose_turn = 'BLUE'
        self._board = Board()

    def set_game_state(self, new_state):
        """changes the game state"""
        self._game_state = new_state

    def get_game_state(self):
        """returns private data member game state """
        return self._game_state

    def set_whose_turn(self):
        """sets private data member whose turn"""
        if self._whose_turn == 'BLUE':
            self._whose_turn = 'RED'
        else:
            self._whose_turn = 'BLUE'

    def get_whose_turn(self):
        """returns private data member whose turn"""
        return self._whose_turn

    def is_in_check(self, player):
        """looks for generals that are in check"""
        for general in self._board.get_generals_in_check:
            if general.get_team() == player:
                return True
        return False

    def make_move(self, start, finish):
        """
        moves players piece from start to finish. If the square being moved from does not contain a piece belonging to
        the player whose turn it is, or if the indicated move is not legal or if the game is already won it will return
        False. Otherwise it will make the indicated move, remove any captured pieces, update game state if necessary,
        update whose turn it is and return True. If passed the same value for start and finish return True and update
        turn.
        :param start: string represents square to move from
        :param finish: string represents square to move to
        :return: True or False
        """
        print("make_move(", start, ",", finish, ")")
        # check for game status
        if self.get_game_state() != 'UNFINISHED':
            return False

        # check to make sure player is moving the correct piece
        if not self._board.is_player_piece(self, start):
            return False

        # find game piece
        row, col = self._board.algebraic_to_index(start)
        piece = self._board.get_piece(row, col)

        # check if General is in check then find move to get out of check
        team = piece.get_team()
        for general in self._board.get_generals_in_check():
            # check to see if your general is in the list of checked generals if so pass the general to the neutralize
            # threat method
            if general.get_team() == team:
                threats = general.get_threatened_by()
                self._board.neutralize_threats(self, general, threats)

                # check for game status
                if self.get_game_state() != 'UNFINISHED':
                    return False
                return True
            elif team == "blue":
                self._game_state = "BLUE_WON"
            else:
                self._game_state = "RED_WON"
            return True

        # finish location
        fut_row, fut_col = self._board.algebraic_to_index(finish)

        # check piece rules
        if not piece.move_rules(self._board, fut_row, fut_col):
            return False

        # make move
        self._board.move_piece(piece, fut_row, fut_col)

        # change turn
        self.set_whose_turn()

        self._board.print_game_board()

        return True


class Board:
    """
    This class represents the game board
    """

    def __init__(self):
        self._board = [
            ["-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----"],
            ["-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----"],
            ["-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----"],
            ["-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----"],
            ["-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----"],
            ["-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----"],
            ["-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----"],
            ["-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----"],
            ["-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----"],
            ["-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----"],
            ]
        self._board_status = "EMPTY"
        self.initialize_piece()
        self._conversion = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7, "i":8}
        self._revert = {0:"a", 1:"b", 2:"c", 3:"d", 4:"d", 5:"f", 6:"g", 7:"h", 8:"i"}
        self._red_fortress = [self._board[0][3], self._board[0][4], self._board[0][5],
                              self._board[1][3], self._board[1][4], self._board[1][5],
                              self._board[2][3], self._board[2][4], self._board[2][5]]
        self._blue_fortress = [self._board[9][3], self._board[9][4], self._board[9][5],
                               self._board[8][3], self._board[8][4], self._board[8][5],
                               self._board[7][3], self._board[7][4], self._board[7][5]]
        self._generals_in_check = []

    def initialize_piece(self):
        """ creates instances of each game piece """
        if self._board_status == "FULL":
            pass
        General(self._board, "BGN", "blue", row=8, col=4)
        General(self._board,"RGN", "red", row=1, col=4)
        Guard(self._board,"Bg1", "blue", row=9, col=3)
        Guard(self._board,"Bg2", "blue", row=9, col=5)
        Guard(self._board,"Rg1", "red", row=0, col=3)
        Guard(self._board,"Rg2", "red", row=0, col=5)
        Horse(self._board,"BH1", "blue", row=9, col=2)
        Horse(self._board,"BH2", "blue", row=9, col=7)
        Horse(self._board,"RH1", "red", row=0, col=2)
        Horse(self._board,"RH2", "red", row=0, col=7)
        Chariot(self._board,"BC1", "blue", row=9, col=0)
        Chariot(self._board,"BC2", "blue", row=9, col=8)
        Chariot(self._board,"RC1", "red", row=0, col=0)
        Chariot(self._board,"RC2", "red", row=0, col=8)
        Cannon(self._board,"BN1", "blue", row=7, col=1)
        Cannon(self._board,"BN2", "blue", row=7, col=7)
        Cannon(self._board,"RN1", "red", row=2, col=1)
        Cannon(self._board,"RN2", "red", row=2, col=7)
        Elephant(self._board,"BE1", "blue", row=9, col=1)
        Elephant(self._board,"BE2", "blue", row=9, col=6)
        Elephant(self._board,"RE1", "red", row=0, col=1)
        Elephant(self._board,"RE2", "red", row=0, col=6)
        Soldier(self._board,"BS1", "blue", row=6, col=0)
        Soldier(self._board,"BS2", "blue", row=6, col=2)
        Soldier(self._board,"BS3", "blue", row=6, col=4)
        Soldier(self._board,"BS4", "blue", row=6, col=6)
        Soldier(self._board,"BS5", "blue", row=6, col=8)
        Soldier(self._board,"RS1", "red", row=3, col=0)
        Soldier(self._board,"RS2", "red", row=3, col=2)
        Soldier(self._board,"RS3", "red", row=3, col=4)
        Soldier(self._board,"RS4", "red", row=3, col=6)
        Soldier(self._board,"RS5", "red", row=3, col=8)

        # update board status after pieces are initiated so the pieces don't get reset at each board call
        self._board_status = "FULL"

    def get_generals_in_check(self):
        """returns a list of generals in check"""
        return self._generals_in_check

    def get_board(self):
        """ returns board"""
        return self._board

    def get_piece(self, row, col):
        """returns piece position"""
        return self._board[row][col]

    def get_board_status(self):
        """return board status"""
        return self._board_status

    def set_board_status(self, status):
        """ changes board state to new status"""
        self._board_status = status

    def get_red_fortress(self):
        """returns red fortress"""
        return self._red_fortress

    def get_blue_fortress(self):
        """return blue fortress"""
        return self._blue_fortress

    def algebraic_to_index(self, string_notation):
        """ takes an algebraic string notation and returns the index"""
        # dictionary map to convert string letters to integers
        conversion = self._conversion

        # the first element in algebraic notation is a letter, assign the letter to a variable
        first_char = string_notation[0]
        # after the letter the rest of the notation is a string number, assign the number to a variable
        nums = string_notation[1:]
        # change the string number to integer number
        row = int(nums)
        row -= 1
        # look up first character conversion and assign to variable
        col = conversion[first_char]
        return row, col

    def move_piece(self,piece, row, col):
        """ updates chess board and object location after proposed move has been validated"""
        # preserve current position in case move is unsuccessful and we have to revert back
        prev_row = piece.get_row()
        prev_col = piece.get_col()

        occupant = self._board[row][col]

        # if future space is occupied check to see if the occupant is on the same team. If the team is the same the
        # move is invalid. If the occupant is the opps team we call the capture method.
        if occupant != "-----":
            if occupant.get_team == piece.get_team:
                return False
            # capture piece
            self.capture(row, col)

        # the future position is empty and now we move the piece to the future location and empty the pieces
        # current location.
        self._board[prev_row][prev_col] = "-----"
        self._board[row][col] = piece

        # now that the piece has moved we need to check if the move results in the general being in check. If the
        # general is in check we move the piece back to its previous location, put the captured piece back on the board
        # and move becomes invalid otherwise the piece new location is updated.

        for general in self._generals_in_check:
            if general.get_team() == piece.get_team():
                self._board[prev_row][prev_col] = piece
                self._board[row][col] = occupant
            return False
        piece.set_row(row)
        piece.set_col(col)

        # now that the move has been made the next step is to check if the move put the opps general in check.
        self.general_in_check(piece)

    def print_game_board(self):  # works
        """
        prints a pretty game board with piece object titles in the current location, location references around the
        boarder and without commas or brackets
        :return: prints pretty game board
        """
        print("      a     b     c     d     e     f     g     h     i")
        num = 1
        while num <= 10:
            for row in self._board:
                if num == 10:
                    print(str(num) + "  " + " ".join([str(piece) for piece in row]) + "  " + str(num))
                else:
                    print(str(num) + "   " + " ".join([str(piece) for piece in row]) + "   " + str(num))
                num += 1
        print("      a     b     c     d     e     f     g     h     i")

    def general_in_check(self, piece):
        """
        checks if a player has put opponents General in check
        :param piece: 'red' or 'blue'
        :return: True or False
        """
        # delete old move map
        piece.reset_move_map()

        # locate the opps general to see if the future location (generals location) is a valid move
        general_obj, row, col = self.locate_general(piece)

        # generate a new move map with the generals location as the move to if its a valid move the general is in check
        if piece.move_rules(self, row, col):
            general = general_obj()
            general_obj.set_check(piece)
            self.general_in_check(general)

        # if next move doesn't create a checked scenario, check the generals checked_by list to make sure the piece
        # isn't listed. If the piece is listed, remove the piece from the list. If there is only one element in the list
        # and the element is the newly moved piece then take the piece out of check and check by = False
        checked_by = general_obj.get_checked()

        if checked_by:
            for obj in checked_by:
                if obj == piece:
                    general_obj.remove_check(piece)

        if not checked_by:
            for gen in self._generals_in_check:
                if gen == general_obj:
                    self._generals_in_check.remove(gen)

        # delete hypothetical move_map
        piece.reset_move_map()

    def is_player_piece(self, the_game, start_place):
        """
        checks to see if players piece is in the start location
        :param the_game: the board game object
        :param start_place: starting move location
        :return: True or False
        """

        turn = JanggiGame.get_whose_turn(the_game)
        row, col = self.algebraic_to_index(start_place)
        piece = self._board[row][col]
        if piece == "-----":
            return False
        team = piece.get_team()

        # if blues turn, locate the piece at the start position then check Blues dictionary for piece
        if turn == 'BLUE':
            if team == "blue":
                return True
            return False
        # if reds turn, locate the piece at the start position then check reds dictionary for piece
        if turn == 'RED':
            if team == "red":
                return True
            return False

    def locate_general(self, piece_obj):
        """ locate opponents general and returns the location """
        team = piece_obj.get_team()
        if team == "blue":
            for general in self._red_fortress:
                if general != "-----":
                    title = general.get_title()
                    if title == "RGN":
                        row = general.get_row()
                        col = general.get_col()
                        return general, row, col
        if team == "red":
            for general in self._blue_fortress:
                if general != "-----":
                    title = general.get_title()
                    if title == "BGN":
                        row = general.get_row()
                        col = general.get_col()
                        return general, row, col

    def capture(self, row, col):
        """
        takes the row and column of the future location and removes the object from the board
        :param col: future column
        :param row: future row
        """
        # empties space
        self._board[row][col] = "-----"

    def neutralize_threats(self, game, general, threats):
        row = general.get_row()
        col = general.get_col()
        neutralize = []
        move_direction = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        for threat in threats:
            threat_row = threat.get_row()
            threat_col = threat.get_col()
            location = threat_row, threat_col
            neutralize.append(location)

        for line in self._board:
            for piece in line:
                if piece != "-----":
                    if piece.get_team() == general.get_team():
                        for x,y in move_direction:
                            piece.move_rules(self, row + x, col + y)
                            moves = piece.get_move_map()
                            neutralize.append(moves)
                        for x,y in neutralize:
                            if piece.make_move(self, x, y):
                                self.move_piece(piece, x, y)
                            for threat in threats:
                                if not threat.move_rules(self, row, col):
                                    general.remove_threat(threat)
                                    game.set_whose_turn()
                                    return
                        else:
                            if general.get_team() == "blue":
                                game.set_game_state("RED_WON")
                            else:
                                game.set_game_state("BLUE_WON")
                                return False


class Piece:
    """
    This class represents a game piece it has a subclass for each specific piece all pieces share a title, team and
    position but each piece have a few unique attributes. All data members are private and can be only accessed outside
    the class via getters and setters.
    """

    def __init__(self, board, title, team, row, col):
        self._title = title
        self._team = team
        self._row = row
        self._col = col
        board[row][col] = self
        self._move_map = []

    def get_title(self):
        """:returns piece title"""
        return self._title

    def get_team(self):
        """:returns game piece's team"""
        return self._team

    def get_row(self):
        """:returns row coordinate"""
        return self._row

    def get_col(self):
        """:returns column coordinate"""
        return self._col

    def set_row(self, row):
        """changes the row of the piece"""
        self._row = row

    def set_col(self, col):
        """ changes the column of the piece"""
        self._col = col

    def check_general(self, board_obj):
        """take a board object and passed the general to it to if the general is in check"""
        board = board_obj.get_board()
        board.generals_in_check(self)

    def get_move_map(self):
        """returns piece move map which is a list of possible movements for the piece"""
        return self._move_map

    def reset_move_map(self):
        """resets move map"""
        self._move_map = []


class General(Piece):
    """
    This class inherits the Piece class. It has an init method that overrides the parent class. All data members are
    private and must be accessed outside the class via getters and setters.
    """

    def __init__(self, board, title, team, row, col):
        """
        represents a General game piece, it has inherited attributes from the parent class
        :param title: General = "RG" or "BG"
        :param team: "red" or "blue
        :param row: y-coordinates
        :param col: x-coordinates
        """
        super().__init__(board, title, team, row, col)
        self._checked_by = []
        self._threatened_by = []

    def __repr__(self):
        return repr(self._title)

    def get_checked(self):
        """returns checked"""
        return self._checked_by

    def get_threatened_by(self):
        """returns list of piece objects that threaten the general"""
        return self._threatened_by

    def remove_threat(self, piece):
        """removes a threat from the generals threatened by list"""
        self._threatened_by.remove(piece)

    def add_threat(self, piece):
        """adds a threat to the generals threat list"""
        self._threatened_by.append(piece)

    def set_checked(self, piece):
        """adds game piece object to the list of game piece that have the General in check """
        self._checked_by.append(piece)

    def remove_check(self, piece):
        """removes a piece from the list of game pieces that have the General in check"""
        self._checked_by.remove(piece)

    def reset_checked(self):
        self._checked_by = []

    def move_rules(self, board_obj, fut_row, fut_col):
        """generals move rules"""
        board = board_obj.get_board()
        board_len = len(board)
        row, col = fut_row, fut_col
        move_directions = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]

        # generate all possible moves
        for x,y in move_directions:
            self._move_map.append((self._row + x, self._col + y))

        # remove any moves outside of the fortress
        for ele in range(0, len(self._move_map)):
            for x,y in self._move_map:
                if self._team == "blue":
                    if board_len <= x or x <= 6 or 6 <= y or y <= 2:
                        self._move_map.remove((x,y))
                        ele -= 1
                if self._team == "red":
                    if 3 <= x or x < 0 or 6 <= y or y <= 2:
                        self._move_map.remove((x,y))
                        ele -= 1

        # if finish after conversion isn't a possible move, move is invalid
        for ele in self._move_map:
            if self._move_map:
                if (row,col) == ele:
                    return True
        self._move_map = []
        return False


class Soldier(Piece):
    """
    This class inherits the Piece class. It has an init method that overrides the parent class. All data members are
    private and must be accessed outside the class via getters and setters.
    """

    def __init__(self,board, title, team, row, col):
        """
        represents a Soldier game piece, it has inherited attributes from the parent class. There are 10 soldiers that
        will use this class to determine if their movements are legal. Each team has 5 soldiers.
        Soldiers are initially placed on alternating points. Soldiers are only allowed to move one move forward,
        sideways or diagonal. Once a soldier reaches the opponents end of the board the soldiers are only allowed to
        move sideways.
        :param title: Soldier = "RS#" or "BS#"
        :param team: "red" or "blue
        :param row: y-coordinates
        :param col: x-coordinates
        """
        super().__init__(board, title, team, row, col)
        self._can_capture = []

    # __repr__ method shows objects attributes making it easier to debug
    def __repr__(self):
        return repr(self._title)

    def move_rules(self, board_obj, fut_row, fut_col):
        """
        Soldiers movement rules. This method returns True if the proposed move is within the parameters of the pieces
        movement ability.
        :param board_obj: board object
        :param fut_row: future row
        :param fut_col: future column
        :return: True or False
        """
        board = board_obj.get_board()
        board_len = len(board)
        board_width = len(board[0])
        row, col = fut_row, fut_col
        move_dir_red = [(0, 0), (0, 1), (0, -1), (1, 0), (1, 1), (1, -1)]
        move_dir_blue = [(0,0), (0, 1), (0, -1), (-1, 0), (-1, 1), (-1, -1)]

        # generate all possible moves
        if self._team == "blue":
            for x,y in move_dir_blue:
                self._move_map.append((self._row + x, self._col + y))
        if self._team == "red":
            for x,y in move_dir_red:
                self._move_map.append((self._row + x, self._col + y))

        # check if any moves are outside the game board
        for ele in range(0, len(self._move_map)):
            for x, y in self._move_map:
                if board_len <= x or x < 0 or board_width < y or y < 0:
                    self._move_map.remove((x, y))
                    ele -= 1

        # if finish after conversion isn't a possible move, move is invalid
        for ele in self._move_map:
            if self._move_map:
                if (row, col) == ele:
                    return True
        self._move_map = []
        return False


class Guard(Piece):
    """
    This class inherits the Piece class. It has an init method that overrides the parent class. All data members are
    private and must be accessed outside the class via getters and setters.
    """

    def __init__(self, board, title, team, row, col):
        """
        represents a Guard game piece, it has inherited attributes from the parent class
        :param title: Guard = "Rg#" or "Bg#"
        :param team: "red" or "blue
        :param row: y-coordinates
        :param col: x-coordinates
        """
        super().__init__(board, title, team, row, col)

    # __repr__ method shows objects attributes making it easier to debug
    def __repr__(self):
        return repr(self._title)

    def move_rules(self, board_obj, fut_row, fut_col):
        """guard piece move rules"""
        board = board_obj.get_board()
        board_len = len(board)
        row, col = fut_row, fut_col
        move_directions = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]

        # check if General is in check then find move to get out of check

        # generate all possible moves
        for x, y in move_directions:
            self._move_map.append((self._row + x, self._col + y))

        # remove any moves outside of the fortress
        for ele in range(0, len(self._move_map)):
            for x, y in self._move_map:
                if self._team == "blue":
                    if board_len <= x or x <= 6 or 6 <= y or y <= 2:
                        self._move_map.remove((x, y))
                        ele -= 1
                if self._team == "red":
                    if 3 <= x or x < 0 or 6 <= y or y <= 2:
                        self._move_map.remove((x, y))
                        ele -= 1

        # if finish after conversion isn't a possible move, move is invalid
        for ele in self._move_map:
            if self._move_map:
                if (row, col) == ele:
                    return True
        self._move_map = []
        return False


class Horse(Piece):
    """
    This class inherits the Piece class. It has an init method that overrides the parent class. All data members are
    private and must be accessed outside the class via getters and setters.
    """

    def __init__(self, board, title, team, row, col):
        """
        represents a Horse game piece, it has inherited attributes from the parent class
        :param title: Horse = "BH#" or "BH#"
        :param team: "red" or "blue
        :param row: y-coordinates
        :param col: x-coordinates
        """
        super().__init__(board, title, team, row, col)

    # __repr__ method shows objects attributes making it easier to debug
    def __repr__(self):
        return repr(self._title)

    def move_rules(self, board_obj, fut_row, fut_col):
        """horse piece move rules"""
        board = board_obj.get_board()
        board_len = len(board)
        board_width = len(board[0])
        row, col = fut_row, fut_col
        move_directions = [(0, 0), (2, 1), (2, -1), (-2, 1), (-2, -1), (1, -2), (1, 2), (-1, 2), (-1, -2)]

        # generate all possible moves
        for x,y in move_directions:
            self._move_map.append((self._row + x, self._col + y))

        # check if any moves are outside the game board:
        for ele in range(0, len(self._move_map)):
            for x,y in self._move_map:
                if board_len <= x or x < 0 or board_width < y or y < 0:
                    self._move_map.remove((x, y))
                    ele -= 1

        x = self._row   # chose non descriptive short variables because x, y are synonymous with coordinates and it
        y = self._col   # makes the lengthy comparisons more readable
        check_1 = x + 1
        check_2 = x - 1
        check_3 = y + 1
        check_4 = y - 1

        if check_1 < board_len:
            if board[check_1][y] != "-----":
                if board_len > x + 2 >= 0:
                    if board_width > y - 1 >= 0:
                        self._move_map.remove((x +2, y - 1))
                    if board_width > y + 1 >= 0:
                        self._move_map.remove((x + 2, y + 1))

        if check_2 >= 0:
            if board[check_2][self._col] != "-----":
                if board_len > x - 2 >= 0:
                    if board_width > y - 1 >= 0:
                        self._move_map.remove((x - 2, y - 1))
                    if board_width > y + 1 >= 0:
                        self._move_map.remove((x - 2, y + 1))

        if check_3 < board_width:
            if board[self._row][check_3] != "-----":
                if board_width > y + 2 >= 0:
                    if board_len > x + 1 >= 0:
                        self._move_map.remove((x + 1, y + 2))
                    if board_len > x - 1 >= 0:
                        self._move_map.remove((x - 1, y + 2))

        if check_4 >= 0:
            if board[self._row][check_4] != "-----":
                if board_width > y - 2 >= 0:
                    if board_len > x + 1 >= 0:
                        self._move_map.remove((x + 1, y - 2))
                    if board_len > x - 1 >= 0:
                        self._move_map.remove((x - 1, y - 2))

        for ele in self._move_map:
            if self._move_map:
                if (row, col) == ele:
                    return True
        self._move_map = []
        return False


class Chariot(Piece):
    """
    This class inherits the Piece class. It has an init method that overrides the parent class. All data members are
    private and must be accessed outside the class via getters and setters.
    """

    def __init__(self, board, title, team, row, col):
        """
        represents a Chariot game piece, it has inherited attributes from the parent class
        :param title: Chariot = "RC#" or "BC#"
        :param team: "red" or "blue
        :param row: y-coordinates
        :param col: x-coordinates
        """
        super().__init__(board, title, team, row, col)

    # __repr__ method shows objects attributes making it easier to debug
    def __repr__(self):
        return repr(self._title)

    def move_rules(self, board_obj, fut_row, fut_col):
        """chariot piece move rules"""
        board = board_obj.get_board()
        board_len = len(board)
        board_width = len(board[0])
        row, col = fut_row, fut_col
        y = 0
        i = 0
        # generate all possible moves
        for x in range(board_len):
            self._move_map.append((self._row + x, self._col + y))
            self._move_map.append((self._row - x, self._col + y))

        for j in range(board_width):
            self._move_map.append((self._row + i, self._col + j))
            self._move_map.append((self._row + i, self._col - j))

        # if piece is in the fortress invoke fortress moves
        blue_fortress = board_obj.get_blue_fortress()
        red_fortress = board_obj.get_red_fortress()
        if self._title in blue_fortress:
            self.fortress_rules(board_obj)
        if self._title in red_fortress:
            self.fortress_rules(board_obj)

        # check if any moves are outside the game board
        for ele in range(0, len(self._move_map)):
            for x, y in self._move_map:
                if board_len <= x or x < 0 or board_width < y or y < 0:
                    self._move_map.remove((x, y))
                    ele -= 1

        for ele in self._move_map:
            if self._move_map:
                if (row, col) == ele:
                    return True
        self._move_map = []
        return False

    def fortress_rules(self, board_obj):
        """when piece is inside the fortress invoke movement like a general"""
        direction = [(0, 0), (0, 1), (0, 2), (1, 0),(1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        board = board_obj.get_board()
        for x,y in direction:
            self._move_map.append((self._row + x, self._col + y))

        # remove any moves outside of the fortress
        for x, y in self._move_map:
            if board.get_board[x][y] not in board_obj.get_blue_fortress() or board_obj.get_red_fortress():
                self._move_map.remove((x, y))


class Elephant(Piece):
    """
    This class inherits the Piece class. It has an init method that overrides the parent class. All data members are
    private and must be accessed outside the class via getters and setters.
    """

    def __init__(self, board, title, team, row, col):
        """
        represents a Guard game piece, it has inherited attributes from the parent class
        :param title: Elephant = "RE#" or "BE#"
        :param team: "red" or "blue
        :param row: y-coordinates
        :param col: x-coordinates
        """
        super().__init__(board, title, team, row, col)
        self._block_map = []

    # __repr__ method shows objects attributes making it easier to debug
    def __repr__(self):
        return repr(self._title)

    def move_rules(self, board_obj, fut_row, fut_col):
        """Elephant piece move rules"""
        board = board_obj.get_board()
        board_len = len(board)
        board_width = len(board[0])
        row, col = fut_row, fut_col
        move_directions = [(0, 0), (3, 2), (3, -2), (-3, 2), (-3, -2), (2, -3), (2, 3), (-2, 3), (-2, -3)]
        block = [(1, 0), (-1, 0), (0, 1), (0, -1), (2,1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2),(-1, -2)]

        # generate all possible moves
        for x, y in move_directions:
            if board_len > self._row + x >= 0 and board_width > self._col + y >= 0:
                self._move_map.append((self._row + x, self._col + y))

        # check if any moves are blocked
        for x, y in block:
            if board_len > self._row + x >= 0 and board_width > self._col + y >= 0:
                if x == 1 and y == 0:
                    if board[self._row + x][self._col + y] != "-----":
                        self._block_map.append((self._row + 3, self._col + 2))
                        self._block_map.append((self._row + 3, self._col - 2))
                elif x == -1 and y == 0:
                    if board[self._row + x][self._col + y] != "-----":
                        self._block_map.append((self._row - 3, self._col + 2))
                        self._block_map.append((self._row - 3, self._col - 2))
                elif x == 0 and y == 1:
                    if board[self._row + x][self._col + y] != "-----":
                        self._block_map.append((self._row + 2, self._col + 3))
                        self._block_map.append((self._row - 2, self._col + 3))
                elif x == 0 and y == -1:
                    if board[self._row + x][self._col + y] != "-----":
                        self._block_map.append((self._row + 2, self._col - 3))
                        self._block_map.append((self._row - 2, self._col - 3))
                elif x == 2 and y == 1:
                    if board[self._row + x][self._col + y] != "-----":
                        self._block_map.append((self._row + 3, self._col + 2))
                elif x == 2 and y == - 1:
                    if board[self._row + x][self._col + y] != "-----":
                        self._block_map.append((self._row + 3, self._col - 2))
                elif x == - 2 and y == 1:
                    if board[self._row + x][self._col + y] != "-----":
                        self._block_map.append((self._row - 3, self._col + 2))
                elif x == - 2 and y == - 1:
                    if board[self._row + x][self._col + y] != "-----":
                        self._block_map.append((self._row - 3, self._col - 2))
                elif x == 1 and y == 2:
                    if board[self._row + x][self._col + y] != "-----":
                        self._block_map.append((self._row + 2, self._col + 3))
                elif x == 1 and y == - 2:
                    if board[self._row + x][self._col + y] != "-----":
                        self._block_map.append((self._row + 2, self._col - 3))
                elif x == - 1 and y == 2:
                    if board[self._row + x][self._col + y] != "-----":
                        self._block_map.append((self._row - 2, self._col + 3))
                elif x == - 1 and y == - 2:
                    if board[self._row + x][self._col + y] != "-----":
                        self._block_map.append((self._row - 2, self._col - 3))

        # remove any moves that can be blocked
        # elephant can move + 2 forward and + 3 diagonal so there are exactly 2 block positions for each possible move
        for ele in self._block_map:
            if ele in self._move_map:
                self._move_map.remove(ele)

        for ele in self._move_map:
            if self._move_map:
                if (row, col) == ele:
                    return True
        self._move_map = []
        return False


class Cannon(Piece):
    """
    This class inherits the Piece class. It has an init method that overrides the parent class. All data members are
    private and must be accessed outside the class via getters and setters.
    """

    def __init__(self, board, title, team, row, col):
        """
        represents a Cannon game piece, it has inherited attributes from the parent class
        :param title: Cannon = "RN#" or "BN#"
        :param team: "red" or "blue
        :param row: y-coordinates
        :param col: x-coordinates
        """
        super().__init__(board, title, team, row, col)

    # __repr__ method shows objects attributes making it easier to debug
    def __repr__(self):
        return repr(self._title)

    def move_rules(self, board_obj, fut_row, fut_col):
        """cannon piece move rules"""
        board = board_obj.get_board()
        board_len = len(board)
        board_width = len(board[0])
        row, col = fut_row, fut_col
        move_direction = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # generate all moves, cannons can only move if they are jumping over another piece, cannons can not jump
        # over another cannon
        for x,y in move_direction:
            check_x, check_y = self._row + x, self._col + y
            while board_len > check_x >= 0 and board_width > check_y >= 0 and board[check_x][check_y] == "-----":
                check_x, check_y = check_x + x, check_y + y
            after_jump = 0
            while board_len > check_x >= 0 and board_width > check_y >= 0:
                piece = board[check_x][check_y]
                if piece != "-----":
                    # we found an occupied space to jup over now lets see if the next space in on the board
                    if board_len > check_x + x >= 0 and board_width > check_y + y >= 0:
                        # the next position is on the board so before we start to move lets see if the occupant
                        # is a cannon
                        title = piece.get_title()
                        if title[1] != "N":
                            # occupant isn't a cannon so we add the move to the move map
                            check_x, check_y = check_x + x, check_y + y
                            self._move_map.append((check_x, check_y))
                            after_jump += 1
                        else:
                            after_jump = 0
                    check_x, check_y = check_x + x, check_y + y
                if piece == "-----":
                    if after_jump > 0:
                        self._move_map.append((check_x, check_y))
                        after_jump += 1
                    check_x, check_y = check_x + x, check_y + y

        # if piece is in the fortress invoke fortress moves
        blue_fortress = board_obj.get_blue_fortress()
        red_fortress = board_obj.get_red_fortress()
        if self._title in blue_fortress:
            self.fortress_rules(board_obj)
        if self._title in red_fortress:
            self.fortress_rules(board_obj)

        for ele in self._move_map:
            if self._move_map:
                if (row, col) == ele:
                    return True
        self._move_map = []
        return False

    def fortress_rules(self, board_obj):
        """when piece is inside the fortress invoke movement like a general"""
        move_direction = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0), (1, 1)]
        board = board_obj.get_board()
        board_len = len(board)
        board_width = len(board[0])

        for x,y in move_direction:
            check_x, check_y = self._row + x, self._col + y
            while board_len < check_x <= 0 and board_width < check_y <= 0 and board[check_x][check_y] == "-----":
                check_x, check_y = check_x + x, check_y + y
            while board_len < check_x <= 0 and board_width < check_y <= 0:
                if board[check_x][check_y] is not Cannon:
                    self._move_map.append((check_x, check_y))
                check_x, check_y = check_x + x, check_y + y

        # remove any moves outside of the fortress
        for x, y in self._move_map:
            if board[x][y] not in board_obj.get_blue_fortress() or board_obj.get_red_fortress():
                self._move_map.remove((x, y))


if __name__ == "__main__":
    g = JanggiGame()
    g.make_move("e9", "f8")

