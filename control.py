def start_button_on_click(event):
    """スタートボタンがクリックされたときの処理"""
    # スタートボタンの無効化
    document.getElementById("start_button").disabled = True
    init_game() # ゲーム初期化
    game_loop() # ゲームループ開始

def player_move(dx):
    """プレイヤーのバーを移動する"""
    if game["game_over"]:
        return  # ゲームオーバー時は移動しない
    px = game["px"] + dx  # 新しいバーの位置
    # バーが画面外に出ないように制限
    if 0 <= px <= (canvas.width - PLAYER_W):
        game["px"] = px
        draw_screen()

def right_button_on_click(event):
    """右移動ボタンがクリックされたときの処理"""
    player_move(PLAYER_MOVE)  # 右に移動

def left_button_on_click(event):
    """左移動ボタンがクリックされたときの処理"""
    player_move(-1 * PLAYER_MOVE)  # 左に移動

def key_down(event):
    """キーが押されたときの処理"""
    if event.key == "ArrowRight":
        right_button_on_click(event)  # 右に移動
    elif event.key == "ArrowLeft":
        left_button_on_click(event)  # 左に移動

# キー押下イベントリスナーの登録
document.addEventListener("keydown", key_down)
