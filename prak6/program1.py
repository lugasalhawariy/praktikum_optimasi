import time
import random
import math
import sys

# ===
people = [
    ("Lisbon", "LIS"),
    ("Madrid", "MAD"),
    ("Paris", "CDG"),
    ("Dublin", "DUB"),
    ("Brussels", "BRU"),
    ("London", "LHR")]
# ===
flights = {}
for line in open("flights.txt"):
    # print(line)
    # print(line.split(','))
    origin, destiny, departure, arrival, price = line.split(",")
    flights.setdefault((origin, destiny), [])
    flights[(origin, destiny)].append((departure, arrival, int(price)))
# ===
def print_schedule(schedule):
    flight_id = -1
    total_price = 0
    for i in range(len(schedule) // 2):
        name = people[i][0]
        origin = people[i][1]
        flight_id += 1
        going = flights[(origin, destiny)][schedule[flight_id]]
        total_price += going[2]
        flight_id += 1
        returning = flights[(destiny, origin)][schedule[flight_id]]
        total_price += returning[2]
        print(
            "%10s%10s %5s-%5s U$%3s %5s-%5s U$%3s"
            % (
                name,
                origin,
                going[0],
                going[1],
                going[2],
                returning[0],
                returning[1],
                returning[2],
            )
        )

    print("Total price: ", total_price)
# ===
schedule = [1, 2, 3, 2, 7, 3, 6, 3, 2, 4, 5, 3]
print_schedule(schedule)
# ===
t = time.strptime("7:39", "%H:%M")
t
# ===
def get_minutes(hour):
    t = time.strptime(hour, "%H:%M")
    minutes = t[3] * 60 + t[4]
    return minutes
# ===
get_minutes("6:13"), get_minutes("23:59"), get_minutes("00:00")
# ===
flights[("LIS", "FCO")]
# ===
flights[("FCO", "LIS")]
# ===
# Fitness function
def fitness_function(solution):
    total_price = 0
    last_arrival = 0
    first_departure = 1439
    flight_id = -1
    for i in range(len(solution) // 2):
        origin = people[i][1]
        flight_id += 1
        going = flights[(origin, destiny)][solution[flight_id]]
        flight_id += 1
        returning = flights[(destiny, origin)][solution[flight_id]]
        total_price += going[2]
        total_price += returning[2]
        if last_arrival < get_minutes(going[1]):
            last_arrival = get_minutes(going[1])
        if first_departure > get_minutes(returning[0]):
            first_departure = get_minutes(returning[0])
            total_wait = 0
            flight_id = -1
        for i in range(len(solution) // 2):
            origin = people[i][1]
            flight_id += 1
            going = flights[(origin, destiny)][solution[flight_id]]
            flight_id += 1
            returning = flights[(destiny, origin)][solution[flight_id]]
            total_wait += last_arrival - get_minutes(going[1])
            total_wait += get_minutes(returning[0]) - first_departure
            # 3PM - 10AM
            # 11AM - 3PM
            if last_arrival > first_departure:
                total_price += 50
    return total_price + total_wait
# ===
schedule = [1, 4, 3, 2, 7, 3, 6, 3, 2, 4, 5, 3]
fitness_function(schedule)
# ===
schedule = [1, 3, 3, 2, 7, 3, 6, 3, 2, 4, 5, 3]
fitness_function(schedule)
# ===
# Genetic algorithm
# Mutation
len(people)
domain = [(0, 9)] * (len(people) * 2)
domain
# ===
[random.randint(0, 9) for i in range(len(domain))]
# ===
random.random()
# ===
def random_search(domain, fitness_function):
    best_cost = sys.maxsize
    for i in range(1000):
        solution = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
    cost = fitness_function(solution)
    if cost < best_cost:
        best_cost = cost
        best_solution = solution
        return best_solution
# ===
def mutation(domain, step, solution):
    gene = random.randint(0, len(domain) - 1)
    mutant = solution
    if random.random() < 0.5:
        if solution[gene] != domain[gene][0]:
            mutant = solution[0:gene] + [solution[gene] - step] + solution[gene + 1 :]
    else:
        if solution[gene] != domain[gene][1]:
            mutant = solution[0:gene] + [solution[gene] + step] + solution[gene + 1 :]
            return mutant
# ===
s = [6, 7, 6, 7, 3, 9, 7, 7, 0, 7, 6, 7]
mutation(domain, 2, s)
# ===
# Crossover
# [6, 7, 6, 7, 3, 9, 7, 7, 0, 9, 6, 7]
def crossover(domain, solution1, solution2):
    gene = random.randint(1, len(domain) - 2)
    return solution1[0:gene] + solution2[gene:]
# ===
s1 = [1, 4, 3, 2, 7, 3, 6, 3, 2, 4, 5, 3]
s2 = [0, 1, 2, 5, 8, 9, 2, 3, 5, 1, 0, 6]
crossover(domain, s1, s2)
# ===
random.random()
# ===
def genetic(
    domain,
    fitness_function,
    population_size=100,
    step=1,
    probability_mutation=0.2,
    elitism=0.2,
    number_generations=500,
    search=False,
):
    population = []


    for i in range(population_size):
        if search == True:
            solution = random_search(domain, fitness_function)
        else:
            solution = [
                random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))
            ]
    population.append(solution)
    number_elitism = int(elitism * population_size)
    for i in range(number_generations):
        costs = [(fitness_function(individual), individual) for individual in population]
    costs.sort()
    ordered_individuals = [individual for (cost, individual) in costs]
    population = ordered_individuals[0:number_elitism]
    while len(population) < population_size:
        if random.random() < probability_mutation:
            m = random.randint(0, number_elitism)
            population.append(mutation(domain, step, ordered_individuals[m]))
        else:
            i1 = random.randint(0, number_elitism)
            i2 = random.randint(0, number_elitism)
            population.append(crossover(domain, ordered_individuals[i1], ordered_individuals[i2]))
        return costs[0][1]
    # ===
    genetic_solution = genetic(domain, fitness_function)
    genetic_solution
    # ===
    fitness_function(genetic_solution)
    # ===
    print_schedule(genetic_solution)
    # ===
    genetic_random_solution = genetic(domain, fitness_function, search=True)
    genetic_random_solution
    # ===
    fitness_function(genetic_random_solution)
