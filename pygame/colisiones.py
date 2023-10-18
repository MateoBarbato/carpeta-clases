import math
import pygame
import config
from random import randint
def punto_en_rectangulo(punto,rect):
    x, y = punto
    return x >= rect.left and x <= rect.rigth and y>= rect.top and y<= rect.bottom

def detectar_colision_circ(rect1 ,rect2):
    distancia = distancia_entre_puntos(rect1.center,rect2.center)
    r1 = calcular_radio_rectangulo(rect1)
    r2 = calcular_radio_rectangulo(rect2)

    return distancia <= (r1+r2)

def distancia_entre_puntos(punto1,punto2):
    x1,y1 = punto1
    x2,y2 = punto2
    return math.sqrt((y1-y2) ** 2 + (x1-x2) ** 2)

def distancia_centros_rect ( rect_1, rect_2):
    return distancia_entre_puntos(rect_1.center , rect_2.center)


def calcular_radio_rectangulo (rect):
    return rect.width // 2

def crearBloque (left=0,top=0,ancho=25,alto=25,color=config.GREEN, borde = 0, radio= -1):
    rect = pygame.Rect(left,top,ancho,alto)
    return { 'rect':rect , 'color':color, 'borde':borde,'radio':radio}

def crearRecImagen (left=0,top=0,ancho=25,alto=25,color=config.GREEN, borde = 0, radio= -1,image=None,vidas= 1):
    if image:
        image = pygame.transform.scale(image,(ancho,alto))
    else:
        image = None
    rect = pygame.Rect(left,top,ancho,alto)
    return { 'rect':rect , 'color':color, 'borde':borde,'radio':radio,'image':image,'vidas':vidas,'speed-y':randint(2,3),'speed-x':randint(2,3)}

def randomColor ():
    color = (randint(0,255),randint(0,255),randint(0,255))
    return color

def crearDisparo(left,top,imagen):
    ancho=10
    alto=20
    mainBlockWidth = 45
    left = left + (mainBlockWidth/2.5)

    imagenRotada = pygame.transform.rotate(imagen, 90)
    imagen = pygame.transform.scale(imagenRotada,(ancho,alto))
    
    disparoRec = pygame.Rect(left,top,ancho,alto)
    return { 'rect':disparoRec,"image":imagen}

def waitUser (events,sys):
    while True:
        for event in events:
            if event.type == pygame.QUIT:
                print('Hasta luego lucassss')
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print('See ya laater lucass')
                    sys.exit()
            return

def mostrarTexto (fuente,texto,AA,color,coordinates,screen):
    text_score = fuente.render(texto,AA,color)
    screen.blit(text_score,coordinates)
