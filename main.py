import pygame
import os
from renderers import *
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
startscreen = StartScreen(gui,images)
winscreen = WinScreen(gui,images)

render_sequence = [startscreen]
process_stage = 0

progress = False
cont = False

keys = []

while not done:
  for e in gui.event():
    if e.type == pygame.QUIT:
      done = True
      break
    if e.type == pygame.KEYUP:
      for i in render_sequence:
        i.key_hit(keys)
    if e.type == pygame.MOUSEBUTTONUP:
      if e.button == 1:
        if process_stage == 0:
          progress = startscreen.click()
        if process_stage == 1:
          if not started:
            grid.cursor.covered = False
            grid.drawMines(int(startscreen.vars['mines']))
            grid.cursor.covered = True
            grid.open(grid.cursor,True)
            started = True
          win = grid.open(grid.cursor,True)
        if process_stage == 2:
          cont = winscreen.click()
      elif e.button == 3:
        grid.mark(grid.cursor)

  for i in render_sequence:
    i.setCursorPos(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])

  if gui.keysDown(pygame.K_ESCAPE):
    done = True

  if process_stage == 0:
    keys = gui.keysDown()

    if progress:
      grid.drawGrid(int(startscreen.vars['width']),int(startscreen.vars['height']))
      render_sequence = [grid]
      process_stage += 1

  if process_stage == 1:
    complete = grid.Clock()

    if complete:
      grid.render(False)
      render_sequence = [winscreen]
      process_stage = 2

  if process_stage == 2:
    if cont:
      gui.page.fill((0,0,0))
      process_stage = 0
      startscreen = StartScreen(gui,images)
      render_sequence = [startscreen]
      grid = Grid(gui,images)
      progress = False
      cont = False
      started = False
      win = False


  for i in render_sequence:
    i.render()

  gui.flip(32)
