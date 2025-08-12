import sys

def turn_orientation(cur_ori, turn_str):
    # 0: N, 1: E, 2: S, 3: W
    if turn_str == "left":
        return (cur_ori + 3) % 4
    if turn_str == "right":
        return (cur_ori + 1) % 4
    if turn_str == "straight":
        return cur_ori
    if turn_str == "back":
        return (cur_ori + 2) % 4
    raise ValueError("Unknown turn: " + turn_str)

# movement vectors for orientations 0..3
MOVES = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def solve():
    data = sys.stdin.read().strip().split()
    it = iter(data)
    try:
        n = int(next(it))
    except StopIteration:
        return

    instr = []
    for _ in range(n):
        # each instruction: turn distance
        t = next(it)
        d = int(next(it))
        instr.append((t, d))

    sx = int(next(it)); sy = int(next(it))
    tx = int(next(it)); ty = int(next(it))

    # prefix: position and orientation BEFORE executing instruction i stored at prefix[i]
    # prefix[0] = (sx, sy, ori=0)
    prefix_pos = [(0,0,0)] * (n + 1)
    px, py, pori = sx, sy, 0
    prefix_pos[0] = (px, py, pori)
    for i in range(n):
        t, d = instr[i]
        new_ori = turn_orientation(pori, t)
        dx, dy = MOVES[new_ori]
        px += dx * d
        py += dy * d
        pori = new_ori
        prefix_pos[i+1] = (px, py, pori)

    # suffix[i][s] = (dx, dy, end_ori) displacement and end orientation if we start executing
    # instructions from i..n-1 with starting orientation = s.
    # We'll store as three arrays for compactness.
    # Initialize suffix at n -> zero displacement, orientation stays same
    suffix_dx = [[0]*4 for _ in range(n+1)]
    suffix_dy = [[0]*4 for _ in range(n+1)]
    suffix_end_ori = [[0]*4 for _ in range(n+1)]
    for s in range(4):
        suffix_dx[n][s] = 0
        suffix_dy[n][s] = 0
        suffix_end_ori[n][s] = s

    # fill from i = n-1 down to 0
    for i in range(n-1, -1, -1):
        turn_i, dist_i = instr[i]
        for s in range(4):
            ori_after = turn_orientation(s, turn_i)
            mx, my = MOVES[ori_after]
            move_x = mx * dist_i
            move_y = my * dist_i
            # then follow suffix starting orientation = ori_after at i+1
            dx_suf = suffix_dx[i+1][ori_after]
            dy_suf = suffix_dy[i+1][ori_after]
            end_ori_suf = suffix_end_ori[i+1][ori_after]
            suffix_dx[i][s] = move_x + dx_suf
            suffix_dy[i][s] = move_y + dy_suf
            suffix_end_ori[i][s] = end_ori_suf

    turns = ["left", "right", "straight", "back"]

    # Try each instruction index i, attempt replacing its turn by each alternative
    for i in range(n):
        px, py, ori_before = prefix_pos[i]  # state before executing instruction i
        actual_turn, dist = instr[i]
        for alt in turns:
            if alt == actual_turn:
                continue
            ori_after_alt = turn_orientation(ori_before, alt)
            dx_i, dy_i = MOVES[ori_after_alt]
            pos_after_i_x = px + dx_i * dist
            pos_after_i_y = py + dy_i * dist
            # add suffix starting at i+1 with starting orientation ori_after_alt
            dx_suf = suffix_dx[i+1][ori_after_alt]
            dy_suf = suffix_dy[i+1][ori_after_alt]
            final_x = pos_after_i_x + dx_suf
            final_y = pos_after_i_y + dy_suf
            if final_x == tx and final_y == ty:
                # Found solution: print in required format
                # Note: sample output prints blank lines between lines — replicate that.
                print("Yes")
                print()
                print(f"{actual_turn} {dist}")
                print()
                print(f"{alt} {dist}")
                return

    print("No")

if __name__ == "__main__":
    solve()
