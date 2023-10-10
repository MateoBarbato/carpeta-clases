import pygame , sys 
import config 
from pygame import draw, time,event,display
from random import randint
import colisiones

Speed = config.VELOCIDAD 

pygame.init()
clock = time.Clock()

height=800
width = 400
size = (width,height)
is_running = True

ancho=30
alto=30
bloques= []

pos_y=700
pos_x =( width - 50 )//2 

pos_BloquesCaida = 0

screen = display.set_mode(size)

# movements:
move_up = None
move_down = None
move_left = None
move_rigth = None

# evento personalizado 
EVENT_NEW_COIN = pygame.USEREVENT + 1

# block_dict = [
#     {"rect":pygame.Rect(pos_BloquesCaida,randint(50,350),ancho,alto),'color':config.GREEN},
#     {"rect":pygame.Rect(pos_BloquesCaida,randint(50,350),ancho,alto),'color':config.GREEN},
#     {"rect":pygame.Rect(pos_BloquesCaida,randint(50,350),ancho,alto),'color':config.GREEN},
#     {"rect":pygame.Rect(pos_BloquesCaida,randint(50,350),ancho,alto),'color':config.GREEN},
#     {"rect":pygame.Rect(pos_BloquesCaida,randint(50,350),ancho,alto),'color':config.GREEN},
#     # {"rect":pygame.Rect(133,250,ancho,alto),'color':config.RED},
#     # {"rect":pygame.Rect(133,250,ancho,alto),'color':config.RED},
#     # {"rect":pygame.Rect(133,250,ancho,alto),'color':config.RED},
#     # {"rect":pygame.Rect(133,250,ancho,alto),'color':config.RED},
#     ]



while is_running:
    clock.tick(config.FPS)
    # DETECTO EVENTOS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Saliendo')
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if mainBlock.centerx == 
            pass
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
    if bloques == []:
        for i in range (2):
            b=colisiones.crearBloque(pos_BloquesCaida,randint(50,350),ancho,alto)
            bloques.append(b)
    # DIBUJO LOS BLOQUES
    for bloque in block_dict:
        draw.rect(screen,bloque['color'],bloque['rect'])

    # BLOQUE PRINCIPAL
    mainBlock = draw.circle(screen,config.RED,(pos_x,pos_y),26,draw_top_left=True,draw_top_right=True)

    if move_left and mainBlock.left > 0:
        pos_x -= Speed
    
    if move_rigth and mainBlock.right < width :
        pos_x += Speed
   


    # ACTUALIZO PANTALLA
    pygame.display.flip()

    