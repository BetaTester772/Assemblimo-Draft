import matplotlib.pyplot as plt
import networkx as nx
import random
import sys

sys.setrecursionlimit(10 ** 7)  # 재귀 호출 제한을 늘림


class Node:
    def __init__(self, value, level):
        self.value = value
        self.children = []
        self.level = level


def generate_tree(height):
    root = Node(random.randint(1, 10), 0)
    level_nodes = {0: [root]}  # 레벨별로 노드를 그룹화

    for level in range(height - 1):
        level_nodes[level + 1] = []  # 다음 레벨의 노드 그룹을 초기화
        for node in level_nodes[level]:
            for _ in range(3):  # 각 노드에 최대 3개의 자식 노드를 추가
                # 현재 레벨의 노드 그룹에서 무작위로 노드를 선택하여 중복을 허용
                if level_nodes[level + 1] and random.random() < 0.2:
                    child = random.choice(level_nodes[level + 1])
                else:
                    child = Node(random.randint(1, 10), level + 1)
                node.children.append(child)
                level_nodes[level + 1].append(child)  # 다음 레벨의 노드 그룹에 자식 노드를 추가

    return root


def draw_tree(node, graph=None, pos=None, level=0,
              width=2., vert_gap=0.2, vert_shift=0.,
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
                                           xcenter=xcenter_child, parsed=parsed)
    return graph, pos, parsed


results = []


def calculate_sum(node, current_sum=0):
    global results
    current_sum += node.value  # 현재 노드의 값 더하기
    if not node.children:  # Leaf 노드에 도달하면 합계 출력
        results.append(current_sum)
        print(f'Sum to leaf node: {current_sum}')
    for child in node.children:
        calculate_sum(child, current_sum)  # 재귀적으로 자식 노드에 대해 합계 계산


root = generate_tree(5)
graph, pos, parsed = draw_tree(root)

# Draw nodes and edges
nx.draw(graph, pos, with_labels=False, arrows=False)

# Draw node labels
labels = {node: node.value for node in graph.nodes()}
nx.draw_networkx_labels(graph, pos, labels)

plt.show()

# Calculating sum
calculate_sum(root)
print(results)
print(f'Total number of paths: {len(results)}',
      f'(Max: {max(results)}, Min: {min(results)})',
      f'Average: {sum(results) / len(results)}', sep='\n')
