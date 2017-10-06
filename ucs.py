import bisect, itertools

class Node:
    def __init__(self, cost, state, steps):
        self.cost = cost
        self.state = state
        self.steps = steps

    def __lt__(self, other):
        return self.cost < other.cost

    def print_steps(self):
        i = 0
        while i < len(self.steps):
            if (i+1) % 3 == 0:
                print(self.steps[i], '<-')
                i += 1
            else:
                print(self.steps[i], self.steps[i+1], '->')
                i += 2

class Tree:
    def __init__(self, fitness):
        state = [0] * len(fitness)
        steps = []
        cost = 0
        root = Node(cost, state, steps)

        self.fringe = [root]
        self.fitness = fitness

    def has_repeated_states(self, node):
        for item in self.fringe:
            if node.state == item.state and node.cost < item.cost:
                self.fringe.remove(item)
                bisect.insort(self.fringe, node)
                return True
            if node.state == item.state:
                return True
        return False

    def generate_nodes(self, node):
        fitness_len = len(self.fitness)
        if len(node.steps) % 3 == 0:
            for elem in itertools.combinations(list(range(fitness_len)), 2):
                if (node.state[elem[0]] == 0 and node.state[elem[1]] == 0):
                    new_state = list(node.state)
                    new_state[elem[0]] = 1
                    new_state[elem[1]] = 1

                    new_steps = list(node.steps)
                    new_steps.extend([elem[0]+1, elem[1]+1])

                    new_cost = node.cost + max(self.fitness[elem[0]], self.fitness[elem[1]])

                    new_node = Node(new_cost, new_state, new_steps)

                    # Check for Repeated States
                    if not self.has_repeated_states(new_node):
                        bisect.insort(self.fringe, new_node)

        else:
            for elem in list(range(fitness_len)):
                if (node.state[elem] == 1):
                    new_state = list(node.state)
                    new_state[elem] = 0

                    new_steps = list(node.steps)
                    new_steps.append(elem+1)

                    new_cost = node.cost + self.fitness[elem]

                    new_node = Node(new_cost, new_state, new_steps)

                    # Check for Repeated States
                    if not self.has_repeated_states(new_node):
                        bisect.insort(self.fringe, new_node)

    def uniform_cost_search(self):
        num_visited = 0
        fitness_len = len(self.fitness)
        while True:
            if not self.fringe:
                return 'Failure'

            # Explore Fringe
            node = self.fringe.pop(0)
            num_visited += 1

            # Check for Goal State
            if node.state == [1] * fitness_len:
                print(node.cost, num_visited)
                node.print_steps()
                return 'Success'

            # Generate Successor States
            self.generate_nodes(node)

import time
t = time.process_time()

# inp = [1,2,5,10] #(a)
inp = [1,2,5,10,3,4,14,18,20,50] #(b)
# inp = [1,2,5,10,12,17,24,21,20,20,11,33,15,19,55] #(c)
state_space = Tree(inp)
state_space.uniform_cost_search()

elapsed_time = time.process_time() - t
print(elapsed_time)
