import colour

################################################################################
class Settings():
    #
    def __init__(self):
        #自定义
        self.screen_width = 1280
        self.screen_height = 720
        self.background_colour = colour.RGB()
        self.background_colour.LYPurple()
        self.frame_colour = colour.RGB()
        self.frame_colour.Cyan()
        self.FPS = 60
        self.board_width = 9
        self.board_height = 9
        self.board_size = 60
        self.gap_size =10
        #计算结果
        self.Board_Width = 0
        self.Board_Height = 0
        self.XMargin = 0
        self.YMargin = 0
    #
    def BoardInf(self):
        #
        self.Board_Width = self.board_width * (self.board_size + self.gap_size) + self.gap_size
        self.Board_Height = self.board_height * (self.board_size + self.gap_size) + self.gap_size
        self.XMargin = (self.screen_width - self.Board_Width) / 2
        self.YMargin = (self.screen_height - self.Board_Height) / 2
