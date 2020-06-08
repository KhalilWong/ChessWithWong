import sys
import numpy as np
import pygame
import ai
import colour
import functions
import piece
import player
import settings
import usercontrol

################################################################################
def main():
    #
    pygame.init()
    #
    fpsClock = pygame.time.Clock()
    userMouse = usercontrol.Mouse()
    The_Settings = settings.Settings()
    The_Settings.BoardInf()
    Dis_Surface = pygame.display.set_mode((The_Settings.screen_width, The_Settings.screen_height))
    #Date =
    #pygame.display.set_caption('Chess with Wong (Version: ' + Date +  ')')
    pygame.display.set_caption('Chess with Wong (Version: 0.2.0)')
    #
    GridX, GridY, Grids = functions.Create_BoardGrids(The_Settings)
    #
    TurnType = []
    P0 = player.Player('P', 0, 'White')
    A0 = player.Player('A', 1, 'Black')
    MP = player.Player('M', -2, P0.colour)
    CurrentTurn = [0]
    #
    Pieces = pygame.sprite.Group()
    Mouse_Piece = piece.Piece(MP, 0, 0)
    while True:
        #
        functions.Check_Events(userMouse, GridX, GridY, Grids, Pieces, Mouse_Piece, P0, MP, CurrentTurn)
        ai.AI_Player(The_Settings, GridX, GridY, Grids, Pieces, A0, CurrentTurn)
        #
        functions.Update_Screen(The_Settings, Dis_Surface, GridX, GridY, Grids, Pieces, Mouse_Piece, P0, A0)
        #
        fpsClock.tick(The_Settings.FPS)

################################################################################
if __name__ == '__main__':
    #
    main()
