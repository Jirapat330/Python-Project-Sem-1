"""
This class is responsible for storing all the information about the current state of
a chess game. It will also be responsible for determining the valid moves at the current state.
It also keep a chess-move log (undo move, check opponent & your current moves)
"""


class GameState():
    """Chess board"""  # 2 dimensional-list  8x8 matrix

    def __init__(self):  # each list represent a row on the chess board
        # board is an 8x8 2d list, each element of the list has 2 characters
        # The First lowercase character represents the color of the piece, ('b' or 'w')
        # The Second uppercase character represents the Type of the piece, ('K', 'Q', 'R', 'B', 'N' or 'p')
        # "--" represents an Empty space on chess board with no piece.
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
        self.moveLog = []
        self.whiteToMove = True
        # Keeping track of the Kings to make valid move calculation and castling easier.
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        # Keep track of checkmate and stalemate
        self.checkmate = False
        self.stalemate = False
        self.enPassantPossible = ()  # coordinates for the square where en-passant capture is possible


        # Castling
        self.currentCastlingRights = CastleRights(True, True, True, True)
        # self.castleRightsLog = [self.currentCastlingRights] # this will pose a problem as we are not copying the
        # self.currentCastlingRights object we are just storing another reference to it.
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.wqs,
                                             self.currentCastlingRights.bks, self.currentCastlingRights.bqs)]

    """
    A function to move pieces on the board and record it (this will not work for castling, pawn promotion and end-passant)
    """

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"  # --Empty the start sq--#
        self.board[move.endRow][move.endCol] = move.pieceMoved  # Keep the piece move on the end sq
        self.moveLog.append(move)  # Log/record the move, "Or replay history of game"
        self.whiteToMove = not self.whiteToMove  # swap the turn
        # Update the King's Position if moved
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        # ----Pawn Promotion----#
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + "Q"  # Hardcode for now, add options later

        # ----En-Passant---- #
        if move.enPassant:
            self.board[move.startRow][move.endCol] = "--"  # Capturing the pawn

        # ----Update enPassantPossible variable---- #
        # if pawn moves twice, next move can capture enpassant
        if move.pieceMoved[1] == "p" and abs(move.startRow - move.endCol) == 2:  # only on 2 square pawn advance
            self.enPassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enPassantPossible = ()

        # ---Castle Move--- #
        if move.isCastleMove:
            if move.endCol < move.startCol:  # Queen side castle (left)
                self.board[move.endRow][0] = "--" # erase old rook
                self.board[move.endRow][move.endCol + 1] = move.pieceMoved[0] + "R" # move the rook
            else:  # King side castle (right)
                self.board[move.endRow][7] = "--" # erase old rook
                self.board[move.endRow][move.endCol - 1] = move.pieceMoved[0] + "R" # move the rook

        # self.enPassantPossible.append(self.enPassantPossible)

        # ---Update Castling Rights--- #
        self.updateCastleRights(move)
        newCastleRights = CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.wqs,
                                       self.currentCastlingRights.bks, self.currentCastlingRights.bqs)
        self.castleRightsLog.append(newCastleRights)



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

        # ---Update the KING's Position--- #
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.startRow, move.startCol)
        if move.pieceMoved == "bK":
            self.blackKingLocation = (move.startRow, move.startCol)

        # ---Undo En-Passant move--- #
        if move.enPassant:
            self.board[move.endRow][move.endCol] = "--"  # removes the pawn that was added in the wrong square
            self.board[move.startRow][move.endCol] = move.pieceCaptured # puts the pawn back on the correct square it was captured from
            self.enPassantPossible = (move.endRow, move.endCol)

        # UNDO a 2 sq pawn advance
        if move.pieceMoved[1] == 'P' and abs(move.endRow - move.startRow) == 2:
            self.enPassantPossible = ()

        # ---Undo Castling Rights--- #
        self.castleRightsLog.pop()  # get rid of new Castling rights from the move we are undoing
        self.currentCastlingRights.wks = self.castleRightsLog[-1].wks # set the current castle rights to the last one in the list
        self.currentCastlingRights.wqs = self.castleRightsLog[-1].wqs # update current castling right
        self.currentCastlingRights.bks = self.castleRightsLog[-1].bks # update current castling right
        self.currentCastlingRights.bqs = self.castleRightsLog[-1].bqs # update current castling right

        # ----Undo Castling Move---- #
        if move.isCastleMove:
            if move.endCol < move.startCol:  # Queen side castle (left)
                self.board[move.endRow][move.endCol + 1] = "--" # remove rook
                self.board[move.endRow][0] = move.pieceMoved[0] + "R" # replace rook
            else:  # King side castle (right)
                self.board[move.endRow][move.endCol - 1] = "--" # remove rook
                self.board[move.endRow][7] = move.pieceMoved[0] + "R" # replace rook

        # Set checkmate and stalemate false again
        self.checkmate = False
        self.stalemate = False

    """
    Updating the castle rights given the move >> when it's a Rook or a King Move
    """

    def updateCastleRights(self, move):
        # If King or Rook is Moved
        if move.pieceMoved == "wK":
            self.currentCastlingRights.wqs = False
            self.currentCastlingRights.wks = False

        elif move.pieceMoved == "bK":
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False

        elif move.pieceMoved == "wR":
            if move.startRow == 7 and move.startCol == 0:  # Left Rook
                self.currentCastlingRights.wqs = False
            if move.startRow == 7 and move.startCol == 7:  # Right Rook
                self.currentCastlingRights.wks = False

        elif move.pieceMoved == "bR":
            if move.startRow == 0 and move.startCol == 0: # Left Rook
                self.currentCastlingRights.bqs = False
            if move.startRow == 0 and move.startCol == 7: # Right Rook
                self.currentCastlingRights.bks = False

    # ---------if a Rook is captured----------- #
            if move.pieceCaptured == 'wR':
                if move.endRow == 7:
                    if move.endCol == 0:
                        self.currentCastlingRights.wqs = False
                    elif move.endCol == 7:
                        self.currentCastlingRights.wks = False
            elif move.pieceCaptured == 'bR':
                if move.endRow == 0:
                    if move.endCol == 0:
                        self.currentCastlingRights.bqs = False
                    elif move.endCol == 7:
                        self.currentCastlingRights.bks = False

    """
    Get a list of all the valid moves -> the moves that user can actually make. => All moves with considering checks
    """

    def getValidMoves(self):
        #----Castle rights test terminal
        # for log in self.castleRightsLog:
        #     print(log.wks, log.wqs, log.bks, log.bqs, end=", ")
        # print()
        tempEnpassantPossible = self.enPassantPossible
        tempCastlingRights = self.currentCastlingRights #copy current castling rights
        # 1) Get a List of all possible Moves
        moves = self.getAllPossibleMoves()
        currentKingLocation = self.whiteKingLocation if self.whiteToMove else self.blackKingLocation
        self.getCastlingMoves(currentKingLocation[0], currentKingLocation[1], moves)
        # ---Other way of implementing this
        # if self.whiteToMove:
        #     self.getCastlingMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        # else:
        #     self.getCastlingMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        # ----2) Make a move from the list of possible moves---- #
        for i in range(len(moves)-1, -1, -1):  # when removing elements from a list go backwards through that list
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            # 3) Generate all of the opponents move after making the move in the previous
            # 4) Check if any of the opponents move attacks your king -> if so remove the moves from our list
            if self.inCheck():
                moves.remove(moves[i])
                # print("Check White" if self.whiteToMove else "Check Black")
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        # 5) Return the final list of moves
        if len(moves) == 0:  # either checkmate or stalemate
            if self.inCheck():
                self.checkmate = True
                if self.whiteToMove:
                    print("CheckM8: Player 2 wins!!")
                else:
                    print("CheckM8: Player 1 wins!!")
            else:
                self.stalemate = True
                print("DRAW!! Stalemate", end=", ")
                if self.whiteToMove:
                    print("White Does Not have Moves")
                else:
                    print("Black Does Not have Moves")
        else:
            self.checkmate = False
            self.stalemate = False

        self.enPassantPossible = tempEnpassantPossible
        self.currentCastlingRights = tempCastlingRights
        return moves

    """
    Determine if the current player (Check if sq (r,c) is under check) is in check.
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
        self.whiteToMove = not self.whiteToMove  # switch to opponent's turn
        opponentMoves = self.getAllPossibleMoves()  # generate opponents move
        self.whiteToMove = not self.whiteToMove  # switch turns back
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
                piece = self.board[r][c][1]
                # if piece != "--":
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    self.moveFunctions[piece](r, c, moves)  # calls the appropriate move function based on piece types.
        return moves

    """
    Get all the Pawn moves for the pawn located at (r,c) and add these moves to the list
    """

    def getPawnMoves(self, r, c, moves):
        # ------ White pawn moves ------#
        if self.whiteToMove and self.board[r][c][0] == "w":
            if self.board[r - 1][c] == "--":  # 1 square pawn advance
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r - 2, c), self.board))
            # captures
            if c - 1 >= 0:  # Capture to the left (diagonally)
                if self.board[r - 1][c - 1][0] == "b":  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif self.enPassantPossible == (r - 1, c - 1):
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, enPassant=True))

            if c + 1 <= 7:  # Captures to the right (diagonally)
                if self.board[r - 1][c + 1][0] == "b":  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif self.enPassantPossible == (r - 1, c + 1):
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, enPassant=True))

        # -----black pawn moves-----#
        if not self.whiteToMove and self.board[r][c][0] == 'b':  # BLACK PAWN MOVES
            if self.board[r + 1][c] == "--":  # 1 square move
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":  # 2 square pawn move
                    moves.append(Move((r, c), (r + 2, c), self.board))
            # captures
            if c - 1 >= 0:  # Capture to the left (diagonally)
                if self.board[r + 1][c - 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif self.enPassantPossible == (r + 1, c - 1):
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, enPassant=True))

            if c + 1 <= 7:  # Captures to the right (diagonally)
                if self.board[r + 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif self.enPassantPossible == (r + 1, c + 1):
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, enPassant=True))

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
                        break  # same color piece
                else:
                    break  # off board

    """
      Get all the Knight moves for the pawn located at row, column and add these moves to the list
    """

    def getKnightMoves(self, r, c, moves):
        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # not an ally piece (empty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    # no need to check when Knight runs into a piece, since knight can jump over piece.

    """
      Get all the Bishop moves for the pawn located at row, column and add the moves to the list
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
                        break  # same color piece
                else:
                    break  # off board

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
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"  # ally color according to current turn
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # not an ally piece (empty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))


    """ 
    Get all the valid castling move for the king at row, column and add them to the list of moves
    """
    def getCastlingMoves(self, r, c, moves):
        if self.inCheck():
            return  # can't castle when king is under attack

        if self.whiteToMove and self.currentCastlingRights.wks or \
                (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingSideCastleMoves(r, c, moves)

        if self.whiteToMove and self.currentCastlingRights.wqs or \
                (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQueenSideCastleMoves(r, c, moves)

    def getKingSideCastleMoves(self, r, c, moves):
        if self.board[r][c + 1] == "--" and self.board[r][c + 2] == "--":
            if not self.isUnderAttack(r, c + 1) and not self.isUnderAttack(r, c + 2):
                moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove=True))

    def getQueenSideCastleMoves(self, r, c, moves):
        if self.board[r][c - 1] == "--" and self.board[r][c - 2] == "--" and self.board[r][c - 3] == "--":
            if not self.isUnderAttack(r, c - 1) and not self.isUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))


class CastleRights():
    def __init__(self, wks, wqs, bks, bqs):
        self.wks = wks
        self.wqs = wqs
        self.bks = bks
        self.bqs = bqs

    """ Overloading the __str__ function to print the Castling Rights Properly"""
    def __str__(self):
        return ("Castling Rights(wk, wq, bk, bq): " + str(self.wks) + " " + str(self.wqs)
                + " " + str(self.bks) + " " + str(self.bqs))


class Move():
    """Chess Moves"""  # keep track of each information, grab data from board
    # dictionary to map keys to values
    # key : value
    # For converting (row, col) to Chess Notations => (0,0) -> a8
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, enPassant=False, pawnPromotion=False, isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]  # keep track of what pieces are moved, can't be '--'
        self.pieceCaptured = board[self.endRow][self.endCol]  # keep track of what pieces was captured, can be '--' > no piece was captured

        # ----Pawn Promotion----#
        self.pawnPromotion = pawnPromotion
        self.isPawnPromotion = (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bP" and self.endRow == 7)

        # ---En-Passant--- #
        self.enPassant = enPassant
        if self.enPassant:
            self.pieceCaptured = "bp" if self.pieceMoved == "wp" else "wp" #enpassant captures opposite colored pawn

        # ---CastleMove--- #
        self.isCastleMove = isCastleMove

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def GetChessNotation(self):
        # you can add to make this like real chess notation, we will just record the squares in rank/file notation
        return self.GetRankFile(self.startRow, self.startCol) + self.GetRankFile(self.endRow, self.endCol)

    def GetRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    """
    Overriding equal to method
    """

    def __eq__(self, other):  # comparing objects to the other objects
        return isinstance(other, Move) and self.moveID == other.moveID








