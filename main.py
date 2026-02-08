import random
import math
from js import setTimeout, document

# 定数の宣言
INTERVAL=50 # ボールの移動間隔（ミリ秒）
PLAYER_W=100 # プレイヤーのバーの幅
PLAYER_Y=470  # プレイヤーのバーのY座標
PLAYER_MOVE=30 # プレイヤーのバーの移動量
BALL_SPEED=15 # ボールの速度
BALL_SIZE=15 # ボールのサイズ
BLOCK_W=50 # ブロックの幅
BLOCK_H=20 # ブロックの高さ
COLS=400 // BLOCK_W # ブロックの列数
ROWS=8 # ブロックの行数
BLOCK_COLORS=[  #ブロックの色
    "white", "red", "orange", "magenta", "pink", "cyan", "lime", "green", "blue"]

# グローバル変数の宣言
info=document.getElementById("info") # 情報表示用の要素を取得
canvas=document.getElementById("canvas") # Canvas要素を取得
context=canvas.getContext("2d") #2D描画コンテキストを取得
blocks=[] # ブロックのリスト
game={"game_over":True} # ゲームの状態を管理する辞書

def init_game():
    """ゲームの初期化"""
    global blocks,game
    # ブロックの初期化
    blocks=[[(y+1)] * COLS for y in range(ROWS)] 
    # ゲーム状態の初期化
    px=canvas.width - PLAYER_W // 2 # プレイヤーのバーのX座標
    game={
        "score":0, # スコア
        "px":px, # プレイヤーのバーのX座標
        "ball_x":(px+PLAYER_W // 2), # ボールのX座標
        "ball_y":PLAYER_y,
        "ball_dir":225 + random.randint(0,90), #ボールの進行方向
        "game_over":False, # ゲームオーバー状態
    }

def game_loop():
    """ゲームのメインループ"""
    update_ball() # ボールの位置更新
    draw_screen() # 画面の更新
    # ゲームオーバーでなければ次のループをセット
    if not game["game_over"]:
        setTimeout(game_loop, INTERVAL)

def ball_turn_angle(angle,range):
    """ボールの角度をangleだけ変化させる"""
    r = random.randint(-range, range)
    game["ball_dir"] = (game["ball_dir"] + angle + r) % 360

def update_ball():
    """ボール位置の更新"""
    rad = game["ball_dir"] * math.pi / 180 # 角度をラジアンに変換
    dx = int(BALL_SPEED * math.cos(rad)) # X方向の移動量
    dy = int(BALL_SPEED * math.sin(rad)) # Y方向の移動量
    bx = game["ball_x"] + dx # ボールの新しいX座標
    by = game["ball_y"] + dy # ボールの新しいY座標
    # プレーヤーのバーとの衝突判定
    px = game["px"] # プレイヤーのバーのX座標
    if (by >= PLAYER_Y) and (px <= bx < (px+PLAYER_W)):
        game["ball_dir"]=255 + random.randint(0,90)
    # 壁との衝突判定
    elif (bx < 0) or (bx > canvas.width) or (by <=0):
        ball_turn_angle(90,10) #角度変更
    # ブロックとの衝突判定
    elif check_blocks(bx,by):
        ball_turn_angle(180,20) #角度変更
        game["score"] += 1 # スコア加算
        # すべてのブロックを破壊したか判定
        if game["score"] >= (COLS * ROWS):
            game_over("クリア！")
    # 穴に落ちたらゲームオーバー判定
    elif by > (canvas.height - BALL_SIZE):
        game_over("ゲームオーバー")
    # ボールの座標を記録
    game["ball_x"] = bx
    game["ball_y"] = by

def check_blocks(bx,by):
    """ブロックとの衝突判定"""
    block_x, block_y = bx // BLOCK_W, by // BLOCK_H
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
