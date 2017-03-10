import pygame
from gui import GUI

gui = GUI(640,540,'Minesweeper')
images = {
  'tile' : pygame.image.load('tile.png')
  'background' : pygame.image.load('background.png')
  'overlay' : pygame.image.load('overlay.png')
}

done = False

started = False

grid = 

while not done:
  for e in gui.event():
    if e.type == pygame.QUIT:
      done = True
      break



  print(str(pygame.mouse.get_pos()))
  if gui.keysDown(pygame.K_ESCAPE):
    done = True

  gui.flip(128)
