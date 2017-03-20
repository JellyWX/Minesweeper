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
lossscreen = LossScreen(gui,images)
endscreen = lossscreen

render_sequence = [startscreen]
process_stage = 0

progress = False
cont = False
loss = False

keys = []

first_click = ()
release = ()
mouse_1_down = False
grid_moved = False

while not done:
  for e in gui.event():
    if e.type == pygame.QUIT:
      done = True
      break
    if e.type == pygame.KEYUP:
      for i in render_sequence:
        i.key_hit(keys)

    if e.type == pygame.MOUSEBUTTONUP:
      release = pygame.mouse.get_pos()
      if e.button == 1:

        if process_stage == 0:
          progress = startscreen.click()

        if process_stage == 1:
          mouse_1_down = False
          if not grid_moved:
            if not started:
              grid.cursor.covered = False
              grid.drawMines(int(startscreen.vars['mines']))
              grid.cursor.covered = True
              grid.open(grid.cursor,True)
              started = True
            loss = grid.open(grid.cursor,True)
          else:
            grid_moved = False

        if process_stage == 2:
          cont = endscreen.click()
      elif e.button == 3:
        if process_stage == 1:
          grid.mark(grid.cursor)

    if e.type == pygame.MOUSEBUTTONDOWN:
      first_click = pygame.mouse.get_pos()
      if process_stage == 1:
        if e.button == 1:
          mouse_1_down = True
          grid.setClickPos(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
        if e.button == 4:
          grid.scale()
        elif e.button == 5:
          grid.scale(False)

  if mouse_1_down:
    if grid.getCursorVariation(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
      release = pygame.mouse.get_pos()
      grid.shift(first_click[0]-release[0],first_click[1]-release[1])
      first_click = pygame.mouse.get_pos()
      grid_moved = True

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
      endscreen = winscreen

    elif loss:
      endscreen = lossscreen

    if complete or loss:
      grid.render(False)
      render_sequence = [endscreen]
      process_stage = 2

  if process_stage == 2:
    if cont:
      gui.page.fill((0,0,0))
      process_stage = 0
      startscreen = StartScreen(gui,images)
      winscreen = WinScreen(gui,images)
      lossscreen = LossScreen(gui,images)
      render_sequence = [startscreen]
      grid = Grid(gui,images)
      progress = False
      cont = False
      started = False
      loss = False
      complete = False
      endscreen = lossscreen


  for i in render_sequence:
    i.render()

  gui.flip(32)
