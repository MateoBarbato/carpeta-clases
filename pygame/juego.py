import pygame , sys 
import config 
from pygame import draw, time,event,display,font
from random import randint
import colisiones

Speed = config.VELOCIDAD 

pygame.init()
font.init()

my_font = pygame.font.SysFont('Comic Sans MS', 18)
clock = time.Clock()

height=800
width = 400
size = (width,height)
is_running = True

ancho=25
alto=25
bloques= []
contadorVidas = 3
pos_y=700
pos_x =( width - 50 )//2 

pos_BloquesCaida = 0
tiro = ''

screen = display.set_mode(size)
color = config.GREEN
# movements:
move_up = None
move_down = None
move_left = None
move_rigth = None
counter = 0
# intervalo de spawn de bloques
time_interval = 900
# evento personalizado 
timer_event = pygame.USEREVENT+1
# seteamos el timer
pygame.time.set_timer(timer_event, time_interval)

while is_running:
    clock.tick(config.FPS)
    print()
    # DETECTO EVENTOS
    screen.fill(config.BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Saliendo')
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            color = config.RED
        if event.type == pygame.MOUSEBUTTONUP:
            color = config.GREEN
            # draw.line(screen,config.WHITE,(mainBlock.centerx,mainBlock.centery-20),(mainBlock.centerx,0))
        if event.type == timer_event:
            bloques.append(colisiones.crearBloque(left=randint(50,350),top=0))
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

    # DISPARAR
    if pygame.mouse.get_pressed()[0] == True and clock.get_rawtime() == 1:
       tiro = draw.line(screen,config.WHITE,(mainBlock.centerx,mainBlock.centery-20),(mainBlock.centerx,0))
       
    
    text_vidas = my_font.render(f'Vidas:{contadorVidas}',True,config.WHITE)
    screen.blit(text_vidas,(50,90))
    # DIBUJO LOS BLOQUES
    for bloque in bloques:
        draw.rect(screen,config.BLUE,bloque['rect'])
    # HAGO CAER LOS BLOQUES Y DETECTO COLISIONES
    for bloque in bloques[:]:
        
        # muevo los bloques que caen
        rect=bloque['rect']
        rect.y += Speed
        if rect.top > screen.get_height():
            bloques.remove(bloque)
        # chequeo la colision con la recta de tiro
        if tiro != '':
            if tiro.colliderect(bloque['rect']):
                bloques.remove(bloque)
        # detecto las colisiones con el mainbody para restar vidas
        if colisiones.detectar_colision_circ(rect,mainBlock):
            if contadorVidas == 1 :
                bloques = []
                is_running = False
            else:
                contadorVidas -= 1
                bloques.remove(bloque)

        
    # BLOQUE PRINCIPAL
    mainBlock = draw.circle(screen,color,(pos_x,pos_y),26,19,draw_top_left=True,draw_top_right=True)
    
   
    
    if move_left and mainBlock.left > 0:
        pos_x -= Speed
    
    if move_rigth and mainBlock.right < width :
        pos_x += Speed
    



    # ACTUALIZO PANTALLA
    pygame.display.flip()

    