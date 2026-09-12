from board import Board
from movegen import get_legal_moves, moveorder
from psqt import PESTO





def get_bit( b, square):
        return 1 if (b & (1<<square)) else 0

#sets a piece on a square
def set_bit( b, square):
    return b | (1<<square)
    

#removes a bit from a square
def remove_bit( b, square):
    return b ^ ( 1<<square if get_bit(b , square) else 0 )
    

#counts zeros until you hit a piece
def ctz(b): # count trailing zeros
    return (b & -b).bit_length() - 1

# invert, or perform a bitflip on, a bitboard
def invert(b):
    return b ^ (1<<64)-1

pawntable = [0,0,0,0,0,0,0,0, 
                150, 150, 150, 150, 150, 150, 150, 150, 
                110, 110, 120, 130, 130, 120, 110, 110, 
                105, 105, 110, 125, 125, 110, 105, 105, 
                100, 100, 100, 120, 120, 100, 100, 100, 
                105, 95, 90, 100, 100, 90, 95, 105, 
                105, 110, 110, 80, 80, 110, 110, 105, 
                0,0,0,0,0,0,0,0]

horsetable = [270, 280, 290, 290, 290, 290, 280, 270, 
                280, 300, 320, 320, 320, 320, 300, 280, 
                290, 320, 330, 335, 335, 330, 320, 290, 
                290, 325, 335, 340, 340, 335, 325, 290, 
                290, 320, 335, 340, 340, 335, 320, 290, 
                290, 325, 330, 335, 335, 330, 325, 290, 
                280, 300, 320, 325, 325, 320, 300, 280, 
                270, 280, 290, 290, 290, 290, 280, 270]

rooktable = [500, 500, 500, 500, 500, 500, 500, 500, 
                505, 510, 510, 510, 510, 510, 510, 505, 
                495, 500, 500, 500, 500, 500, 500, 495, 
                495, 500, 500, 500, 500, 500, 500, 495, 
                495, 500, 500, 500, 500, 500, 500, 495, 
                495, 500, 500, 500, 500, 500, 500, 495, 
                495, 500, 500, 500, 500, 500, 500, 495, 
                500, 500, 500, 505, 505, 500, 500, 500]
bishoptable = [310, 320, 320, 320, 320, 320, 320, 310, 
                320, 330, 330, 330, 330, 330, 330, 320, 
                320, 330, 335, 340, 340, 335, 330, 320, 
                320, 335, 335, 340, 340, 335, 335, 320, 
                320, 330, 340, 340, 340, 340, 330, 320, 
                320, 340, 340, 340, 340, 340, 340, 320, 
                320, 335, 330, 330, 330, 330, 335, 320, 
                310, 320, 320, 320, 320, 320, 320, 310]

queentable = [880, 890, 890, 895, 895, 890, 890, 880, 
                890, 900, 900, 900, 900, 900, 900, 890, 
                890, 900, 905, 905, 905, 905, 900, 890, 
                895, 900, 905, 905, 905, 905, 900, 895, 
                900, 900, 905, 905, 905, 905, 900, 895, 
                890, 905, 905, 905, 905, 905, 900, 890, 
                890, 900, 905, 900, 900, 900, 900, 890, 
                880, 890, 890, 895, 895, 890, 890, 880]

kingsafety = [(19970, 19950), (19960, 19960), (19960, 19970), (19950, 19980), (19950, 19980), (19960, 19970), (19960, 19960), (19970, 19950), (19970, 19970), (19960, 19980), (19960, 19990), (19950, 20000), (19950, 20000), (19960, 19990), (19960, 19980), (19970, 19970), (19970, 19970), (19960, 19990), (19960, 20020), (19950, 20030), (19950, 20030), (19960, 20020), (19960, 19990), (19970, 19970), (19970, 19970), (19960, 19990), (19960, 20030), (19950, 20040), (19950, 20040), (19960, 20030), (19960, 19990), (19970, 19970), (19980, 19970), (19970, 19990), (19970, 20030), (19960, 20040), (19960, 20040), (19970, 20030), (19970, 19990), (19980, 19970), (19990, 19970), (19980, 19990), (19980, 20020), (19980, 20030), (19980, 20030), (19980, 20020), (19980, 19990), (19990, 19970), (20020, 19970), (20020, 19970), (19990, 20000), (19980, 20000), (19980, 20000), (19990, 20000), (20020, 19970), (20020, 19970), (20020, 19950), (20030, 19970), (20010, 19970), (20000, 19970), (20000, 19970), (20010, 19970), (20030, 19970), (20020, 19950)]


MG_PIECE_VALUES = (82, 477, 337, 365,  1025, 24000)

EG_PIECE_VALUES = (94, 512, 281, 297,  936, 24000)

PIECE_VALUES = (MG_PIECE_VALUES, EG_PIECE_VALUES)

#counts the amount of files a pawn is dubbled
filemask = [72340172838076673, 144680345676153346, 289360691352306692, 578721382704613384, 1157442765409226768, 2314885530818453536, 4629771061636907072, 9259542123273814144]
def dubble_pawns(pos):
    Wdubble = 0
    Bdubble = 0
    for i in range(8):
        white = pos[0] & filemask[i]
        black = pos[1] & filemask[i]
        if white.bit_count() >1:
            Wdubble += 1
        if black.bit_count() >1:
            Bdubble += 1
    
    return (Wdubble*80,Bdubble*80)

def openfile(pos): #search for rooks on open files and gives a bonus
    Wopen = 0
    Bopen = 0
    for i in range(8):
        white = pos[0] & filemask[i]
        black = pos[1] & filemask[i]
        if white ==0:
            if pos[2] & filemask[i] != 0:
                Wopen += 1
        if black ==0:
            if pos[3] & filemask[i] != 0:
                Bopen += 1
    return (Wopen*50,Bopen*50)


def inverersePSQT(table):
    tmp = []
    for i in range(7,-1,-1):
        tmp.extend(table[i*8:i*8+8])
    return tmp
def evaluation(pos,turn):

    if pos[8] | pos[9] == 0 or (pos[8] | pos[9] != 0 and pos[14] <=12):
        endgame = 1
    else: 
        endgame = 0
    white_material =  sum([int(y)*z for (y, z) in zip(list(bin(pos[0])[2:].zfill(64)), pawntable[::-1])]) + \
        sum([int(y) * z for (y, z) in zip(list(bin(pos[2])[2:].zfill(64)), rooktable[::-1])])+ \
        sum([int(y) * z for (y, z) in zip(list(bin(pos[4])[2:].zfill(64)), horsetable[::-1])]) +\
        sum([int(y) * z for (y, z) in zip(list(bin(pos[6])[2:].zfill(64)), bishoptable[::-1])]) + \
        sum([int(y) * z for (y, z) in zip(list(bin(pos[8])[2:].zfill(64)), queentable[::-1])]) +\
        kingsafety[ctz(pos[10])][endgame]
    

    black_material = sum([int(y) * z for (y, z) in zip(list(bin(pos[1])[2:].zfill(64)), pawntable)]) + \
        sum([int(y) * z for (y, z) in zip(list(bin(pos[3])[2:].zfill(64)), rooktable)]) + \
        sum([int(y) * z for (y, z) in zip(list(bin(pos[5])[2:].zfill(64)), horsetable)]) + \
        sum([int(y) * z for (y, z) in zip(list(bin(pos[7])[2:].zfill(64)), bishoptable)]) + \
        sum([int(y) * z for (y, z) in zip(list(bin(pos[9 ])[2:].zfill(64)), queentable)]) +\
        kingsafety[::-1][ctz(pos[11])][endgame]

    (Wdubble,Bdubble) = dubble_pawns(pos)
    (Wopen,Bopen) = openfile(pos)

    eval = white_material - Wdubble + Wopen - (black_material - Bdubble + Bopen)
    return eval

def evaluation_fast(pos,turn):
    if pos[8] | pos[9] == 0 or (pos[8] | pos[9] != 0 and pos[14] <=12):
        endgame = 1
    else: 
        endgame = 0
    white_mat = 0
    black_mat = 0
    for i in range(6): #makes a list of al pieces an their positions
        Wpieces = pos[i*2]
        Bpieces = pos[i*2+1]
        while ctz(Wpieces) != -1: #checks the white pieces
            square = ctz(Wpieces)
            white_mat += PIECE_VALUES[endgame][i] + PESTO[endgame][i][square]
            Wpieces = remove_bit(Wpieces,square)
        while ctz(Bpieces) != -1: #checks the white pieces
            square = ctz(Bpieces)
            black_mat += PIECE_VALUES[endgame][i] + inverersePSQT(PESTO[endgame][i])[square]
            Bpieces = remove_bit(Bpieces,square)

    (Wdubble,Bdubble) = dubble_pawns(pos)
    (Wopen,Bopen) = openfile(pos)

    eval = white_mat - Wdubble + Wopen - (black_mat - Bdubble + Bopen)
    return eval

def ischeckmate(pos, turn):
    moves = get_legal_moves(pos, turn)
    for move in moves:
        if move[1] != 0:
            return 0
    return 1


def minmax(pos, turn, depth, alpha = float('-inf'), beta= float('inf')):
    if ischeckmate(pos,turn)==1:
        if turn == 0:
            return (-9999,0,0)
        else:
            return (9999,0,0)
    elif depth==0: 
         return (evaluation(pos,turn),0,0)
    else:
        if turn == 0:
            moves = get_legal_moves(pos,turn)
            order = moveorder(moves,pos,turn)
            sqaure1 = None
            sqaure2 = None
            for move in order:
                piece = move[1]
                
                while ctz(piece) != -1:
                    b = Board(pos = pos.copy())
                    end = ctz(piece)
                    b.move(move[0], end)
                    piece = remove_bit(piece, end)
                    eval, a, c = minmax(b.pos, 1,depth-1, alpha, beta)
                    
                    if eval > alpha:
                        alpha = eval
                        sqaure1 = move[0]
                        sqaure2 = end
                        if alpha>=beta:
                            break
                if alpha>=beta:
                    break
            return (alpha, sqaure1, sqaure2)
        else:
            moves = get_legal_moves(pos,turn)
            order = moveorder(moves,pos,turn)
            sqaure1 = None
            sqaure2 = None   
            for move in order:
                piece = move[1]
                while ctz(piece) != -1:
                    b = Board(pos = pos.copy())
                    end = ctz(piece)
                    b.move(move[0], end)
                    piece = remove_bit(piece, end)
                    eval, a, c = minmax(b.pos,0,depth-1, alpha, beta)
                    if eval < beta:
                        beta = eval
                        sqaure1 = move[0]
                        sqaure2 = end
                        if alpha>=beta:
                            break
                if alpha>=beta:
                    break
            return (beta, sqaure1, sqaure2)

def minmax_fast(pos, turn, depth, alpha = float('-inf'), beta= float('inf')):
    if ischeckmate(pos,turn)==1:
            if turn == 0:
                return (-9999,0,0)
            else:
                return (9999,0,0)
    elif depth==0: 
            return (evaluation_fast(pos,turn),0,0)
    else:
        if turn == 0:
            moves = get_legal_moves(pos,turn)
            order = moveorder(moves,pos,turn)
            sqaure1 = None
            sqaure2 = None
            for move in order:
                piece = move[1]
                
                while ctz(piece) != -1:
                    b = Board(pos = pos.copy())
                    end = ctz(piece)
                    b.move(move[0], end)
                    piece = remove_bit(piece, end)
                    eval, a, c = minmax_fast(b.pos, 1,depth-1, alpha, beta)
                    
                    if eval > alpha:
                        alpha = eval
                        sqaure1 = move[0]
                        sqaure2 = end
                        if alpha>=beta:
                            return (alpha, sqaure1, sqaure2)

            return (alpha, sqaure1, sqaure2)
        else:
            moves = get_legal_moves(pos,turn)
            order = moveorder(moves,pos,turn)
            sqaure1 = None
            sqaure2 = None   
            for move in order:
                piece = move[1]
                while ctz(piece) != -1:
                    b = Board(pos = pos.copy())
                    end = ctz(piece)
                    b.move(move[0], end)
                    piece = remove_bit(piece, end)
                    eval, a, c = minmax_fast(b.pos,0,depth-1, alpha, beta)
                    if eval < beta:
                        beta = eval
                        sqaure1 = move[0]
                        sqaure2 = end
                        if alpha>=beta:
                            return (beta, sqaure1, sqaure2)
            return (beta, sqaure1, sqaure2)
    
