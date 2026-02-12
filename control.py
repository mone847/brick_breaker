def start_button_on_click(event):

mouse_active = False
_last_t = None
_last_px = None

def start_button_on_click(event):
    document.getElementById("start_button").disabled = True
    init_game()
    # 速度推定の初期化
    global _last_t, _last_px
    _last_t = performance.now()
    _last_px = game["px"]
    game["paddle_vx"] = 0.0
    game_loop()

def _clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

def set_player_x_from_mouse(client_x):
    # ゲーム中のみ
    if game["game_over"]:
        return

    rect = canvas.getBoundingClientRect()
    x = client_x - rect.left
    new_px = x - (PLAYER_W / 2)
    new_px = _clamp(new_px, 0, canvas.width - PLAYER_W)

    # ---- バー速度（px/フレーム相当）を推定して game["paddle_vx"] に保存 ----
    # performance.now() は ms
    global _last_t, _last_px
    now = performance.now()
    if _last_t is None:
        _last_t = now
        _last_px = new_px
        game["paddle_vx"] = 0.0
    else:
        dt = now - _last_t  # ms
        if dt <= 0:
            dt = 1
        # 1フレーム(=INTERVAL ms)あたりの移動量に換算： px / (dt/INTERVAL)
        vx = (new_px - _last_px) * (INTERVAL / dt)

        # ちょい平滑化（ブレを減らす）
        prev = game.get("paddle_vx", 0.0)
        game["paddle_vx"] = prev * 0.6 + vx * 0.4

        _last_t = now
        _last_px = new_px

    game["px"] = new_px
    draw_screen()

def on_mouse_enter(event):
    global mouse_active, _last_t, _last_px
    mouse_active = True
    _last_t = performance.now()
    _last_px = game.get("px", 0)

def on_mouse_leave(event):
    global mouse_active
    mouse_active = False
    game["paddle_vx"] = 0.0

def on_mouse_move(event):
    if not mouse_active:
        return
    set_player_x_from_mouse(event.clientX)

canvas.addEventListener("mouseenter", on_mouse_enter)
canvas.addEventListener("mouseleave", on_mouse_leave)
canvas.addEventListener("mousemove", on_mouse_move)

def player_move(dx):
    """プレイヤーのバーを移動する"""
    if game["game_over"]:
        return  # ゲームオーバー時は移動しない
    px = game["px"] + dx  # 新しいバーの位置
    # バーが画面外に出ないように制限
    if 0 <= px <= (canvas.width - PLAYER_W):
        game["px"] = px
        draw_screen()

def key_down(event):
    """キーが押されたときの処理"""
    if event.key == "ArrowRight":
       player_move(PLAYER_MOVE)  # 右に移動
    elif event.key == "ArrowLeft":
        player_move(-1 * PLAYER_MOVE)  # 左に移動

# キー押下イベントリスナーの登録
document.addEventListener("keydown", key_down)
