from board import Board
knightmoves = []
for i in range(0,64):
    if i%8 ==0 :
        tmp = [(2**i)<<10,(2**i)<<17,(2**i)>>6,(2**i)>>15]
    elif i%8==1:
        tmp = [(2**i)<<10,(2**i)<<15,(2**i)<<17,(2**i)>>6,(2**i)>>15,(2**i)>>17]
    elif i%8 ==6:
        tmp = [(2**i)<<6,(2**i)<<15,(2**i)<<17,(2**i)>>10,(2**i)>>15,(2**i)>>17]
    elif i%8 == 7:
        tmp = [(2**i)<<6,(2**i)<<15,(2**i)>>10,(2**i)>>17]
    else:
        tmp = [(2**i)<<6,(2**i)<<10,(2**i)<<15,(2**i)<<17,(2**i)>>6,(2**i)>>10,(2**i)>>15,(2**i)>>17]
    knightmoves.append(sum(tmp))
move = Board(pos=knightmoves[63])
move.print_bitboard()
