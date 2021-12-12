"""
This is our main driver file. It will be responsible for handling user input
and displaying the current Game state
"""

import pygame as p
from Chess import ChessEngine
import ChessBot

p.init()

WIDTH = HEIGHT = 800  # 512, 400 another option
DIMENSION = 8  # dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION  # 100 x 100px per SQ , Image size <= 100, Canvas size <= 100
MAX_FPS = 15  # for animations
IMAGES = {}

# loading Images .png, own method instead of putting in main. To support picking
# couple different chess sets options later on.
"""
Initialize a global dictionary of images. This will be called exactly once in the main
"""


# Manual image load
# IMAGES["wp"] = p.transform.scale(p.image.load("White piece/wK.png"), (SQ_SIZE, SQ_SIZE))

def loadImages():
    white_chess_pieces = ["wp", "wR", "wN", "wB", "wQ", "wK"]
    for piece in white_chess_pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("White piece/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # Note: access an image by using 'IMAGES['wp']'-> return white pawn image.
    # Change image directory in 'images/'
    # IMAGES["wp"] = p.transform.scale(p.image.load("White piece/wQ.png"), (SQ_SIZE, SQ_SIZE))

    black_chess_pieces = ["bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in black_chess_pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Black piece/" + piece + ".png"),
                                          (SQ_SIZE, SQ_SIZE))  # p.transform.scale(p.image>>>,(SQ_SIZE,SQ_SIZE)
    # Note: access an image by using 'IMAGES['bp']'
    # Change image directory in 'images/'

    # black_chess_pieces = ["bp", "bR", "bN", "bB", "bQ", "bK"]
    # for piece in black_chess_pieces:
    #     IMAGES[piece] = p.transform.scale(p.image.load("Black piece/" + piece + ".png"),
    #                                       (SQ_SIZE, SQ_SIZE))  # p.transform.scale(p.image>>>,(SQ_SIZE,SQ_SIZE)


def images(screen):
    ############ Load on-screen images ######################
    Kmitl = (p.image.load("Logo/KMITL-GO 200px.png"))
    screen.blit(Kmitl, (800, 0))
    FE = (p.image.load("Logo/FE Logo fix.png"))
    screen.blit(FE, (800, 30))


"""
This will be out main driver. This will handle user input and update the graphics
"""


############### This will be out main driver. It will handle user input and update the graphics. Add in later, menu, image, displaying move-log on RHS.######################
def main():
    # p.mixer.pre_init(44100, -16, 2, 2048)  # setup mixer to avoid sound lag
    p.mixer.init()  # Music mixer
    playlist = list()  # Music playlist
    playlist.append("music/4. FKJ - Just Piano (mp3cut.net).mp3")  # 5
    playlist.append("music/3. Giorno's Theme in the style of JAZZ (mp3cut.net).mp3")  # 4
    playlist.append("music/2. FKJ - Ylang Ylang (mp3cut.net).mp3")  # 3
    playlist.append("music/1. FKJ - Die With A Smile (mp3cut.net).mp3")  # 2
    # playlist.append("music/Wii.mp3")  # 1
    p.mixer.music.load(playlist.pop())  # Get the first track from the playlist
    p.mixer.music.queue(playlist.pop())  # Queue the 2nd song
    p.mixer.music.set_endevent(p.USEREVENT)  # Setup the end track event
    p.mixer.music.set_volume(1)
    p.mixer.music.play()
    p.event.wait()

    ############# Main Chess ui : Display screen #################
    screen = p.display.set_mode((1000, HEIGHT))  # (0,0) top left >>> (1000,800) bottom right
    p.display.set_caption("|ChessM8| Checkmate Chess beta 1.0_by: Jirapat_Wongjaroenrat")
    clock = p.time.Clock()
    screen.fill(p.Color("grey"))
    game_state = ChessEngine.GameState()  # Calls _init_ from ChessEngine
    validMoves = game_state.getValidMoves()
    moveMade = False  # flag variable for when a move is made
    animate = False  # flag variable for when we should animate a move

    loadImages()  # do this once, before while loop
    images(screen)  # load def images, before game loop

    running = True
    sqSelected = ()  # no square is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = []  # keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    gameOver = False

    # ------- Choosing GAME MODE ---------#
    Player_One_Human = True # If a Human is playing white, then this will be True. If AI is playing, then this will be False
    Player_Two_Human = True  # Same as above
    # ----------------------------------- #
    if Player_One_Human and not Player_Two_Human:
        gameMode(screen, "Player 1 VS Bot")
    elif Player_Two_Human and not Player_One_Human:
        gameMode(screen, "Player 2 VS Bot")
    elif Player_One_Human and Player_Two_Human:
        gameMode(screen, "Player 1 VS Player 2")
    else:
        gameMode(screen, "Bot VS Bot")

    ############# Game driver : Don't touch ##############
    while running:
        humanTurn = (game_state.whiteToMove and Player_One_Human) or (not game_state.whiteToMove and Player_Two_Human)

        for event in p.event.get():
            if event.type == p.QUIT:  # ---- Event -----#
                running = False

            elif event.type == p.USEREVENT:  # A track has ended
                if len(playlist) > 0:  # If there are more tracks in the queue...
                    p.mixer.music.queue(playlist.pop())  # queue next song in list

            ########## Mouse Handlers: User input ################
            elif event.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()  # (x, y) location of mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if (col >= 8) or col < 0:  # Click out of board (on move log panel) -> do nothing
                        continue
                    if sqSelected == (row, col):  # the user clicked the same square twice
                        sqSelected = ()  # deselect
                        playerClicks = []  # contains players clicks => [(6,4),(4,4)]  -> pawn at (6,4) moved 2 steps up on (4,4)
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)  # append for both 1st and 2nd clicks
                        # ----- print out players move log-------#
                        if len(playerClicks) == 2:  # after 2nd click
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], game_state.board)
                            print(move.GetChessNotation())
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    game_state.makeMove(validMoves[i])
                                    moveMade = True
                                    animate = True
                                    sqSelected = ()  # reset user clicks
                                    playerClicks = []
                            if not moveMade:  # Use if not instead of else: to prevent bugs
                                playerClicks = [sqSelected]

            # ------key handlers Key Press------ #
            elif event.type == p.KEYDOWN:
                if event.key == p.K_z:  # UNDO when "z" is being pressed
                    game_state.undoMove()
                    moveMade = True
                    animate = False
                if event.key == p.K_r:  # RESET the board when "R" is pressed
                    game_state = ChessEngine.GameState()
                    validMoves = game_state.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
        # AI Move finder logic
        if not gameOver and not humanTurn:
            AIMove = ChessBot.findRandomMove(validMoves)
            game_state.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMoves(game_state.moveLog[-1], screen, game_state.board, clock)
            validMoves = game_state.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, game_state, validMoves, sqSelected)

        if game_state.checkmate:
            gameOver = True
            if game_state.whiteToMove:
                drawText(screen, "Black wins by checkmate")
            else:
                drawText(screen, "White wins by checkmate")

        elif game_state.stalemate:
            gameOver = True
            drawText(screen, "STALEMATE DRAW")

        clock.tick(MAX_FPS)
        p.display.flip()
        p.display.update()


"""
Highlight square selected and moves for piece selected
"""


def highlightSquares(screen, game_state, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        # sqSelected is a piece that can be moved
        if game_state.board[r][c][0] == ("w" if game_state.whiteToMove else "b"):
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(220)  # transparency value -> 0 transparent; 255 opaque
            s.fill(p.Color("blue"))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            # highlight moves from that square
            s.fill(p.Color("yellow"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))


#
"""
Responsible for all the graphics within a current game state
"""


# ---- add in chess piece highlighting, move suggestions later -----#

def drawGameState(screen, game_state, validMoves, sqSelected):
    drawBoard(screen)  # draw squares on the board (should be called before drawing anything else)
    highlightSquares(screen, game_state, validMoves, sqSelected)
    drawPieces(screen, game_state.board)  # draw piece on top of the squares


"""
Draw the squares on the board. (Top Left square is always white)
"""


def drawBoard(screen):  # white (even), r = 2.  black (odd), r = 1
    global colors
    colors = [p.Color("#E35205"), p.Color("white")]  # KMITL Hex color #E35205, white
    for r in range(DIMENSION):  # r = row , c = coluom
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


"""
Draw the pieces on the board using the current GameState.board
"""


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # not empty square
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


"""
Animate a move transition between square selected
"""


def animateMoves(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framePerSquare = 10  # frames to move 1 square
    frameCount = (abs(dR) + abs(dC)) * framePerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # ---erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # ---draw captured piece onto rectangle
        if move.pieceCaptured != "--":
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # ---draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 70, True, True)
    textObject = font.render(text, 0, p.Color("White"))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObject.get_width() / 2,
                                                    HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Black"))
    screen.blit(textObject, textLocation.move(2, 2))

    shadow = p.font.SysFont("Arial", 30, True, True)
    textObject2 = shadow.render("Thanks for playing!!", True, p.Color("Grey"))
    screen.blit(textObject2, (300, 470))
    font2 = p.font.SysFont("Arial", 30, True, True)
    textObject2 = font2.render("Thanks for playing!!", True, p.Color("Red"))
    screen.blit(textObject2, (302, 472))


def gameMode(screen, text):
    mode = p.font.SysFont("Arial", 20, True, False)
    textObject3 = mode.render("||-GameMode-||", True, p.Color("Black"))
    screen.blit(textObject3, (820, 650))

    font3 = p.font.SysFont("Arial", 18, True, False)
    textObject4 = font3.render(text, True, p.Color("Brown"))
    screen.blit(textObject4, (825, 680))


if __name__ == "__main__":
    main()
