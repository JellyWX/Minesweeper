import pygame
import os
from gui import GUI
from grid import Grid

gui = GUI(800,800,'Minesweeper')
images = {}

for f in os.listdir('assets/images'):
  if f[-4:] == '.png':
    print('Loading asset ' + f)
    images[f[0:-4]] = pygame.image.load('assets/images/' + f)

done = False
started = False

grid = Grid(gui,images)

while not done:
  for e in gui.event():
    if e.type == pygame.QUIT:
      done = True
      break
    if e.type == pygame.MOUSEBUTTONUP:
      if e.button == 1:
        if not started:
          started = True
          grid.release()
          grid.post_initial()
        done = grid.release()
      elif e.button == 3:
        grid.mark()


  grid.cursor(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])

  if gui.keysDown(pygame.K_ESCAPE):
    done = True

  grid.render()

  gui.flip(32)
