# CheckM8 Chess (Checkmate Chess)
**Create and developed by Jirapat Wongjaroenrat_64011405_ Pycharm IDE**


## My Python Project progress tracking log report
**https://docs.google.com/document/d/1P94rIcMt08JfpNwGHNfSqtR5iQyTaE2yxylx_PZQxKo/edit?usp=sharing**


## Files :
**- 1. ChessMain.py:**       Contains the code to handle user input and draw the game visuals

**- 2. ChessEngine.py:**     Contains the logic of the Chess game (Using Brute Force Algorithm for calculating valid moves). Responsible for storing all the information about the current state of a chess game. It will also be responsible for determining the valid moves at the current state. It also keep a chess-move log (undo move, check opponent & your current moves)

**- 3. ChessBot.py:**      Contains the logic for the AI to play smartly considering captures, defences and positional advantages to some extent. With different methods and   evaluating moves ahead in depth 

## Library to be installed for this Chess engine to work :

pyGame: pip3 install pygame

## In-Game User Controls
**L_Click - moving Chess piece**

**R_Click - Go back (MainMenu)**

**Escape_Esc - Exit Game (MainMenu)**

**Key_"r" - Reset Game**

**Key_"u" - Undo Move (works for human moves)**
