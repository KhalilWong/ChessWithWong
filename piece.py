import colour
import pygame

################################################################################
class Piece(pygame.sprite.Sprite):
    #
    def __init__(self, Player, mousex, mousey):
        #
        super().__init__()
        self.Player = Player
        self.colour = colour.RGB()
        getattr(self.colour, self.Player.colour)                                #getattr(self.colour, 'White') = self.colour.White()
        self.shape = 'O'
        self.size = 25
        self.x = mousex
        self.y = mousey
        self.GX = -1
        self.GY = -1
        self.Exist = False
    #
    def Attach_to_Board(self, BoardGridX, BoardGridY, BoardGrids, Clicked = False):
        #
        NX = len(BoardGridX)
        NY = len(BoardGridY)
        for i in range(NX):
            if BoardGridX[i, 0] <= self.x <= BoardGridX[i, 2]:
                self.GX = i
                self.x = BoardGridX[i, 1]
                break
        for j in range(NY):
            if BoardGridY[j, 0] <= self.y <= BoardGridY[j, 2]:
                self.GY = j
                self.y = BoardGridY[j, 1]
                break
        if self.GX == -1 or self.GY == -1:
            self.Exist = False
        else:
            if BoardGrids[self.GY, self.GX] < 0:
                if Clicked:
                    self.Exist = True
                    BoardGrids[self.GY, self.GX] = self.Player.turn
                else:
                    self.Exist = True
    #
    def update(self, screen, alpha = False):
        #
        if self.Exist:
            if alpha:
                screen_alpha = screen.convert_alpha()
                pygame.draw.circle(screen_alpha, (self.colour.R, self.colour.G, self.colour.B, 128), (self.x, self.y), self.size, 0)
                screen.blit(screen_alpha, (0, 0))
            else:
                print(self.colour.R, self.size)
                pygame.draw.circle(screen, (self.colour.R, self.colour.G, self.colour.B), (self.x, self.y), self.size, 0)
