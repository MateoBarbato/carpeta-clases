import pygame , sys 
import config as cfg
from pygame import draw, time,event,display,font
from random import randint
from colisiones import *

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
contadorVidas = 3
contadorScore = cfg.SCORE
pos_y=cfg.POS_Y
pos_x = cfg.POS_X
mute = False
alive = True
vidasDificultad = 1
# LLAMO A LOS ASSETS
backgroundImage = pygame.image.load('./assets/background.jpg')
EnemiesImage0 = pygame.image.load('./assets/enemy0.png')
EnemiesImage1 = pygame.image.load('./assets/enemy1.png')
mainBlockImg = pygame.image.load('./assets/spaceShip.png')
bulletImg = pygame.image.load('./assets/bullet.png')
dying = pygame.mixer.Sound('./assets/dyingsound.mp3')
golpenave = pygame.mixer.Sound('./assets/golpenave.mp3')
explosionFinal = pygame.mixer.Sound('./assets/explosionFinal.mp3')
explosion = pygame.mixer.Sound('./assets/explosion.mp3')
music = pygame.mixer.music.load('./assets/8Bit.mp3')
pygame.mixer.music.play(-1)
bloques= []
disparos = []
enemiesImages = [EnemiesImage0,EnemiesImage1]
screen = display.set_mode(size)
backgroundRect = pygame.Rect(0,0,400,800)
# flags:
move_up = None
move_down = None
move_left = None
move_rigth = None
posiciones = True
musicIndex = True
hardcoreMode = False
# intervalo de spawn de bloques
time_interval = cfg.TIME_INTERVAL
deathInterval = cfg.DEATH_INTERVAL
shootInterval = cfg.SHOOT_INTERVAL
# evento personalizado 
deathEvent = pygame.USEREVENT+2
timer_event = pygame.USEREVENT+1
shootEvent = pygame.USEREVENT+3
# seteamos el timer
pygame.time.set_timer(timer_event, time_interval)
# volumen default
pygame.mixer.music.set_volume(0.5)

while is_running:
    clock.tick(cfg.FPS)
    # CHEQUEAR CON EL PROFE SI ALGO ASI ESTA BIEN
    # if alive:
    #     pygame.time.set_timer(timer_event, time_interval)
    # DETECTO EVENTOS
    screen.fill(cfg.BLACK)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            print('Saliendo')
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            disparos.append(crearDisparo(mainBlock['rect'].x,mainBlock['rect'].y,bulletImg))
        if event.type == deathEvent:
            is_running = False
        if event.type == shootEvent:
            disparos.append(crearDisparo(mainBlock['rect'].x,mainBlock['rect'].y,bulletImg))
        if event.type == timer_event:
            i = randint(1,4)
            if i%2==0:
                index = 0
                bloques.append(crearRecImagen(left=randint(50,350),ancho=ancho,alto=alto,top=0,image=enemiesImages[index],vidas=3))
            else:
                index = 1
                bloques.append(crearRecImagen(left=randint(50,350),ancho=ancho,alto=alto,top=0,image=enemiesImages[index],vidas=vidasDificultad))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print('Saliendo')
                sys.exit()
            if event.key == pygame.K_SPACE:
                disparos.append(crearDisparo(mainBlock['rect'].x,mainBlock['rect'].y,bulletImg))
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move_left = False
                move_rigth = True
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move_rigth = False
                move_left = True
            if event.key == pygame.K_h:
                hardcoreMode = not hardcoreMode
            if event.key == pygame.K_m:
                if mute == True:
                    pygame.mixer.music.set_volume(0.5)
                    mute = not mute
                else:
                    mute = not mute
                    pygame.mixer.music.set_volume(False)
            if event.key == pygame.K_k:
                if musicIndex == True:
                   music =  pygame.mixer.music.load('./assets/8BitMateo.mp3')
                   pygame.mixer.music.play(-1)
                   musicIndex = not musicIndex
                else:
                   music =  pygame.mixer.music.load('./assets/8Bit.mp3')
                   pygame.mixer.music.set_volume(0.3)
                   pygame.mixer.music.play(-1)
                   musicIndex = not musicIndex

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move_rigth = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move_left = False
    # keyspressed = pygame.key.get_pressed()
    mousepressed = pygame.mouse.get_pressed()
# ACTUALIZO ELEMENTOS
    # Blit De Textos
    backgroundImage = pygame.transform.scale(backgroundImage,(width,height))
    screen.blit(backgroundImage,backgroundRect)
    mainBlock = crearRecImagen(pos_x,pos_y,45,45,color=cfg.GREEN,image=mainBlockImg)
    screen.blit(mainBlock['image'],mainBlock['rect'])
    if alive:
        text_vidas = my_font.render(f'Vidas:{contadorVidas}',True,cfg.WHITE)
        screen.blit(text_vidas,(50,90))
        text_score = my_font.render(f'Score:{contadorScore}',True,cfg.WHITE)
        screen.blit(text_score,(width - 150, 90))
    else:
        text_death = deathFont.render(f'GAME OVER' , True , cfg.RED)
        screen.blit(text_death,((width - text_death.get_width())/2,(height - text_death.get_height())/2))
    # Blit de disparos
    if alive:
        for disparo in disparos:
            screen.blit(disparo['image'],disparo['rect'])
            pass
        for bloque in bloques:
            screen.blit(bloque['image'],bloque['rect'])

    # PREGUNTAR PORQUE EL BUG DE CUANDO ESTA EN FALSE LO TOMA COMO TRUE Y VICEVERSA, ACA DEBERIA IR UN TRUE PERO LO CONSIDERA UN FALSE Y NO DISPARA. SE QUEDA DISPARANDO CUANDO SOLTAS ES CLICK SI ESTA EN TRUE.
    # Y PORQUE EL BUG DE CUANDO PONGO LA BARRA ESPACIADORA TAMBIEN SOLO FUNCIONA CUANDO AMBAS CONDICIONES ESTAN
    if  mousepressed[0] == False : 
        pygame.time.set_timer(shootEvent, shootInterval)
    # if keyspressed[pygame.K_SPACE] == False :
    #     pygame.time.set_timer(shootEvent, shootInterval)

        
        
# MOVER ELEMENTOS

    # MUEVO LOS ALIENS CAYENDO Y LOS DISPAROS
    for disparo in disparos[:]:
        rectDisparo=disparo['rect']
        rectDisparo.y -= Speed * 2
        color = cfg.RED
        if rectDisparo.top > screen.get_height():
            disparos.remove(disparo)
    for bloque in bloques[:]:
        rect=bloque['rect']
        rect.y += Speed

    # AUMENTO LA DIFICULTAD CON HARDCORE MODE O CON PUNTOS A 30 PARA QUE EMPIEZEN A MOVERSE LOS OBJETOS
        if contadorScore > 30 or hardcoreMode == True:
            random = randint(0,2)
            if contadorScore > 2:
                random = randint(4,5)
            if posiciones == True : 
                if rect.x < width - rect.width:
                    rect.x += random
                else:
                    posiciones = False
            else:
                if rect.x > 0 :
                    rect.x -= random
                else:
                    posiciones=True
            
    # DETECTO COLISIONES
        if rect.top > screen.get_height():
            bloques.remove(bloque)
        # chequeo la colision con el tiro y los aliens
        for disparo in disparos:
            if detectar_colision_circ(rect,disparo['rect']):
                if bloque['vidas'] <= 1:
                    bloques.remove(bloque)
                    contadorScore +=1
                else:
                    bloque['vidas'] -= 1
                    # dificultad
                if contadorScore >= 50:
                    vidasDificultad = 2
                elif contadorScore >= 100:
                    vidasDificultad = 3
                disparos.remove(disparo)
                explosion.play()
        # detecto las colisiones con el mainbody para restar vidas
        if detectar_colision_circ(rect,mainBlock['rect']):
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
# MUEVO EL MAIN BLOCK
    if move_left and mainBlock['rect'].left > 0:
        pos_x -= Speed
    if move_rigth and mainBlock['rect'].right < width :
        pos_x += Speed

    # ACTUALIZO PANTALLA
    pygame.display.flip()

    