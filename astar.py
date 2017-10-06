import bisect, itertools

class Node:
    def __init__(self, cost, heuristic, state, steps):
        self.cost = cost
        self.evaluation_function = cost + heuristic
        self.state = state
        self.steps = steps

    def __lt__(self, other):
        return self.evaluation_function < other.evaluation_function

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
        root = Node(cost, 0, state, steps)

        self.fringe = [root]
        self.fitness = fitness

    def has_repeated_states(self, node):
        for item in self.fringe:
            if node.state == item.state and node.evaluation_function < item.evaluation_function:
                self.fringe.remove(item)
                bisect.insort(self.fringe, node)
                return True
            if node.state == item.state:
                return True
        return False
    '''
    h = the sum of every other time taken by people on the left of the bridge
    We choose this heuristic to minimize the wasted time by letting the slowest
    and 2nd slowest, 3rd slowest and 4th slowest, and so on cross the bridge
    to "mask" the 2nd person's time
    '''
    def find_heuristic(self,node):
        l = []
        h = 0
        for elem in list(range(len(self.fitness))):
                if node.state[elem] == 0:
                        l.append(self.fitness[elem])
        l = l[::-1]
        for elem in range(len(l),2):
                h += l[elem]
        #print(h)
        return h

    def generate_nodes(self,node):
        fitness_len = len(self.fitness)
        if len(node.steps) % 3 == 0:
            #print("old " ,node.state)
            h = self.find_heuristic(node)
            fin = []
            left = []
            c = 0
            for elem in list(range(fitness_len)):
                    if node.state[elem] == 0:
                            left.append(elem)
                            c += 1
            if c == 2:
                fin = [ [left[0],left[1]] ]
            else:
                fin = [ [left[0],left[1]] , [left[0],left[-1]] , [left[-2],left[-1]] ]
            c = 0
            #print(fin)
            for elem in fin:
                    new_state = list(node.state)
                    
                    new_state[elem[0]] = 1
                    new_state[elem[1]] = 1
                    new_steps = list(node.steps)
                    new_steps.extend([elem[0]+1, elem[1]+1])
                    
                    new_cost = node.cost + max(self.fitness[elem[0]], self.fitness[elem[1]])
                    new_node = Node(new_cost, 0 , new_state, new_steps)
                    #print("new ",new_state)
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

                    new_node = Node(new_cost, 0, new_state, new_steps)

                    if not self.has_repeated_states(new_node):
                        bisect.insort(self.fringe, new_node)

    def a_star(self):
        num_visited = 0;
        fitness_len = len(self.fitness)
        while True:
            if not self.fringe:
                return 'Failure'
            
            # Explore Fringe
            node = self.fringe.pop(0)
            num_visited += 1
            if node.state == [1] * fitness_len:
                print(node.cost, num_visited)
                node.print_steps()
                return 'Success'

            self.generate_nodes(node)

inp = [1,2,5,10,12,17,24,21,20,20,11,33,15,19,55]
#[1,2,5,9,15,15,19]
state_space = Tree(sorted(inp))
state_space.a_star()


