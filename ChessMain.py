"""
This is our main driver file. It will be responsible for handling user input
and displaying the current Game state
"""

import pygame as p
from Chess import ChessEngine

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


def loadImages():
    white_chess_pieces = ["wp", "wR", "wN", "wB", "wQ", "wK"]
    for piece in white_chess_pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("White piece/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # Note: access an image by using 'IMAGES['wp']', return wp image. Check draw image not blank
    # Change image directory in 'images/'

    black_chess_pieces = ["bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in black_chess_pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Black piece/" + piece + ".png"),
                                          (SQ_SIZE, SQ_SIZE))  # p.transform.scale(p.image>>>,(SQ_SIZE,SQ_SIZE)
    # Note: access an image by using 'IMAGES['bp']'
    # Change image directory in 'images/'


def images(screen):
    ############ Load on-screen images ######################
    Kmitl = (p.image.load("Logo/KMITL-GO 200px.png"))
    screen.blit(Kmitl, (800, 0))
    FE = (p.image.load("Logo/FE Logo fix.png"))
    screen.blit(FE, (800, 30))


"""
The main driver for our code. This will handle user input and updating the graphics
"""


############### add in later, menu, image, displaying move-log on RHS.######################
def main():
    # p.mixer.pre_init(44100, -16, 2, 2048)  # setup mixer to avoid sound lag
    p.init()
    p.mixer.init()  # Music mixer
    playlist = list()  # Music playlist
    playlist.append("music/Giorno's Theme in the style of JAZZ.mp3")  # 4
    playlist.append("music/FKJ - Ylang Ylang.mp3")  # 3
    # playlist.append("music/FKJ - Die With A Smile.mp3")  # 2
    # playlist.append("music/Wii.mp3")  # 1
    p.mixer.music.load(playlist.pop())  # Get the first track from the playlist
    p.mixer.music.queue(playlist.pop())  # Queue the 2nd song
    p.mixer.music.set_endevent(p.USEREVENT)  # Setup the end track event
    p.mixer.music.set_volume(0.5)
    p.mixer.music.play()
    p.event.wait()

    ############# Main Chess Gui : Display screen #################
    screen = p.display.set_mode((1000, HEIGHT))  # (0,0) top left >>> (1000,800) bottom right
    p.display.set_caption("|ChessM8| Checkmate Chess beta 1.0_by: Jirapat_Wongjaroenrat")
    clock = p.time.Clock()
    screen.fill(p.Color("grey"))
    game_state = ChessEngine.GameState()  # Calls _init_ from ChessEngine
    validMoves = game_state.getValidMoves()
    moveMade = False  # flag variable for when a move is made

    loadImages()  # do this once, before while loop
    images(screen)  # load def images, before game loop

    ############# Game event : Don't touch ##############
    running = True
    sqSelected = ()  # no square is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = []  # keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:  ###### Event ######
                running = False

            elif event.type == p.USEREVENT:  # A track has ended
                if len(playlist) > 0:  # If there are more tracks in the queue...
                    p.mixer.music.queue(playlist.pop())  # queue next song in list

            ########## Mouse Handler: User input ################
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x, y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):  # the user clicked the same square twice
                    sqSelected = ()  # deselect
                    playerClicks = []  # clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)  # append for both 1st and 2nd clicks

                if len(playerClicks) == 2:  # after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], game_state.board)
                    print(move.GetChessNotation())
                    if move in validMoves:
                        game_state.makeMove(move)
                        moveMade = True
                        sqSelected = ()  # reset user clicks
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]

            # key handlers
            elif event.type == p.KEYDOWN:
                if event.key == p.K_z:  # undo when "z" is being pressed
                    game_state.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = game_state.getValidMoves()
            moveMade = False

        drawGameState(screen, game_state)
        clock.tick(MAX_FPS)
        p.display.flip()
        p.display.update()


"""
Responsible for all the graphics within a current game state
"""


############### add in chess piece highlighting, move suggestions later ####################
def drawGameState(screen, game_state):
    drawBoard(screen)  # draw squares on the board
    drawPieces(screen, game_state.board)  # draw chess pieces on top of those squares


"""
Draw the squares on the board. (Top Left square is always white)
"""


def drawBoard(screen):  # white (even), r = 2.  black (odd), r = 1
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


if __name__ == "__main__":
    main()
