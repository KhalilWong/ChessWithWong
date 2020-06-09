class RGB():
    #
    def __init__(self, R = 0, G = 0, B = 0):
        #
        self.R = R
        self.G = G
        self.B = B
    def Red(self):
        #
        self.R = 255
        self.G = 0
        self.B = 0
    def Green(self):
        #
        self.R = 0
        self.G = 255
        self.B = 0
    def Blue(self):
        #
        self.R = 0
        self.G = 0
        self.B = 255
    def White(self):
        #
        self.R = 255
        self.G = 255
        self.B = 255
    def Black(self):
        #
        self.R = 0
        self.G = 0
        self.B = 0
    def Yellow(self):
        #
        self.R = 255
        self.G = 255
        self.B = 0
    def Magenta(self):
        #
        self.R = 255
        self.G = 0
        self.B = 255
    def Cyan(self):
        #
        self.R = 0
        self.G = 255
        self.B = 255
    def Purple(self):
        #
        self.R = 128
        self.G = 0
        self.B = 128
    def LYPurple(self):
        #
        self.R = 170
        self.G = 43
        self.B = 213
