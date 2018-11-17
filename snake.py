import pygame
import os, random

SCREEN_SIZE = 30

DIRECTIONS = [
  (0, 1), # UP
  (1, 0), # RIGHT
  (0, -1), # DOWN
  (-1, 0) # LEFT
]

class Snake():
  snake, fruit = None, None

  def __init__(self):
    self.score = 0
    self.snake = [(15, 2), (15, 1), (15, 0)]
    self.place_fruit()

  def place_fruit(self, coord=None):
    if coord:
      self.fruit = coord
      return

    while True:
      x = random.randint(0, SCREEN_SIZE-1)
      y = random.randint(0, SCREEN_SIZE-1)
      if (x, y) not in self.snake:
        self.fruit = x, y
        return

  def step(self, direction):
    old_head = self.snake[0]
    movement = DIRECTIONS[direction]
    new_head = (old_head[0] + movement[0], old_head[1] + movement[1])

    if (
        new_head[0] < 0 or
        new_head[0] >= SCREEN_SIZE or
        new_head[1] < 0 or
        new_head[1] >= SCREEN_SIZE or
        new_head in self.snake
      ):
      return False
      
    if new_head == self.fruit:
      self.score += 1
      self.place_fruit()
    else:
      tail = self.snake[-1]
      del self.snake[-1]

    self.snake.insert(0, new_head)
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

    pygame.init()
    s = pygame.display.set_mode((SCREEN_SIZE * 10, SCREEN_SIZE * 10))
    pygame.display.set_caption('Snake')
    appleimage = pygame.Surface((10, 10))
    appleimage.fill((0, 255, 0))
    img = pygame.Surface((10, 10))
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
        pygame.quit()
        return self.score

      s.fill((255, 255, 255))	
      for bit in self.snake:
        s.blit(img, (bit[0] * 10, (SCREEN_SIZE - bit[1] - 1) * 10))
      s.blit(appleimage, (self.fruit[0] * 10, (SCREEN_SIZE - self.fruit[1]-1) * 10))
      pygame.display.update()

while True:
  snake = Snake()
  score = snake.run()

  print('Best Score: %s' % score)
