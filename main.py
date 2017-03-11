import pygame
from gui import GUI
from grid import Grid

gui = GUI(800,800,'Minesweeper')
images = {
  'tile' : pygame.image.load('tile.png'),
  'background' : pygame.image.load('background.png'),
  'overlay' : pygame.image.load('overlay.png')
}

done = False

started = False

grid = Grid(gui,images,30,30,15)

while not done:
  for e in gui.event():
    if e.type == pygame.QUIT:
      done = True
      break
    if e.type == pygame.MOUSEBUTTONDOWN:
      if e.button == 1:
        grid.release()



  #print(str(pygame.mouse.get_pos()))

  grid.cursor_x = pygame.mouse.get_pos()[0]
  grid.cursor_y = pygame.mouse.get_pos()[1]


  if gui.keysDown(pygame.K_ESCAPE):
    done = True

  grid.render()

  gui.flip(64)
