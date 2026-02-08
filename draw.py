def draw_screen():
    """画面の更新"""
    context.clearRect(0, 0, canvas.width, canvas.height)  # 画面クリア
    # ブロックの描画
    for y in range(ROWS):
        for x in range(COLS):
            if blocks[y][x] == 0:
                continue  # ブロックがなければスキップ
            # ブロックの色を設定して描画
            context.fillStyle = BLOCK_COLORS[blocks[y][x]]
            context.fillRect(x * BLOCK_W, y * BLOCK_H, BLOCK_W - 2, BLOCK_H - 2)
    # プレイヤーのバーの描画
    context.fillStyle = "black" # プレイヤーのバーの色
    context.fillRect(game["px"], PLAYER_Y, PLAYER_W, 10) # バーを描画
    # ボールの描画
    context.fillStyle = "red" # ボールの色
    context.beginPath() # 新しいパスを開始
    context.arc(game["ball_x"], game["ball_y"], BALL_SIZE // 2, 0, 2 * math.pi) # 円を描く
    context.fill() # 円を塗りつぶす

    # スコア表示
    if not game["game_over"]:
        info.innerText = f"ブロック崩し　スコア: {game['score']}点"