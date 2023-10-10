import pygame , sys 
import config 
from pygame import draw, time,event,display


Speed = config.VELOCIDAD + 5 

pygame.init()
clock = time.Clock()

height=800
width = 400
size = (width,height)
is_running = True
bajando = True
haciaDerecha = True
ancho=50
alto=50

pos_y1=700
pos_x1 = 150


screen = display.set_mode(size)

# movements:
move_up = None
move_down = None
move_left = None
move_rigth = None


# evento personalizado 

EVENT_NEW_COIN = pygame.USEREVENT + 1

while is_running:
    clock.tick(config.FPS)
    # DETECTO EVENTOS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Saliendo')
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print('CLikeaste wey')
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move_rigth = True
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                move_down = True
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                move_up = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move_rigth = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                move_down = False
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                move_up = False 
            if event.key == pygame.K_ESCAPE:
                print('Saliendo')
                sys.exit()
            

    # ACTUALIZO ELEMENTOS
    screen.fill(config.BLACK)
    r = draw.rect(screen,config.RED,(pos_x1,pos_y1,ancho,alto))
    # r2 = draw.rect(screen,config.RED,(pos_x2,pos_y2,ancho,alto))
    


    # if move_down and r.bottom < height:
    #     pos_y1 += Speed
    
    # if move_up and r.top > 0:
    #     pos_y1 -= Speed

    if move_left and r.left > 0:
        pos_x1 -= Speed
    
    if move_rigth and r.right < width :
        pos_x1 += Speed


    # if bajando == True:
    #     if pos_y <  height - alto:
    #         pos_y += Speed
    #     else:
    #         bajando=False
    # else:
    #     if pos_y > 0 :
    #         pos_y -= Speed
    #     else:
    #         bajando=True

    # if haciaDerecha == True : 
    #     if pos_x < width - ancho:
    #         pos_x += Speed
    #     else:
    #         haciaDerecha = False
    # else:
    #     if pos_x > 0 :
    #         pos_x -= Speed
    #     else:
            
    #         haciaDerecha=True

    
   


    # ACTUALIZO PANTALLA
    pygame.display.flip()

    