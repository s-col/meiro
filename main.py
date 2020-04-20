import sys
import os
import datetime 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from PIL import Image

from meiro import generate_meiro, solve_meiro



START_COLOR = (245, 0, 0)
GOAL_COLOR = (0, 210, 0)
ROOT_COLOR = (50, 50, 155)

BASEPATH = os.path.dirname(os.path.abspath(__file__))


def init_meiro_show(meiro_show, meiro, start, goal):
    meiro_show[meiro == True] = 255
    meiro_show[meiro == False] = 0
    meiro_show[start] = START_COLOR
    meiro_show[goal] = GOAL_COLOR


def refresh(fig, ax, meiro_show, meiro, rows, cols, start, goal):
    print('refreshing... ', end='', flush=True)
    meiro[:, :] = generate_meiro(rows, cols)
    init_meiro_show(meiro_show, meiro, start, goal)
    ax.set_data(meiro_show)
    fig.canvas.draw_idle()
    print('refreshed!', flush=True)


def solve(fig, ax, meiro_show, meiro, start, goal):
    print('solving... ', end='', flush=True)
    init_meiro_show(meiro_show, meiro, start, goal)
    solution = solve_meiro(meiro, start, goal)
    for p in solution:
        meiro_show[p] = ROOT_COLOR
    ax.set_data(meiro_show)
    fig.canvas.draw_idle()
    #Image.fromarray(meiro_show).save('solve_10001.png')
    print('solved!', flush=True)
    

def save(meiro_show):
    savedir = os.path.join(BASEPATH, 'fig')
    if not os.path.exists(savedir):
        os.mkdir(savedir)
    filename = 'meiro_ ' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.png'
    filepath = os.path.join(savedir, filename)
    Image.fromarray(meiro_show).save(filepath)
    print('image saved at {:s}'.format(filepath))


def main():
    assert len(sys.argv) == 3, 'Input row and column size!'

    # 迷路の大きさを指定
    rows = int(sys.argv[1])
    cols = int(sys.argv[2])

    # 迷路を生成
    meiro = generate_meiro(rows, cols)

    # 迷路の可視化用の行列を作成
    meiro_show = np.zeros((rows, cols, 3), dtype='uint8')

    # スタートとゴールを指定
    start = (1, 1)
    goal = (rows - 2, cols - 2)

    # meiro_showを初期化
    init_meiro_show(meiro_show, meiro, start, goal)
    #Image.fromarray(meiro_show).save('meiro_10001.png')

    # figureの作成
    fig = plt.figure()

    # 迷路の描画
    ax = plt.imshow(meiro_show, cmap='gray')

    # saveボタンの描画
    b_save_ax = plt.axes([0.85, 0.35, 0.1, 0.05])
    b_save = Button(b_save_ax, 'save')
    b_save_fun = lambda event: save(meiro_show)
    b_save.on_clicked(b_save_fun)

    # refreshボタンの描画
    b_refresh_ax = plt.axes([0.85, 0.25, 0.1, 0.05])
    b_refresh = Button(b_refresh_ax, 'refresh')
    b_refresh_fun = lambda event: refresh(fig, ax, meiro_show, meiro, rows, cols, start, goal)
    b_refresh.on_clicked(b_refresh_fun)

    # solveボタンの描画
    b_solve_ax = plt.axes([0.85, 0.15, 0.1, 0.05])
    b_solve = Button(b_solve_ax, 'solve')
    b_solve_fun = lambda event: solve(fig, ax, meiro_show, meiro, start, goal)
    b_solve.on_clicked(b_solve_fun)

    # closeボタンの描画
    b_close_ax = plt.axes([0.85, 0.05, 0.1, 0.05])
    b_close = Button(b_close_ax, 'close')
    b_close_fun = lambda event: plt.close('all')
    b_close.on_clicked(b_close_fun)

    plt.show()


if __name__ == "__main__":
    main()





