"""
This is our main driver file. It will be responsible for handling user input
and displaying the current Game state
"""

import pygame as p
import sys
from Chess import ChessEngine
import ChessBot
# import Config

p.init()
p.mixer.init()  # Music mixer

WIDTH = HEIGHT = 800  # 512, 400 another option
DIMENSION = 8  # dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION  # 100 x 100px per SQ , Image size <= 100, Canvas size <= 100
MAX_FPS = 15  # for animations
IMAGES = {}

font = p.font.SysFont("Helvitca", 70, True, True)
font2 = p.font.SysFont("Arial", 30, True, True)
font3 = p.font.SysFont("constantia", 80, True, True)
font4 = p.font.SysFont("Helvetica", 30, True, False)
font5 = p.font.SysFont("Helvetica", 23, True, False)

############# Main Chess ui : Display screen #################
screen = p.display.set_mode((1000, HEIGHT))  # (0,0) top left >>> (1000,800) bottom right
p.display.set_caption("|ChessM8| Checkmate Chess beta 1.0_by: Jirapat_Wongjaroenrat")
clock = p.time.Clock()

# loading Images .png, own method instead of putting in main. To support picking
# couple different chess sets options later on.
"""
Initialize a global dictionary of images. This will be called exactly once in the main
"""


# Manual image load
# IMAGES["wp"] = p.transform.scale(p.image.load("White piece/wK.png"), (SQ_SIZE, SQ_SIZE))

def loadImages():
    # ---Player 1--- #
    white_chess_pieces = ["wp", "wR", "wN", "wB", "wQ", "wK"]
    for piece in white_chess_pieces:
        # IMAGES[piece] = p.transform.scale(p.image.load(Config.Player_1 + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        IMAGES[piece] = p.transform.scale(p.image.load(Player_1 + piece + ".png"), (SQ_SIZE, SQ_SIZE))

    # Note: access an image by using 'IMAGES['wp']'-> return white pawn image.
    # Change image directory in 'images/'
    # IMAGES["wp"] = p.transform.scale(p.image.load("White piece/wQ.png"), (SQ_SIZE, SQ_SIZE))

    # ---Player 2--- #
    black_chess_pieces = ["bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in black_chess_pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(Player_2 + piece + ".png"),
                                          (SQ_SIZE, SQ_SIZE))  # p.transform.scale(p.image>>>,(SQ_SIZE,SQ_SIZE)
    # Note: access an image by using 'IMAGES['bp']'
    # Change image directory in 'images/'


def images():
    ############ Load on-screen images ######################
    Kmitl = (p.image.load("Logo/KMITL-GO 200px.png"))
    screen.blit(Kmitl, (800, 0))
    FE = (p.image.load("Logo/FE Logo fix.png"))
    screen.blit(FE, (800, 30))


"""
This will be out main driver. This will handle user input and update the graphics
"""


# ------- Choosing GAME MODE ---------#
# playerOne = Config.PLAYER_ONE_HUMAN  # If a Human is playing white, then this will be True.
# playerTwo = Config.PLAYER_TWO_HUMAN  # If AI is playing, then this will be False


############### This will be out main driver. It will handle user input and update the graphics. Add in later, menu, image, displaying move-log on RHS.######################
def main():
    # p.mixer.pre_init(44100, -16, 2, 2048)  # setup mixer to avoid sound lag

    playlist = list()  # Music playlist
    playlist.append("music/1. FKJ - Die With A Smile (mp3cut.net).mp3")  # 2
    playlist.append("music/4. FKJ - Just Piano (mp3cut.net).mp3")  # 5
    playlist.append("music/2. FKJ - Ylang Ylang (mp3cut.net).mp3")  # 3
    playlist.append("music/3. Giorno's Theme in the style of JAZZ (mp3cut.net).mp3")  # 4
    # playlist.append("music/Wii.mp3")  # 1

    p.mixer.music.load(playlist.pop())  # Get the first track from the playlist
    p.mixer.music.queue(playlist.pop())  # Queue the 2nd song
    p.mixer.music.set_endevent(p.USEREVENT)  # Setup the end track event
    p.mixer.music.set_volume(1)
    p.mixer.music.play()
    p.event.wait()
    screen.fill(p.Color("grey"))
    game_state = ChessEngine.GameState()  # Calls _init_ from ChessEngine
    validMoves = game_state.getValidMoves()
    moveMade = False  # flag variable for when a move is made
    animate = False  # flag variable for when we should animate a move

    loadImages()  # do this once, before while loop
    images()  # load def images, before game loop

    running = True
    sqSelected = ()  # no square is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = []  # keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    gameOver = False
    # -------GameMode Label----------- #
    if playerOne and not playerTwo:
        gameModeLabel("Player 1 VS Bot")
    elif playerTwo and not playerOne:
        gameModeLabel("Player 2 VS Bot")
    elif playerOne and playerTwo:
        gameModeLabel("Player 1 VS Player 2")
    else:
        gameModeLabel("Bot VS Bot")

    ############# Game driver : Don't touch ##############
    while running:
        humanTurn = (game_state.whiteToMove and playerOne) or (not game_state.whiteToMove and playerTwo)

        for event in p.event.get():
            if event.type == p.QUIT:  # ---- Event -----#
                running = False
                sys.exit()

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
                    gameOver = False
                if event.key == p.K_r:  # RESET the board when "R" is pressed
                    game_state = ChessEngine.GameState()
                    validMoves = game_state.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False

                if event.key == p.K_ESCAPE:
                    main_menu()

            # AI Move finder logic
        if not gameOver and not humanTurn:
            AIMove = ChessBot.findBestMove(game_state, validMoves)
            if AIMove is None:
                AIMove = ChessBot.findRandomMove(validMoves)
            game_state.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMoves(game_state.moveLog[-1], game_state.board)
            validMoves = game_state.getValidMoves()
            moveMade = False
            animate = False

        if game_state.checkmate:
            gameOver = True
            if game_state.whiteToMove:
                drawText("Black wins by checkmate")
            else:
                drawText("White wins by checkmate")

        elif game_state.stalemate:
            gameOver = True
            drawText("STALEMATE DRAW")

        drawGameState(game_state, validMoves, sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()


"""
Highlight square selected and moves for piece selected
"""


def highlightSquares(game_state, validMoves, sqSelected):
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

def drawGameState(game_state, validMoves, sqSelected):
    drawBoard()  # draw squares on the board (should be called before drawing anything else)
    highlightSquares(game_state, validMoves, sqSelected)
    drawPieces(game_state.board)  # draw piece on top of the squares


"""
Draw the squares on the board. (Top Left square is always white)
"""


def drawBoard():  # white (even), r = 2.  black (odd), r = 1
    global colors
    colors = [p.Color("#E35205"), p.Color("white")]  # KMITL Hex color #E35205, white
    for r in range(DIMENSION):  # r = row , c = coluom
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


"""
Draw the pieces on the board using the current GameState.board
"""


def drawPieces(board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # not empty square
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


"""
Animate a move transition between square selected
"""


def animateMoves(move, board):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framePerSquare = 10  # frames to move 1 square
    frameCount = (abs(dR) + abs(dC)) * framePerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard()
        drawPieces(board)

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


def drawText(text):
    textObject = font.render(text, 0, p.Color("White"))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObject.get_width() / 2,
                                                    HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Black"))
    screen.blit(textObject, textLocation.move(2, 2))
    textObject2 = font2.render("Thanks for playing!!", True, p.Color("Grey"))
    screen.blit(textObject2, (300, 470))

    textObject2 = font2.render("Thanks for playing!!", True, p.Color("Red"))
    screen.blit(textObject2, (302, 472))

    p.display.update()


def gameModeLabel(text):
    mode = p.font.SysFont("Arial", 20, True, False)
    textObject3 = mode.render("||-GameMode-||", True, p.Color("Black"))
    screen.blit(textObject3, (820, 650))

    label = p.font.SysFont("Arial", 18, True, False)
    textObject4 = label.render(text, True, p.Color("Brown"))
    screen.blit(textObject4, (820, 680))


"""
All the functions from here will be responsible for the MainMenu Ui
"""


# if __name__ == "__main__":
#     main()
def color_options():
    global Player_1, Player_2
    while True:
        screen.fill(p.Color("grey"))
        Chess = (p.image.load("Logo/Chess-Wallpaper2.png"))
        screen.blit(Chess, (-40, 0))
# --------Chess Piece Color options------- #
        title = font4.render("Chess Pieces Color", True, p.Color("Brown"))
        screen.blit(title, (63, 500))
        title = font4.render("Chess Pieces Color", True, p.Color("White"))
        screen.blit(title, (60, 500))
        # title = font5.render("White (Default)", True, p.Color("White"))
        # screen.blit(title, (80, 545))
        step1 = font.render("Step 1:", True, p.Color("#fc9003"))
        screen.blit(step1, (74, 430))

        p.draw.rect(screen, p.Color("#fc9003"), ((70, 560), (150, 60)))  # screen, color, (x,y location), (size)
        play2 = font5.render("Black piece", True, p.Color("Black"))
        screen.blit(play2, (77, 575))

        p.draw.rect(screen, p.Color("#fc9003"), ((70, 640), (150, 60)))  # screen, color, (x,y location), (size)
        play2 = font5.render("Gold piece", True, p.Color("Black"))
        screen.blit(play2, (77, 655))

        p.draw.rect(screen, p.Color("#fc9003"), ((70, 720), (150, 60)))  # screen, color, (x,y location), (size)
        play2 = font5.render("White piece", True, p.Color("Black"))
        screen.blit(play2, (77, 735))

# ------Current Blank buttons------ #
        title = font3.render("Game Modes", True, p.Color("White"))
        screen.blit(title, (100, 50))
        title = font3.render("Game Modes", True, p.Color("Black"))
        screen.blit(title, (102, 50))
        p.draw.rect(screen, p.Color("#fc9003"), ((415, 200), (270, 100)))  # screen, color, (x,y location), (size)
        play1 = font2.render("Player vs AI", True, (255, 255, 255))
        screen.blit(play1, (460, 233))
        p.draw.rect(screen, p.Color("#fc9003"), ((415, 350), (270, 100)))  # screen, color, (x,y location), (size)
        play1 = font2.render("AI vs AI", True, (255, 255, 255))
        screen.blit(play1, (490, 380))
        p.draw.rect(screen, p.Color("#fc9003"), ((405, 500), (290, 100)))  # screen, color, (x,y location), (size)
        play1 = font2.render("Player1 vs Player2", True, (255, 255, 255))
        screen.blit(play1, (420, 533))

        for event in p.event.get():
            if event.type == p.QUIT:
                sys.exit()
            elif event.type == p.MOUSEBUTTONDOWN and event.button == 3:
                main_menu()
            elif event.type == p.KEYDOWN and p.K_ESCAPE:
                main_menu()

            elif event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if 70 <= x <= 220 and 560 <= y <= 620:
                    Player_1 = "Black piece1/"
                    Player_2 = "White piece2/"
                    game_mode()
                if 70 <= x <= 220 and 640 <= y <= 700:
                    Player_1 = "Gold piece/"
                    Player_2 = "Black piece/"
                    game_mode()
                if 70 <= x <= 220 and 720 <= y <= 800:
                    Player_1 = "White piece/"
                    Player_2 = "Gold piece2/"
                    game_mode()
        p.display.update()

def game_mode():
    # -------Choose GameMode menu-------- #
    global playerOne, playerTwo
    while True:
        screen.fill(p.Color("grey"))
        Chess = (p.image.load("Logo/Chess-Wallpaper2.png"))
        screen.blit(Chess, (-40, 0))

        title = font3.render("Game Modes", True, p.Color("White"))
        screen.blit(title, (100, 50))
        title = font3.render("Game Modes", True, p.Color("Black"))
        screen.blit(title, (102, 50))

        step2 = font.render("Step 2:", True, p.Color("#fc9003"))
        screen.blit(step2, (460, 150))
        p.draw.rect(screen, p.Color("#fc9003"), ((415, 200), (270, 100)))  # screen, color, (x,y location), (size)
        play1 = font2.render("Player vs AI", True, (255, 255, 255))
        screen.blit(play1, (460, 233))

        p.draw.rect(screen, p.Color("#fc9003"), ((415, 350), (270, 100)))  # screen, color, (x,y location), (size)
        play1 = font2.render("AI vs AI", True, (255, 255, 255))
        screen.blit(play1, (490, 380))

        p.draw.rect(screen, p.Color("#fc9003"), ((405, 500), (290, 100)))  # screen, color, (x,y location), (size)
        play1 = font2.render("Player1 vs Player2", True, (255, 255, 255))
        screen.blit(play1, (420, 533))

        # --------Chess Piece Color options------- #
        # title = font4.render("Chess Pieces Color", True, p.Color("Brown"))
        # screen.blit(title, (63, 500))
        # title = font4.render("Chess Pieces Color", True, p.Color("White"))
        # screen.blit(title, (60, 500))
        # title = font5.render("White (Default)", True, p.Color("White"))
        # screen.blit(title, (80, 545))
        # p.draw.rect(screen, p.Color("#d0d2c7"), ((70, 580), (150, 60)))  # screen, color, (x,y location), (size)
        # play2 = font5.render("Black piece", True, p.Color("Black"))
        # screen.blit(play2, (77, 595))
        #
        # p.draw.rect(screen, p.Color("#d0d2c7"), ((70, 660), (150, 60)))  # screen, color, (x,y location), (size)
        # play2 = font5.render("Gold piece", True, p.Color("#D4AF37"))
        # screen.blit(play2, (77, 675))

        for event in p.event.get():
            if event.type == p.QUIT:
                sys.exit()
            elif event.type == p.MOUSEBUTTONDOWN and event.button == 3:
                main_menu()
            elif event.type == p.KEYDOWN and p.K_ESCAPE:
                main_menu()

            elif event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if 415 <= x <= 685 and 200 <= y <= 300:
                    playerOne = True  # If a Human is playing white, then this will be True.
                    playerTwo = False  # If AI is playing, then this will be False
                    main()

                if 415 <= x <= 685 and 350 <= y <= 450:
                    playerOne = False  # If a Human is playing white, then this will be True.
                    playerTwo = False  # If AI is playing, then this will be False
                    main()

                if 410 <= x <= 700 and 500 <= y <= 600:
                    playerOne = True  # If a Human is playing white, then this will be True.
                    playerTwo = True  # If AI is playing, then this will be False
                    main()

        p.display.update()


def credit():
    while True:
        screen.fill(p.Color("grey"))
        Chess = (p.image.load("Logo/Chess-Wallpaper.png"))
        screen.blit(Chess, (-320, -280))

        title = font3.render("Credits", True, p.Color("White"))
        screen.blit(title, (100, 50))
        title = font3.render("Credits", True, p.Color("Black"))
        screen.blit(title, (102, 50))

        detail = font4.render("Create & Developed by:", True, p.Color("grey"))
        screen.blit(detail, (120, 150))
        detail2 = font5.render("Jirapat Wongjaroenrat (Year 1, FE03 KMITL)", True, p.Color("White"))
        screen.blit(detail2, (188, 200))

        detail = font4.render("Art & Concept Design:", True, p.Color("grey"))
        screen.blit(detail, (120, 300))
        detail2 = font5.render("Jirapat Wongjaroenrat", True, p.Color("White"))
        screen.blit(detail2, (188, 350))

        special = font4.render("Special Thanks:", True, p.Color("grey"))
        screen.blit(special, (120, 450))
        detail2 = font5.render("Mr. Eddie Sharick, Computer Science & Physics Teacher", True, p.Color("White"))
        screen.blit(detail2, (188, 500))
        detail2 = font5.render("Dr. Natthapong Jungteerapanich, Instructor", True, p.Color("White"))
        screen.blit(detail2, (188, 550))
        detail2 = font5.render("School of International & Interdisciplinary", True, p.Color("White"))
        screen.blit(detail2, (188, 600))
        detail2 = font5.render("Engineering Programs(SIIE), KMITL.", True, p.Color("White"))
        screen.blit(detail2, (188, 620))

        detail2 = font5.render("This program is a part of 01006813 INTRODUCTION TO PROGRAMMING - Semester 1/2021", True, p.Color("White"))
        screen.blit(detail2, (10, 740))

        for event in p.event.get():
            if event.type == p.QUIT:
                sys.exit()
            elif event.type == p.MOUSEBUTTONDOWN and event.button == 3:
                main_menu()
            elif event.type == p.KEYDOWN and p.K_ESCAPE:
                main_menu()

        p.display.update()


# ----event.button 1 = L click, 3 = right click---- #
def main_menu():
    p.mixer.pre_init(44100, -16, 2, 2048)
    p.mixer.music.load("music/Wii.mp3")
    p.mixer.music.set_volume(0.5)
    p.mixer.music.play()
    while True:
        screen.fill(p.Color("grey"))
        Chess = (p.image.load("Logo/Chess-Wallpaper2.png"))
        screen.blit(Chess, (-40, 0))
        title = font.render("|ChessM8| Checkmate", True, p.Color("White"))
        screen.blit(title, (103, 100))
        textObject = font.render("|ChessM8| Checkmate", True, p.Color("Black"))
        screen.blit(textObject, (100, 100))
        title2 = font.render("Chess", 0, p.Color("White"))
        screen.blit(title2, (103, 150))
        textObject2 = font.render("Chess", True, p.Color("Black"))
        screen.blit(textObject2, (100, 150))
        knight = (p.image.load("White piece/wN 1.png"))
        screen.blit(knight, (300, 140))

#---- Click and calls color options >>> game_mode ----#
        p.draw.rect(screen, p.Color("#fc9003"), ((440, 250), (200, 80)))  # screen, color, (x,y location), (size)
        play = font2.render("Play Game", True, (255, 255, 255))
        screen.blit(play, (460, 270))
# ---- Click and calls credits ----#
        p.draw.rect(screen, p.Color("#fc9003"), ((450, 350), (180, 80)))  # screen, color, (x,y location), (size)
        credits_ = font2.render("Credits", True, (255, 255, 255))
        screen.blit(credits_, (480, 370))

        for event in p.event.get():
            if event.type == p.QUIT:
                sys.exit()
            elif event.type == p.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if 450 <= x <= 720 and 250 <= y <= 330:
                    color_options()
                if 450 <= x <= 720 and 350 <= y <= 430:
                    credit()

        p.display.update()


main_menu()
