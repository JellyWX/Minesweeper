import pygame
import os
import time
from renderers import *
from gui import GUI
from grid import Grid
from timer import Timer

gui = GUI(800,800,'Minesweeper')
images = {}

for f in os.listdir('assets/images'):
  if f[-4:] == '.png':
    print('Loading asset ' + f)
    images[f[0:-4]] = pygame.image.load('assets/images/' + f)

timer = Timer(True)
done = False

started = False
grid = Grid(gui,images)
startscreen = StartScreen(gui,images)
endscreen = WinScreen(gui,images,'')
gridscreen = GridScreen(gui,images,timer)
stats = GridStats(gui,images,timer)

render_sequence = [startscreen]
process_stage = 0

progress = -1
cont = -1
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
              timer.Reset(True)
              started = True
            loss = grid.open(grid.cursor,True)
          else:
            grid_moved = False

        elif process_stage == 2:
          cont = endscreen.click()

        elif process_stage == 3:
          mouse_1_down = False

    if e.type == pygame.MOUSEBUTTONDOWN:
      first_click = pygame.mouse.get_pos()

      if process_stage == 1: #if game is ongoing
        if e.button == 1:
          mouse_1_down = True
          grid.setClickPos(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
        elif e.button == 3:
          grid.mark(grid.cursor)
        if e.button == 4:
          grid.scale()
        elif e.button == 5:
          grid.scale(False)

      elif process_stage == 3: #if the player reopens the grid
        if e.button == 1:
          mouse_1_down = True
          grid.setClickPos(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
        if e.button == 4:
          grid.scale()
        elif e.button == 5:
          grid.scale(False)

    if e.type == pygame.VIDEORESIZE:
      gui.resize(e.dict['size'][0],e.dict['size'][1])

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

  if process_stage == 0: #if the main menu is open
    keys = gui.keysDown()
    startscreen.checkBoxes()

    if progress == 0:
      grid.drawGrid(int(startscreen.vars['width']),int(startscreen.vars['height']))
      render_sequence = [grid,stats]
      process_stage += 1
    elif progress == 1:
      done = True

  if process_stage == 1: #if the game is running
    complete = grid.Clock()

    if complete:
      endscreen.display_text = 'Well Done!'
    elif loss:
      endscreen.display_text = '    RIP   '

    if complete or loss:
      gui.page.fill((0,0,0))
      timer.Bookmark('endgame')
      print(timer.get('endgame'))
      render_sequence = [endscreen]
      process_stage = 2

  if process_stage == 2: #if the game has ended, due to win or loss
    if cont == -1:
      gui.page.fill((0,0,0))
      render_sequence = [endscreen]
    elif cont == 1: #show grid again
      render_sequence = [grid,gridscreen]
      process_stage = 3
    elif cont == 0: #replay
      gui.page.fill((0,0,0))
      process_stage = 0
      startscreen = StartScreen(gui,images)
      render_sequence = [startscreen]
      grid = Grid(gui,images)
      progress = False
      cont = -1
      started = False
      loss = False
      complete = False
    elif cont == 2:
      done = True

  if process_stage == 3: #if the player chooses to review the grid
    cont = -1
    if gui.keysDown(pygame.K_BACKSPACE):
      gui.page.fill((0,0,0))
      process_stage = 2

  for i in render_sequence:
    i.render()
    if process_stage == 3 and i == grid:
      grid.render(True,True)

  gui.flip(64)
