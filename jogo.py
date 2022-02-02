#pip install pygame
#https://www.pygame.org/docs/
import pygame, random  
from pygame.locals import * #biblioteca pygame importando tudo
import xml.etree.cElementTree as ET #XML


def on_grid_random():
    x = random.randint(0,390)
    y = random.randint(0,490)
    return (x//10 * 10, y//10 * 10) #retorna valores inteiro

def collision (c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])


UP=0 #sentido
RIGHT=1
DOWN=2
LEFT=3


pygame.init() #inicializando
screen = pygame.display.set_mode((400,500)) #Criando display -> matriz
pygame.display.set_caption ('Snake') 

snake = [(200,200), (210,200), (220,200)] #cobra é uma lista, representado por um tupla (x,y)
my_direction = LEFT #direção da cobra

snake_skin = pygame.Surface((10,10)) #(quadrado 10x10 e posição) ( pygame.image.load// pygame.transform.scale)
snake_skin.fill((255,255,255))  #cor do objeto

apple_pos = on_grid_random()
apple = pygame.Surface((10,10))
apple.fill((255,0,0))
pos_apple1 = 0
clock = pygame.time.Clock()
game_over = False

root = ET.Element("root")
doc = ET.SubElement(root, "doc")

while not game_over:             #loop infinito
  clock.tick(20)
  for event in pygame.event.get(): #eventos que irão acontecer no jogo
    if event.type == QUIT:         #evento de sair
      pygame.quit()

    if event.type == KEYDOWN:   #teclado
        if event.key == K_UP:
            my_direction = UP
        if event.key == K_DOWN:
            my_direction = DOWN
        if event.key == K_LEFT:
            my_direction = LEFT
        if event.key == K_RIGHT:
            my_direction = RIGHT

  if collision(snake[0], apple_pos):
      apple_pos = on_grid_random()
      snake.append((0,0))  

  if snake[0][0] == 400 or snake[0][1] == 500 or snake[0][0] < 0 or snake[0][1] < 0:
        game_over = True
        break
    
  for i in range(1, len(snake) - 1):
        if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
            game_over = True
            break



  for i in range(len(snake) -1, 0, -1):
    snake[i] =(snake[i-1][0], snake[i-1][1])    

  if my_direction == UP: #direção da cobra == sentido
      snake[0] = (snake[0][0], snake[0][1] - 10) #cabeça da cobra recebe tupla e muda a direção (x,y)
  elif my_direction == DOWN:
      snake[0] = (snake[0][0], snake[0][1] + 10)
  elif my_direction == RIGHT:
      snake[0] = (snake[0][0] + 10, snake[0][1])
  else:
      snake[0] = (snake[0][0] - 10, snake[0][1])

 
  
  screen.fill((0,0,0)) #limpar tela
  screen.blit(apple,apple_pos) #plotagem da maçã
  for pos in snake:    #posição na tela   
    screen.blit(snake_skin,pos)  #plotar na tela - poderia ser um sprite

  if pos_apple1 != apple_pos:
    pos_apple1 = apple_pos  
    ET.SubElement(doc, "Apple", name="posicao").text = str(apple_pos)
    ET.SubElement(doc, "Snake", name="direcao").text = str(my_direction) 
    ET.SubElement(doc, "Snake", name="Tempo").text = str(clock)
  pygame.display.update()       #evento de atualização do jogo

#Gerar XML
tree = ET.ElementTree(root)
ET.indent(tree, space = '  ' , level= 0)
tree.write("filename.xml")