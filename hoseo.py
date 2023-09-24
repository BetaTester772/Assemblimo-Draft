import random


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
        # print(f'Sum to leaf node ({node}): {current_sum}')
    for child in node.children:
        calculate_sum(child, current_sum)  # 재귀적으로 자식 노드에 대해 합계 계산


max_value = 10
min_value = 1

root = generate_tree(5)
calculate_sum(root)

print(results)
print(f"max: {max(results)}")
print(f"min: {min(results)}")
print(f"avg: {sum(results) / len(results)}")

results.sort(reverse=True)
for i in range(1, 6):
    # 평균 소수젓 아래 3째 자리까지 출력
    print(f"{sum(results[:i])/i:.3f}", results[:i])
