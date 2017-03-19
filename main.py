import pygame
import os
from gui import GUI
from grid2 import Grid

gui = GUI(800,800,'Minesweeper')
images = {}

for f in os.listdir('assets/images'):
  if f[-4:] == '.png':
    print('Loading asset ' + f)
    images[f[0:-4]] = pygame.image.load('assets/images/' + f)

done = False
started = False
grid = Grid(gui,images)
grid.drawGrid(9,9)

render_sequence = [grid.render]

while not done:
  for e in gui.event():
    if e.type == pygame.QUIT:
      done = True
      break
    if e.type == pygame.MOUSEBUTTONUP:
      if e.button == 1:
        if not started:
          grid.cursor.covered = False
          grid.drawMines(10)
          grid.cursor.covered = True
          grid.open(grid.cursor,True)
          started = True
        done = grid.open(grid.cursor,True)
      elif e.button == 3:
        grid.mark(grid.cursor)


  grid.setCursorPos(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])

  if gui.keysDown(pygame.K_ESCAPE):
    done = True

  complete = grid.Clock()

  if complete:
    print('well done!')

  for i in render_sequence:
    i()

  gui.flip(32)
