import pygame
import numpy 

# Farben definieren
COLOR_ALIVE = (255, 255, 215)
COLOR_ALIVE_BUT_DEAD_IN_NEXT_GEN = (200, 200, 225)
COLOR_GRIDLINE = (30, 30, 60)
COLOR_BACKGROUND = (10, 10, 40)

# Auf diese Oberfläche werden die Zellen gerendert
MAIN_WINDOW_SURFACE = None


# Erstellt ein leeres Spielfeld
def init(rows, cols):   
    board = numpy.zeros((rows, cols))
    #addBlinker(board, 3, 3)
    #addDieIn54Gen(board, 21, 33)
    addRPentomino(board, 21, 33)
    return board


# Berechnet die nächste Generation und zeichnet das Spielfeld neu
# @param currentGenerationBoard - Array - aktuelles Spielfeld
# @param cellSize - int - Größe einer Zelle (Spielfeldkästchens) in px
def update(currentGenerationBoard, cellSize):
    nextGenerationBoard = numpy.zeros((currentGenerationBoard.shape[0], currentGenerationBoard.shape[1]))

    for row, col in numpy.ndindex(currentGenerationBoard.shape):
        numAliveNeighbors = numpy.sum(currentGenerationBoard[row-1:row+2, col-1:col+2]) - currentGenerationBoard[row, col]

        if currentGenerationBoard[row, col] == 1 and numAliveNeighbors < 2 or numAliveNeighbors > 3:
            color = COLOR_ALIVE_BUT_DEAD_IN_NEXT_GEN
        elif (currentGenerationBoard[row, col] == 1 and 2 <= numAliveNeighbors <= 3) or (currentGenerationBoard[row, col] == 0 and numAliveNeighbors == 3):
            nextGenerationBoard[row, col] = 1
            color = COLOR_ALIVE

        color = color if currentGenerationBoard[row, col] == 1 else COLOR_BACKGROUND
        
        global MAIN_WINDOW_SURFACE
        pygame.draw.rect(MAIN_WINDOW_SURFACE, color, (col*cellSize, row*cellSize, cellSize-1, cellSize-1))

    return nextGenerationBoard



# Die folgenden FUnktionen fügen dem Spielfeld jeweils eine Figur hinzu. Müssen in der
# init()-Funktion aufgerufen werden. ACHTUNG: Bei Mehrfachaufrufen muss die Größe beachtet
# werden, da sich die Figuren sonst überschreiben!
# @param cells
# @param xPos
# @param yPos
def addBlinker(board, xPos, yPos):
    pattern = numpy.array([[1,1,1]])
    pos = (xPos, yPos)
    board[pos[0]:pos[0]+pattern.shape[0], pos[1]:pos[1]+pattern.shape[1]] = pattern

def addDieIn54Gen(board, xPos, yPos):
    pattern = numpy.array([[1,1,1],
                           [1,0,1],
                           [1,0,1],
                           [0,0,0],
                           [1,0,1],
                           [1,0,1],
                           [1,1,1]])
    pos = (xPos, yPos)
    board[pos[0]:pos[0]+pattern.shape[0], pos[1]:pos[1]+pattern.shape[1]] = pattern            

def addRPentomino(board, xPos, yPos): 
    pattern = numpy.array([[0,1,1],
                           [1,1,0],
                           [0,1,0]])
    pos = (xPos, yPos)
    board[pos[0]:pos[0]+pattern.shape[0], pos[1]:pos[1]+pattern.shape[1]] = pattern                               


# Einstiegsmethode
# @param rows - int - Anzahl der Zeilen, die das Spielfeld haben soll
# @param cols - int - Anzahl der Spalten, die das Spielfeld haben soll
# @param cellsize - int - Seitenlänge eines Spielfeldkästchens in px
def main(rows, cols, cellSize):
    
    pygame.init()    
    pygame.display.set_caption("John Conway's Game of Life")

    global MAIN_WINDOW_SURFACE
    MAIN_WINDOW_SURFACE = pygame.display.set_mode((cols * cellSize, rows * cellSize))    

    cells = init(rows, cols)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        MAIN_WINDOW_SURFACE.fill(COLOR_GRIDLINE)
        cells = update(cells, cellSize)
        pygame.display.update()
        #pygame.time.delay(100)


if __name__ == "__main__":
    main(50, 70, 10)