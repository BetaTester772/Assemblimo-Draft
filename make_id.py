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
                if level_children[current_node.level + 1] and random.random() < 0.5 and len(chose_nodes) < len(
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

check = 0

already = []

def calculate_sum(node, current_sum=0, probability=1, path=[]):
    global results
    global check
    global already
    current_sum += node.value
    path.append(node)  # Add the current node to the path
    if not node.children:
        if path in already:
            return
        results.append((current_sum, probability))
        check += probability
        # print(f'Sum to leaf node ({node}): {current_sum}, Probability: {probability:.4f}')
        print('Path:', ' -> '.join(str(n) for n in path), f"Probability: {probability:.4f}")  # Print the path to the leaf node
        already.append(path)
    for child, child_probability in zip(node.children, node.probabilities):
        calculate_sum(child, current_sum, probability * child_probability, path.copy())  # Pass a copy of the path


max_value = 10000
min_value = 1

root = generate_tree(5)
calculate_sum(root)

sums, probabilities = zip(*results)
print(f"max: {max(sums)}")
print(f"min: {min(sums)}")
print(f"avg: {sum(sums) / len(sums):.3f}")

print(check)

# results.sort(reverse=True)
# for i in range(1, 6):
#     # 평균 소수젓 아래 3째 자리까지 출력
#     print(f"{sum(results[:i]) / i:.3f}", results[:i])
#
# for node in nodes:
#     print(node, list(set(node.children)))
a = 0
for node in nodes:
    a += sum(node.probabilities)
    print(node, node.children, node.probabilities, sum(node.probabilities))

# 두번째 코드의 draw_tree 함수 병합
import networkx as nx
import matplotlib.pyplot as plt  # matplotlib 추가

plt.figure(figsize=(10, 6))  # 원하는 크기로 조절


def draw_tree(node, graph=None, pos=None, level=0,
              width=2., vert_gap=0.4, vert_shift=0.,
              xcenter=0.5, root=None, parsed=[], edge_labels={}):
    if graph is None:
        graph = nx.DiGraph()
    if pos is None:
        pos = {node: (xcenter, 1 - level * vert_gap - vert_shift)}
    else:
        pos[node] = (xcenter, 1 - level * vert_gap - vert_shift)
    parsed.append(node)

    if node.children:
        children_num = len(node.children)
        xcenter_child = xcenter - width / 2 - ((1 - children_num) / 2) * width / (children_num + 1)
        for i, child in enumerate(node.children):
            xcenter_child += (i + 1) * width / (children_num + 1)
            graph.add_edge(node, child)
            edge_labels[(node, child)] = f'{node.probabilities[i]:.2f}'  # 확률 레이블 추가
            graph, pos, parsed, edge_labels = draw_tree(child, graph=graph, pos=pos,
                                                        level=level + 1, width=width,
                                                        xcenter=xcenter_child, parsed=parsed,
                                                        edge_labels=edge_labels)  # edge_labels 인자 추가
    return graph, pos, parsed, edge_labels  # edge_labels 반환 추가


# Now to use this function to draw your tree:
graph, pos, parsed, edge_labels = draw_tree(root)  # edge_labels 반환 받기
labels = {node: f'{node.id}: {node.value}' for node in parsed}  # 각 노드에 대한 레이블 생성
nx.draw(graph, pos, with_labels=True, labels=labels)
nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)  # 원하는 크기로 조절
plt.show()  # 트리 그래프를 출력하기 위한 코드 추가
