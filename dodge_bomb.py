from random import randint as ran
import sys
import pygame as pg

# ウィンドウサイズ
WIDTH, HEIGHT = 1600, 900

# 矢印キーと移動量の対応辞書
delta = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, 5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(5, 0),
}

# 加速度のリスト
accs = [a for a in range(1, 10)]

def check_bound(obj_rct: pg.Rect):
    """
    引数:こうかとんか爆弾のRect
    戻り値:タプル(横方向判定結果,縦方向判定結果)
    画面内ならTrue,外ならFalse
    """
    horizontal, vartical = True, True
    if (obj_rct.left < 0) or (WIDTH < obj_rct.right): # よこ
        horizontal = False
    
    if (obj_rct.top < 0) or (HEIGHT < obj_rct.bottom): # たて
        vartical = False
    
    return horizontal, vartical

def roto_rct(obj_img: pg.image):
    """
    引数:回転させたいImage
    戻り値:rotozoomされたSurfaceの辞書
    キーは移動量のタプル
    """
    # 反転画像
    fliped = pg.transform.flip(obj_img, True, False)
    return {
        (0, 0):obj_img,
        (-5, 0):pg.transform.rotozoom(obj_img, 0, 1.0),
        (-5, -5):pg.transform.rotozoom(obj_img, 315, 1.0),
        (0, -5):pg.transform.rotozoom(fliped, 90, 1.0),
        (5, -5):pg.transform.rotozoom(fliped, 45, 1.0),
        (5, 0):pg.transform.rotozoom(fliped, 0, 1.0),
        (5, 5):pg.transform.rotozoom(fliped, 315, 1.0),
        (0, 5):pg.transform.rotozoom(fliped, 270, 1.0),
        (-5, 5):pg.transform.rotozoom(obj_img, 45, 1.0)
    }


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")

    """こうかとんの初期設定"""
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_death = pg.image.load("ex02/fig/8.png")
    kk_death = pg.transform.rotozoom(kk_death, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = (900, 400)

    dct = roto_rct(kk_img)

    """爆弾の初期設定"""
    bomb = pg.Surface((20, 20))
    pg.draw.circle(bomb, (255, 0, 0), (10, 10), 10)
    bomb.set_colorkey((0, 0, 0))
    bomb_rct = bomb.get_rect()
    bomb_x, bomb_y = ran(0, WIDTH), ran(0, HEIGHT)
    bomb_rct.center = (bomb_x, bomb_y)
    vx, vy = +5, +5

    clock = pg.time.Clock()

    tick = 100
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        
        
        """背景画像"""
        screen.blit(bg_img, [0, 0])

        """こうかとんが爆死したら"""
        if kk_rct.colliderect(bomb_rct):
            kk_img = kk_death
            print("YOU DIED")
            return
        
        """こうかとんの更新"""
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in delta.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_img = dct[(sum_mv[0], sum_mv[1])]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        """爆弾の更新"""
        bomb_rct.move_ip(vx * accs[min(tmr // 500, 9)],
                         vy * accs[min(tmr // 500, 9)])
        horizontal, vartical = check_bound(bomb_rct)
        if not horizontal:
            vx *= -1
        if not vartical:
            vy *= -1
        screen.blit(bomb, bomb_rct)

        """時が流れる"""
        pg.display.update()
        tmr += 1
        clock.tick(tick)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()