import random

# A map of piece to score value -> Standard chess scores
pieceScore = {"K": 0, "p": 1, "N": 3, "B": 3, "R": 5, "Q": 9} # making King = 0, as no one can capture the King
CHECKMATE = 1000 # if you lead to checkmate, you'll win -> hence max attainable score
STALEMATE = 0   # If you can win(capture opponent's piece) avoid it but if you loosing(opponent can give you Checkmate) try it hence 0 and not -1000


"""
Function to calculate Random move from the list of valid moves.
"""
def findRandomMove(validMoves):
    return random.choice(validMoves)

"""
Function to find the Best move based on the list of valid moves
"""
def findBestMove(game_state, validMoves):
    turnMultiplier = 1 if game_state.whiteToMove else -1 # for allowing AI to play as any color
    playerMaxScore = -CHECKMATE
    bestMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
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

