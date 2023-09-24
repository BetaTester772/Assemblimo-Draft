import random


class Node:
    def __init__(self, value, level):
        self.value = value
        self.children = []
        self.level = level


def generate_tree(height):
    root = Node(random.randint(1, 10), 0)  # 각 노드의 값 범위를 1~10으로 수정
    nodes = [root]
    while nodes:
        current_node = nodes.pop(0)
        if current_node.level < height - 1:
            for _ in range(3):  # 각 노드에 최대 3개의 자식 노드를 추가
                child = Node(random.randint(1, 10), current_node.level + 1)
                current_node.children.append(child)
                nodes.append(child)
    return root


resultes = []


def calculate_sum(node, current_sum=0):
    global resultes
    current_sum += node.value  # 현재 노드의 값 더하기
    if not node.children:  # Leaf 노드에 도달하면 합계 출력
        resultes.append(current_sum)
        print(f'Sum to leaf node: {current_sum}')
    for child in node.children:
        calculate_sum(child, current_sum)  # 재귀적으로 자식 노드에 대해 합계 계산


root = generate_tree(10)
calculate_sum(root)

print(resultes)
print(max(resultes))
print(min(resultes))
print(len(resultes))
print(sum(resultes) / len(resultes))
