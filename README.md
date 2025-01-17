# Social-Media-Sampling
## Social Media Network Simulation & Sampling

This project simulates a social media network, allowing the creation of nodes (representing individuals) and connections between them, with various options for network analysis, including random walks and Metropolis-Hastings random walks.

## Features
- Generate a network with nodes divided into male and female categories.
- Define connections between nodes based on Gaussian distribution parameters.
- Perform random walks to analyze connection patterns.
- Utilize Metropolis-Hastings random walks for probabilistic network exploration.
- Return network statistics such as the number of male and female nodes.

## Algorithms
This project employs two main algorithms:
1. **Random Walk with Unbiased Estimation**: A simple random walk is performed on the network, and an unbiased probability of encountering female nodes is calculated.
2. **Metropolis-Hastings Random Walk**: A probabilistic random walk is performed, using a transition rule that ensures better exploration of the network while accounting for connection biases.

## Installation
Ensure you have Python installed (version 3.6 or higher). Additionally, install the following dependencies:

```bash
pip install numpy
```

## Usage

### 1. Importing the Module
Save the code in a file, e.g., `social_network.py`, and import it into your project.

```python
from social_network import SocialMediaNetwork
```

### 2. Creating the Network
Create an instance of the `SocialMediaNetwork` class, specifying the total number of nodes and the male-to-female ratio (default is 0.4):

```python
network = SocialMediaNetwork(num_nodes=1000, male_ratio=0.3)
```

### 3. Generating the Network
Generate the network by specifying the mean and standard deviation for the number of connections:

```python
nodes, graph = network.generate_network(
    males_con_with_males=(23, 5),
    males_con_with_females=(5, 3),
    females_con_with_males=(5, 3),
    females_con_with_females=(12, 3)
)
```

#### Parameters for `generate_network`:
- **males_con_with_males** *(tuple)*: Mean and standard deviation for connections between male nodes.
- **males_con_with_females** *(tuple)*: Mean and standard deviation for connections between male and female nodes.
- **females_con_with_males** *(tuple)*: Mean and standard deviation for connections between female and male nodes.
- **females_con_with_females** *(tuple)*: Mean and standard deviation for connections between female nodes.

### 4. Retrieving Network Statistics
Retrieve the number of male and female nodes in the network:

```python
network_data = network.get_network()
print(network_data)  # Output: {'male': 300, 'female': 700}
```

### 5. Performing a Random Walk
Simulate a random walk through the network for a given number of steps:

```python
steps = 100
results = network.random_walk(steps=steps)
print(results)  # Outputs seen sexes, probabilities, etc.
```

#### Parameters for `random_walk`:
- **steps** *(int)*: Number of steps for the random walk.
- **start_node_id** *(int, optional)*: ID of the starting node. If not specified, a random node is selected.

### 6. Performing a Metropolis-Hastings Random Walk
Run a Metropolis-Hastings random walk to explore the network:

```python
mh_results = network.metropolis_hastings_random_walk(steps=100)
print(mh_results)
```

#### Parameters for `metropolis_hastings_random_walk`:
- **steps** *(int)*: Number of steps for the random walk.
- **start_node_id** *(int, optional)*: ID of the starting node. If not specified, a random node is selected.

### 7. Customizing Probability Calculations
Probability calculations for the Metropolis-Hastings random walk are handled by the `_get_probability_list` method. It can be customized to modify transition probabilities.

## Example Output
```python
network = SocialMediaNetwork(num_nodes=10, male_ratio=0.5)
nodes, graph = network.generate_network()
print("Nodes:", nodes)
print("Graph:", dict(graph))

# Perform a random walk
seen_sex, prob, unbiased_prob = network.random_walk(steps=10)
print("Random Walk Results:", seen_sex, prob, unbiased_prob)
```

Sample output:
```
Nodes: [{'id': 0, 'sex': 'male'}, {'id': 1, 'sex': 'male'}, ...]
Graph: {0: [1, 3], 1: [0, 4], ...}
Random Walk Results: Counter({'female': 6, 'male': 4}) 0.6 0.5
```

## Notes
- The connections in the graph are two-way, ensuring mutual relationships.
- Parameters for connection distributions allow flexibility in network design.

## Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

