#import modules
import pygame
from board import Board
from movegen import get_legal_moves
from engine import minmax_fast
from engine import minmax
from openings import openings, convert


squares = ['a8', 'b8', "c8", 'd8', 'e8', "f8", "g8", "h8", 
            'a7', 'b7', 'c7', 'd7', "e7", "f7", "g7", "h7", 
            'a6', "b6", 'c6', 'd6', 'e6', 'f6', 'g6', 'h6', 
            'a5', 'b5', 'c5', 'd5', 'e5', 'f5','g5', 'h5', 
            'a4', 'b4', "c4", 'd4', 'e4', 'f4', 'g4', 'h4', 
            'a3', "b3", 'c3', 'd3', 'e3', 'f3', 'g3', 'h3', 
            "a2", 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2', 
            'a1', 'b1', "c1", 'd1', 'e1', 'f1', 'g1', 'h1']
def change_notation(move):
    start = None
    end = None
    for i in range(64):
        if move[0:2] == squares[i]:
            start = i
        elif move[4:6] == squares[i]:
            
            end = i
    if start ==None or end == None:
        return (128,0)

    return (start,end)


print("K/k is King")
print("Q/q is queen")
print("R/r is rook")
print("B/b is bishop")
print("N/n is Knigth")
print("P/p is pawn")
print("Upper case letters are white, lower case are black")

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
            move = input("Geef de zet die je wil spelen in formaat: start, eind: ")
            start,end = change_notation(move)
            print(start)
            print(end)
            if start != 128 and (start,1<<end) in legal_moves:
                game.move(start,end)
                not_moved = False
            else:
                print("This move is not legal")

    return playing


running = True
turn = 0
#keep game running until quit


while running:
    game.print_board()
    #whites move
    play = make_a_move(turn%2)
    turn +=1
    game.print_board()
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
    
    print(turn)
    
game.print_board()
