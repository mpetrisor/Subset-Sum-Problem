import random
import math

iteration = 1


def generate_initial_population(array_length, population_size):
    population = []
    for _ in range(0, population_size):
        population.append(''.join(random.choice(["0", "1"]) for _ in range(array_length)))
    return population


def fitness_function(solution, array):
    sum = 0
    for index, entry in enumerate(solution):
        if entry == "1":
            sum += array[index]
    return abs(sum)


def get_choice_probability(P_s_best, s_best, s_worst, s_current, array):
    step = P_s_best/float(fitness_function(s_worst, array) - fitness_function(s_best, array) + 1)
    return P_s_best - (fitness_function(s_current, array) - fitness_function(s_best, array))*step


def select_solution(P_s_current):
    rand = random.uniform(0, 1)
    return rand <= P_s_current


def crossover(s_1, s_2, length):
    crossover_point = int(random.uniform(0, length-1))
    new_individual_1 = s_1[:crossover_point] + s_2[crossover_point:]
    new_individual_2 = s_2[:crossover_point] + s_1[crossover_point:]
    return new_individual_1, new_individual_2


def mutation(s_current, length):
    gene_index = int(random.uniform(0, length-1))
    s_list = list(s_current)
    if s_list[gene_index] == "0":
        s_list[gene_index] = "1"
    else:
        s_list[gene_index] = "0"
    return "".join(s_list)


def clone_N_individuals(sorted_s, N):
    return sorted_s[:N]


def genetic_algorithm(array, s, s_best, population_size, iterations_number, crossover_rate, mutation_rate,
                      cloning_rate):
    global iteration

    if fitness_function(s_best, array) == 0:
        return s_best
    if iteration == iterations_number:
        return s_best

    print "\n~~~Iteration: {}~~~".format(iteration)

    s.sort(key=lambda k: fitness_function(k, array))
    print s

    s_best = s[0]
    s_worst = s[population_size-1]
    # s_best gets a 90% chance, s_worst a 10% chance, everything in between is computed based on this
        
    new_s = []
    while len(new_s) < population_size*crossover_rate:
        s_current = []
        s_current.append(None)
        s_current.append(None)

        i = 0

        while i < 2:
            s_current[i] = s[int(random.uniform(0, population_size-1))]
            P_s_current = get_choice_probability(0.9, s_best, s_worst, s_current[i], array)
            if select_solution(P_s_current):
                i += 1

        s_1, s_2 = crossover(s_current[0], s_current[1], len(array))
        
        new_s.append(s_1)
        new_s.append(s_2)

    while len(new_s) < population_size*(crossover_rate + mutation_rate):
        s_current = s[int(random.uniform(0, population_size-1))]
        s_mutated = mutation(s_current, len(array))
        new_s.append(s_mutated)

    while len(new_s) < population_size*(crossover_rate + mutation_rate + cloning_rate):
        clones = clone_N_individuals(s, int(population_size*cloning_rate))  
        new_s.extend(clones)
    print new_s

    new_s.sort(key=lambda k: fitness_function(k, array))

    if fitness_function(new_s[0], array) < fitness_function(s_best, array):
        s_best = new_s[0]
    
    iteration += 1
    return genetic_algorithm(array, new_s, s_best, population_size, iterations_number, crossover_rate, mutation_rate,
                             cloning_rate)

if __name__ == "__main__":
    array = [-7, -3, -2, 5, 8, 3, 2, -1, 10]
    s = generate_initial_population(len(array), 10)

    population_size = 10
    iterations_number = 50
    crossover_rate = 0.8
    mutation_rate = 0.15
    cloning_rate = 0.05

    s.sort(key=lambda k: fitness_function(k, array))

    s_final = genetic_algorithm(array, s, s[0], population_size, iterations_number, crossover_rate, mutation_rate,
                                cloning_rate)

    print "Final solution: ", s_final, fitness_function(s_final, array)
