#import modules
import pygame
from board import Board
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
    legal_moves = game.get_legal_moves(turn)
    tmp = 0
    for key in legal_moves:
        tmp = tmp | legal_moves[key]
    other_move= game.get_legal_moves((turn+1)%2)
    pos_moves=0
    for key1 in other_move:
        pos_moves = pos_moves | other_move[key1]
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
                    elif start !=square and start <64:
                        end = square
                        legal_move = legal_moves[start]
                        if legal_move & 1<<end == 0:
                            print('This move is not legal')
                        else:
                            game.move(start,end)
                            not_moved = False
    return playing


running = True
turn = 0
#keep game running until quit
game.draw_pieces(window)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #whites move
    play = make_a_move(turn%2)
    turn +=1
    game.draw_pieces(window)

    
    if play == "mate":
        print("checkmate")
        running = False
    if play =='stalemate':
        print('stalemate')
        running = False
print('game over')
    
    
