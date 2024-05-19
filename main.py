

def read_input():
    n = int(input())
    scores = [int(score) for score in input().split()]
    return n, scores

possible_results = {

    (3, 0) : "<",
    (0, 3) : ">",
    (2, 1) : "<=",
    (1, 2) : ">=",

}

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
        self.team_start = team_start
        

    def bfs(self, s, t, parent):

        visited = [False] * self.size
        queue = []  
        queue.append(s)
        visited[s] = True

        while queue:
            u = queue.pop(0) 

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

        return max_flow

    def get_result(self):
        team_start = n*(n-1)//2+1
        pointer = 1
        for i in range(n):
            for j in range(i+1, n):
                yield "{0} {1} {2}".format(
                    i + 1,
                    possible_results[(self.matrix[pointer][team_start+i], self.matrix[pointer][team_start+j])],
                    j + 1
                )
                pointer += 1

n, scores = read_input()

network = Network(n, scores)

if sum(scores) == network.edmonds_karp(0, network.size-1):
    print("CORRECT")
    for result in network.get_result():
        print(result)
else:
    print("INCORRECT")


