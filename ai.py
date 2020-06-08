import random
import numpy as np
import functions
import piece

################################################################################
def Level0(BoardGridUnFilled):
    #
    GridID = random.choice(BoardGridUnFilled)
    return(GridID)

################################################################################
def Level1(BoardGridUnFilled):
    #
    GridID = random.choice(BoardGridUnFilled)
    return(GridID)

################################################################################
def AI_Player(settings, BoardGridX, BoardGridY, BoardGrids, Pieces, AI0, CurrentTurn, AI_Model = Level0):
    #
    if CurrentTurn[0] % 2 == AI0.turn:
        BoardGridFilled, BoardGridUnFilled = functions.Count_Grids(BoardGrids)
        XID, YID = AI_Model(BoardGridUnFilled)
        #
        new_piece = piece.Piece(AI0, BoardGridX[XID, 1], BoardGridY[YID, 1])
        new_piece.Exist = True
        if new_piece.Exist:
            Pieces.add(new_piece)
            CurrentTurn[0] += 1
            BoardGrids[YID, XID] = new_piece.Player.turn
