# meiro
迷路を作ったり解いたりする

## 必要なライブラリ
 * numpy
 * matplotlib
 
## 使い方

```
python main.py ROWS COLS
```

`ROWS`と`COLS`は迷路のサイズ  
それぞれ5以上の奇数でなければならない。

## 迷路の生成と解探索の可視化

```
python main_enjoy.py ROWS COLS
```

可視化しない場合よりとても遅いので注意。
`main_enjoy.py`の上の方にある`SLEEP_TIME1`や`SLEEP_TIME2`をいじれば、
表示速度を変更できる。
