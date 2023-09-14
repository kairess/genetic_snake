import pygame
import random
import numpy as np
import pickle  # Import the pickle module for serialization
from copy import deepcopy
from snake import Snake, SCREEN_SIZE, PIXEL_SIZE
from genome import Genome

N_POPULATION = 50
N_BEST = 5
N_CHILDREN = 5
PROB_MUTATION = 0.4

# Define a function to save the data
def save_data(data, filename):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

# Define a function to load the data
def load_data(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

pygame.init()
pygame.font.init()
s = pygame.display.set_mode((SCREEN_SIZE * PIXEL_SIZE, SCREEN_SIZE * PIXEL_SIZE))
pygame.display.set_caption('Snake')

# Load saved data if it exists
try:
    saved_data = load_data('snake_data.pkl')
    n_gen, genomes, best_genomes = saved_data
except FileNotFoundError:
    n_gen = 0
    genomes = [Genome() for _ in range(N_POPULATION)]
    best_genomes = None

while True:
    n_gen += 1

    for i, genome in enumerate(genomes):
        snake = Snake(s, genome=genome)
        fitness, score = snake.run()

        genome.fitness = fitness

    if best_genomes is not None:
        genomes.extend(best_genomes)
    genomes.sort(key=lambda x: x.fitness, reverse=True)

    print('===== Generation #%s\tBest Fitness %s =====' % (n_gen, genomes[0].fitness))

    best_genomes = deepcopy(genomes[:N_BEST])

    # crossover
    for i in range(N_CHILDREN):
        new_genome = deepcopy(best_genomes[0])
        a_genome = random.choice(best_genomes)
        b_genome = random.choice(best_genomes)

        cut = random.randint(0, new_genome.w1.shape[1])
        new_genome.w1[i, :cut] = a_genome.w1[i, :cut]
        new_genome.w1[i, cut:] = b_genome.w1[i, cut:]

        cut = random.randint(0, new_genome.w2.shape[1])
        new_genome.w2[i, :cut] = a_genome.w2[i, :cut]
        new_genome.w2[i, cut:] = b_genome.w2[i, cut:]

        cut = random.randint(0, new_genome.w3.shape[1])
        new_genome.w3[i, :cut] = a_genome.w3[i, :cut]
        new_genome.w3[i, cut:] = b_genome.w3[i, cut:]

        cut = random.randint(0, new_genome.w4.shape[1])
        new_genome.w4[i, :cut] = a_genome.w4[i, :cut]
        new_genome.w4[i, cut:] = b_genome.w4[i, cut:]

        best_genomes.append(new_genome)

    # mutation
    genomes = []
    for i in range(int(N_POPULATION / (N_BEST + N_CHILDREN))):
        for bg in best_genomes:
            new_genome = deepcopy(bg)

            mean = 20
            stddev = 10

            if random.uniform(0, 1) < PROB_MUTATION:
                new_genome.w1 += new_genome.w1 * np.random.normal(mean, stddev, size=(6, 10)) / 100 * np.random.randint(-1, 2,
                                                                                                                    (6, 10))
            if random.uniform(0, 1) < PROB_MUTATION:
                new_genome.w2 += new_genome.w2 * np.random.normal(mean, stddev, size=(10, 20)) / 100 * np.random.randint(
                    -1, 2, (10, 20))
            if random.uniform(0, 1) < PROB_MUTATION:
                new_genome.w3 += new_genome.w3 * np.random.normal(mean, stddev, size=(20, 10)) / 100 * np.random.randint(
                    -1, 2, (20, 10))
            if random.uniform(0, 1) < PROB_MUTATION:
                new_genome.w4 += new_genome.w4 * np.random.normal(mean, stddev, size=(10, 3)) / 100 * np.random.randint(
                    -1, 2, (10, 3))

            genomes.append(new_genome)

    # Save the data after each generation
    save_data((n_gen, genomes, best_genomes), 'snake_data.pkl')
