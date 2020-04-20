import sys
import time
import random
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List
from matplotlib.widgets import Button


START_COLOR = (245, 0, 0)
GOAL_COLOR = (0, 210, 0)
SEARCH_COLOR = (180, 23, 17)
ROOT_COLOR = (50, 50, 155)

SLEEP_TIME1 = 0.0
SLEEP_TIME2 = 0.0


def generate_meiro(fig, ax, aximage, rows: int, cols: int) -> np.ndarray:
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

    # 描画用配列
    meiro_show = np.ones((rows, cols, 3), dtype='uint8') * 255

    # 周囲を壁にする
    res[0, :] = False
    res[:, 0] = False
    res[-1, :] = False
    res[:, -1] = False

    meiro_show[0, :] = 0
    meiro_show[:, 0] = 0
    meiro_show[-1, :] = 0
    meiro_show[:, -1] = 0
    update_fig(fig, ax, aximage, meiro_show, SLEEP_TIME1)
    

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

        meiro_show[start_pos] = 0
        update_fig(fig, ax, aximage, meiro_show, SLEEP_TIME1)

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

                        meiro_show[next1] = 0
                        update_fig(fig, ax, aximage, meiro_show, SLEEP_TIME1)

                        is_finished = True
                    else:
                        res[next1] = False
                        res[next2] = False

                        meiro_show[next1] = 0
                        meiro_show[next2] = 0
                        update_fig(fig, ax, aximage, meiro_show, SLEEP_TIME1)

                        building_set.add(next2)
                        building_stack.append(next2)
                    break

            else:
                # 周囲を現在拡張中の壁に囲まれたときは拡張可能な位置まで戻る
                building_stack.pop()
        
    return res



def solve_meiro(
    fig,
    ax,
    aximage,
    meiro: np.ndarray,
    meiro_show: np.ndarray,
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

        if now_pos != start:
            meiro_show[now_pos] = SEARCH_COLOR
            update_fig(fig, ax, aximage, meiro_show, SLEEP_TIME2)

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



def update_fig(fig, ax, aximage, meiro_show, sleep):
    aximage.set_data(meiro_show)
    ax.draw_artist(ax.patch)
    ax.draw_artist(aximage)
    fig.canvas.blit(ax.bbox)
    fig.canvas.flush_events()
    time.sleep(sleep)


def init_meiro_show(meiro_show, meiro, start, goal):
    meiro_show[meiro == True] = 255
    meiro_show[meiro == False] = 0
    meiro_show[start] = START_COLOR
    meiro_show[goal] = GOAL_COLOR


def refresh(fig, ax, aximage, meiro_show, meiro, rows, cols, start, goal):
    print('refreshing... ', end='')
    meiro[:, :] = generate_meiro(fig, ax, aximage, rows, cols)
    init_meiro_show(meiro_show, meiro, start, goal)
    update_fig(fig, ax, aximage, meiro_show, 0.0)
    print('refreshed!')


def solve(fig, ax, aximage, meiro_show, meiro, start, goal):
    print('solving... ', end='')
    init_meiro_show(meiro_show, meiro, start, goal)
    solution = solve_meiro(fig, ax, aximage, meiro, meiro_show, start, goal)
    for p in solution:
        meiro_show[p] = ROOT_COLOR
    update_fig(fig, ax, aximage, meiro_show, 0.0)
    #Image.fromarray(meiro_show).save('solve_10001.png')
    print('solved!')
    


def main():
    assert len(sys.argv) == 3, 'Input row and column size!'

    # 迷路の大きさを指定
    rows = int(sys.argv[1])
    cols = int(sys.argv[2])

    # 迷路の可視化用の行列を作成
    meiro = np.zeros((rows, cols), dtype='bool')
    meiro_show = np.ones((rows, cols, 3), dtype='uint8') * 255

    # figureの作成
    fig, ax = plt.subplots()

    # 迷路の描画
    aximage = plt.imshow(meiro_show, cmap='gray')

    # スタートとゴールを指定
    start = (1, 1)
    goal = (rows - 2, cols - 2)

    # refreshボタンの描画
    b_refresh_ax = plt.axes([0.85, 0.25, 0.1, 0.05])
    b_refresh = Button(b_refresh_ax, 'refresh')
    b_refresh_fun = lambda event: refresh(fig, ax, aximage, meiro_show, meiro, rows, cols, start, goal)
    b_refresh.on_clicked(b_refresh_fun)

    # solveボタンの描画
    b_solve_ax = plt.axes([0.85, 0.15, 0.1, 0.05])
    b_solve = Button(b_solve_ax, 'solve')
    b_solve_fun = lambda event: solve(fig, ax, aximage, meiro_show, meiro, start, goal)
    b_solve.on_clicked(b_solve_fun)

    # closeボタンの描画
    b_close_ax = plt.axes([0.85, 0.05, 0.1, 0.05])
    b_close = Button(b_close_ax, 'close')
    b_close_fun = lambda event: plt.close('all')
    b_close.on_clicked(b_close_fun)

    plt.show()


if __name__ == "__main__":
    main()





