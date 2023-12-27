import random
#TODO - Check that we don't create children with infinty length.

# 1. Order Crossover (OX)
def order_crossover(parent1, parent2):
    size = len(parent1)
    # Choose random start and end indices for the slice
    start, end = sorted(random.sample(range(size), 2))

    # Initialize offspring with 'None' values
    child1 = [None] * size
    child2 = [None] * size

    # Copy the sub-path from parent1 to child1 and from parent2 to child2
    child1[start:end] = parent1[start:end]
    child2[start:end] = parent2[start:end]

    # Create sets for quick lookup
    set1 = set(child1[start:end])
    set2 = set(child2[start:end])

    # Fill the remaining positions for child1
    p2_remaining = [item for item in parent2 if item not in set1]
    p1_remaining = [item for item in parent1 if item not in set2]

    child1[:start] = p2_remaining[:start]
    child1[end:] = p2_remaining[start:]
    child2[:start] = p1_remaining[:start]
    child2[end:] = p1_remaining[start:]

    return child1, child2

# 2. Partially Mapped Crossover (PMX)
def resolve_mapping(city, mapping):
    """Recursively resolve the city mapping until a city not in the mapping is found."""
    while city in mapping:
        city = mapping[city]
    return city

def pmx(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))

    child1 = [-1] * size
    child2 = [-1] * size

    # Copy the segment from parents to children
    child1[start:end] = parent1[start:end]
    child2[start:end] = parent2[start:end]

    # Create mapping for cities in the segments
    mapping1 = dict(zip(parent1[start:end], parent2[start:end]))
    mapping2 = dict(zip(parent2[start:end], parent1[start:end]))

    # Resolve conflicts using the mapping
    for i in list(range(start)) + list(range(end, size)):
        child1[i] = resolve_mapping(parent2[i], mapping1)
        child2[i] = resolve_mapping(parent1[i], mapping2)

    return child1, child2

# 3. Cycle Crossover (CX)
def cycle_crossover(parent1, parent2):
    size = len(parent1)
    used_indices = set()
    cycles = []
    parent1_to_index = {value: index for index, value in enumerate(parent1)}

    while len(used_indices) < size:
        current_index = next(i for i in range(size) if i not in used_indices)
        current_cycle = []

        while current_index not in used_indices:
            used_indices.add(current_index)
            current_cycle.append(current_index)
            current_index = parent1_to_index[parent2[current_index]]

        cycles.append(current_cycle)

    child1, child2 = parent1.copy(), parent2.copy()
    for i in range(len(cycles)):
        if i % 2 == 0:
            for index in cycles[i]:
                child1[index] = parent1[index]
                child2[index] = parent2[index]
        else:
            for index in cycles[i]:
                child1[index] = parent2[index]
                child2[index] = parent1[index]

    return child1, child2

# You can continue with the implementations for ERX, SCX, and POS using a similar approach.
