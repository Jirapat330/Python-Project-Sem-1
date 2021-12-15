import random

# A map of piece to score value -> Standard chess scores
pieceScore = {"K": 0, "p": 1, "N": 3, "B": 3, "R": 5, "Q": 10}  # making King = 0, as no one can capture the King

knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],  # The Knight at the center of the board is better than being position
                [1, 2, 3, 4, 4, 3, 2, 1],  # outside of the board, since it can reach more squares.
                [1, 2, 3, 3, 3, 3, 2, 1],  # AI will consider the higher value as a better move. Because it can attack more squares
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

queenScores = [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]]

rookScores = [[4, 3, 4, 4, 4, 4, 3, 4],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [4, 3, 4, 4, 4, 4, 3, 4]]

whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [1, 2, 3, 3, 2, 2, 1, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 2, 3, 3, 2, 2, 1, 1],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8]]

piecePositionScores = {"N": knightScores, "Q": queenScores, "B": bishopScores,
                       "R": rookScores, "wp": whitePawnScores, "bp": blackPawnScores}

CHECKMATE = 1000  # if you lead to checkmate, you'll win -> hence max attainable score
STALEMATE = 0  # If you can win(capture opponent's piece) avoid it but if you loosing(opponent can give you Checkmate) try it hence 0 and not -1000
DEPTH = 2  # Depth for recursive calls

"""
Function to calculate Random move from the list of valid moves.
"""


def findRandomMove(validMoves):
    return random.choice(validMoves)


"""
Function to find the move based on the list of valid moves
"""


# Simple Algorithm, not in use anymore...
def findBestMoveMinMaxNoRecursion(game_state, validMoves):
    turnMultiplier = 1 if game_state.whiteToMove else -1  # for allowing AI to play as any color
    playerMaxScore = -CHECKMATE  # as AI is playing Black this is the worst possible score -> AI will start from worst and try to improve
    bestMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:  # not assigning colors so AI can play as both: playerMove -> move of the current player || opponentMove -> opponent's move
        game_state.makeMove(playerMove)
        opponentMinScore = CHECKMATE
        opponentMoves = game_state.getValidMoves()
        if game_state.checkmate:
            game_state.undoMove()
            return playerMove
        elif game_state.stalemate:
            opponentMinScore = STALEMATE
        else:
            for opponentMove in opponentMoves:
                game_state.makeMove(opponentMove)
                game_state.getValidMoves()
                if game_state.checkmate:
                    score = -CHECKMATE
                elif game_state.stalemate:
                    score = STALEMATE
                else:
                    score = turnMultiplier * scoreMaterial(game_state.board)
                if score < opponentMinScore:
                    opponentMinScore = score
                game_state.undoMove()
        if playerMaxScore < opponentMinScore:
            playerMaxScore = opponentMinScore
            bestMove = playerMove
        game_state.undoMove()
        return bestMove


"""
Helper method to call recursion for the 1st time
"""


def findBestMove(game_state, validMoves):
    global nextMove, counter
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    findMoveNegaMaxAlphaBeta(game_state, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if game_state.whiteToMove else -1)  # For using Nega Max Algorithm with Alpha Beta Pruning
    # findMoveNegaMax(game_state, validMoves, DEPTH, 1 if game_state.whiteToMove else -1)     # For using Nega Max Algorithm
    # findMoveMinMax(game_state, validMoves, DEPTH, game_state.whiteToMove)     # For using Min-Max Algorithm

    print(counter)
    return nextMove


'''
 Find the best move based on material itself
'''


def findMoveMinMax(game_state, validMoves, depth, whiteToMove):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return scoreMaterial(game_state.board)

    if whiteToMove:  # Try to maximize score
        maxScore = -CHECKMATE
        for move in validMoves:
            game_state.makeMove(move)
            nextMoves = game_state.getValidMoves()
            score = findMoveMinMax(game_state, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            game_state.undoMove()
        return maxScore

    else:  # Try to minimize score
        minScore = CHECKMATE
        for move in validMoves:
            game_state.makeMove(move)
            nextMoves = game_state.getValidMoves()
            score = findMoveMinMax(game_state, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            game_state.undoMove()
        return minScore


# compared to findbestmoveMinMaxNoRecursion is making a move getting our opponents move scoring that board finding the min-max
# findbestmoveMinMaxNoRecursion can go only in depth 1, but with this method. The algorithm can now look as many moves ahead as we want since we've set the depth parameters

"""
Best Move Calculator using NegaMax Algorithm
"""


def findMoveNegaMax(game_state, validMoves, depth, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(game_state)

    maxScore = -CHECKMATE
    for move in validMoves:
        game_state.makeMove(move)
        nextMoves = game_state.getValidMoves()
        score = -findMoveNegaMax(game_state, nextMoves, depth - 1, -turnMultiplier)  # negative for NEGA Max
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        game_state.undoMove()
    return maxScore


"""
Best Move Calculator using NegaMax Algorithm along with Alpha Beta Pruning
"""


def findMoveNegaMaxAlphaBeta(game_state, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(game_state)

    # Move ordering - implement later
    maxScore = -CHECKMATE
    for move in validMoves:
        game_state.makeMove(move)
        nextMoves = game_state.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(game_state, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)  # negative for NEGA Max
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        game_state.undoMove()
        if maxScore > alpha:  # pruning happens
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


"""
better scoring algorithm with considering checks and stalemates.
+ positive score is good for white, - negative score is good for black ( when Human = White & AI = Black)
"""

# ----- AI scoring basic(works with every algorithms / fast) -----#
def scoreBoard(game_state):
    if game_state.checkmate:
        if game_state.whiteToMove:
            return -CHECKMATE   # BLACK WINS
        else:
            return CHECKMATE
    if game_state.stalemate:
        return STALEMATE

    score = 0
    for row in game_state.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score

# ----- AI scoring for NegaMax & NegaMaxBeta, smarter algorithm (Involved piecePositionScores) -----#
# def scoreBoard(game_state):
#     if game_state.checkmate:
#         if game_state.whiteToMove:
#             return -CHECKMATE  # Black wins
#         else:
#             return CHECKMATE  # White wins
#     if game_state.stalemate:
#         return STALEMATE
#
#     score = 0
#     for row in range(len(game_state.board)):  # len = 8
#         for col in range(len(game_state.board[row])):
#             square = game_state.board[row][col]
#             if square != "--":
#                 # score it positionally based on what type of piece it is
#                 piecePositionScore = 0
#                 if square[1] != "K":  # no position table for king
#                     if square[1] == "p":  # for pawns
#                         piecePositionScore = piecePositionScores[square][row][col]
#                     else:  # for other pieces
#                         piecePositionScore = piecePositionScores[square[1]][row][col]
#
#                 if square[0] == "w":
#                     score += pieceScore[square[1]] + piecePositionScore * 0.1  # 0.1 to make the game less positional
#                 elif square[0] == "b":
#                     score -= pieceScore[square[1]] + piecePositionScore * 0.1
#
#     return score


"""
Gives the score of the board according to the material on it -> White piece positive material and Black piece negative material.
Assuming that Human is playing White and BOT is playing black
"""


def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += pieceScore[square[1]]
            elif square[0] == "b":
                score -= pieceScore[square[1]]
    return score
