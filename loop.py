import random

next_node_id = 1


class Node:
    def __init__(self, value, level):
        global next_node_id  # Access the global next_node_id variable
        self.id = next_node_id  # Assign the next_node_id value to this node's id
        next_node_id += 1  # Increment next_node_id for the next node
        self.value = value
        self.children = []
        self.probabilities = []  # 각 자식 노드로의 확률을 저장하는 리스트
        self.level = level

    def __str__(self):
        return f'{self.id}'  # Include the node id in the string representation


nodes = []


def generate_tree(height):
    global nodes
    root = Node(random.randint(min_value, max_value), 0)
    level_children = {0: []}  # 레벨별 자식 노드를 추적
    nodes.append(root)

    nodes_to_expand = [(root, 1)]  # 확률을 유지하기 위해 튜플 사용
    while nodes_to_expand:
        current_node, current_probability = nodes_to_expand.pop(0)
        if current_node.level < height - 1:
            level_children[current_node.level + 1] = level_children.get(current_node.level + 1, [])
            chose_nodes = []
            total_probability = 0
            if len(current_node.children) >= 3:
                continue
            for _ in range(3):  # 각 노드에 최대 3개의 자식 노드를 추가
                if level_children[current_node.level + 1] and random.random() < 0.3 and len(chose_nodes) < len(
                        level_children[current_node.level + 1]):
                    # 같은 레벨의 자식 중에서 중복을 허용하여 선택
                    choice = random.choice(level_children[current_node.level + 1])
                    while choice in chose_nodes:
                        choice = random.choice(level_children[current_node.level + 1])
                    child = choice
                else:
                    child = Node(random.randint(min_value, max_value), current_node.level + 1)
                    level_children[current_node.level + 1].append(child)
                    # nodes_to_expand.append(child)
                    nodes.append(child)
                current_node.children.append(child)

            children_probabilities = {}

            set_children = list(set(current_node.children))
            for i in range(len(set_children)):
                if i == len(set_children) - 1:
                    child_probability = 1 - total_probability
                else:
                    child_probability = random.uniform(0, 1 - total_probability)
                total_probability += child_probability
                children_probabilities[set_children[i]] = child_probability
                # children_probabilities.append(child_probability)

            for i in range(3):
                current_node.probabilities.append(children_probabilities[current_node.children[i]])
            for child, probability in zip(set(current_node.children), set(children_probabilities)):
                nodes_to_expand.append((child, probability))

    return root


results = []
leaf_results = []

check = 0

already = []


def calculate_sum(node, current_sum=0, probability=1, path=[]):
    global results
    global check
    global already
    global leaf_results
    current_sum += node.value
    path.append(node)  # Add the current node to the path
    if not node.children:
        if path in already:
            return
        results.append((current_sum, probability))
        check += probability
        # print(f'Sum to leaf node ({node}): {current_sum}, Probability: {probability:.4f}')
        print('Path:', ' -> '.join(str(n) for n in path),
              f"Probability: {probability:.4f}")  # Print the path to the leaf node
        leaf_results.append(current_sum * probability)
        already.append(path)
    for child, child_probability in zip(node.children, node.probabilities):
        calculate_sum(child, current_sum, probability * child_probability, path.copy())  # Pass a copy of the path


def main():
    global nodes
    global next_node_id
    global results
    global leaf_results
    global check
    global already

    leaf_results_maxes = []
    passed1 = 0
    passed2 = 0

    for _ in range(loop_time):
        # init

        nodes = []
        next_node_id = 1

        results = []
        leaf_results = []

        check = 0

        already = []

        if len(nodes) == 0:
            passed2 += 1

        root = generate_tree(tree_lenght)

        # for node in nodes:
        #     node.children = list(set(node.children))
        #     node.probabilities = list(set(node.probabilities))

        calculate_sum(root, 0, 1, [])

        print("check:", check)
        if abs(check - 1) < 0.01:
            passed1 += 1

        for node in nodes:
            print(node, node.children, node.probabilities, sum(node.probabilities))

        print(leaf_results)
        print(max(leaf_results))
        leaf_results_maxes.append(max(leaf_results))
    print(leaf_results_maxes)
    print(sum(leaf_results_maxes) / len(leaf_results_maxes))
    if loop_time != passed1:
        raise Exception("passed1 != loop_time")
    if loop_time != passed2:
        raise Exception("passed2 != loop_time")


if __name__ == '__main__':
    max_value = 100
    min_value = 10

    loop_time = 10
    tree_lenght = 10

    main()
