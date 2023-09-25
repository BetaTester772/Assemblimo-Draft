import random
from asciitree import LeftAligned
from collections import OrderedDict



class Node:
    def __init__(self, value, level):
        self.value = value
        self.children = []
        self.level = level

    def items(self):
        child_dict = OrderedDict()
        for child in self.children:
            child_dict[child] = None  # 자식 노드를 순서가 지정된 dict에 추가
        return child_dict.items()


def generate_tree(height):
    root = Node(random.randint(1, 10), 0)
    level_children = {0: []}  # 레벨별 자식 노드를 추적

    nodes_to_expand = [root]
    while nodes_to_expand:
        current_node = nodes_to_expand.pop(0)
        if current_node.level < height - 1:
            level_children[current_node.level + 1] = level_children.get(current_node.level + 1, [])
            for _ in range(3):  # 각 노드에 최대 3개의 자식 노드를 추가
                if level_children[current_node.level + 1] and random.random() < 0.5:
                    # 같은 레벨의 자식 중에서 중복을 허용하여 선택
                    child = random.choice(level_children[current_node.level + 1])
                else:
                    child = Node(random.randint(1, 10), current_node.level + 1)
                    level_children[current_node.level + 1].append(child)
                    nodes_to_expand.append(child)
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


root = generate_tree(5)
calculate_sum(root)

print(results)
print(len(results))


def draw_node(node):
    if node is not None:
        return str(node.value)
    return None

def draw_tree(root):
    tr = LeftAligned(draw=draw_node)
    print(tr({root: None}))

# 이전에 정의한 generate_tree 함수를 사용하여 트리 생성
root = generate_tree(5)

# 트리를 그림
draw_tree(root)