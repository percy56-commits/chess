class Rook:
    def __init__(self, color, position):
        self.color = color
        self.x, self.y = position
    def move(self, step, direction):
        if direction == "x" and 0 <self.x + step<9:
            self.x = self.x + step
        elif direction == "y" and 0<self.y + step<9:
            self.y = self.y + step
        else:
            print("This move is not legal!")
R1 = Rook(color="black", position=(4,6))
R1.x
R1.move(step = 3, direction="y")
R1.x
R1.y

