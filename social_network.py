import numpy as np
import random
from collections import defaultdict, Counter

class SocialMediaNetwork:
    def __init__(self, num_nodes, male_ratio=0.4):
        """
        Initialize the Social Media Network.
        
        Parameters:
            num_nodes (int): Total number of nodes in the network.
            male_ratio (float): Ratio of male nodes in the network.
        """
        self.num_nodes = num_nodes
        self.male_ratio = male_ratio
        self.nodes = []  # List of nodes with properties (id and sex)
        self.males = []  # List of male nodes
        self.females = []  # List of female nodes
        self.graph = defaultdict(list)  # Adjacency list for relationships

    def generate_network(self, males_con_with_males=(23, 5), males_con_with_females=(5, 3),
                          females_con_with_males=(5, 3), females_con_with_females=(12, 3)):
        """
        Generate the social media network with nodes and random connections.
        
        Parameters:
            males_con_with_males (tuple): Mean and std-dev for male-male connections.
            males_con_with_females (tuple): Mean and std-dev for male-female connections.
            females_con_with_males (tuple): Mean and std-dev for female-male connections.
            females_con_with_females (tuple): Mean and std-dev for female-female connections.
        
        Returns:
            tuple: List of nodes and the graph (connections).
        """
        # Calculate the number of male nodes
        num_males = int(self.num_nodes * self.male_ratio)

        # Assign sexes to nodes
        for i in range(self.num_nodes):
            if i < num_males:
                self.males.append({'id': i, 'sex': 'male'})
            else:
                self.females.append({'id': i, 'sex': 'female'})

        # Combine male and female nodes
        self.nodes = self.males + self.females

        # Create random connections between nodes
        for node in self.nodes:
            if node['sex'] == 'male':
                # Male connection counts
                num_con_with_males = max(1, int(random.gauss(males_con_with_males[0], males_con_with_males[1])))
                num_con_with_females = max(1, int(random.gauss(males_con_with_females[0], males_con_with_females[1])))
            else:
                # Female connection counts
                num_con_with_males = max(1, int(random.gauss(females_con_with_males[0], females_con_with_males[1])))
                num_con_with_females = max(1, int(random.gauss(females_con_with_females[0], females_con_with_females[1])))

            # Select random samples for connections
            samples = random.sample(self.males, num_con_with_males) + random.sample(self.females, num_con_with_females)

            # Add connections to the graph (avoid self-loops)
            
            for sample in samples:
                if sample['id'] != node['id']:
                    if sample['id'] not in self.graph[node['id']]:
                        self.graph[node['id']].append(sample['id'])
                        # Add the reverse connection if not already present
                        if node['id'] not in self.graph[sample['id']]:
                            self.graph[sample['id']].append(node['id'])

        return self.nodes, self.graph

    def get_network(self):
        """
        Get the overall network data, including the number of males and females.

        Returns:
            dict: Network statistics (male and female counts).
        """
        self.data = {
            'male': len(self.males),
            'female': len(self.females)
        }
        return self.data

    def random_walk(self, steps, start_node_id=-1):
        """
        Perform a simple random walk on the network.
        
        Parameters:
            steps (int): Number of steps for the random walk.
            start_node_id (int): Starting node ID (-1 for random start).

        Returns:
            tuple: Counts of seen sexes, ratio of females, unbiased ratio.
        """
        seen_sex = []
        num_of_con = []
        
        # Random start node if not specified
        if start_node_id == -1:
            start_node_id = random.randint(0, self.num_nodes - 1)
        current_node = start_node_id

        for _ in range(steps):
            # Store the number of connections and current node's sex
            num_of_con.append([len(self.graph[current_node]),
                               1 if self.nodes[current_node]['sex'] == 'male' else 0])

            # Move to a randomly connected node
            next_node = random.choice(self.graph[current_node])
            seen_sex.append(self.nodes[next_node]['sex'])
            current_node = next_node

        # Calculate ratio
        number_of_seen_sex = Counter(seen_sex)
        # biased ratio
        ratio = number_of_seen_sex['female'] / steps
        # unbiased ratio
        num_of_con = np.array(num_of_con)
        unbiased_ratio = np.sum(1 / num_of_con[num_of_con[:, 1] == 0, 0]) / np.sum(1 / num_of_con[:, 0])

        return Counter(seen_sex), ratio, unbiased_ratio

    def metropolis_hastings_random_walk(self, steps, start_node_id=-1):
        """
        Perform a Metropolis-Hastings random walk on the network.

        Parameters:
            steps (int): Number of steps for the random walk.
            start_node_id (int): Starting node ID (-1 for random start).

        Returns:
            tuple: Counts of visited node sexesm, ratio of females.
        """
        # Random start node if not specified
        if start_node_id == -1:
            start_node_id = random.randint(0, self.num_nodes - 1)

        current_node = start_node_id
        seen_sex = [] # List of seen

        for _ in range(steps):
            seen_sex.append(self.nodes[current_node]['sex'])

            # Get transition probabilities
            probabilities = self._get_probability_list(current_node)

            # Select the next node based on probabilities
            selected_node = np.random.choice(self.graph[current_node] + [current_node], p=probabilities)
            current_node = selected_node
            
        # calculate the ratio of female nodes
        number_of_seen_sex = Counter(seen_sex)
        ratio = number_of_seen_sex['female'] / steps

        return Counter(seen_sex), ratio

    def _get_probability_list(self, node_id):
        """
        Calculate the transition probabilities for the given node.

        Parameters:
            node_id (int): Current node ID.

        Returns:
            np.array: List of probabilities for neighbors and staying on the current node.
        """
        # List of neighbors for the current node
        neighbors = self.graph[node_id]
        # create a list for probabilities
        probability_list = np.zeros(len(neighbors) + 1)
        # Number of Neighbors 
        num_con_current_node = len(neighbors)
        
        # Calculate the transition probability for each neighbor
        for i, neighbor_id in enumerate(neighbors):    
            num_con_neighbor = len(self.graph[neighbor_id])
            probability_list[i] = (1 / num_con_current_node) * min(1, num_con_current_node / num_con_neighbor)

        # Calculate the transition probability for staying on the current node
        probability_list[-1] = max(0, 1 - np.sum(probability_list))

        return probability_list