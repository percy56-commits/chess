#import modules
import pygame
from board import Board
#initialize game
pygame.init()


#draw the board
#set display width and height
window = pygame.display.set_mode((800,800))
pygame.display.set_caption('Chess')
window.fill((102,51,0))
sqsize = 100
#Using draw.rect module of
#pygame to draw the solid rectangle
for x in range(0,8):
    for y in range(0,8):
        if (x+y)%2 == 0:
            pygame.draw.rect(window, (255,  224, 192),
                [x*sqsize, y*sqsize, sqsize, sqsize])
pygame.display.update()

#start a new chess match
game = Board(pos=1)
game.new_board()

game.pos[game.Bpawn] = game.set_bit(game.pos[game.Bpawn], game.e5)

game.pos[game.Bpawn] = game.remove_bit(game.pos[game.Bpawn], game.e7)

game.update_bitboards()
game.print_board()

running = True
#keep game running until quit
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Draws the pieces on to the screen.
    game.draw_pieces(window)
    
    

