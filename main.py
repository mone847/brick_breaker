import random
import math
from js import setTimeout, document, performance
from pyodide.ffi import create_proxy

# 定数の宣言
INTERVAL = 50 # ボールの移動間隔（ミリ秒）
PLAYER_W = 100 # プレイヤーのバーの幅
PLAYER_Y = 470  # プレイヤーのバーのY座標
PLAYER_MOVE = 30 # プレイヤーのバーの移動量
BALL_SPEED = 15 # ボールの速度
BALL_SIZE = 16 # ボールのサイズ
BLOCK_W = 50 # ブロックの幅
BLOCK_H = 20 # ブロックの高さ
COLS = 400 // BLOCK_W # ブロックの列数
ROWS = 8 # ブロックの行数
BLOCK_COLORS = [  #ブロックの色
    "white", "red", "orange", "magenta", "pink", "cyan", "lime", "green", "blue"]

# グローバル変数の宣言
info = document.getElementById("info") # 情報表示用の要素を取得
canvas = document.getElementById("canvas") # Canvas要素を取得
context = canvas.getContext("2d") # 2D描画コンテキストを取得
blocks = [] # ブロックのリスト
game = {"game_over":True} # ゲームの状態を管理する辞書
loop_proxy = None

def init_game():
    """ゲームの初期化"""
    global blocks,game
    # ブロックの初期化
    blocks = [[(y+1)] * COLS for y in range(ROWS)] 
    # スピード
    speed = 10  # 初期値
    # ランダムな角度を作る
    while True:
        angle = random.uniform(200, 340)
        if abs(math.cos(math.radians(angle))) > 0.3:
            break
    rad = math.radians(angle) 
    
    dx = speed * math.cos(rad)
    dy = speed * math.sin(rad)

    px = (canvas.width - PLAYER_W) // 2 # プレイヤーのバーのX座標
    game.update({
        "score":0, # スコア
        "px": px, # プレイヤーのバーのX座標
        "ball_x": canvas.width / 2, # ボールのX座標
        "ball_y": canvas.height / 2, # ボールのY座標
        "dx": dx, 
        "dy": dy,
        "paddle_vx": 0.0, # プレイヤーのバーの速度
        "game_over": False, # ゲームオーバー状態
    })
    

def game_loop():

    """ゲームのメインループ"""
    update_ball() # ボールの位置更新
    draw_screen() # 画面の更新
    # ゲームオーバーでなければ次のループをセット
    if not game["game_over"]:
        setTimeout(loop_proxy, INTERVAL)
        # setTimeout(create_proxy(game_loop), INTERVAL)
        # setTimeout(game_loop, INTERVAL)

def update_ball():
    global dx,dy
    """ボール位置の更新"""
    r = BALL_SIZE / 2

    bx = game["ball_x"] + game["dx"]
    by = game["ball_y"] + game["dy"]

    dx = game["dx"]
    dy = game["dy"]

    # 上壁
    if by - r <= 0:
        by = r
        dy = -dy
    # 左右壁
    if bx - r <= 0:
        bx = r
        dx = -dx
    elif bx + r >= canvas.width:
        bx = canvas.width - r
        dx = -dx

    # プレイヤーバー
    px = game["px"]
    if (by + r >= PLAYER_Y) and (px <= bx <= px + PLAYER_W):
        by = PLAYER_Y - r

        # 反射：必ず上に返す
        dy = -abs(dy)

        # 当たった位置（-1.0 ～ +1.0）
        hit = (bx - (px + PLAYER_W/2)) / (PLAYER_W/2)

        # バーの横速度（+右 / -左）を打球に反映
        pvx = game.get("paddle_vx", 0.0)

        # hit：端ほど角度が付く
        # pvx：バーを振るほど dx がその方向に寄る（左に素早く振れば左に返しやすい）
        dx = dx + hit * 1.8 + pvx * 0.35

        # 速度の上限・下限（暴走/失速防止）
        sp = math.hypot(dx, dy)
        MIN_S, MAX_S = 7, 25
        target = sp
        if target < MIN_S: target = MIN_S
        if target > MAX_S: target = MAX_S
        if sp > 0:
            scale = target / sp
            dx *= scale
            dy *= scale

    # ブロック
    elif check_blocks(bx, by):
        dy = -dy
        game["score"] += 1
        # スピードアップ
        dx *= 1.02
        dy *= 1.02
        if game["score"] >= COLS * ROWS:
            game_over("クリア！")
    # 落下
    elif by - r > canvas.height:
        game_over("ゲームオーバー")

    # 状態更新
    game["ball_x"] = bx
    game["ball_y"] = by
    game["dx"] = dx
    game["dy"] = dy

def check_blocks(bx,by):
    """ブロックとの衝突判定"""
    block_x, block_y = int(bx // BLOCK_W), int(by // BLOCK_H)
    if 0 <= block_x < COLS and 0 <= block_y < ROWS:
        if blocks[block_y][block_x] != 0: # ブロックが存在する場合
            blocks[block_y][block_x] = 0 # ブロックを消す
            return True
    return False

def game_over(msg):
    # ゲームオーバー処理
    # スタートボタンの有効化
    document.getElementById("start_button").disabled=False
    # ゲームオーバーとスコアの表示
    info.innerText=f"{msg} スコア: {game['score']}"
    game["game_over"] = True
