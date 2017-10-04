import bisect, itertools

class Node:
    def __init__(self, cost, heuristic, state, steps):
        self.cost = cost
        self.f = cost + heuristic
        self.state = state
        self.steps = steps

    def __lt__(self, other):
        return self.f < other.f

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
            if node.state == item.state and node.f < item.f:
                self.fringe.remove(item)
                bisect.insort(self.fringe, node)
                return True
            if node.state == item.state:
                return True
        return False

    
    def find_heuristic(self,node,place):
    	l = []
    	for elem in list(range(len(self.fitness))):
    		if node.state[elem] == place:
    			l.append(self.fitness[elem])
    	l.sort()
    	print(l)
    	if len(l) >= 4:
    		h = (len(l)-3)*l[0]
    		for elem in range(1,len(l)-2):
    			h += l[elem]
    		h += min(2*l[1],l[0]+l[len(l)-2]) + l[len(l)-1]
    	elif len(l) == 3:
    		h = sum(l)
    	else:
    		h = max(l)
    	print(h)
    	return h

    def generate_nodes(self,node):
    	fitness_len = len(self.fitness)
    	if len(node.steps) % 3 == 0:
    		h = self.find_heuristic(node,0)
    		for elem in itertools.combinations(list(range(fitness_len)), 2):
    			if (node.state[elem[0]] == 0 and node.state[elem[1]] == 0):
    				new_state = list(node.state)
    				new_state[elem[0]] = 1
    				new_state[elem[1]] = 1

    				new_steps = list(node.steps)
    				new_steps.extend([elem[0]+1, elem[1]+1])

    				new_cost = node.cost + max(self.fitness[elem[0]], self.fitness[elem[1]])
    				new_node = Node(new_cost, h	, new_state, new_steps)

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

inp = [6,8,14,33,59]
#[1,2,5,9,15,15,19]
state_space = Tree(inp)
state_space.a_star()


'''


'''