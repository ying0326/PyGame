import pygame
from pathlib import Path
from player import Player  # ✅ 請確認你有 player.py 檔案，且 Player 類別定義在裡面

def main():
    # 初始化 Pygame
    pygame.init()

    # 畫面設定
    screen_width = 1000
    screen_height = 760
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("pygame")
    playground = [screen_width, screen_height]

    # 載入 icon（圖示）
    parent_path = Path(__file__).parents[1]  # ⬅ 若你專案不是這樣結構，請改成 Path(__file__).parent
    res_path = parent_path / 'res'
    icon_path = res_path / 'airplan.png'
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)

    # 建立背景
    background = pygame.Surface(screen.get_size()).convert()
    background.fill((50, 50, 50))  # 深灰背景

    # 建立時脈
    fps = 120
    clock = pygame.time.Clock()
    moving_scale = 600 / fps

    # 建立玩家
    player = Player(playground=playground, sensitivity=moving_scale)

    # 鍵盤按鍵計數（處理多鍵同時按下）
    keyCountX = 0
    keyCountY = 0

    # 遊戲主迴圈
    running = True
    while running:
        # 處理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 按下按鍵
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    keyCountX += 1
                    player.to_the_left()
                if event.key == pygame.K_d:
                    keyCountX += 1
                    player.to_the_right()
                if event.key == pygame.K_s:
                    keyCountY += 1
                    player.to_the_bottom()
                if event.key == pygame.K_w:
                    keyCountY += 1
                    player.to_the_top()

            # 放開按鍵
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_a, pygame.K_d):
                    if keyCountX == 1:
                        keyCountX = 0
                        player.stop_x()
                    else:
                        keyCountX -= 1
                if event.key in (pygame.K_w, pygame.K_s):
                    if keyCountY == 1:
                        keyCountY = 0
                        player.stop_y()
                    else:
                        keyCountY -= 1

        # 更新邏輯
        player.update()

        # 畫面渲染
        screen.blit(background, (0, 0))
        screen.blit(player.image, player.xy)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    main()
