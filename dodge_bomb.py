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

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")

    """こうかとんの初期設定"""
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = (900, 400)

    """爆弾の初期設定"""
    bomb = pg.Surface((20, 20))
    pg.draw.circle(bomb, (255, 0, 0), (10, 10), 10)
    bomb.set_colorkey((0, 0, 0))
    bomb_rct = bomb.get_rect()
    bomb_x, bomb_y = ran(0, WIDTH), ran(0, HEIGHT)
    bomb_rct.center = (bomb_x, bomb_y)
    vx, vy = +5, +5

    clock = pg.time.Clock()

    tick = 50
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        screen.blit(bg_img, [0, 0])

        """こうかとんの更新"""
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in delta.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        screen.blit(kk_img, kk_rct)

        """爆弾の更新"""
        bomb_rct.move_ip(vx, vy)
        screen.blit(bomb, bomb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(tick)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()