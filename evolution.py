import pygame
from snake import Snake, SCREEN_SIZE, PIXEL_SIZE
from genome import Genome

n_population = 50

pygame.init()
pygame.font.init()
s = pygame.display.set_mode((SCREEN_SIZE * PIXEL_SIZE, SCREEN_SIZE * PIXEL_SIZE))
pygame.display.set_caption('Snake')

genomes = [Genome() for _ in range(n_population)]

while True:
  for i, genome in enumerate(genomes):
    print('Genome #%s' % (i))

    snake = Snake(s, genome=genome)
    fitness, score = snake.run()

    genome.fitness = fitness

    print('Fitness: %s, Score: %s' % (fitness, score))
