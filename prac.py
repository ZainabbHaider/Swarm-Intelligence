import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt


class Ant:
    def __init__(self, num_vertices):
        self.solution = [-1] * num_vertices
        self.colors = []
        self.cost = None
    
    def _ant_solution(self, start_vertex, graph, alpha, beta, pheromone_matrix):
        # solution = [-1] * len(self.graph)
        visited = [False] * len(graph)
        visited[start_vertex] = True
        self.solution[start_vertex] = 1
        self.colors.append(1)

        for i in range(1, len(graph)):
            current_vertex = self.solution[i - 1]
            # print(current_vertex)
            neighbors = [index for index, value in enumerate(graph[current_vertex]) if value == 1 and not visited[index]]
            next_vertex = -1

            if neighbors:
                probabilities = [((pheromone_matrix[current_vertex][neighbor] ** alpha) *
                                  ((1.0 / len(neighbors)) ** beta)) for neighbor in neighbors]
                total_prob = sum(probabilities)
                probabilities = [prob / total_prob for prob in probabilities]
                next_vertex = np.random.choice(neighbors, p=probabilities)

            if next_vertex == -1:
                next_vertex = random.choice([index for index, value in enumerate(visited) if not value])
                # self.solution[current_vertex] = random.randint(0, self.num_colors - 1)
                
            neighbors = [index for index, value in enumerate(graph[next_vertex]) if value == 1]
            if neighbors:
                adjacent_colors = [self.solution[n] for n in neighbors if self.solution[n] != -1]
                available_colors = [color for color in self.colors if color not in adjacent_colors]
                if available_colors:
                    self.solution[next_vertex] = random.choice(available_colors)
                else:
                    self.colors.append(len(self.colors)+1)
                    self.solution[next_vertex] = len(self.colors) + 1
            else:
                self.colors.append(len(self.colors)+1)
                self.solution[next_vertex] = len(self.colors) + 1
                
            visited[next_vertex] = True
        self.cost = len(self.colors)
        return self.solution
    
class AntColony:
    def __init__(self, num_ants, evaporation_rate, alpha, beta, Q):
        self.graph = None
        self.num_ants = num_ants
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha
        self.beta = beta
        self.Q = Q
        self.pheromone_matrix = None
        self.best_solution = None
        self.best_solution_cost = float('inf')
        # self.colors = []

    def _update_pheromone(self, solution, cost):
        for i in range(len(solution)):
            for j in range(len(solution)):
                if i != j and cost != 0:
                    if self.graph[i][j] == 1:  # If vertices i and j are adjacent
                        if solution[i] == solution[j]:  # If vertices i and j have the same color
                            self.pheromone_matrix[i][j] = (1 - self.evaporation_rate) * self.pheromone_matrix[i][j] + (self.Q / (2 * cost))
                        else:  # If vertices i and j have different colors
                            self.pheromone_matrix[i][j] = (1 - self.evaporation_rate) * self.pheromone_matrix[i][j] + ( self.Q / (1 * cost))
                    elif solution[i] == solution[j]:  # If vertices i and j are not adjacent but have the same color
                        self.pheromone_matrix[i][j] = (1 - self.evaporation_rate) * self.pheromone_matrix[i][j] + (self.Q / (1 * cost))

    

    def run(self, iterations):
        # print(self.pheromone_matrix)
        for _ in range(iterations):
            iteration_solutions = []
            iteration_costs = []
            for i in range(self.num_ants):
                ant = Ant(len(self.graph))
                start_vertex = random.randint(0, len(self.graph) - 1)
                # print(start_vertex)
                ant._ant_solution(start_vertex, self.graph, self.alpha, self.beta, self.pheromone_matrix)
                print("Ant:", i, "Cost:",ant.cost)
                iteration_solutions.append(ant.solution)
                iteration_costs.append(ant.cost)
                if ant.cost < self.best_solution_cost:
                    self.best_solution = ant.solution
                    self.best_solution_cost = ant.cost

                self._update_pheromone(ant.solution, ant.cost)
            print("Iteration:", _ ,"Best Solution:", iteration_solutions[iteration_costs.index(min(iteration_costs))], "Cost:", min(iteration_costs))
            # print(self.pheromone_matrix)
        # print("Best Solution:", self.best_solution, "Cost:", self.best_solution_cost)
        
    def _calculate_cost(self, solution):
        return len(set(solution))  # Number of unique colors used in the solution

    
    def read_data(self, file_path):
        with open(file_path, 'r') as file:
            n = int(file.readline().strip().split(" ")[2])
            print(n)
            matrix = []
            for i in range(n):
                row = []
                for j in range(n):
                    row.append(0)
                matrix.append(row)
            for line in file:
                if line.startswith('e'):
                    # Split the line and extract vertices
                    _, vertex1, vertex2 = line.strip().split()
                    vertex1 = int(vertex1)
                    vertex2 = int(vertex2)
                    # Append the edge as a tuple of vertices
                    matrix[vertex1-1][vertex2-1] = 1
        self.graph = matrix
        self.pheromone_matrix = np.ones((len(self.graph), len(self.graph)))  # Pheromone matrix
        
    def plot(self):
        G = nx.Graph()
        G.add_nodes_from(range(len(self.graph)))
        for i in range(len(self.graph)):
            for j in range(i+1, len(self.graph)):
                if self.graph[i][j] == 1:
                    G.add_edge(i, j)

        # Plot the graph
        plt.figure(figsize=(10, 5))

        # Plot the graph layout
        plt.subplot(1, 1, 1)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color=self.best_solution, cmap=plt.cm.Set1, node_size=500)
        plt.title('Graph with Coloring')
        plt.show()

# Example usage:

num_ants = 50
iterations = 10
evaporation_rate = 0.8
alpha = 0.8
beta = 0.8
Q = 1

aco = AntColony(num_ants, evaporation_rate, alpha, beta, Q)
aco.read_data("queen11_11.col")
aco.run(iterations)
aco.plot()

print("Best Solution:", aco.best_solution)
print("Cost:", aco.best_solution_cost)
