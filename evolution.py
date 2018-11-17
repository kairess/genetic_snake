import pygame, random
import numpy as np
from copy import deepcopy
from snake import Snake, SCREEN_SIZE, PIXEL_SIZE
from genome import Genome

N_POPULATION = 50
PROB_MUTATION = 0.1

pygame.init()
pygame.font.init()
s = pygame.display.set_mode((SCREEN_SIZE * PIXEL_SIZE, SCREEN_SIZE * PIXEL_SIZE))
pygame.display.set_caption('Snake')

# generate 1st population
genomes = [Genome() for _ in range(N_POPULATION)]
best_genome = None

n_gen = 0
while True:
  n_gen += 1

  for i, genome in enumerate(genomes):
    snake = Snake(s, genome=genome)
    fitness, score = snake.run()

    genome.fitness = fitness

    print('Generation #%s, Genome #%s, Fitness: %s, Score: %s' % (n_gen, i, fitness, score))

  if best_genome is not None:
    genomes.append(best_genome)
  genomes.sort(key=lambda x: x.fitness, reverse=True)

  best_genome = deepcopy(genomes[0])

  # mutation
  genomes = []
  for i in range(N_POPULATION):
    new_genome = deepcopy(best_genome)

    if random.uniform(0, 1) < PROB_MUTATION:
      new_genome.w1 += new_genome.w1 * np.random.normal(15, 4, size=(6, 10)) / 100 * np.random.randint(-1, 2, (6, 10))
    if random.uniform(0, 1) < PROB_MUTATION:
      new_genome.w2 += new_genome.w2 * np.random.normal(15, 4, size=(10, 3)) / 100 * np.random.randint(-1, 2, (10, 3))

    genomes.append(new_genome)
