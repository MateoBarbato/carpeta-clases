import pygame , sys 
import config2 as config
from funciones import areaRectangulo,perimetroRectangulo
from pygame import draw, time,event,display,font

clock = time.Clock()
pygame.init()
font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 22)

screen = display.set_mode(config.SIZE)

ancho = config.WIDTH
alto = config.HEIGHT
bloque = {
    'rect':pygame.Rect((ancho-86)/2,(alto-86)/2,86,86),
    'dimensiones':{'x':86,'y':86},
    'posicionInicial':((ancho-86)/2),
    'color':config.GREEN
}
# bloque = pygame.Rect((ancho-86)/2,(alto-86)/2,86,86)
while True:
    clock.tick(config.FPS)
    flag=False
    # DETECTO EVENTOS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Saliendo')
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                print('Saliendo')
                sys.exit()
    # ACTUALIZO ELEMENTOS
    screen.fill(config.BLACK)
    area = areaRectangulo(bloque['dimensiones']['x'],bloque['dimensiones']['y'])
    perimetro = perimetroRectangulo(bloque['dimensiones']['x'],bloque['dimensiones']['y'])

   

    text_area = my_font.render(f'Area: {area} px' , True, config.BLACK)
    text_perimetro = my_font.render(f'Perimetro: {perimetro} px' , True, config.BLACK)
   

    r = draw.rect(screen,bloque['color'],pygame.Rect((ancho-86)/2,(alto-86)/2,bloque['dimensiones']['x'],bloque['dimensiones']['y']))
    r2 = draw.rect(screen,config.WHITE,(80,alto/2,250,80))
    screen.blit(text_area,r2.topleft)
    screen.blit(text_perimetro,r2.midleft)
    # PINTO PANTALLA
    pygame.display.flip()



