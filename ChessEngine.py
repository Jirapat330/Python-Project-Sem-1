"""
This class is responsible for storing all the information about the current state of
a chess game. It will also be responsible for determining the valid moves at the current state.
It kill also keep a chess-move log (undo move, check opponent & your current moves)
"""


class GameState():
    """Chess board"""  # 2 dimensional-list  8x8 matrix

    def __init__(self):  # each list represent a row on the chess board
        # board is an 8x8 2d list, each element of the list has 2 characters
        # The first lowercase character represents the color of the piece, 'b' or 'w'
        # The second uppercase character represents the type of the piece, 'K', 'Q', 'R', 'B', 'N' or 'p'
        # "--" represents an empty space on chess board with no piece.
        # matrix state: Row (0-7) top to bottom, Column (0-7) Left to Right, start at (0, 0) Top Right corner
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]  # map each piece to a given function (dict) to simplify moves logic

        self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []

        #Keeping track of the Kings to make valid move calculation and castling easier.
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)

        #Keep track of checkmate and stalemate
        self.checkMate = False
        self.staleMate = False

    """
    Takes a Move as a parameter and executes it (this will not work for castling, pawn promotion and end-passant)
    """

    def makeMove(self, move):
        if self.board[move.startRow][move.startCol] != "--":  # Empty the start sq
            self.board[move.startRow][move.startCol] = "--"   # Keep the piece move on the end sq
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move)  # Log/record the move, "Or replay history of game"
            self.whiteToMove = not self.whiteToMove  # swap players turn
            # Update the King's location if moved
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.endRow, move.endCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.endRow, move.endCol)

    """
    Undo the last move made
    """

    def undoMove(self):
        if len(self.moveLog) == 0:  # Make sure that there is a move to undo
            print("Can't UNDO at the start of the game!")
            return
        move = self.moveLog.pop()
        self.board[move.startRow][move.startCol] = move.pieceMoved
        self.board[move.endRow][move.endCol] = move.pieceCaptured
        self.whiteToMove = not self.whiteToMove  # switch turns back
        #Update the KING's Position
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.startRow, move.startCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.startRow, move.startCol)
    """
    All moves with considering checks
    """

    def getValidMoves(self):
        #1) Get a List of all possible Moves
        moves = self.getAllPossibleMoves()
        #2) Make a move from the list of possible moves
        for i in range(len(moves)-1, -1, -1): # when removing elements from a list go backwards through that list
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
        #3) Generate all of the opponents move after making the move in the previous
        #4) Check if any of the opponents move attacks your king -> if so remove the moves from our list
            if self.inCheck():
                moves.remove(moves[i])
                print("Check White" if self.whiteToMove else "Check Black")
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        #5) Return the final list of moves
        if len(moves) == 0:     # either checkmate or stalemate
            if self.inCheck():
                print("CHECK MATE! " + ("White" if not self.whiteToMove else "Black") + " wins.")
                self.checkMate = True
            else:
                print("Draw, due to STALEMATE")
                self.staleMate = True

        else:
            self.checkMate = False
            self.staleMate = False

        return moves

    """
    Determine if the current player (Check if square (r,c) is under check) is in check.
    """
    def inCheck(self):
        if self.whiteToMove:
            return self.isUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.isUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    """
    Determine if the enemy can attack the square (r, c). Checks if sq (r,c) is under attack or not.
    """
    def isUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove     # switch to opponent's turn
        opponentMoves = self.getAllPossibleMoves()  # generate opponents move
        self.whiteToMove = not self.whiteToMove     # switch turns back
        for move in opponentMoves:
            if move.endRow == r and move.endCol == c:  # square under attack
                return True

        return False


    """
    Get a list of all possible moves, without considering CHECKS.
    """

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of columns in a given row
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  # calls the appropriate move function based on piece types.
        return moves

    """
    Get all the Pawn moves for the pawn located at (r,c) and add these moves to the list
    """

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  #------ White pawn moves ------#
            if self.board[r - 1][c] == "--":  # 1 square pawn advance
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r - 2, c), self.board))
            # captures
            if c-1 >= 0:  # Capture to the left (eats diagonally)
                if self.board[r - 1][c - 1][0] == "b":  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))

            if c+1 <= 7:  # Captures to the right (eats diagonally)
                if self.board[r - 1][c + 1][0] == "b":  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:  # black pawn moves
            if self.board[r + 1][c] == "--":  # 1 square move
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":  # 2 square pawn move
                    moves.append(Move((r, c), (r + 2, c), self.board))
            # captures
            if c-1 >= 0:  # Capture to the left (eats diagonally)
                if self.board[r + 1][c - 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))

            if c+1 <= 7:  # Captures to the right (eats diagonally)
                if self.board[r + 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
        # add pawn promotions later......

    """
      Get all the Rook moves for the pawn located at row, column and add these moves to the list
    """

    def getRookMoves(self, r, c, moves):
        # ---- Best way to implement this using coordinates ---- #
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right | define directions patterns
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):  # Rook can move up to 7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # is it on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # check when rook runs into a piece
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy piece valid move
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece invalid
                        break
                else:  # off board
                    break


    """
      Get all the Knight moves for the pawn located at row, column and add these moves to the list
    """

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for d in knightMoves:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # not an ally piece (empty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    # no need to check when Knight runs into a piece, since knight can jump over piece.

    """
      Get all the Bishop moves for the pawn located at row, column and add these moves to the list
    """

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # 4 diagonals
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):  # bishop can move 7 squares maximum
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # make sure if on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # check when rook runs into a piece
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy piece valid move
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece invalid
                        break
                else:  # off board
                    break

    """
      Get all the Queen moves for the pawn located at row, column and add these moves to the list
    """

    # Bishop x Rook combined, smart method
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    """
      Get all the King moves for the pawn located at row, column and add these moves to the list
    """

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # not an ally piece (empty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))


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
