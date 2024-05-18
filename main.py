

def read_input():
    with open('input.txt', 'r') as f:
        n = int(f.readline())
        scores = [int(score) for score in f.readline().split()]
    return n, scores

class Network():
     
    def __init__(self, n, scores):

        size = 2 + n + n*(n-1)//2
        self.matrix = [[0 for j in range(size)] for i in range(size)]
        games = []

        # Поток из источника
        self.matrix[0][1:n*(n-1)//2 + 1] = [3]*(len( self.matrix[1:n*(n-1)//2 + 1]))
        # Игры
        team_start = n*(n-1)//2+1
        pointer = 1
        for i in range(n):
            for j in range(i+1, n):
                self.matrix[pointer][team_start+i] = 3
                self.matrix[pointer][team_start+j] = 3
                pointer += 1
                games.append((i, j))
        # Сток
        for i in range(n):
            self.matrix[team_start+i][-1] = scores[i]
        
        self.size = size
        self.n = n
        self.scores = scores
        self.games = games
        self.game_results = [''] * len(games)
        self.team_start = team_start

    def to_team(self, vertex):

        if (vertex - self.team_start >= 0) and vertex != self.size-1:
            return vertex-self.team_start
        elif vertex > 0 and vertex < self.team_start:
            return vertex - 1
        else:
            return vertex
        

    def bfs(self, s, t, parent):
        visited = [False] * self.size
        queue = []  # Using list as a queue
        queue.append(s)
        visited[s] = True

        while queue:
            u = queue.pop(0)  # Pop from the start of the list

            for ind, val in enumerate(self.matrix[u]):
                if not visited[ind] and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        return visited[t]

    def edmonds_karp(self, source, sink):
        parent = [-1] * self.size
        max_flow = 0

        while self.bfs(source, sink, parent):
            path_flow = float("Inf")
            s = sink
            while(s != source):
                path_flow = min(path_flow, self.matrix[parent[s]][s])
                s = parent[s]

            max_flow += path_flow
            v = sink
            while(v != source):
                u = parent[v]
                self.matrix[u][v] -= path_flow
                self.matrix[v][u] += path_flow
                v = parent[v]

            path = []
            v = sink
            while(v != source):
                path.append(v)
                v = parent[v]
            path.append(source)
            path.reverse()
            print(path)
            self.game_results[path[1] - 1] = "{0} {1} ({2}) {3}".format(
                self.to_team(path[1])+1,
                self.to_team(path[-2])+1,
                path_flow,
                tuple((el + 1 for el in self.games[path[1]-1]))
            )
            self.print_matrix()
            

        return max_flow

    def print_matrix(self):
        print('-'*20)
        for row in self.matrix:
            print(
                row
            )
        print('='*20)

n, scores = read_input()

network = Network(n, scores)

print(sum(scores) == network.edmonds_karp(0, network.size-1))
print("\n".join(network.game_results))
network.print_matrix()


