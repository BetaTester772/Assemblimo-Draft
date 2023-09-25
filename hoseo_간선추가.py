import random


class Node:
    def __init__(self, value, level):
        self.value = value
        self.children = []
        self.probabilities = []  # 각 자식 노드로의 확률을 저장하는 리스트
        self.level = level

    def __str__(self):
        return str(self.value)


nodes = []


def generate_tree(height):
    global nodes
    root = Node(random.randint(min_value, max_value), 0)
    nodes.append(root)

    nodes_to_expand = [(root, 1)]  # 확률을 유지하기 위해 튜플 사용
    while nodes_to_expand:
        current_node, current_probability = nodes_to_expand.pop(0)
        if current_node.level < height - 1:
            total_probability = 0
            children_probabilities = []
            """for i in range(3):  # 각 노드에 최대 3개의 자식 노드를 추가
                if i == 2:  # 마지막 자식 노드는 남은 확률을 모두 가져감
                    child_probability = 1 - total_probability
                else:
                    child_probability = random.uniform(0, 1 - total_probability)
                total_probability += child_probability
                children_probabilities.append(child_probability)"""

            for i in range(3):
                child = Node(random.randint(min_value, max_value), current_node.level + 1)
                current_node.children.append(child)
                nodes.append(child)

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
                nodes_to_expand.append((current_node.children[i], children_probabilities[current_node.children[i]]))

    return root


check = 0


def calculate_sum(node, current_sum=0, probability=1):
    global results
    global check
    current_sum += node.value
    if not node.children:
        results.append((current_sum, probability))
        check += probability
        # print(f'Sum to leaf node ({node}): {current_sum}, Probability: {probability:.4f}')
    for child, child_probability in zip(node.children, node.probabilities):
        calculate_sum(child, current_sum, probability * child_probability)


max_value = 10
min_value = 1

root = generate_tree(5)

results = []
calculate_sum(root)

# 결과 출력
sums, probabilities = zip(*results)
print(f"max: {max(sums)}")
print(f"min: {min(sums)}")
print(f"avg: {sum(sums) / len(sums):.3f}")

print(check)
