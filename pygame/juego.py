import pygame , sys 
import config as cfg
from pygame import draw, time,event,display,font
from random import randint
import colisiones

pygame.init()
font.init()

Speed = cfg.VELOCIDAD 
my_font = pygame.font.SysFont('Comic Sans MS', 24,True)
deathFont = pygame.font.SysFont('Comic Sans MS', 38,True)
clock = time.Clock()
width = cfg.WIDTH
height = cfg.HEIGHT
size = (width,height)
is_running = True
ancho=cfg.ANCHO
alto=cfg.ALTO
contadorVidas = cfg.VIDAS
contadorScore = cfg.SCORE
pos_y=cfg.POS_Y
pos_x = cfg.POS_X
tiro = ''
color = cfg.GREEN
mute = False
alive = True
# LLAMO A LOS ASSETS
backgroundImage = pygame.image.load('./assets/background.jpg')
EnemiesImage0 = pygame.image.load('./assets/enemy0.png')
EnemiesImage1 = pygame.image.load('./assets/enemy1.png')
mainBlockImg = pygame.image.load('./assets/spaceShip.png')
dying = pygame.mixer.Sound('./assets/dyingsound.mp3')
golpenave = pygame.mixer.Sound('./assets/golpenave.mp3')
explosionFinal = pygame.mixer.Sound('./assets/explosionFinal.mp3')
explosion = pygame.mixer.Sound('./assets/explosion.mp3')
music = pygame.mixer.music.load('./assets/8BitMateo.mp3')
pygame.mixer.music.play(-1)
bloques= []
enemiesImages = [EnemiesImage0,EnemiesImage1]

screen = display.set_mode(size)
backgroundRect = pygame.Rect(0,0,400,800)
# movements:
move_up = None
move_down = None
move_left = None
move_rigth = None

# intervalo de spawn de bloques
time_interval = 900
deathInterval = 2400
# evento personalizado 
deathEvent = pygame.USEREVENT+2
timer_event = pygame.USEREVENT+1
# seteamos el timer
pygame.time.set_timer(timer_event, time_interval)


while is_running:
    clock.tick(cfg.FPS)
    # CHEQUEAR CON EL PROFE
    # if alive:
    #     pygame.time.set_timer(timer_event, time_interval)
    # DETECTO EVENTOS
    screen.fill(cfg.BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Saliendo')
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            color = cfg.GREEN
        if event.type == deathEvent:
            is_running = False
        if event.type == timer_event:
            i = randint(1,4)
            if i%2==0:
                random = 0
            else:
                random = 1
            bloques.append(colisiones.crearRecImagen(left=randint(50,350),ancho=ancho,alto=alto,top=0,image=enemiesImages[random]))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move_left = False
                move_rigth = True
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move_rigth = False
                move_left = True
            if event.key == pygame.K_m:
                if mute == True:
                    pygame.mixer.music.set_volume(1)
                    mute = False
                elif mute == False:
                    mute = True
                    pygame.mixer.music.set_volume(False)
                    
            if event.key == pygame.K_ESCAPE:
                print('Saliendo')
                sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move_rigth = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move_left = False

# ACTUALIZO ELEMENTOS
    # Blit De Todo
    backgroundImage = pygame.transform.scale(backgroundImage,(width,height))
    screen.blit(backgroundImage,backgroundRect)
    mainBlock = colisiones.crearRecImagen(pos_x,pos_y,45,45,color=cfg.GREEN,image=mainBlockImg)
    screen.blit(mainBlock['image'],mainBlock['rect'])
    if alive:
        text_vidas = my_font.render(f'Vidas:{contadorVidas}',True,cfg.WHITE)
        screen.blit(text_vidas,(50,90))
        text_score = my_font.render(f'Score:{contadorScore}',True,cfg.WHITE)
        screen.blit(text_score,(width - 150, 90))
    else:
        text_death = deathFont.render(f'GAME OVER' , True , cfg.RED)
        screen.blit(text_death,((width - text_death.get_width())/2,(height - text_death.get_height())/2))
    # DISPARAR
    if pygame.mouse.get_pressed()[0] == True and clock.get_rawtime() == 1:
       tiro = draw.line(screen,cfg.WHITE,(mainBlock['rect'].centerx,mainBlock['rect'].centery-20),(mainBlock['rect'].centerx,0))
       color = cfg.RED
    # DIBUJO LOS BLOQUES
    if alive:
        for bloque in bloques:
            screen.blit(bloque['image'],bloque['rect'])
    else:
        for bloque in bloques:
            # FORMA DE HACER INVISIBLE A LOS OBJETOS QUE CAEN AL MORIR
            # screen.blit(bloque['image'],bloque['rect'])
            pass

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
                contadorScore +=1
                explosion.play()
        # detecto las colisiones con el mainbody para restar vidas
        if colisiones.detectar_colision_circ(rect,mainBlock['rect']):
            time = pygame.time.get_ticks()
            if contadorVidas == 1 :
                alive = False
                bloques = []
                pygame.mixer.music.stop()
                explosionFinal.play()
                dying.play()
                # esperar 4 secs
                pygame.time.set_timer(deathEvent, deathInterval)
            else:
                contadorVidas -= 1
                golpenave.play()
                bloques.remove(bloque)
                
                

        
    # # BLOQUE PRINCIPAL
    # mainBlock = draw.circle(screen,color,(pos_x,pos_y),26,19,draw_top_left=True,draw_top_right=True)
    
   
    
    if move_left and mainBlock['rect'].left > 0:
        pos_x -= Speed
    
    if move_rigth and mainBlock['rect'].right < width :
        pos_x += Speed
    



    # ACTUALIZO PANTALLA
    pygame.display.flip()

    