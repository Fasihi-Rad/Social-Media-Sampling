from social_network import SocialMediaNetwork

# Parameters for the network
num_nodes = 1000
male_ratio = 0.3  # 30% males, 70% females

# Parameters for the connection between nodes { Normal(mean, std) }
males_con_with_males=(20, 6)
males_con_with_females=(6, 4)
females_con_with_males=(4, 2)
females_con_with_females=(10, 3)

# Create the network
network = SocialMediaNetwork(num_nodes, male_ratio)

network.generate_network(males_con_with_males, males_con_with_females,
                                females_con_with_males, females_con_with_females)

# Start a random walk
steps = 200
results, ratio, unbairatio = network.random_walk(steps)


#print the network properties
print(network.get_network())
# print the result
print(f"Random walk result after {steps} steps:")
print(results)
print("Biased Ratio of females: ", ratio*100, "%")
print("Unbiased Ratio of females: ", unbairatio*100, "%")

results, ratio = network.metropolis_hastings_random_walk(steps)

print("Visited nodes:", results)
print("Ratio of females (MHRW): ", ratio*100, "%")