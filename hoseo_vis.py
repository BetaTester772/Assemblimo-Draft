import random
import networkx as nx
import matplotlib.pyplot as plt
import os


class Node:
    def __init__(self, value, level):
        self.value = value
        self.children = []
        self.level = level

    def __str__(self):
        return str(self.value)


nodes = []


def generate_tree(height):
    global nodes
    root = Node(random.randint(min_value, max_value), 0)
    level_children = {0: []}  # 레벨별 자식 노드를 추적
    nodes.append(root)

    nodes_to_expand = [root]
    while nodes_to_expand:
        current_node = nodes_to_expand.pop(0)
        if current_node.level < height - 1:
            level_children[current_node.level + 1] = level_children.get(current_node.level + 1, [])
            chose_nodes = []
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
                    nodes_to_expand.append(child)
                    nodes.append(child)
                chose_nodes.append(child)
                current_node.children.append(child)

    return root


results = []


def calculate_sum(node, current_sum=0):
    global results
    current_sum += node.value  # 현재 노드의 값 더하기
    if not node.children:  # Leaf 노드에 도달하면 합계 출력
        results.append(current_sum)
        print(f'Sum to leaf node ({node}): {current_sum}')
    for child in node.children:
        calculate_sum(child, current_sum)  # 재귀적으로 자식 노드에 대해 합계 계산


max_value = 10
min_value = 1

root = generate_tree(5)
calculate_sum(root)

print(results)
print(len(results))
print(f"max: {max(results)}")
print(f"min: {min(results)}")
print(f"avg: {sum(results) / len(results)}")


def draw_tree(node, graph=None, pos=None, level=0,
              width=2., vert_gap=0.4, vert_shift=0.,
              xcenter=0.5, root=None, parsed=[]):
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
            graph, pos, parsed = draw_tree(child, graph=graph, pos=pos,
                                           level=level + 1, width=width,
                                           xcenter=xcenter_child, parsed=parsed, )
    return graph, pos, parsed


# Now to use this function to draw your tree:
graph, pos, parsed = draw_tree(root)
labels = {node: str(node.value) for node in parsed}  # 각 노드에 대한 레이블 생성
nx.draw(graph, pos, with_labels=True, labels=labels)
for i in range(1, 6):
    print(sum(results[:i]) / i, results[:i])

# save plot
os.makedirs('plots', exist_ok=True)
# check files in plots directory
print(os.listdir('plots'))

plt.savefig(f'plots/plot_{len(os.listdir("plots"))}.png')
plt.show()

results.sort(reverse=True)
