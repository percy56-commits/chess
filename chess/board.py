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

    # invert, or perform a bitflip on, a bitboard
    def invert(self,b):
        return b ^ (1<<64)-1

    def new_board(self):
        self.pos = [ 71776119061217280, 65280,   # pawns (white, black)
                9295429630892703744, 129,     # rooks
                4755801206503243776, 66,      # knights
                2594073385365405696, 36,      # bishops
                576460752303423488, 8,        # queens
                1152921504606846976, 16,      # kings
                18446462598732840960, 65535,  # white, black pieces
                18446462598732840960 | 65535, # all board pieces
                0,                            # en passent board 
                1,1,1,1                       # castling rights (wlong, wshort, blong, bshort)
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
        screen.fill((102,51,0))
        for x in range(0,8):
            for y in range(0,8):
                if (x+y)%2 == 0:
                    pygame.draw.rect(screen, (255,  224, 192),
                        [x*100, y*100, 100, 100])
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
        pygame.display.update()


    knightmoves = [132096, 329728, 659712, 1319424, 2638848, 5277696, 10489856, 4202496, 
               33816580, 84410376, 168886289, 337772578, 675545156, 1351090312, 2685403152, 1075839008, 
               8657044482, 21609056261, 43234889994, 86469779988, 172939559976, 345879119952, 687463207072, 275414786112, 
               2216203387392, 5531918402816, 11068131838464, 22136263676928, 44272527353856, 88545054707712, 175990581010432, 70506185244672, 
               567348067172352, 1416171111120896, 2833441750646784, 5666883501293568, 11333767002587136, 22667534005174272, 45053588738670592, 18049583422636032, 
               145241105196122112, 362539804446949376, 725361088165576704, 1450722176331153408, 2901444352662306816, 5802888705324613632, 11533718717099671552, 4620693356194824192, 
               37181722930207260672, 92810189938419040256, 185692438570387636224, 371384877140775272448, 742769754281550544896, 1485539508563101089792, 2952631991577515917312, 1182897499185874993152, 
               9518521070133058732032, 23759408624235274305536, 47537264274019234873344, 95074528548038469746688, 190149057096076939493376, 380298114192153878986752, 755873789843844074831872, 302821759791583998246912]

    def legal_move_rook(self, turn, queen=0):
        #rook
        legal = {}
        n = turn+queen
        rook = self.pos[2+n]
        while self.ctz(rook) != -1:
            teller = 1
            square = self.ctz(rook)
            moves = 0
            down = True
            while down and square + (8*teller) < 64:
                if self.get_bit(self.pos[14], square + (8*teller)) == 0:
                    moves += (1<< (square + 8*teller))
                    teller +=1
                else:
                    moves += (1<< (square + 8*teller))
                    down = False
            teller=1

            up = True
            while up and square - (8*teller) >= 0:
                if self.get_bit(self.pos[14], square - (8*teller)) == 0:
                    moves += (1<< (square - 8*teller))
                    teller +=1
                else:
                    moves += (1<< (square - 8*teller))
                    up = False
            #left en right
            right = True
            teller=1
            while right and (square + teller)%8 !=0:
                if self.get_bit(self.pos[14], square + teller) == 0:
                    moves += (1<< (square + teller))
                    teller +=1
                else:
                    moves += (1<< (square + teller))
                    right = False

            left = True
            teller=1
            while left and (square - teller)%8 !=7 and square - teller >= 0:

                if self.get_bit(self.pos[14], square - teller) == 0:
                    moves += (1<< (square - teller))
                    teller +=1
                else:
                    moves += (1<< (square - teller))
                    left = False


            legal[square]= moves & self.invert(self.pos[12+turn])
            rook = self.remove_bit(rook, square)
        return legal

    def legal_move_bischop(self, turn,queen=0):
        legal = {}
        n = turn+queen
        bischop = self.pos[6+n]
        while self.ctz(bischop) != -1:
            teller = 1
            square = self.ctz(bischop)
            moves = 0
            downleft = True
            while downleft and square + (7*teller) < 64  and (square + 7*teller)%8 !=7:
                if self.get_bit(self.pos[14], square + (7*teller)) == 0:
                    moves += (1<< (square + 7*teller))
                    teller +=1
                else:
                    moves += (1<< (square + 7*teller))
                    downleft = False
            
            teller=1
            upleft = True
            while upleft and square - (9*teller) >= 0 and (square - 9*teller)%8 !=7:
                if self.get_bit(self.pos[14], square - (9*teller)) == 0:
                    moves += (1<< (square - 9*teller))
                    teller +=1
                else:
                    moves += (1<< (square - 9*teller))
                    upleft = False

            downright = True
            teller=1
            while downright and (square + 9*teller)%8 !=0 and square + 9*teller < 64:
                if self.get_bit(self.pos[14], square + (9*teller)) == 0:
                    moves += (1<< (square + (9*teller)))
                    teller +=1
                else:
                    moves += (1<< (square + (9*teller)))
                    downright = False

            upright = True
            teller=1
            while upright and (square - 7*teller)%8 !=0 and square - 7*teller >= 0:
                if self.get_bit(self.pos[14], square - (7*teller)) == 0:
                    moves += (1<< (square - 7*teller))
                    teller +=1
                else:
                    moves += (1<< (square - 7*teller))
                    upright = False

            legal[square]= moves & self.invert(self.pos[12+turn])
            bischop = self.remove_bit(bischop, square)
        return legal        


    def get_moves(self, turn):
        legal_moves = {key: 0 for key in range(64)}
        #which turn is it? white = 0, black = 1
        n = turn
        #knight
        knight = self.pos[4+n]
        while self.ctz(knight) != -1:
            square = self.ctz(knight)
            knight = self.remove_bit(knight,square)
            legal_moves[square] =  Board.knightmoves[square] & self.invert(self.pos[12+n])
        
        legal_moves.update(self.legal_move_rook(turn))
        legal_moves.update(self.legal_move_bischop(turn))
        qr =  self.legal_move_rook(turn,6)
        qb = self.legal_move_bischop(turn,2)
        queen = {}
        for key in qr:
            queen[key] = qr[key] | qb[key]
        legal_moves.update(queen)

        #king
        king = self.pos[10+n]
        pos = self.ctz(king)
        if self.ctz(king) != -1:
            square = 1<<self.ctz(king)
            if pos%8 == 0 and pos!=56:
                moves = (square<<1) + (square<<9) +(square<<8) + (square>>7) + (square>>8)

            elif pos==56:
                moves = (square<<1) + (square>>7) + (square>>8)
            elif pos==63:
                moves = (square>>1) + (square>>9) +(square>>8) 
            elif pos%8 ==7 and pos!=63:
                moves = (square>>1) + (square>>9) +(square>>8) + (square<<7) + (square<<8)

            elif pos > 56:
                moves = (square<<1) + (square>>1) + (square>>7) + (square>>8) + (square>>9)

            else:
                moves = (square<<1) + (square>>1) + (square>>7) + (square>>8) + (square>>9) + (square<<7) + (square<<8) + (square<<9)

            if self.pos[16+2*n] ==1 and square>>1 & self.pos[14] == 0 and square>>3 & self.pos[14] == 0: #adds castling
                moves = moves | (square >>2)
            if self.pos[17+2*n] ==1 and square<<1 & self.pos[14] == 0:
                moves = moves | (square <<2)
            legal_moves[pos] =  moves & self.invert(self.pos[12+n])

        #pawns
        pawns = self.pos[0+n]
        tmp = Board()
        tmp.new_board()
        not_moved = pawns & tmp.pos[0+n]
        while self.ctz(not_moved) != -1:
            square = self.ctz(not_moved)
            moves = 0
            if self.get_bit(self.pos[14], square -16+n*32) == 0 and self.get_bit(self.pos[14], square-8+n*16) == 0:
                moves = (1<<square -16+n*32) + (1<<square -8+n*16)
            elif self.get_bit(self.pos[14], square -8+n*16) == 0:
                moves = 1<<square -8+n*16
            if self.get_bit(self.pos[13-n], square -9+n*18) == 1:
                moves = moves | 1<<square -9+n*18
            if self.get_bit(self.pos[13-n], square -7+n*14) == 1:
                moves = moves | 1<< square -7+n*14   
            legal_moves[square] = moves
            not_moved = self.remove_bit(not_moved, square)
            pawns = self.remove_bit(pawns, square)

        while self.ctz(pawns) != -1:

            square = self.ctz(pawns)
            moves = 0
            if self.get_bit(self.pos[14], square -8+n*16) == 0:
                moves = 1<<square -8+n*16
            if self.get_bit(self.pos[13-n], square -9+n*18) == 1 or self.get_bit(self.pos[15], square -9+n*18):
                moves = moves | 1<<square -9+n*18
            if self.get_bit(self.pos[13-n], square -7+n*14) == 1 or self.get_bit(self.pos[15], square -9+n*18):
                moves = moves | 1<<square -7+n*14
            legal_moves[square] = moves
            pawns = self.remove_bit(pawns, square)
        return legal_moves

    def get_legal_moves(self, turn):
        legal_moves = self.get_moves(turn)
        tmp = legal_moves.copy()
        for key in legal_moves:
            piece = legal_moves[key]
            while self.ctz(piece) >= 0:

                b = Board(pos=self.pos.copy())
                square = self.ctz(piece)

                b.move_for_get_legal_moves(key, square)
                if turn == 0:
                    moves = b.get_moves(1)
                else:
                    moves = b.get_moves(0)
                pos_moves=0
                for key1 in moves:
                    pos_moves = pos_moves | moves[key1]
                if pos_moves & b.pos[10+turn] != 0 and tmp[key] !=0:

                    tmp[key] = tmp[key] ^ 1<<square
                piece = self.remove_bit(piece,square) 
        return tmp


    def test(self, turn):
        legal_moves = self.get_moves(turn)
        if turn == 0:
            moves = self.get_moves(1)
        else:
            moves = self.get_moves(0)
        pos_moves=0
        for key in moves:
            pos_moves += moves[key]
        if pos_moves & self.pos[10+turn] != 0:
            pass
    

    def move(self, start, end):

        for i in range(12):
            self.pos[i] = self.remove_bit(self.pos[i],end)
            if self.get_bit(self.pos[i], start) == 1:
                self.pos[i] = self.set_bit(self.pos[i],end)
                self.pos[i] = self.remove_bit(self.pos[i],start)
                self.update_bitboards()
                if i == 0 or i ==1: # for en passent
                    if abs(start-end)==16:
                        self.pos[15] = self.set_bit(self.pos[15],int((start+end)/2)) # enables en passent
                        self.pos[15] = self.set_bit(self.pos[15],end)
                    elif 1<<end & self.pos[15]!=0:
                        self.pos[(i+1)%2] = self.pos[(i+1)%2] & self.invert(self.pos[15])
                        self.update_bitboards()
                    else:
                        self.pos[15] = 0
                elif i == 10 or i==11:  # for castling
                    self.pos[2*i-4] = 0
                    self.pos[2*i-3] = 0
                    if start == end-2:
                        self.pos[i-8] = self.set_bit(self.pos[i-8],start+1)
                        self.pos[i-8] = self.remove_bit(self.pos[i-8],end+1)
                        
                        self.update_bitboards()
                    elif start == end+2:
                        self.pos[i-8] = self.set_bit(self.pos[i-8],start-1)
                        self.pos[i-8] = self.remove_bit(self.pos[i-8],end-2)
                        self.update_bitboards()
                elif i == 2 or i == 3: # for castling
                    if start == 0 or start == 56:
                        self.pos[2*i+12] = 0
                    else:
                        self.pos[2*i+13] = 0
        return self

    def move_for_get_legal_moves(self, start, end):
        for i in range(12):
            self.pos[i] = self.remove_bit(self.pos[i],end)
            if self.get_bit(self.pos[i], start) == 1:
                self.pos[i] = self.set_bit(self.pos[i],end)
                self.pos[i] = self.remove_bit(self.pos[i],start)
                self.update_bitboards()
                if i == 10 or i==11:
                    self.pos[2*i-4] = 0
                    self.pos[2*i-3] = 0
                    if start == end-2:
                        self.pos[i-8] = self.set_bit(self.pos[i-8],start+1)
                        self.pos[i-8] = self.remove_bit(self.pos[i-8],end+1)
                        self.pos[i] = self.set_bit(self.pos[i], start+1)
                        self.update_bitboards()
                    elif start == end+2:
                        self.pos[i-8] = self.set_bit(self.pos[i-8],start-1)
                        self.pos[i-8] = self.remove_bit(self.pos[i-8],end-2)
                        self.pos[i] = self.set_bit(self.pos[i], start-1)
                        self.update_bitboards()
                        
                elif i == 2 or i == 3:
                    if start == 0 or start == 56:
                        self.pos[2*i+12] = 0
                    else:
                        self.pos[2*i+13] = 0
        return self
