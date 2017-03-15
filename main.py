import pygame
from gui import GUI
from grid import Grid

gui = GUI(800,800,'Minesweeper')
images = {
  'tile' : pygame.image.load('tile.png'),
  'mark' : pygame.image.load('mark.png'),
  'background' : pygame.image.load('background.png'),
  'overlay' : pygame.image.load('overlay.png')
}

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


  grid.cursor_pos(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])

  if gui.keysDown(pygame.K_ESCAPE):
    done = True

  grid.render()

  gui.flip(32)
