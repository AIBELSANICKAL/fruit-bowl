import math
import heapq

def dist(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def point_clear(pt, buildings, rv):
    for (bx, by, br) in buildings:
        if dist(pt, (bx, by)) < rv + br:
            return False
    return True

def side_of_line(p, a, b):
    # >0 left, <0 right, 0 on line
    return (b[0]-a[0])*(p[1]-a[1]) - (b[1]-a[1])*(p[0]-a[0])

def solve():
    S = int(input())
    sx, sy, rv = map(int, input().split())
    dx, dy = map(int, input().split())
    N = int(input())
    buildings = [tuple(map(int, input().split())) for _ in range(N)]
    T = int(input())
    tax_lines = []
    for _ in range(T):
        i1, i2 = map(int, input().split())
        a = (buildings[i1-1][0], buildings[i1-1][1])
        b = (buildings[i2-1][0], buildings[i2-1][1])
        tax_lines.append((a, b))
    
    # Check start/dest clearance
    if not point_clear((sx, sy), buildings, rv) or not point_clear((dx, dy), buildings, rv):
        print("Impossible")
        return

    # Discretize into 1-unit grid for BFS (safe given S ≤ 50)
    grid_size = 1
    W = int(S / grid_size) + 1
    H = W
    def neighbors(x, y):
        for dx_, dy_ in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x+dx_, y+dy_
            if 0 <= nx < W and 0 <= ny < H:
                yield nx, ny
    
    # BFS with cost for crossing tax lines
    start_cell = (int(sx), int(sy))
    dest_cell  = (int(dx), int(dy))
    INF = 10**9
    dist_cost = [[INF]*H for _ in range(W)]
    pq = [(0, start_cell)]
    dist_cost[start_cell[0]][start_cell[1]] = 0
    
    while pq:
        cost, (cx, cy) = heapq.heappop(pq)
        if (cx, cy) == dest_cell:
            print(cost)
            return
        if cost > dist_cost[cx][cy]: continue
        for nx, ny in neighbors(cx, cy):
            # midpoints of cells as coords
            p1 = (cx, cy)
            p2 = (nx, ny)
            # Check clearance
            if not point_clear(p2, buildings, rv):
                continue
            # Check tax line crossing
            extra = 0
            for a, b in tax_lines:
                s1 = side_of_line(p1, a, b)
                s2 = side_of_line(p2, a, b)
                if s1*s2 < 0:
                    extra += 1
            new_cost = cost + extra
            if new_cost < dist_cost[nx][ny]:
                dist_cost[nx][ny] = new_cost
                heapq.heappush(pq, (new_cost, (nx, ny)))
    
    print("Impossible")
