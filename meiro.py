import random
import numpy as np
from typing import Tuple, List



def generate_meiro(rows: int, cols: int) -> np.ndarray:
    '''
    壁伸ばし法で迷路を生成
    
    参考：http://algoful.com/Archive/Algorithm/MazeExtend

    return
        壁の位置が False, 通路の位置が True の np.ndarray (dtype='bool')
    '''

    assert rows >= 5 and cols >= 5, 'Rows and cols must be odd numbers greater than or equal to 5!'
    assert rows % 2 == 1 and cols % 2 == 1, 'Rows and cols must be odd numbers greater than or equal to 5!'

    # 返り値
    res = np.ones((rows, cols), dtype='bool')

    # 周囲を壁にする
    res[0, :] = False
    res[:, 0] = False
    res[-1, :] = False
    res[:, -1] = False

    # 壁伸ばし開始座標のリスト
    start_pos_list = [(i, j) for i in range(2, rows - 1, 2) for j in range(2, cols - 1, 2)]
    l_start_pos_list = len(start_pos_list)
    start_pos_list = random.sample(start_pos_list, l_start_pos_list)

    # 壁伸ばし法開始
    for idx in range(l_start_pos_list):
        is_finished = False

        # 壁伸ばし開始点
        start_pos = start_pos_list[idx]

        # 壁伸ばし候補がすでに壁なら次へ
        if not res[start_pos]:
            continue

        # 壁伸ばし開始点を壁にする
        res[start_pos] = False

        # 現在拡張中の壁の位置の集合
        building_set = set()
        building_set.add(start_pos)

        # 現在拡張中の壁の位置のスタック
        building_stack = []
        building_stack.append(start_pos)

        # 壁を伸ばす
        while building_stack:
            if is_finished:
                break

            now_pos = building_stack[-1]

            # 壁を伸ばす方向を決める
            directions = random.sample(range(4), 4)
            for d in directions:
                # 左
                if d == 0:
                    next1 = (now_pos[0] - 1, now_pos[1])
                    next2 = (now_pos[0] - 2, now_pos[1])
                # 右
                elif d == 1:
                    next1 = (now_pos[0] + 1, now_pos[1])
                    next2 = (now_pos[0] + 2, now_pos[1])
                # 上
                elif d == 2:
                    next1 = (now_pos[0], now_pos[1] - 1)
                    next2 = (now_pos[0], now_pos[1] - 2)
                # 下
                else:
                    next1 = (now_pos[0], now_pos[1] + 1)
                    next2 = (now_pos[0], now_pos[1] + 2)
                
                # 隣のマスが壁でなく、かつ、2つ隣のマスが現在拡張中のマスでなければ壁を伸ばす
                if res[next1] and (next2 not in building_set):
                    if not res[next2]:
                        res[next1] = False
                        is_finished = True
                    else:
                        res[next1] = False
                        res[next2] = False
                        building_set.add(next2)
                        building_stack.append(next2)
                    break

            else:
                # 周囲を現在拡張中の壁に囲まれたときは拡張可能な位置まで戻る
                building_stack.pop()
        
    return res



def solve_meiro(
    meiro: np.ndarray, 
    start: Tuple[int, int], 
    goal: Tuple[int, int]) -> List[Tuple[int, int]]:
    '''
    深さ優先探索で迷路を解く
    '''
    rows, cols = meiro.shape
    range_ok = (min(start[0], goal[0]) >= 0) and (max(start[0], goal[0]) < rows) \
        and (min(start[1], goal[1]) >= 0) and (max(start[1], goal[1]) < cols)
    assert range_ok, 'Out of range!'
    assert meiro[start] and meiro[goal], 'The start and goal must not be walls!'

    is_solved = False

    stack = []
    stack.append(start)
    before_idx = [[(-1, -1)] * cols for _ in range(rows)]
    before_idx[start[0]][start[1]] = (-2, -2)  # (-2, -2)を先頭の印とする

    while stack:
        now_pos = stack.pop()

        if now_pos == goal:
            is_solved = True
            stack.append(now_pos)
            break

        directions = random.sample(range(4), 4)
        for d in directions:
            # 左
            if d == 0:
                next_pos = (now_pos[0] - 1, now_pos[1])
            # 右
            elif d == 1:
                next_pos = (now_pos[0] + 1, now_pos[1])
            # 上
            elif d == 2:
                next_pos = (now_pos[0], now_pos[1] - 1)
            # 下
            else:
                next_pos = (now_pos[0], now_pos[1] + 1)

            if before_idx[next_pos[0]][next_pos[1]] != (-1, -1):
                continue

            if meiro[next_pos]:
                stack.append(next_pos)
                before_idx[next_pos[0]][next_pos[1]] = now_pos

    assert is_solved, 'Failed solving the maze!'

    solution = []
    tail = goal
    while before_idx[tail[0]][tail[1]] != start:
        tail = before_idx[tail[0]][tail[1]]
        solution.append(tail)

    return solution
