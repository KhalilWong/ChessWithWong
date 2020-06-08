import sys
import numpy as np
import pygame
import colour
import piece
import player

################################################################################
def Create_BoardGrids(settings):
    #
    BoardGridX = np.zeros((settings.board_width, 3), dtype=int)
    for i in range(settings.board_width):
        BoardGridX[i, :] = np.array([settings.XMargin + i * settings.board_size + (i + 1) * settings.gap_size, int(settings.XMargin + (i + 1) * (settings.board_size + settings.gap_size) - settings.board_size / 2), settings.XMargin + (i + 1) * (settings.board_size + settings.gap_size)], dtype=int)
    #
    BoardGridY = np.zeros((settings.board_height, 3), dtype=int)
    for j in range(settings.board_height):
        BoardGridY[j, :] = np.array([settings.YMargin + j * settings.board_size + (j + 1) * settings.gap_size, int(settings.YMargin + (j + 1) * (settings.board_size + settings.gap_size) - settings.board_size / 2), settings.YMargin + (j + 1) * (settings.board_size + settings.gap_size)], dtype=int)
    #-1为空，0为玩家，1为AI，-2为鼠标位置
    BoardGrids = np.ones((settings.board_height, settings.board_width), dtype=int) * (-1)
    #
    return(BoardGridX, BoardGridY, BoardGrids)

################################################################################
def Draw_Board(settings, screen):
    #
    Board_Surface = screen.convert_alpha()
    pygame.draw.rect(Board_Surface, (255 - settings.background_colour.R, 255 - settings.background_colour.G, 255 - settings.background_colour.B, 128), (settings.XMargin, settings.YMargin, settings.Board_Width, settings.Board_Height), 0)
    #
    for i in range(settings.board_width + 1):
        pygame.draw.rect(Board_Surface, (settings.frame_colour.R, settings.frame_colour.G, settings.frame_colour.B, 128), (settings.XMargin + i * (settings.board_size + settings.gap_size), settings.YMargin, settings.gap_size, settings.Board_Height), 0)
    #
    for j in range(settings.board_height + 1):
        pygame.draw.rect(Board_Surface, (settings.frame_colour.R, settings.frame_colour.G, settings.frame_colour.B, 128), (settings.XMargin, settings.YMargin + j * (settings.board_size + settings.gap_size), settings.Board_Width, settings.gap_size), 0)
    #
    screen.blit(Board_Surface, (0, 0))

################################################################################
def Check_Events(Mouse, BoardGridX, BoardGridY, BoardGrids, Pieces, Mouse_Piece, Player0, MousePlayer, CurrentTurn):
    #
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            Mouse.x, Mouse.y = event.pos
            #
            Mouse_Piece = piece.Piece(MousePlayer, Mouse.x, Mouse.y)
            Mouse_Piece.Attach_to_Board(BoardGridX, BoardGridY, BoardGrids)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            Mouse.x, Mouse.y = event.pos
            Mouse.Clicked = True
            #
            if CurrentTurn[0] % 2 == Player0.turn:
                new_piece = piece.Piece(Player0, Mouse.x, Mouse.y)
                new_piece.Attach_to_Board(BoardGridX, BoardGridY, BoardGrids, Mouse.Clicked)
                if new_piece.Exist:
                    Pieces.add(new_piece)
                    CurrentTurn[0] += 1
        elif event.type == pygame.MOUSEBUTTONUP:
            Mouse.x, Mouse.y = event.pos
            Mouse.Clicked = False
        #
################################################################################
def Count_Grids(BoardGrids):
    #
    NY, NX = BoardGrids.shape
    BoardGridFilled = []
    BoardGridUnFilled = []
    for j in range(NY):
        for i in range(NX):
            if BoardGrids[j, i] >= 0:
                BoardGridFilled.append([i, j])
            else:
                BoardGridUnFilled.append([i, j])
    #
    return(BoardGridFilled, BoardGridUnFilled)

################################################################################
def Check_Game(settings, screen, BoardGridX, BoardGridY, BoardGrids, Pieces, Player0, AI0):
    #
    NY, NX = BoardGrids.shape
    NP = int(np.max(BoardGrids) + 1)                                            #玩家数 = 玩家 + AI
    count_empty = 0                                                             #空格数
    count_player = np.zeros(NP)                                                 #玩家棋子数
    FiveLinesX = [[] for i in range(NX)]
    FiveLinesY = [[] for i in range(NY)]
    FiveLinesXYp = [[] for i in range(NX + NY - 1 - 8)]
    FiveLinesXYm = [[] for i in range(NX + NY - 1 - 8)]
    for j in range(NY):
        for i in range(NX):
            #X, Y, XY+, XY-
            FiveLinesX[i].append([BoardGrids[j, i], i, j])
            FiveLinesY[j].append([BoardGrids[j, i], i, j])
            if i + j - 4 >= 0 + 0 + 4 - 4 and i + j - 4 <= (NX - 1) + (NY - 1) - 4 - 4:
                FiveLinesXYp[i + j - 4].append([BoardGrids[j, i], i, j])
            if i - j + 4 >= 0 - (NY - 1) + 4 + 4 and i - j + 4 <= (NX - 1) - 0 - 4 + 4:
                FiveLinesXYm[i - j + 4].append([BoardGrids[j, i], i, j])
            #
            if BoardGrids[j, i] < 0:
                count_empty += 1
            for n in range(NP):
                if BoardGrids[j, i] == n:
                    count_player[n] += 1
    #
    if count_empty == 0:
        Mess = '真是旗鼓相当的对手呢~'
        GameOver(settings, screen, Mess, Pieces)
    else:
        #Player
        SomeOneWin = False
        #X
        if not SomeOneWin:
            for i in range(NX):
                XiN = len(FiveLinesX[i])
                Link_N = 0
                LastPlayer = -1
                for k in range(XiN):
                    if FiveLinesX[i][k][0] >= 0:
                        if FiveLinesX[i][k][0] == LastPlayer:
                            Link_N += 1
                            if Link_N == 5:
                                Win_Turn = FiveLinesX[i][k][0]
                                Win_X = [FiveLinesX[i][k][1], FiveLinesX[i][k - 1][1], FiveLinesX[i][k - 2][1], FiveLinesX[i][k - 3][1], FiveLinesX[i][k - 4][1]]
                                Win_Y = [FiveLinesX[i][k][2], FiveLinesX[i][k - 1][2], FiveLinesX[i][k - 2][2], FiveLinesX[i][k - 3][2], FiveLinesX[i][k - 4][2]]
                                SomeOneWin = True
                                break
                        else:
                            Link_N = 1
                            LastPlayer = FiveLinesX[i][k][0]
                    else:
                        Link_N = 0
                        LastPlayer = FiveLinesX[i][k][0]
                if SomeOneWin:
                    break
        #Y
        if not SomeOneWin:
            for i in range(NY):
                YiN = len(FiveLinesY[i])
                Link_N = 0
                LastPlayer = -1
                for k in range(YiN):
                    if FiveLinesY[i][k][0] >= 0:
                        if FiveLinesY[i][k][0] == LastPlayer:
                            Link_N += 1
                            if Link_N == 5:
                                Win_Turn = FiveLinesY[i][k][0]
                                SomeOneWin = True
                                Win_X = [FiveLinesY[i][k][1], FiveLinesY[i][k - 1][1], FiveLinesY[i][k - 2][1], FiveLinesY[i][k - 3][1], FiveLinesY[i][k - 4][1]]
                                Win_Y = [FiveLinesY[i][k][2], FiveLinesY[i][k - 1][2], FiveLinesY[i][k - 2][2], FiveLinesY[i][k - 3][2], FiveLinesY[i][k - 4][2]]
                                break
                        else:
                            Link_N = 1
                            LastPlayer = FiveLinesY[i][k][0]
                    else:
                        Link_N = 0
                        LastPlayer = FiveLinesY[i][k][0]
                if SomeOneWin:
                    break
        #XY+
        if not SomeOneWin:
            for i in range(NX + NY - 1 - 8):
                XYpiN = len(FiveLinesXYp[i])
                Link_N = 0
                LastPlayer = -1
                for k in range(XYpiN):
                    if FiveLinesXYp[i][k][0] >= 0:
                        if FiveLinesXYp[i][k][0] == LastPlayer:
                            Link_N += 1
                            if Link_N == 5:
                                Win_Turn = FiveLinesXYp[i][k][0]
                                Win_X = [FiveLinesXYp[i][k][1], FiveLinesXYp[i][k - 1][1], FiveLinesXYp[i][k - 2][1], FiveLinesXYp[i][k - 3][1], FiveLinesXYp[i][k - 4][1]]
                                Win_Y = [FiveLinesXYp[i][k][2], FiveLinesXYp[i][k - 1][2], FiveLinesXYp[i][k - 2][2], FiveLinesXYp[i][k - 3][2], FiveLinesXYp[i][k - 4][2]]
                                SomeOneWin = True
                                break
                        else:
                            Link_N = 1
                            LastPlayer = FiveLinesXYp[i][k][0]
                    else:
                        Link_N = 0
                        LastPlayer = FiveLinesXYp[i][k][0]
                if SomeOneWin:
                    break
        #XY-
        if not SomeOneWin:
            for i in range(NX + NY - 1 - 8):
                XYmiN = len(FiveLinesXYm[i])
                Link_N = 0
                LastPlayer = -1
                for k in range(XYmiN):
                    if FiveLinesXYm[i][k][0] >= 0:
                        if FiveLinesXYm[i][k][0] == LastPlayer:
                            Link_N += 1
                            if Link_N == 5:
                                Win_Turn = FiveLinesXYm[i][k][0]
                                Win_X = [FiveLinesXYm[i][k][1], FiveLinesXYm[i][k - 1][1], FiveLinesXYm[i][k - 2][1], FiveLinesXYm[i][k - 3][1], FiveLinesXYm[i][k - 4][1]]
                                Win_Y = [FiveLinesXYm[i][k][2], FiveLinesXYm[i][k - 1][2], FiveLinesXYm[i][k - 2][2], FiveLinesXYm[i][k - 3][2], FiveLinesXYm[i][k - 4][2]]
                                SomeOneWin = True
                                break
                        else:
                            Link_N = 1
                            LastPlayer = FiveLinesXYm[i][k][0]
                    else:
                        Link_N = 0
                        LastPlayer = FiveLinesXYm[i][k][0]
                if SomeOneWin:
                    break
        #
        if SomeOneWin:
            if Win_Turn == Player0.turn:
                Mess = '你也太厉害了吧！'
            elif Win_Turn == AI0.turn:
                Mess = '略逊一筹可惜了~'
            Win = player.Player('Win', -7, 'Red')
            Win_Pieces = pygame.sprite.Group()
            for i in range(5):
                win_piece = piece.Piece(Win, BoardGridX[Win_X[i], 1], BoardGridY[Win_Y[i], 1])
                win_piece.Exist = True
                if win_piece.Exist:
                    Win_Pieces.add(win_piece)
            GameOver(settings, screen, Mess, Pieces, Win_Pieces)

################################################################################
def GameOver(settings, screen, mess, Pieces, Win_Pieces = None):
    #
    if Win_Pieces:
        for i in range(50):
            if i % 2 == 0:
                Win_Pieces.update(screen)
            else:
                Pieces.update(screen)
            pygame.display.update()
            pygame.time.wait(200)
    #
    #ZiTis = pygame.font.get_fonts()
    #for ziti in ZiTi:
    #    print(ziti)
    fontObj = pygame.font.SysFont('stzhongsong', 64)
    textColour = colour.RGB()
    textColour.Yellow()
    textSurface = fontObj.render(mess, True, (textColour.R, textColour.G, textColour.B))
    textRect = textSurface.get_rect()
    textRect.center = (settings.screen_width / 2, settings.screen_height / 2)
    screen.blit(textSurface, textRect)
    pygame.display.update()
    pygame.time.wait(3000)
    #
    pygame.quit()
    sys.exit()

################################################################################
def Update_Screen(settings, screen, BoardGridX, BoardGridY, BoardGrids, Pieces, Mouse_Piece, Player0, AI0):
    #
    screen.fill((settings.background_colour.R, settings.background_colour.G, settings.background_colour.B))
    Draw_Board(settings, screen)
    Pieces.update(screen)
    Mouse_Piece.update(screen, True)
    Check_Game(settings, screen, BoardGridX, BoardGridY, BoardGrids, Pieces, Player0, AI0)
    pygame.display.update()                                                     #Update portions of the screen for software displays. If no argument is passed it updates the entire Surface area like pygame.display.flip().
    #pygame.display.flip()                                                      #Update the full display Surface to the screen
