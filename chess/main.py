#import modules
import pygame
from board import Board
from movegen import get_legal_moves
from engine import minmax_fast
from engine import minmax
from openings import openings, convert
#initialize game
pygame.init()


#draw the board
#set display width and height
window = pygame.display.set_mode((800,800))
pygame.display.set_caption('Chess')



#start a new chess match
game = Board(pos=1)
game.new_board()

def make_a_move(turn):
    not_moved = True
    playing=0
    start=64
    legal_moves = get_legal_moves(game.pos,turn)
    tmp = 0
    for move in legal_moves:
        tmp = tmp | move[1]
    other_move= get_legal_moves(game.pos,(turn+1)%2)
    pos_moves=0
    for move in other_move:
        pos_moves = pos_moves | move[1]
    if tmp == 0 and game.pos[10+turn] & pos_moves != 0:
        print('mate')
        playing = 'mate'
        not_moved=False
    elif tmp == 0 :
        playing = 'stalemate'
        not_moved=False
    while not_moved:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos=pygame.mouse.get_pos()
                    square = int(pos[0]/100)+int(pos[1]/100)*8
                    if 1<<square & game.pos[12+turn] !=0:
                        start=square
                    elif start != square and start <64:
                        end = square
                        if (start,1<<end) in legal_moves:
                            game.move(start,end)
                            not_moved = False
                        else:
                            print("This move is not legal")
    return playing


running = True
turn = 0
#keep game running until quit
game.draw_pieces(window)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    game.draw_pieces(window)
    #whites move
    play = make_a_move(turn%2)
    turn +=1
    game.draw_pieces(window)
    if play == "mate":
        print("checkmate")
        running = False
        game.print_board()
    if play =='stalemate':
        print('stalemate')
        running = False
        game.print_board()
    tmp = convert(game.pos)
    if tmp in openings:
        start,end = openings[tmp]
        eval = 0
    else:
        eval, start, end = minmax(game.pos,turn%2,3)
    print(eval, start, end)
    if start == 0 and end == 0:
        print("checkmate, white won")
        running = False
        game.print_board()
    else:
        game.move(start, end)
    turn +=1
    game.draw_pieces(window)
    print(turn)
    
game.print_board()
