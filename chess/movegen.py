from board import Board
from movemask import knightmoves, rook_occupancy_masks, rook_move_masks,bishop_occupancy_masks,bishop_move_maks,king_occupancy_masks, Wpawns_occupancy_masks, Wpawns_move_masks,Bpawns_occupancy_masks,Bpawns_move_masks

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



def legal_move_knight(pos,turn):
    moves= []
    #knight
    knight = pos[4+turn]
    while ctz(knight) != -1:
        square =ctz(knight)
        knight = remove_bit(knight,square)
        tmp = knightmoves[square] & invert(pos[12+turn])
        moves.append((square,tmp))
    return moves


def legal_move_rook(pos, turn,queen=0):
    moves= []
    rooks = pos[2+turn+queen]
    while ctz(rooks)!=-1:
        square = ctz(rooks)

        occupancy_bits = rook_occupancy_masks[square] & pos[14]
        tmp = rook_move_masks[square][occupancy_bits] & invert(pos[12+turn])
        moves.append((square,tmp))
        rooks = remove_bit(rooks, square)
    return moves



def legal_move_bischop(pos, turn,queen=0):
    moves= []
    bishop = pos[6+turn+queen]
    while ctz(bishop)!=-1:
        square = ctz(bishop)

        occupancy_bits = bishop_occupancy_masks[square] & pos[14]
        tmp = bishop_move_maks[square][occupancy_bits] & invert(pos[12+turn])
        moves.append((square,tmp))
        bishop = remove_bit(bishop, square)
    return moves        


def legal_move_king(pos, turn):
    moves = []
    square = ctz(pos[10+turn])
    tmp = king_occupancy_masks[square] & invert(pos[12+turn])
    
    if square !=-1:
        long, short = (pos[16+2*turn],pos[17+2*turn])
        if long and not get_bit(pos[14],square-1) and not get_bit(pos[14],square-2) and not get_bit(pos[14],square-3):
            tmp = tmp | 1<<square-2
        if short and not get_bit(pos[14],square+1) and not get_bit(pos[14],square+2):
            tmp = tmp | 1<<square+2

    moves = [(square,tmp)]
    return moves
    

def legal_move_pawn(pos,turn):
    moves = []
    pawns = pos[0+turn]
    while ctz(pawns) != -1:
        piece_enpassent = pos[14] | pos[15]
        square = ctz(pawns)
        if turn == 1:
            occupancy_bits = Bpawns_occupancy_masks[square] & piece_enpassent
            tmp = Bpawns_move_masks[square][occupancy_bits] & invert(pos[13])
        else:
            occupancy_bits = Wpawns_occupancy_masks[square] & piece_enpassent
            tmp = Wpawns_move_masks[square][occupancy_bits] & invert(pos[12])
        moves.append((square,tmp))
        pawns = remove_bit(pawns, square)
    return moves

def get_moves(pos, turn):
    legal_moves = []
    #which turn is it? white = 0, black = 1
    legal_moves.extend(legal_move_knight(pos,turn))
    
    legal_moves.extend(legal_move_rook(pos,turn))
    legal_moves.extend(legal_move_bischop(pos,turn))
    qr = legal_move_rook(pos,turn,6)
    qb = legal_move_bischop(pos,turn,2)
    queen = []
    for i in range(len(qb)):
        queen.append((qb[i][0],qb[i][1]|qr[i][1])) 
    legal_moves.extend(queen)

    #king
    legal_moves.extend(legal_move_king(pos,turn))

    #pawns
    legal_moves.extend(legal_move_pawn(pos,turn))
    return legal_moves

def check(pos, turn):
    king = pos[10+turn]
    moves = get_moves(pos,(turn+1)%2)
    pos_moves=0
    for move in moves:
        pos_moves = pos_moves | move[1]
    if pos_moves & king == 0:
        return 0
    else:
        return 1


def get_legal_moves(pos, turn):
    legal_moves = get_moves(pos,turn)
    tmp = []
    for move in legal_moves:
        pos_move = move[1]
        moves = 0
        while ctz(pos_move) != -1:

            b = Board(pos=pos.copy())
            square = ctz(pos_move)

            b.move(move[0], square)
            
            if check(b.pos, turn) == 0:
                moves |= 1<<square
            
            pos_move = remove_bit(pos_move,square) 
        
        if get_bit(pos[10+turn],move[0])==1 and (pos[15+2*turn]==1 or pos[16+2*turn]==1): # selects the king and removes castling when in check
            pos_copy1 = pos.copy()
            pos_copy1[10+turn] = 1<<move[0]+1
            pos_copy2 = pos.copy()
            pos_copy2[10+turn] = 1<<move[0]-1
            if check(pos, turn) == 1:
                moves = remove_bit(moves, move[0]+2)
                moves = remove_bit(moves, move[0]-2)
            if check(pos_copy1, turn) == 1:  #checks if king castle throug checks
                moves = remove_bit(moves, move[0]+2)
            if check(pos_copy2, turn) == 1:
                moves = remove_bit(moves, move[0]-2)
        tmp.append((move[0],moves))
        tmp = longer(tmp)
    return tmp

def longer(moves):
    list = []
    for move in moves:
        tmp = move[1]
        while tmp != 0:
            list.append((move[0],1<<ctz(tmp)))
            tmp = remove_bit(tmp, ctz(tmp))
    return list

def moveorder(moves,pos,turn):
    first = []
    third = []

    for move in moves:
        if move [1] == 0:
            pass
        elif move[1] & pos[13-turn] == 0:
            third.append(move)

        else:
            first.append(move)

    if third==0:
         pass
    else:
        first.extend(third)
    return first
