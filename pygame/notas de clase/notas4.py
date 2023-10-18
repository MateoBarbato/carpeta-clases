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
ancho=cfg.ANCHO
alto=cfg.ALTO
contadorVidas = 3
contadorScore = cfg.SCORE
pos_y=cfg.POS_Y
pos_x = cfg.POS_X
vidasDificultad = 1
# intervalo de spawn de bloques
time_interval = cfg.TIME_INTERVAL
deathInterval = cfg.DEATH_INTERVAL
shootInterval = cfg.SHOOT_INTERVAL
# LLAMO A LOS ASSETS
backgroundImage = pygame.image.load('./assets/background.jpg')
backgroundStart = pygame.image.load('./assets/backgroundStart.png')
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
# volumen default
pygame.mixer.music.set_volume(0.5)
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
mute = False
is_running = True
# evento personalizado 
deathEvent = pygame.USEREVENT+2
timer_event = pygame.USEREVENT+1
shootEvent = pygame.USEREVENT+3
# seteamos el timer
pygame.time.set_timer(timer_event, time_interval)
# declaro los array de objetos
bloques= []
disparos = []
enemiesImages = [EnemiesImage0,EnemiesImage1]


def exit():
    pygame.quit()
    sys.exit()

while True:
    backgroundStartImage = pygame.transform.scale(backgroundStart,(width,height))
    screen.blit(backgroundStartImage,backgroundRect)
    mostrarTexto(deathFont,f'Presiona una tecla para jugar...',True,cfg.LAVENDER,((width - 225) /2,(height - 50)/2),screen)
    contadorVidas = 3
    contadorScore = 0
    waitUser()
    
    while is_running:
        clock.tick(cfg.FPS)
        # DETECTO EVENTOS
        screen.fill(cfg.BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Saliendo')
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                disparos.append(crearDisparo(mainBlock['rect'].x,mainBlock['rect'].y,bulletImg))
            if event.type == deathEvent:
                dying.play()
            if event.type == shootEvent:
                disparos.append(crearDisparo(mainBlock['rect'].x,mainBlock['rect'].y,bulletImg))
            if event.type == timer_event:
                i = randint(0,1)
                if i==0:
                    bloques.append(crearRecImagen(left=randint(50,350),ancho=ancho,alto=alto,top=0,image=enemiesImages[i],vidas=1))
                else:
                    bloques.append(crearRecImagen(left=randint(50,350),ancho=ancho,alto=alto,top=0,image=enemiesImages[i],vidas=3))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print('Saliendo')
                    is_running=False
                if event.key == pygame.K_SPACE:
                    disparos.append(crearDisparo(mainBlock['rect'].x,mainBlock['rect'].y,bulletImg))
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    move_left = False
                    move_rigth = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    move_rigth = False
                    move_left = True
                # ARREGLAR LA PAUSA
                # if event.key == pygame.K_p:
                #     waitUser(pygame.event.get(),sys)
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
        keyspressed = pygame.key.get_pressed()
        mousepressed = pygame.mouse.get_pressed()
        # ACTUALIZO ELEMENTOS
        # Blit De Textos
        backgroundImage = pygame.transform.scale(backgroundImage,(width,height))
        screen.blit(backgroundImage,backgroundRect)
        mainBlock = crearRecImagen(pos_x,pos_y,45,45,color=cfg.WHITE,image=mainBlockImg)
        screen.blit(mainBlock['image'],mainBlock['rect'])
        mostrarTexto(my_font,f'Vidas:{contadorVidas}',True,cfg.WHITE,(50,90),screen)
        mostrarTexto(my_font,f'Score:{contadorScore}',True,cfg.WHITE,(width - 150, 90),screen)
        if is_running:
            for disparo in disparos:
                screen.blit(disparo['image'],disparo['rect'])
            for bloque in bloques:
                screen.blit(bloque['image'],bloque['rect'])
        
        # ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><><><><><><><><><><<<>><><><><<><><><><><><><><><><>><><<><><><><>
        # ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><><><><><><><><><><<<>><><><><<><><><><><><><><><><>><><<><><><><>
        # ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><><><><><><><><><><<<>><><><><<><><><><><><><><><><>><><<><><><><>
        # ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><><><><><><><><><><<<>><><><><<><><><><><><><><><><>><><<><><><><>
        # ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><><><><><><><><><><<<>><><><><<><><><><><><><><><><>><><<><><><><>
        # ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><><><><><><><><><><<<>><><><><<><><><><><><><><><><>><><<><><><><>
        # ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><><><><><><><><><><<<>><><><><<><><><><><><><><><><>><><<><><><><>
        # ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><><><><><><><><><><<<>><><><><<><><><><><><><><><><>><><<><><><><>
        # ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><><><><><><><><><><<<>><><><><<><><><><><><><><><><>><><<><><><><>
        # ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><><><><><><><><><><<<>><><><><<><><><><><><><><><><>><><<><><><><>
        # ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><><><><><><><><><><<<>><><><><<><><><><><><><><><><>><><<><><><><>



        # PREGUNTAR PORQUE EL BUG DE CUANDO ESTA EN FALSE LO TOMA COMO TRUE Y VICEVERSA, ACA DEBERIA IR UN TRUE PERO LO CONSIDERA UN FALSE Y NO DISPARA. SE QUEDA DISPARANDO CUANDO SOLTAS ES CLICK SI ESTA EN TRUE.
        # Y PORQUE EL BUG DE CUANDO PONGO LA BARRA ESPACIADORA TAMBIEN SOLO FUNCIONA CUANDO AMBAS CONDICIONES ESTAN



        if  mousepressed[0] == False : 
            pygame.time.set_timer(shootEvent, shootInterval)
        # ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><><><><><><><><><><<<>><><><><<><><><><><><><><><><>><><<><><><><>
        # ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><><><><><><><><><><<<>><><><><<><><><><><><><><><><>><><<><><><><>
        # ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><><><><><><><><><><<<>><><><><<><><><><><><><><><><>><><<><><><><>
        # ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><><><><><><><><><><<<>><><><><<><><><><><><><><><><>><><<><><><><>
        # ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><><><><><><><><><><<<>><><><><<><><><><><><><><><><>><><<><><><><>
        # ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><><><><><><><><><><<<>><><><><<><><><><><><><><><><>><><<><><><><>
        # ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><><><><><><><><><><<<>><><><><<><><><><><><><><><><>><><<><><><><>
        # ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><><><><><><><><><><<<>><><><><<><><><><><><><><><><>><><<><><><><>
        # ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><><><><><><><><><><<<>><><><><<><><><><><><><><><><>><><<><><><><>
        # ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><><><><><><><><><><<<>><><><><<><><><><><><><><><><>><><<><><><><>
            # ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>><><><><><><><><><><><><><><><><><><><><<<>><><><><<><><><><><><><><><><>><><<><><><><>
        # MOVER ELEMENTOS
        # MUEVO LOS ALIENS CAYENDO Y LOS DISPAROS
        for disparo in disparos[:]:
            rectDisparo=disparo['rect']
            rectDisparo.move_ip(0,-Speed*2)
            if rectDisparo.top > screen.get_height():
                disparos.remove(disparo)
        for bloque in bloques[:]:
            rect=bloque['rect']
            rect.move_ip(0,+bloque['speed-y'])
        # AUMENTO LA DIFICULTAD CON HARDCORE MODE O CON PUNTOS A 30 PARA QUE EMPIEZEN A MOVERSE LOS OBJETOS
            if contadorScore > 30 or hardcoreMode == True:
                if posiciones == True : 
                    if rect.x < width - rect.width:
                        rect.move_ip(+bloque['speed-x'],+bloque['speed-y'])
                    else:
                        posiciones = False
                else:
                    if rect.x > 0 :
                        rect.move_ip(-bloque['speed-x'],+bloque['speed-y'])
                    else:
                        posiciones = True
        # DETECTO COLISIONES
            # final de pantalla borro bloque para liberar memoria
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
                    bloques.clear()
                    disparos.clear()
                    explosionFinal.play()
                    if cfg.MAXSCORE<contadorScore:
                        cfg.MAXSCORE = contadorScore
                    is_running=False
                    pygame.time.set_timer(deathEvent,100)
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
    # AFUERA DEL IS_RUNNING
    backgroundImage = pygame.transform.scale(backgroundImage,(width,height))
    screen.blit(backgroundImage,backgroundRect)
    mostrarTexto(deathFont,f'Game Over :(',True,cfg.LAVENDER,((width - 225) /2,(height - 50)/2),screen)
    pygame.mixer.music.stop()
    pygame.display.flip()