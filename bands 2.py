# Bands 2 - solution
# Assumes input exactly as specified in the prompt.

import sys

def read_input():
    data = sys.stdin.read().strip().split()
    it = iter(data)
    S = int(next(it))
    x1 = int(next(it)); y1 = int(next(it))
    seq1 = next(it).strip()
    x2 = int(next(it)); y2 = int(next(it))
    seq2 = next(it).strip()
    return S, (x1, y1, seq1), (x2, y2, seq2)

# move mapping: 'u' = up (y-1) or up as per problem?
# The problem states top-left is (0,0). Usually:
#  - 'u' means decrement row index -> y - 1
#  - 'd' means y + 1
# However in the examples they used coordinates consistent with y increasing downward or upward?
# We'll use the conventional Cartesian assumption used above: top-left (0,0), 'u' -> y-1, 'd' -> y+1.
# That convention is consistent with the example diagrams and typical grid interpretation in such problems.
MOVE = {
    'u': (0, -1),
    'd': (0, 1),
    'l': (-1, 0),
    'r': (1, 0)
}

def build_time_map(start_x, start_y, seq, S):
    # returns dict: (x,y) -> time_index (0-based)
    x, y = start_x, start_y
    time_map = {}
    t = 0
    time_map[(x, y)] = t
    for ch in seq:
        dx, dy = MOVE[ch]
        x += dx; y += dy
        t += 1
        # bounds check (should be valid per problem constraints)
        if not (0 <= x < S and 0 <= y < S):
            # Out-of-bounds shouldn't happen in valid inputs, but guard anyway.
            raise ValueError("Path goes out of bounds.")
        # problem guarantees no self-overlap so no need to check existing key
        time_map[(x, y)] = t
    return time_map

def solve():
    S, b1, b2 = read_input()
    x1, y1, seq1 = b1
    x2, y2, seq2 = b2

    tmap1 = build_time_map(x1, y1, seq1, S)
    tmap2 = build_time_map(x2, y2, seq2, S)

    overlap_positions = set(tmap1.keys()) & set(tmap2.keys())
    if not overlap_positions:
        # No overlap → they are trivially separable with 0 overlap
        print(0)
        return

    top1 = 0
    top2 = 0
    for pos in overlap_positions:
        t1 = tmap1[pos]
        t2 = tmap2[pos]
        if t1 == t2:
            print("Impossible")
            return
        if t1 > t2:
            top1 += 1
        else:
            top2 += 1

    # If both have some cells where they are top, they are interlocked
    if top1 > 0 and top2 > 0:
        print("Impossible")
    else:
        print(max(top1, top2))

if __name__ == "__main__":
    solve()
