import pygame, random
import numpy as np
from copy import deepcopy
from snake import Snake, SCREEN_SIZE, PIXEL_SIZE
from genome import Genome

N_POPULATION = 50
N_BEST = 2
N_CHILDREN = 3
PROB_MUTATION = 0.2

pygame.init()
pygame.font.init()
s = pygame.display.set_mode((SCREEN_SIZE * PIXEL_SIZE, SCREEN_SIZE * PIXEL_SIZE))
pygame.display.set_caption('Snake')

# generate 1st population
genomes = [Genome() for _ in range(N_POPULATION)]
best_genomes = None

n_gen = 0
while True:
  n_gen += 1

  for i, genome in enumerate(genomes):
    snake = Snake(s, genome=genome)
    fitness, score = snake.run()

    genome.fitness = fitness

    print('Generation #%s, Genome #%s, Fitness: %s, Score: %s' % (n_gen, i, fitness, score))

  if best_genomes is not None:
    genomes.extend(best_genomes)
  genomes.sort(key=lambda x: x.fitness, reverse=True)

  best_genomes = deepcopy(genomes[:N_BEST])

  # crossover
  for i in range(N_CHILDREN):
    new_genome = deepcopy(best_genomes[0])
    a_genome = best_genomes[0]
    b_genome = best_genomes[1]

    if random.uniform(0, 1) < 0.5:
      new_genome.w1[i] = a_genome.w1[i]
    else:
      new_genome.w1[i] = b_genome.w1[i]

    if random.uniform(0, 1) < 0.5:
      new_genome.w2[i] = a_genome.w2[i]
    else:
      new_genome.w2[i] = b_genome.w2[i]

    best_genomes.append(new_genome)

  # mutation
  genomes = []
  for i in range(N_POPULATION // (N_BEST + N_BEST // 2 * N_CHILDREN)):
    for bg in best_genomes:
      new_genome = deepcopy(bg)

      if random.uniform(0, 1) < PROB_MUTATION:
        new_genome.w1 += new_genome.w1 * np.random.normal(15, 4, size=(6, 10)) / 100 * np.random.randint(-1, 2, (6, 10))
      if random.uniform(0, 1) < PROB_MUTATION:
        new_genome.w2 += new_genome.w2 * np.random.normal(15, 4, size=(10, 3)) / 100 * np.random.randint(-1, 2, (10, 3))

      genomes.append(new_genome)
