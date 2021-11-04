"""
This class is responsible for storing all the information about the current state of
a chess game. It will also be responsible for determining the valid moves at the current state.
It kill also keep a chess-move log (undo move, check opponent & your current moves)
"""


class GameState():
    """Chess board"""  # 2 dimensional-list  8x8 matrix

    def __init__(self):  # each list represent a row on the chess board
        # board is an 8x8 2d list, each element of the list has 2 characters
        # The first character represents the color of the piece, 'b' or 'w'
        # The second character represents the type of the piece, 'K', 'Q', 'R', 'B', 'N' or 'p'
        # "--" represents an empty space on chess board with no piece.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "wR", "--", "--", "bB", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]                             # map each piece to a given function (dict) to simplify moves logic

        self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []

    """
    Takes a Move as a parameter and executes it (this will not work for castling, pawn promotion and end-passant)
    """

    def makeMove(self, move):
        if self.board[move.startRow][move.startCol] != "--":
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move)  # Log the move so we can undo it later, "Or replay history of game"
            self.whiteToMove = not self.whiteToMove  # swap players

    """
    Undo the last move made
    """

    def undoMove(self):
        if len(self.moveLog) != 0:  # Make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turns back

    """
    All moves with considering checks
    """

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    """
    All moves without considering checks
    """

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of columns in a given row
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) # calls the appropriate move function based on piece types.
        return moves

    """
    Get all the Pawn moves for the pawn located at row, column and add these moves to the list
    """

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  ######## White pawn moves ############
            if self.board[r-1][c] == "--":  # 1 square pawn advance
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r-2, c), self.board))

            if c - 1 >= 0:      # Capture to the left (eats diagonally)
                if self.board[r-1][c-1][0] == "b":      # enemy piece to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))

            if c + 1 <= 7:      # Captures to the right (eats diagonally)
                if self.board[r-1][c+1][0] == "b":      # enemy piece to capture
                    moves.append(Move((r, c), (r-1, c+1), self.board))

        else: # black pawn moves
                if self.board[r + 1][c] == "--":  # 1 square move
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if r == 1 and self.board[r + 2][c] == "--":  # 2 square pawn move
                        moves.append(Move((r, c), (r + 2, c), self.board))

                if c - 1 >= 0:  # Capture to the left (eats diagonally)
                    if self.board[r + 1][c - 1][0] == "w":
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))

                if c + 1 <= 7:  # Captures to the right (eats diagonally)
                    if self.board[r + 1][c + 1][0] == "w":
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))



    """
      Get all the Rook moves for the pawn located at row, column and add these moves to the list
    """

    def getRookMoves(self, r, c, moves):
        pass

    """
      Get all the Knight moves for the pawn located at row, column and add these moves to the list
    """

    def getKnightMoves(self, r, c, moves):
        pass

    """
      Get all the Bishop moves for the pawn located at row, column and add these moves to the list
    """

    def getBishopMoves(self, r, c, moves):
        pass

    """
      Get all the Queen moves for the pawn located at row, column and add these moves to the list
    """

    def getQueenMoves(self, r, c, moves):
        pass

    """
      Get all the King moves for the pawn located at row, column and add these moves to the list
    """

    def getKingMoves(self, r, c, moves):
        pass


class Move():
    """Chess Moves"""  # keep track of each information, grab data from board
    # dictionary to map keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]  # keep track of what pieces are moved
        self.pieceCaptured = board[self.endRow][self.endCol]  # keep track of what pieces are being captured
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


    """
    Overriding the equals method
    """

    def __eq__(self, other):  # comparing objects to the other objects
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def GetChessNotation(self):
        # you can add to make this like real chess notation
        return self.GetRankFile(self.startRow, self.startCol) + self.GetRankFile(self.endRow, self.endCol)

    def GetRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
