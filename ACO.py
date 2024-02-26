class Ant:
    def __init__(self, start_node):
        self.current_node = start_node
        self.visited_nodes = [start_node]
        self.total_distance = 0.0

    def move_to_next_node(self, pheromone_matrix, visibility_matrix):
        # Implement ant movement logic here
        current_node = self.current_node
        next_node = None
        max_pheromone = 0.0

        for node in range(len(visibility_matrix[current_node])):
            if node not in self.visited_nodes:
                pheromone = pheromone_matrix[current_node][node]
                visibility = visibility_matrix[current_node][node]
                attractiveness = pheromone ** self.alpha * visibility ** self.beta

                if attractiveness > max_pheromone:
                    max_pheromone = attractiveness
                    next_node = node

        if next_node is not None:
            self.visited_nodes.append(next_node)
            self.total_distance += pheromone_matrix[current_node][next_node]
            self.current_node = next_node
        

    def update_pheromone(self, pheromone_matrix):
        # Calculate the delta pheromone for each ant
        delta_pheromone = 1 / self.total_distance

        for i in range(len(self.visited_nodes) - 1):
            node1 = self.visited_nodes[i]
            node2 = self.visited_nodes[i + 1]
            self.pheromone_matrix[node1][node2] = (1 - self.rho) * self.pheromone_matrix[node1][node2] + delta_pheromone
    

class ACO:
    def __init__(self, num_ants, num_iterations, alpha, beta, rho):
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.pheromone_matrix = None
        self.visibility_matrix = None
        self.data = []

    def read_data(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('e'):
                    # Split the line and extract vertices
                    _, vertex1, vertex2 = line.strip().split()
                    vertex1 = int(vertex1)
                    vertex2 = int(vertex2)
                    # Append the edge as a tuple of vertices
                    self.data.append((vertex1, vertex2))
    
    def initialize_pheromone_matrix(self):
        # Implement pheromone matrix initialization logic here
        self.pheromone_matrix = [[1.0] * len(self.visibility_matrix) for _ in range(len(self.visibility_matrix))]

    def initialize_visibility_matrix(self):
        # Implement visibility matrix initialization logic here
        self.visibility_matrix = [[1 / distance if distance != 0 else 0 for distance in row] for row in self.data]

    def run(self):
        self.initialize_pheromone_matrix()
        self.initialize_visibility_matrix()

        for iteration in range(self.num_iterations):
            ants = [Ant(start_node) for start_node in range(num_ants)]

            for ant in ants:
                while not ant.visited_all_nodes():
                    ant.move_to_next_node(self.pheromone_matrix, self.visibility_matrix)

                ant.update_pheromone(self.pheromone_matrix)

            # best path extraction 
            best_ant = max(ants, key=lambda ant: ant.total_distance)
            best_path = best_ant.visited_nodes
            print("Best path:", best_path)

# Example usage
num_ants = 20
num_iterations = 10
alpha = 0.8
beta = 0.8
rho = 0.8
file_path = "queen11_11.col"

aco = ACO(num_ants, num_iterations, alpha, beta, rho)
aco.read_data(file_path)
aco.run()