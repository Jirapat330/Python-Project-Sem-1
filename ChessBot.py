import random


def findRandomMove(validMoves):
    return random.choice(validMoves)

def findBestMove(game_state, validMoves):
    return