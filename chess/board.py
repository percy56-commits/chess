#keeps track of the state of the board
import pygame
class Board:
    def __init__(self, pos = 1):
       self.pos = pos
# used to visualise a bitboard
    def print_bitboard(self): 

    # convert to binary string, pad with leading zeros to length of 64
        self.pos = bin(self.pos)[2:].zfill(64) 

        print ("\n      A B C D E F G H ")
        print ("    __________________ ")

        for i in range(8):
            # need to print upside down and back to front to ensure correct formatting
            temp = [' ', 8-i, "|"] + [*(self.pos[-8:])[::-1]]

            # replace 0 with · for readability
            temp = [i if i!='0' else '·' for i in temp] 

            print(*temp, sep=" ") 
            self.pos = self.pos[:-8]  

        print("\n")

    # eumerate chess board square names
    a8, b8, c8, d8, e8, f8, g8, h8, \
    a7, b7, c7, d7, e7, f7, g7, h7, \
    a6, b6, c6, d6, e6, f6, g6, h6, \
    a5, b5, c5, d5, e5, f5, g5, h5, \
    a4, b4, c4, d4, e4, f4, g4, h4, \
    a3, b3, c3, d3, e3, f3, g3, h3, \
    a2, b2, c2, d2, e2, f2, g2, h2, \
    a1, b1, c1, d1, e1, f1, g1, h1 = range(64)

    #check if piece is on a square
    def get_bit(self, b, square):
        return 1 if (b & (1<<square)) else 0

    #sets a piece on a square
    def set_bit(self, b, square):
        return b | (1<<square)
        

    #removes a bit from a square
    def remove_bit(self, b, square):
        return b ^ ( 1<<square if self.get_bit(b , square) else 0 )
        

    #counts zeros until you hit a piece
    def ctz(self, b): # count trailing zeros
        return (b & -b).bit_length() - 1


    def new_board(self):
        self.pos = [ 71776119061217280, 65280,   # pawns (white, black)
                9295429630892703744, 129,     # rooks
                4755801206503243776, 66,      # knights
                2594073385365405696, 36,      # bishops
                576460752303423488, 8,        # queens
                1152921504606846976, 16,      # kings
                18446462598732840960, 65535,  # white, black pieces
                18446462598732840960 | 65535, # all board pieces
            ]
        return self.pos

    # enumerate array indices for convenience
    Wpawn, Bpawn, Wrook, Brook, Wknight, Bknight, Wbishop, Bbishop, Wqueen,\
    Bqueen, Wking, Bking, white, black, all = range(15)
    # enumerate piece names to match the index shown above:
    piece_names = ['P', 'p', 'R', 'r', 'N', 'n', 'B', 'b', 'Q', 'q', 'K', 'k']

    def print_board(self):
        output = [' ' for i in range(64)] 

        # scan the first 12 bitboards for pieces
        for i in range(12): 
            B = self.pos[i]

            # repeatedly find and remove least significant bit from bitboard 
            while B: 
                square = self.ctz(B)
                B = self.remove_bit(B, square)
                output[square] = Board.piece_names[i] # add piece to output string

        print ("\n      A B C D E F G H ")
        print ("    __________________ ")
        
        for i in range(8):
            # need to print upside down and back to front to 
            # ensure correct formatting
            temp = [' ', 8-i, "|"] + output[:8]
            print(*temp, sep=" ") 
            output = output[8:] 
        print ("\n")


    def update_bitboards(self):
        B = self.pos
        # union of other bitboards
        B[Board.white] = B[Board.Wpawn] | B[Board.Wrook] | B[Board.Wknight] | B[Board.Wbishop] | B[Board.Wking] | B[Board.Wqueen]
        B[Board.black] = B[Board.Bpawn] | B[Board.Brook] | B[Board.Bknight] | B[Board.Bbishop] | B[Board.Bking] | B[Board.Bqueen]
        B[Board.all] = B[Board.white] | B[Board.black]
        self.pos = B
        return B

    def position_pieces(self):
        output = [' ' for i in range(64)] 

        # scan the first 12 bitboards for pieces
        for i in range(12): 
            B = self.pos[i]

            # repeatedly find and remove least significant bit from bitboard 
            while B: 
                square = self.ctz(B)
                B = self.remove_bit(B, square)
                output[square] = Board.piece_names[i] # add piece to output string


        pos = []
        for i in range(8):
            # need to print upside down and back to front to 
            # ensure correct formatting
            pos.append(output[:8])
        
            output = output[8:] 
        return pos


        
    def draw_pieces(self, screen):
        piece_pos = self.position_pieces()
        for x in range(8):
            for y in range(8):
                if piece_pos[x][y] == "K":
                    img = pygame.transform.scale(pygame.image.load("images/white_king.png"), (100, 100))
                    screen.blit(img, (y*100,x*100))
                elif piece_pos[x][y] == "k":
                    img = pygame.transform.scale(pygame.image.load("images/black_king.png"), (100, 100))
                    screen.blit(img, (y*100,x*100))
                elif piece_pos[x][y] == "P":
                    img = pygame.transform.scale(pygame.image.load("images/white_pawn.png"), (100, 100))
                    screen.blit(img, (y*100,x*100))
                elif piece_pos[x][y] == "p":
                    img = pygame.transform.scale(pygame.image.load("images/black_pawn.png"), (100, 100))
                    screen.blit(img, (y*100,x*100))
                elif piece_pos[x][y] == "R":
                    img = pygame.transform.scale(pygame.image.load("images/white_rook.png"), (100, 100))
                    screen.blit(img, (y*100,x*100))
                elif piece_pos[x][y] == "r":
                    img = pygame.transform.scale(pygame.image.load("images/black_rook.png"), (100, 100))
                    screen.blit(img, (y*100,x*100))
                elif piece_pos[x][y] == "N":
                    img = pygame.transform.scale(pygame.image.load("images/white_knight.png"), (100, 100))
                    screen.blit(img, (y*100,x*100))
                elif piece_pos[x][y] == "n":
                    img = pygame.transform.scale(pygame.image.load("images/black_knight.png"), (100, 100))
                    screen.blit(img, (y*100,x*100))
                elif piece_pos[x][y] == "B":
                    img = pygame.transform.scale(pygame.image.load("images/white_bishop.png"), (100, 100))
                    screen.blit(img, (y*100,x*100))
                elif piece_pos[x][y] == "b":
                    img = pygame.transform.scale(pygame.image.load("images/black_bishop.png"), (100, 100))
                    screen.blit(img, (y*100,x*100))
                elif piece_pos[x][y] == "Q":
                    img = pygame.transform.scale(pygame.image.load("images/white_queen.png"), (100, 100))
                    screen.blit(img, (y*100,x*100))
                elif piece_pos[x][y] == "q":
                    img = pygame.transform.scale(pygame.image.load("images/black_queen.png"), (100, 100))
                    screen.blit(img, (y*100,x*100))
        pygame.display.flip()
    
    def get_legal_moves(self, turn):
        legal_moves = []
        if turn == "white":
            n = 0
        elif turn == "black":
            n = 1
        pawns = self.pos[n]
