import random
import math

iteration = 1


# 1. Generate a random solution for the problem and call it S
def generate_random_solution(array, length):
    indices = sorted(random.sample(xrange(len(array)), length))
    return [array[i] for i in indices]


# 4. ~~~Compute the neighborhood of S~~~ and choose S' as the best solution in the neighborhood
def get_neighborhood_1(array, subset):
    neighborhood = []
    # neighbours with one element less
    if len(subset) > 1:
        for index, item in enumerate(subset):
            neighborhood.append(subset[:index] + subset[index+1:])
    
    # neighbours with one element more
    if len(subset) < len(array):
        for item in array:
            if item not in subset:
                neighborhood.append(subset + [item])

    return neighborhood


def get_neighborhood_2(array, subset):
    neighborhood = []
    # replace every element in subset with one element from set

    for index, subset_item in enumerate(subset):
        for set_item in array:
            if set_item not in subset:
                neighborhood.append(subset[:index] + [set_item] + subset[index+1:])

    return neighborhood


# 4. Compute the neighborhood of S and ~~~choose S' as the best solution in the neighborhood~~~
def choose_random_sol_in_neighborhood(neighborhood):
    return random.choice(neighborhood)


# 5. If S' is better than S then go to step 6, else go to step 9
# returns True if S' is better, False otherwise
def compare_solutions(s, s_prime):
    if s_prime:
        return abs(sum(s_prime)) < abs(sum(s))
    else:
        return False

# Calls steps 4, 5 and does the rest:
# 6. S = S'
# 7. Sbest = S
# 8. Go to step 12
# 9. Generate a random number R between 0 and 1
# 10. If R is lower than e -abs(S' - S) / T then go to step 11, else go to step 12
# 11. S = S'
# 12. T = alfa * T (where alfa = 0.99, for example, or you can use another function that decreases T)
# 13. If T has reached a certain value then go to step 14, else go to step 4
# 14. Return Sbest as the best solution encountered
def simulated_annealing(array, s, s_best, initial_temp, final_temp, temp_length, cooling_ratio):
    if sum(s) == 0:
        return s_best
    if initial_temp <= final_temp:
        return s_best
    if iteration == temp_length:
        return s_best

    global iteration
    print "\n~~~Iteration: {}~~~".format(iteration)

    # Step 4
    s_neighborhood_1 = get_neighborhood_1(array, s)
    s_neighborhood_2 = get_neighborhood_2(array, s)
    s_neighborhood = s_neighborhood_1 + s_neighborhood_2

    print "Neighborhood: ", s_neighborhood
    s_prime = choose_random_sol_in_neighborhood(s_neighborhood)
    print "Random solution in the neighborhood: \n", s_prime, sum(s_prime)

    # Step 5
    if compare_solutions(s, s_prime):
        # Step 6 and 7
        print "S' is better than S"

        s = s_prime
        s_best = s
        
    else:
        # Step 9
        r = random.uniform(0, 1)
        print "exp", math.exp(-abs(sum(s_prime)- sum(s))/float(initial_temp))
        if r < math.exp(-abs(sum(s_prime)- sum(s))/float(initial_temp)):
            s = s_prime
    # Step 12
    iteration += 1
    initial_temp = cooling_ratio * initial_temp
    print "Temp: ", initial_temp
    print "S", s, sum(s)
    print "S_best", s_best, sum(s_best)
    return simulated_annealing(array, s, s_best, initial_temp, final_temp, temp_length, cooling_ratio)

if __name__ == "__main__":
    array = [-7, -3, -2, 5, 8, 3, 2, -1, 10]

    # Step 1
    s = generate_random_solution(array, random.randint(1, len(array)))

    # Step 2
    s_best = s

    # Step 3
    initial_temp = 1500
    temp_length = 500
    cooling_ratio = 0.9
    final_temp = 0.01
    
    print "Random solution: ", s, sum(s)
    s_final = simulated_annealing(array, s, s_best, initial_temp, final_temp, temp_length, cooling_ratio)

    print "Final solution: ", s_final, sum(s_final)