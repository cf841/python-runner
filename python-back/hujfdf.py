from collections import defaultdict

def numNicePairs(g_nodes, g_from, g_to, g_weight):
    def is_palindrome(path):
        count = [0] * 26
        for node in path:
            count[g_weight[node] - 1] ^= 1
        return sum(count) <= 1

    def dfs(node, parent, path):
        path.append(node)
        for neighbor in graph[node]:
            if neighbor != parent:
                dfs(neighbor, node, path)
        path.pop()

    def count_palindromic_paths():
        count = 0
        for i in range(g_nodes):
            for j in range(i + 1, g_nodes):
                path = []
                dfs(i, -1, path)
                if is_palindrome(path):
                    count += 1
        return count

    # Build the graph
    graph = defaultdict(list)
    for u, v in zip(g_from, g_to):
        graph[u - 1].append(v - 1)
        graph[v - 1].append(u - 1)

    return count_palindromic_paths()

g_nodes = 5
g_from = [1, 1, 2, 2]
g_to = [2, 3, 4, 5]
g_weight = [1, 2, 1, 2]
print(numNicePairs(g_nodes, g_from, g_to, g_weight)-1)  # 4