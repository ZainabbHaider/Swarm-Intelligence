import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt
import bisect

class Graph:
    def __init__(self, file_path):
        self.num_nodes = 0
        self.num_edges = 0
        self.graph = np.zeros((self.num_nodes,self.num_nodes))
        self.maximal_degree = 0
        self.node_degrees = []
        self.file_path = file_path
        self.edges = []
        self.read_data()

    def read_data(self):
        with open(self.file_path, 'r') as file:
            self.num_nodes, self.num_edges = map(int, file.readline().strip().split(" ")[2:])
            self.graph = [[0] * self.num_nodes for _ in range(self.num_nodes)]
            for line in file:
                if line.startswith('e'):
                    _, v1, v2 = line.strip().split()
                    v1, v2 = int(v1), int(v2)
                    self.edges.append((v1,v2))
                    self.graph[v1-1][v2-1] = 1
                    self.graph[v2-1][v1-1] = 1
        self.node_degrees = [sum(row) for row in self.graph]
        self.maximal_degree = max(self.node_degrees)

class Ant:
    def __init__(self, G, pheromone_matrix, colors, Q, alpha, beta):
        self.G = G
        self.graph = G.graph
        self.num_nodes = G.num_nodes
        self.num_edges = G.num_edges
        self.node_degrees = G.node_degrees

        self.colors =  colors
        self.colormap = {color: set() for color in self.colors}
        self.pheromones = pheromone_matrix

        self.unvisited = set(range(self.num_nodes))
        self.solution = [None] * self.num_nodes # assigned colors

        self.alpha = alpha
        self.beta = beta
        self.Q = Q

        self.cost = 0
        
    def getDesirability(self, v):
        return self.G.node_degrees[v]
        
    def getPheromones(self, v, c, p):
        if len(self.colormap[c]) == 0:
            return 0.1
        total_p = sum([p[v][w] for w in self.colormap[c]])
        return total_p / len(self.colormap[c])

    def color_graph(self):
        self.cost = 0
        while self.unvisited:
            current_color = self.cost + 1
            colorable = set(self.unvisited)
            
            while colorable:
                if current_color not in self.colormap:
                    self.colormap[current_color] = set()
                
                # calculate desirability and pheromone for each vertex
                desirabilities = {v: self.getDesirability(v) for v in colorable}
                pheromone_trails = {v: self.getPheromones(v, current_color, self.pheromones) for v in colorable}
                
                probabilities = []
                vertices_list = list(colorable)
                for v in vertices_list:
                    pheromone = max(pheromone_trails[v], 1e-4)
                    desirability = max(desirabilities[v], 1e-4)
                    probability = (pheromone ** self.alpha) * (desirability ** self.beta)
                    probabilities.append(probability)
                
                # normalize
                total = sum(probabilities)
                probabilities = [p / total for p in probabilities]

                next_vertex = np.random.choice(vertices_list, p=probabilities)
                
                # update colored set
                self.colormap[current_color].add(next_vertex)
                self.solution[next_vertex] = current_color
                colorable.remove(next_vertex)
                self.unvisited.remove(next_vertex)

                # update colorable vertices
                neighbors = {i for i in range(self.num_nodes) if self.G.graph[next_vertex][i] == 1}
                colorable = colorable.difference(neighbors)
            self.cost += 1
        return self.solution, self.cost

    def updatePheromones(self):
        PheromoneMatrix = np.zeros((self.num_nodes,self.num_nodes))
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if self.solution[i] == self.solution[j] and (i != j):
                    PheromoneMatrix[i, j] = self.Q /self.cost
                    PheromoneMatrix[j, i] = PheromoneMatrix[i,j]
        return PheromoneMatrix

class AntColony:
    def __init__(self, G, num_ants, Q, alpha, beta, evaporation_rate, initial_p):
        self.graph = G.graph
        self.num_nodes = G.num_nodes
        self.initial_pheromones = initial_p
        self.pheromones = np.ones((G.num_nodes, G.num_nodes)) * self.initial_pheromones
        
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if self.graph[i][j] == 1:
                    self.pheromones[i][j] = 0

        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.Q = Q
        self.evaporation_rate = evaporation_rate

        self.colors = list(range(1, G.maximal_degree + 1))
        
        self.best_solution = None
        self.best_solution_cost = float('inf')

        self.iteration_best_costs = []
        self.iteration_average_costs = []

    def run(self, iterations):
       for _ in range(iterations):
            print("Iteration", _)
            iteration_average = 0
            solutions = []
            costs = []
            delta = np.zeros((self.num_nodes, self.num_nodes))
            for __ in range(self.num_ants):
                ant = Ant(G, self.pheromones, self.colors, self.Q, self.alpha, self.beta)
                s, c = ant.color_graph()
                solutions.append(s)
                costs.append(c)
                if c < self.best_solution_cost:
                    self.best_solution = s.copy()
                    self.best_solution_cost = c
                iteration_average += c
                print("Ant:", __, "Cost:", c)
                # update pheromones
                delta += ant.updatePheromones()
                self.pheromones = (1-self.evaporation_rate)*self.pheromones + delta
            iteration_average /= self.num_ants
            self.iteration_best_costs.append(self.best_solution_cost)
            self.iteration_average_costs.append(iteration_average)

    def show_plot(self):
        # Plot the iteration number against the best and average costs
        plt.figure(figsize=(10, 5))
        plt.plot(range(1, len(self.iteration_best_costs) + 1), self.iteration_best_costs, label='Best Cost')
        plt.plot(range(1, len(self.iteration_average_costs) + 1), self.iteration_average_costs, label='Average Cost')
        plt.xlabel('Iteration')
        plt.ylabel('Cost')
        plt.title('Evolution of Best and Average Costs over Iterations')
        plt.legend()
        plt.grid(True)
        plt.show()

    def show_best(self):
        G_nx = nx.Graph()
        G_nx.add_nodes_from(range(len(self.graph)))
        for i in range(len(self.graph)):
            for j in range(i+1, len(self.graph)):
                if self.graph[i][j] == 1:
                    G_nx.add_edge(i, j)

        # Plot the graph
        plt.figure(figsize=(10, 5))

        # Plot the graph layout
        plt.subplot(1, 1, 1)
        pos = nx.spring_layout(G_nx)
        nx.draw(G_nx, pos, with_labels=True, node_color=self.best_solution, cmap=plt.cm.Set1, node_size=500)
        plt.title('Graph with Coloring')
        plt.show()

# Fine-tune parameters
num_ants = 20
iterations = 500
evaporation_rate = 0.5
alpha = 3
beta = 2
Q = 1
initial_pheromones = 0.1

G = Graph("queen11_11.col")
aco = AntColony(G, num_ants, Q, alpha, beta, evaporation_rate, initial_pheromones)
aco.run(iterations)

print("-"*20)
print("Best Solution:", aco.best_solution)
print("Cost:", aco.best_solution_cost)

aco.show_plot()
aco.show_best()