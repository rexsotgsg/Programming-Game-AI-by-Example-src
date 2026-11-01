import math
import random

POPULATION_SIZE = 8
CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.1
SIZE = 5

class Chromosome:
    def __init__(self, g=None):
        # 기본 인수로 []를 사용하지 않는다.
        self.genes = (
            [random.randint(0, 1) for _ in range(SIZE)]
            if g is None else g.copy()
        )
        self.fitness = 0
    def cal_fitness(self):
        value = 0
        for bit in self.genes:
            value = 2 * value + bit

        self.fitness = 6 * value - value * value
        return self.fitness
    def __str__(self):
        return str(self.genes)

def print_p(pop):
    for i, c in enumerate(pop):
        print(f"염색체 #{i} = {c}, 적합도 = {c.cal_fitness()}")
    print()

def select(pop):
    # 6개체의 10%는 0.6개이므로 최소 3개를 비교한다.
    k = min(len(pop), max(3, math.ceil(len(pop) * 0.1)))
    selected = random.sample(pop, k=k)
    # 적합도 값이 아니라 염색체 객체를 반환한다.
    return max(selected, key=lambda c: c.cal_fitness())

def crossover(pop):
    father = select(pop)
    mother = select(pop)
    if random.random() < CROSSOVER_RATE:
        index = random.randint(1, SIZE - 1)
        child1 = father.genes[:index] + mother.genes[index:]
        child2 = mother.genes[:index] + father.genes[index:]
    else:
        # 교차하지 않아도 같은 자료형인 유전자 리스트를 반환한다.
        child1 = father.genes.copy()
        child2 = mother.genes.copy()
    return child1, child2

def mutate(c):
    for i in range(SIZE):
        if random.random() < MUTATION_RATE:
            c.genes[i] = 1 - c.genes[i]  # 비트 뒤집기

population = [Chromosome() for _ in range(POPULATION_SIZE)]

for generation in range(100):
    population.sort(key=lambda c: c.cal_fitness(), reverse=True)
    top = population[:3]
    print("세대 번호 =", generation)
    print_p(population)

    if generation == 99:
        break

    new_pop = []
    for _ in range(POPULATION_SIZE // 2):
        c1, c2 = crossover(population)
        new_pop.extend([Chromosome(c1), Chromosome(c2)])

    population = new_pop
    for c in population:
        mutate(c)

    population = sorted(population, key=lambda c: c.cal_fitness(), reverse=True)
    population[-3:] = top[:3] # keep the best child
