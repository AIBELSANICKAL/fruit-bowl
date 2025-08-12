def char_worth(s):
    return sum(ord(c) - ord('a') + 1 for c in s)

def solve():
    # Read inputs
    N, M = map(int, input().split())
    strings = input().split()
    costs = list(map(int, input().split()))

    worths = [char_worth(s) for s in strings]
    
    # Conflict matrix
    conflict = [[False] * N for _ in range(N)]
    for _ in range(M):
        a, b = input().split()
        i, j = strings.index(a), strings.index(b)
        conflict[i][j] = conflict[j][i] = True

    budget = int(input())

    from functools import lru_cache

    @lru_cache(None)
    def dfs(idx, used_mask, remaining):
        if idx == N:
            return 0
        # Skip current string
        best = dfs(idx + 1, used_mask, remaining)
        # Try to take current string
        if costs[idx] <= remaining:
            can_take = True
            for prev in range(N):
                if (used_mask >> prev) & 1 and conflict[idx][prev]:
                    can_take = False
                    break
            if can_take:
                best = max(best,
                           worths[idx] + dfs(idx + 1, used_mask | (1 << idx), remaining - costs[idx]))
        return best

    print(dfs(0, 0, budget))
