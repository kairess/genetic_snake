import pygame
import os, random
import numpy as np

SCREEN_SIZE = 30
PIXEL_SIZE = 10

DIRECTIONS = np.array([
  (0, 1), # UP
  (1, 0), # RIGHT
  (0, -1), # DOWN
  (-1, 0) # LEFT
])

class Snake():
  snake, fruit = None, None

  def __init__(self, s):
    self.s = s
    self.score = 0
    self.snake = np.array([(15, 2), (15, 1), (15, 0)])
    self.place_fruit()

    # fitness
    self.fitness = 0.
    self.last_dist = np.inf

  def place_fruit(self, coord=None):
    if coord:
      self.fruit = np.array(coord)
      return

    while True:
      x = random.randint(0, SCREEN_SIZE-1)
      y = random.randint(0, SCREEN_SIZE-1)
      if (x, y) not in self.snake.tolist():
        break
    self.fruit = np.array([x, y])

  def step(self, direction):
    old_head = self.snake[0]
    movement = DIRECTIONS[direction]
    new_head = old_head + movement

    if (
        new_head[0] < 0 or
        new_head[0] >= SCREEN_SIZE or
        new_head[1] < 0 or
        new_head[1] >= SCREEN_SIZE or
        new_head.tolist() in self.snake.tolist()
      ):
      return False
    
    # eat fruit
    if all(new_head == self.fruit):
      self.score += 1
      self.fitness += 10
      self.place_fruit()
    else:
      tail = self.snake[-1]
      self.snake = self.snake[:-1, :]

    self.snake = np.concatenate([[new_head], self.snake], axis=0)
    return True

  def get_inputs(self):
    result = []
    for y in range(SCREEN_SIZE-1, -1, -1):
      for x in range(SCREEN_SIZE):
        out = 0
        if (x, y) in self.snake:
          out = 1
        elif (x, y) == self.fruit:
          out = 2
        result.append(out)

    return result

  def run(self):
    direction = 0 # UP
    prev_key = pygame.K_UP

    font = pygame.font.Font('/Users/brad/Library/Fonts/3270Medium.otf', 20)
    font.set_bold(True)
    appleimage = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
    appleimage.fill((0, 255, 0))
    img = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
    img.fill((255, 0, 0))
    clock = pygame.time.Clock()

    while True:
      # os.system('clear')
      # print(self.get_inputs())

      clock.tick(10)
      for e in pygame.event.get():
        if e.type == pygame.QUIT:
          pygame.quit()
        elif e.type == pygame.KEYDOWN:
          # QUIT
          if e.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()
          # PAUSE
          if e.key == pygame.K_SPACE:
            pause = True
            while pause:
              for ee in pygame.event.get():
                if ee.type == pygame.QUIT:
                  pygame.quit()
                elif ee.type == pygame.KEYDOWN:
                  if ee.key == pygame.K_SPACE:
                    pause = False
          # CONTROLLER
          if prev_key != pygame.K_DOWN and e.key == pygame.K_UP:
            direction = 0
            prev_key = e.key
          elif prev_key != pygame.K_LEFT and e.key == pygame.K_RIGHT:
            direction = 1
            prev_key = e.key
          elif prev_key != pygame.K_UP and e.key == pygame.K_DOWN:
            direction = 2
            prev_key = e.key
          elif prev_key != pygame.K_RIGHT and e.key == pygame.K_LEFT:
            direction = 3
            prev_key = e.key

      if not self.step(direction):
        break

      # compute fitness
      current_dist = np.linalg.norm(self.snake[0] - self.fruit)
      if self.last_dist > current_dist:
        self.fitness += 1.
      else:
        self.fitness -= 1.5
      self.last_dist = current_dist

      self.s.fill((0, 0, 0))
      for bit in self.snake:
        self.s.blit(img, (bit[0] * PIXEL_SIZE, (SCREEN_SIZE - bit[1] - 1) * PIXEL_SIZE))
      self.s.blit(appleimage, (self.fruit[0] * PIXEL_SIZE, (SCREEN_SIZE - self.fruit[1]-1) * PIXEL_SIZE))
      score_ts = font.render(str(self.score), False, (255, 255, 255))
      self.s.blit(score_ts, (5, 5))
      pygame.display.update()

    return self.score

if __name__ == '__main__':
  pygame.init()
  pygame.font.init()
  s = pygame.display.set_mode((SCREEN_SIZE * PIXEL_SIZE, SCREEN_SIZE * PIXEL_SIZE))
  pygame.display.set_caption('Snake')

  while True:
    snake = Snake(s)
    score = snake.run()

    print('Best Score: %s' % score)
